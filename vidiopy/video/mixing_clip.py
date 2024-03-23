from typing import Callable, Sequence
from PIL import Image, ImageOps
from ..audio.AudioClip import SilenceClip, concatenate_audioclips, composite_audioclips
from .ImageSequenceClip import ImageSequenceClip
from .VideoClip import VideoClip


def composite_videoclips(
    clips: Sequence[VideoClip],
    fps: int | float | None = None,
    bg_color: tuple[int, ...] = (0, 0, 0, 0),
    use_bg_clip: bool = False,
    audio: bool = True,
    audio_fps=44100,
):
    """
    Composites multiple video clips into a single video clip.

    This function takes a sequence of video clips and composites them into a single video clip. The clips are layered on top of each other in the order they appear in the sequence. The background of the composite clip can be a solid color or the first clip in the sequence. The function also handles the positioning of each clip in the composite clip and the audio of the composite clip.

    Args:
        clips (Sequence[VideoClip]): The sequence of video clips to composite.
        fps (int | float | None, optional): The frames per second of the composite clip. If not specified, it is set to the maximum fps of the clips in the sequence or raises a ValueError if none of the clips have fps set.
        bg_color (tuple[int, ...], optional): The background color of the composite clip as a tuple of integers representing RGBA values. Default is (0, 0, 0, 0) which is transparent.
        use_bg_clip (bool, optional): Whether to use the first clip in the sequence as the background of the composite clip. Default is False.
        audio (bool, optional): Whether to include audio in the composite clip. If True, the audio of the clips in the sequence is also composited. Default is True.
        audio_fps (int, optional): The frames per second of the audio of the composite clip. Default is 44100.

    Returns:
        ImageSequenceClip: The composite video clip as an instance of the ImageSequenceClip class.

    Raises:
        ValueError: If neither fps nor duration is set for any of the clips in the sequence.
        ValueError: If the position of a clip in the composite clip is not specified correctly.
        TypeError: If the position of a clip in the composite clip is not of the correct type.

    Example:
        >>> clip1 = VideoClip(...)
        >>> clip2 = VideoClip(...)
        >>> composite_clip = composite_videoclips([clip1, clip2], fps=24)

    Note:
        This function uses the ImageSequenceClip class to create the composite video clip and the composite_audioclips function to composite the audio of the clips.
    """
    fps = int(
        fps
        or max(*(clip.fps if clip.fps else 0.0 for clip in clips), 0.0)
        or (_ for _ in ()).throw(ValueError("fps is not set"))
    )

    if use_bg_clip:
        bg_clip = clips[0]
        clips = clips[1:]
        duration = bg_clip.duration
        if not duration:
            duration = bg_clip.end
        if not duration:
            raise ValueError("duration is not set of bg_clip")
        bg_make_frame = bg_clip.make_frame_pil
    else:
        size = [0, 0]
        duration = 0.0
        for clip in clips:
            if clip.end:
                duration = max(clip.end, duration)
            elif clip.duration:
                duration = max(clip.duration, duration)
            else:
                ...
            if clip.size:
                if size[0] < clip.size[0]:
                    size[0] = clip.size[0]
                if size[1] < clip.size[1]:
                    size[1] = clip.size[1]
        if size == [0, 0]:
            raise ValueError("size is not set of any clip")
        if duration == 0.0:
            raise ValueError("duration is not set of any clip")
        bg = Image.new("RGBA" or "RGB", tuple(size), bg_color)

        def bg_make_frame(t):
            return bg.copy()

    t = 0.0
    frames = []
    while t < duration:
        f = bg_make_frame(t)
        for clip in clips:
            if clip.start <= t + clip.start < (clip.end or float("inf")):
                pos_x = 0
                pos_y = 0
                frame = clip.make_frame_pil(t + clip.start)
                pos_: tuple[int | str | float, int | str | float] = clip.pos(
                    t + clip.start
                )
                if isinstance(pos_[0], str):
                    if pos_[0] == "center":
                        pos_x = f.size[0] // 2 - frame.size[0] // 2
                    elif pos_[0] == "left":
                        pos_x = 0
                    elif pos_[0] == "right":
                        pos_x = f.size[0] - frame.size[0]
                    else:
                        raise ValueError(f"pos[0] must be 'center', 'left' or 'right'")
                elif isinstance(pos_[0], (int, float)):
                    if clip.relative_pos:
                        pos_x = int(pos_[0] * f.size[0])
                    else:
                        pos_x = int(pos_[0])
                else:
                    raise TypeError(
                        f"pos must output tuple of str or float or int, not {type(pos_[0])}"
                    )

                if isinstance(pos_[1], str):
                    if pos_[1] == "center":
                        pos_y = f.size[1] // 2 - frame.size[1] // 2
                    elif pos_[1] == "top":
                        pos_y = 0
                    elif pos_[1] == "bottom":
                        pos_y = f.size[1] - frame.size[1]
                    else:
                        raise ValueError(f"pos[1] must be 'center', 'top' or 'bottom'")
                elif isinstance(pos_[1], int) or isinstance(pos_[1], float):
                    if clip.relative_pos:
                        pos_y = int(pos_[1] * f.size[1])
                    else:
                        pos_y = int(pos_[1])
                else:
                    raise TypeError(
                        f"pos must output tuple of str or float or int, not {type(pos_[1])}"
                    )
                f.paste(
                    frame,
                    (pos_x, pos_y),
                    frame if frame.has_transparency_data else None,
                )
        frames.append(f)
        t += 1 / fps
    f_frames = tuple(frames)
    del frames

    if audio:
        aud_ = []
        for clip in clips:
            if clip.audio is not None:
                aud_.append(clip.audio)
            else:
                aud_.append(SilenceClip(duration=duration))
        aud = composite_audioclips(aud_, fps=audio_fps, use_bg_audio=use_bg_clip)
    else:
        aud = None

    return ImageSequenceClip(f_frames, fps=fps, duration=duration, audio=aud)


def concatenate_videoclips(
    clips: Sequence[VideoClip],
    transparent: bool = False,
    fps: int | float | None = None,
    scaling_strategy: str = "scale_same",
    transition: (
        VideoClip | Callable[[Image.Image, Image.Image, int | float], VideoClip] | None
    ) = None,
    audio: bool = True,
    audio_fps: int | None = None,
):
    """
    Concatenates multiple video clips into a single video clip.

    This function takes a sequence of video clips and concatenates them into a single video clip. The clips are appended one after the other in the order they appear in the sequence. The function also handles the scaling of each clip in the concatenated clip and the audio of the concatenated clip.

    Args:
        clips (Sequence[VideoClip]): The sequence of video clips to concatenate.
        transparent (bool, optional): Whether to use a transparent background for the concatenated clip. Default is False.
        fps (int | float | None, optional): The frames per second of the concatenated clip. If not specified, it is set to the maximum fps of the clips in the sequence or raises a ValueError if none of the clips have fps set.
        scaling_strategy (bool | None, optional): The scaling strategy to use for the clips in the concatenated clip. If 'scale_up', the clips are scaled up to fit the size of the concatenated clip. If 'scale_down', the clips are scaled down to fit the size of the concatenated clip. If 'scale_same', the clips are not scaled. Default is 'scale_same'.
        transition (VideoClip | Callable[[Image.Image, Image.Image, int | float], VideoClip] | None, optional): The transition to use between the clips in the concatenated clip. If a VideoClip, it is used as the transition. If a callable, it is called with the last frame of the previous clip, the first frame of the next clip, and the duration of the transition to generate the transition. If None, no transition is used. Default is None.
        audio (bool, optional): Whether to include audio in the concatenated clip. If True, the audio of the clips in the sequence is also concatenated. Default is True.
        audio_fps (int | None, optional): The frames per second of the audio of the concatenated clip. Default is None.

    Returns:
        ImageSequenceClip: The concatenated video clip as an instance of the ImageSequenceClip class.

    Raises:
        ValueError: If neither fps nor duration is set for any of the clips in the sequence.
        ValueError: If the size of a clip in the concatenated clip is not specified correctly.
        TypeError: If the scaling strategy of a clip in the concatenated clip is not of the correct type.

    Example:
        >>> clip1 = VideoClip(...)
        >>> clip2 = ImageClip(...)
        >>> concatenated_clip = concatenate_videoclips([clip1, clip2], fps=24)

    Note:
        This function uses the ImageSequenceClip class to create the concatenated video clip and the concatenate_audioclips function to concatenate the audio of the clips.
    """
    # TODO: Add transition support
    if transition is not None:
        raise NotImplementedError("transition is not supported yet")

    fps = (
        fps if fps is not None else max(clip.fps if clip.fps else 0.0 for clip in clips)
    )
    duration_per_clip: list[int | float] = [
        (
            clip.end
            if clip.end
            else (
                clip.duration
                if clip.duration
                else (_ for _ in ()).throw(
                    ValueError(
                        f"Clip duration and end is not set __str__={clip.__str__()}"
                    )
                )
            )
        )
        for clip in clips
    ]
    td = 1 / fps
    duration: int | float = sum(duration_per_clip)

    if scaling_strategy == "scale_same":

        def increase_scale(
            frame: Image.Image, new_size: tuple[int, int]
        ) -> Image.Image:
            new_frame = Image.new("RGBA" if transparent else "RGB", new_size)
            new_frame.paste(
                frame,
                (
                    new_size[0] // 2 - frame.size[0] // 2,
                    new_size[1] // 2 - frame.size[1] // 2,
                ),
            )
            return new_frame

        size: tuple[int, int] = max(
            tuple(
                (
                    clip.size
                    if clip.size and clip.size[0] and clip.size[1]
                    else (_ for _ in ()).throw(
                        ValueError(
                            f"Clip Size is not set, clip.__str__ = {clip.__str__()}"
                        )
                    )
                )
                for clip in clips
            )
        )

        frames = []
        for i, clip in enumerate(clips):
            current_clip_current_time = 0.0
            while current_clip_current_time < duration_per_clip[i]:
                current_clip_current_frame = clip.make_frame_pil(
                    current_clip_current_time
                )
                current_clip_current_frame = increase_scale(
                    current_clip_current_frame, size
                )
                frames.append(current_clip_current_frame)
                current_clip_current_time += td
        f_frames = tuple(frames)
        del frames

        if audio:
            audios = []
            for i, clip in enumerate(clips):
                if clip.audio is not None:
                    audios.append(clip.audio)
                else:
                    audios.append(SilenceClip(duration=duration_per_clip[i]))
            return ImageSequenceClip(
                f_frames,
                fps=fps,
                duration=duration,
                audio=concatenate_audioclips(audios, fps=audio_fps),
            )
        else:
            return ImageSequenceClip(f_frames, fps=fps, duration=duration)

    elif scaling_strategy == "scale_up":

        def increase_scale(
            frame: Image.Image, new_size: tuple[int, int]
        ) -> Image.Image:
            return ImageOps.pad(frame, new_size, color=(0, 0, 0, 0)).convert(
                "RGBA" if transparent else "RGB"
            )

        size: tuple[int, int] = max(
            tuple(
                (
                    clip.size
                    if clip.size and clip.size[0] and clip.size[1]
                    else (_ for _ in ()).throw(
                        ValueError(
                            f"Clip Size is not set, clip.__str__ = {clip.__str__()}"
                        )
                    )
                )
                for clip in clips
            )
        )
        frames = []
        for i, clip in enumerate(clips):
            current_clip_current_time = 0.0
            while current_clip_current_time < duration_per_clip[i]:
                current_clip_current_frame = clip.make_frame_pil(
                    current_clip_current_time
                )
                current_clip_current_frame = increase_scale(
                    current_clip_current_frame, size
                )
                frames.append(current_clip_current_frame)
                current_clip_current_time += td
        f_frames = tuple(frames)
        del frames

        if audio:
            audios = []
            for i, clip in enumerate(clips):
                if clip.audio is not None:
                    audios.append(clip.audio)
                else:
                    audios.append(SilenceClip(duration=duration_per_clip[i]))
            return ImageSequenceClip(
                f_frames,
                fps=fps,
                duration=duration,
                audio=concatenate_audioclips(audios, fps=audio_fps),
            )
        else:
            return ImageSequenceClip(f_frames, fps=fps, duration=duration)
    elif scaling_strategy == "scale_down":

        def increase_scale(
            frame: Image.Image, new_size: tuple[int, int]
        ) -> Image.Image:
            return ImageOps.fit(frame, new_size).convert(
                "RGBA" if transparent else "RGB"
            )

        size: tuple[int, int] = max(
            tuple(
                (
                    clip.size
                    if clip.size and clip.size[0] and clip.size[1]
                    else (_ for _ in ()).throw(
                        ValueError(
                            f"Clip Size is not set, clip.__str__ = {clip.__str__()}"
                        )
                    )
                )
                for clip in clips
            )
        )
        frames = []
        for i, clip in enumerate(clips):
            current_clip_current_time = 0.0
            while current_clip_current_time < duration_per_clip[i]:
                current_clip_current_frame = clip.make_frame_pil(
                    current_clip_current_time
                )
                current_clip_current_frame = increase_scale(
                    current_clip_current_frame, size
                )
                frames.append(current_clip_current_frame)
                current_clip_current_time += td
        f_frames = tuple(frames)
        del frames

        if audio:
            audios = []
            for i, clip in enumerate(clips):
                if clip.audio is not None:
                    audios.append(clip.audio)
                else:
                    audios.append(SilenceClip(duration=duration_per_clip[i]))
            return ImageSequenceClip(
                f_frames,
                fps=fps,
                duration=duration,
                audio=concatenate_audioclips(audios, fps=audio_fps),
            )
        else:
            return ImageSequenceClip(f_frames, fps=fps, duration=duration)
    else:
        raise TypeError(
            f"scaling_strategy must be 'scale_same', 'scale_up' or 'scale_down', not '{scaling_strategy}'"
        )
