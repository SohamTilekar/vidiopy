from typing import Callable, Sequence
from PIL import Image, ImageOps

from ..audio.AudioClip import SilenceClip, concatenate_audioclips, composite_audioclips
from .ImageSequenceClip import ImageSequenceClip
from .ImageClips import ColorClip
from .VideoClip import VideoClip


def composite_videoclips(
    clips: Sequence[VideoClip],
    fps: int | float | None = None,
    bg_color: tuple[int, ...] = (0, 0, 0, 0),
    use_bg_clip: bool = False,
    audio: bool = True,
    audio_fps=44100,
):
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
    else:
        duration = 0.0
        for clip in clips:
            if clip.end:
                duration = max(clip.end, duration)
            elif clip.duration:
                duration = max(clip.duration, duration)
            else:
                ...
        if duration == 0.0:
            raise ValueError("duration is not set of any clip")
        bg_clip = ColorClip(bg_color, duration=duration)

    t = 0.0
    frames = []
    while t < duration:
        f = bg_clip.make_frame_pil(t)
        for clip in clips:
            if clip.start <= t < (clip.end or float("inf")):
                pos_x = 0
                pos_y = 0
                frame = clip.make_frame_pil(t)
                pos_: tuple[int | str | float, int | str | float] = clip.pos(t)
                if isinstance(pos_[0], str):
                    if pos_[0] == "center":
                        pos_x = f.size[0] // 2 - frame.size[0] // 2
                    elif pos_[0] == "left":
                        pos_x = 0
                    elif pos_[0] == "right":
                        pos_x = f.size[0] - frame.size[0]
                    else:
                        raise ValueError(f"pos[0] must be 'center', 'left' or 'right'")
                elif isinstance(pos_[0], int) or isinstance(pos_[0], float):
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
    scaling_strategy: bool | None = None,
    transition: (
        VideoClip | Callable[[Image.Image, Image.Image, int | float], VideoClip] | None
    ) = None,
    audio: bool = True,
    audio_fps: int | None = None,
):
    # TODO: Add transition support
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

    if scaling_strategy is None:

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

    elif scaling_strategy is True:

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
    elif scaling_strategy is False:

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
            f"scaling_strategy must be bool or None, not {type(scaling_strategy)}"
        )
