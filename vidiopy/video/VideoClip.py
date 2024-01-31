from re import S
from rich import print as rich_print
from functools import wraps
import rich.progress as progress
from fractions import Fraction
import os
from copy import copy as copy_
import subprocess
import tempfile
from typing import Callable, Generator, Any, Self
from PIL import Image
import ffmpegio
import numpy as np
from ..Clip import Clip
from ..audio.AudioClip import AudioClip
from ..decorators import *
from .. import config


class VideoClip(Clip):
    def __init__(self) -> None:
        super().__init__()

        # Time-related properties
        self._st: int | float = 0.0
        self._ed: int | float | None = None
        self._dur: int | float | None = None

        # Video and audio properties
        self.audio: AudioClip | None = None
        self.fps: int | float | None = None
        self.size: tuple[int, int] | None = None

        # Position-related properties
        self.pos = lambda t: (0, 0)
        self.relative_pos = False

    #################
    # Magic Methods #
    #################

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}, start={self.start}, end={self.end}, fps={self.fps}, size={self.size}, duration={self.duration}, audio={self.audio} id={hex(id(self))}"""

    def __str__(self) -> str:
        return f"""{self.__class__.__name__}, start={self.start}, end={self.end}, fps={self.fps}, size={self.size}, duration={self.duration}, audio={self.audio}"""

    def __len__(self) -> int | float | None:
        return self._dur

    @requires_fps
    def __iter__(self) -> Generator[np.ndarray[Any, Any], Any, None]:
        if not self.fps:
            raise ValueError("FPS is not set")
        return self.iterate_frames_array_t(self.fps)

    #############################
    # Properties getter & setter#
    #############################

    @property
    @requires_size
    def width(self) -> int:
        if self.size is not None:
            return self.size[0]
        else:
            raise ValueError("Size is not set")

    w = width

    @property
    @requires_size
    def height(self) -> int:
        if self.size is not None:
            return self.size[1]
        else:
            raise ValueError("Size is not set")

    h = height

    @property
    @requires_size
    def aspect_ratio(self) -> Fraction:
        if isinstance(self.w, int) and isinstance(self.w, int):
            return Fraction(self.w, self.h)
        else:
            raise ValueError("Size is not Valid")

    @property
    def start(self) -> int | float:
        return self._st

    @start.setter
    def start(self, t) -> Self:
        self._st = t

        if self.start is None:
            return self

        if self.audio:
            self.audio.start = self.start
        return self

    def set_start(self, value: int | float) -> Self:
        self.start = value
        return self

    @property
    def end(self) -> int | float | None:
        return self._ed

    @end.setter
    def end(self, t) -> Self:
        self._ed = t
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def set_end(self, value) -> Self:
        self.end = value
        return self

    @property
    def duration(self) -> int | float | None:
        return self._dur

    @duration.setter
    def duration(self, dur: int | float) -> Self:
        self.set_duration(dur)
        return self

    def set_duration(self, value) -> Self:
        raise ValueError("Duration is not allowed to be set")
        return self

    def set_position(
        self,
        pos: (
            tuple[int | float, int | float]
            | Callable[[float | int], tuple[int | float, int | float]]
        ),
        relative=False,
    ) -> Self:
        self.relative_pos = relative
        if callable(pos):
            if relative:
                self.pos = lambda t: (
                    int(pos(t)[0] * self.width),
                    int(pos(t)[1] * self.height),
                )
            else:
                if (
                    isinstance(pos(1), float)
                    and isinstance(pos(1.1), float)
                    and isinstance(pos(0), float)
                ):
                    raise ValueError("Pos is Invalid Type not tuple of int.")
                self.pos = lambda t: ((lambda p: (p[0], p[1]))(pos(t)))  # type: ignore
        elif isinstance(pos, tuple):
            pos_ = int(pos[0]), int(pos[1])
            self.pos: Callable[[float | int], tuple[int, int]] = (
                (lambda t: pos_)
                if not self.relative_pos
                else (lambda t: (int(pos[0] * self.width), int(pos[1] * self.height)))
            )
        else:
            raise TypeError("Pos is Invalid Type not Callable or tuple of int.")
        return self

    def set_audio(self, audio: AudioClip | None) -> Self:
        self.audio = audio
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
        return self

    def set_fps(self, fps: int | float) -> Self:
        self.fps = fps
        return self

    def without_audio(self) -> Self:
        self.audio = None
        return self

    def __copy__(self) -> Self:
        # Get the class of the current instance
        cls = self.__class__

        # Create a new instance of the class
        new_clip = cls.__new__(cls)

        # Iterate through the attributes of the current instance
        for attr, value in self.__dict__.items():
            # Set the attribute in the new instance
            setattr(new_clip, attr, copy_(value))

        # Return the shallow copy
        return new_clip

    # Alias for the __copy__ method
    copy = __copy__

    ####################################
    # EFFECT METHODS  F I L T E R I N G#
    ####################################

    def make_frame_array(self, t) -> np.ndarray:
        raise NotImplemented("Make Frame is Not Set.")

    def make_frame_pil(self, t) -> Image.Image:
        raise NotImplemented("Make Frame pil is Not Set.")

    def get_frame(self, t: int | float, is_pil=None) -> np.ndarray | Image.Image:
        if is_pil is None or is_pil is False:
            return self.make_frame_array(t)
        elif is_pil is True:
            return self.make_frame_pil(t)
        else:
            raise ValueError("is_pil must be True, False, or None")

    def iterate_frames_pil_t(
        self, fps: int | float
    ) -> Generator[Image.Image, Any, None]:
        time_dif = 1 / fps
        t = self.start
        if self.end is not None:
            while t <= self.end:
                yield self.make_frame_pil(t)
                t += time_dif
        elif self.duration is not None:
            while t <= self.duration:
                yield self.make_frame_pil(t)
                t += time_dif
        else:
            raise ValueError("end or duration must be set.")

    def iterate_frames_array_t(
        self, fps: int | float
    ) -> Generator[np.ndarray, Any, None]:
        time_dif = 1 / fps
        t = 0
        if self.end is not None:
            while t <= self.end:
                yield self.make_frame_array(t)
                t += time_dif
        elif self.duration is not None:
            while t <= self.duration:
                yield self.make_frame_array(t)
                t += time_dif
        else:
            raise ValueError("end or duration must be set.")

    def sub_clip_copy(
        self, t_start: int | float | None = None, t_end: int | float | None = None
    ) -> Self:
        """\
        Returns a subclip of the clip.__copy__, starting at time t_start (in seconds)
        """
        raise NotImplementedError("sub_clip method must be overridden in the subclass.")

    def sub_clip(
        self, t_start: int | float | None = None, t_end: int | float | None = None
    ) -> Self:
        """\
        Returns a subclip of the clip, starting at time t_start (in seconds)
        """
        raise NotImplementedError("sub_clip method must be overridden in the subclass.")

    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """\
        Apply a frame transformation function to each frame of the video clip.
        calls the function func on each frame of the clip. like below
        >>> frames = []
        >>> for frame in clip._Depends_upon_sub_class_:
        >>>     frame = func(frame, *args, **kwargs)
        >>>     frames.append(frame)
        >>> clip._Depends_upon_sub_class_ = tuple(frames)
        Just boiler plate code can be modified as per the need.
        """
        raise NotImplementedError(
            "fl_frame_transform method must be overridden in the subclass."
        )
        return self

    def fl_clip_transform(self, func, *args, **kwargs) -> Self:
        """\
        Apply a function to the entire video clip, generating a new clip.
        calls the function func on the clip. like below
        >>> frames = []
        >>> for frame in clip._Depends_upon_sub_class_:
        >>>     frame = func(frame, frame_time, *args, **kwargs)
        >>>     frames.append(frame)
        >>> clip._Depends_upon_sub_class_ = tuple(frames)
        """
        raise NotImplementedError(
            "fl_clip_transform method must be overridden in the subclass."
        )
        return self

    def fl_time_transform(self, func_t: Callable[[int], int]) -> Self:
        original_make_frame_pil_t = self.make_frame_pil
        original_make_frame_array_t = self.make_frame_array

        @wraps(original_make_frame_array_t)
        def modified_make_frame_array_t(t):
            transformed_t = func_t(t)
            return original_make_frame_array_t(transformed_t)

        @wraps(original_make_frame_pil_t)
        def modified_make_frame_pil_t(t):
            transformed_t = func_t(t)
            return original_make_frame_pil_t(transformed_t)

        self.make_frame_array = modified_make_frame_array_t
        self.make_frame_pil = modified_make_frame_pil_t
        return self

    def fx(self, func, *args, **kwargs) -> Self:
        self = func(self, *args, **kwargs)
        return self

    def sub_fx(
        self,
        func,
        *args,
        start_t: int | float | None = None,
        end_t: int | float | None = None,
        **kwargs,
    ) -> Self:
        """\
        """
        clip = copy_(self)
        clip = clip.sub_clip(start_t, end_t)
        clip = clip.fx(func, *args, **kwargs)
        return clip

    def _sync_audio_video_s_e_d(self) -> Self:
        if self.audio:
            self.audio.start = self.start
            self.audio.end = self.end
            self.audio._original_dur = self.duration
        return self

    #####################
    # EXPORT OPERATIONS #
    #####################

    def write_videofile(
        self,
        filename,
        fps=None,
        codec=None,
        bitrate=None,
        audio=True,
        audio_fps=44100,
        preset="medium",
        pixel_format=None,
        audio_codec=None,
        audio_bitrate=None,
        threads=None,
        ffmpeg_params: dict[str, str] | None = None,
        logger="bar",
        over_write_output=True,
    ) -> Self:
        # Generate video frames using iterate_frames_array_t method
        total_frames = (
            int(
                (self.end - self.start)
                / (
                    1
                    / (
                        fps
                        if fps
                        else (
                            self.fps
                            if self.fps
                            else (_ for _ in ()).throw(
                                Exception("fps is not provided and set.")
                            )
                        )
                    )
                )
            )
            if self.end is not None
            else 0
        )

        video_np = np.asarray(
            tuple(
                progress.track(
                    self.iterate_frames_array_t(
                        fps
                        if fps
                        else (
                            self.fps
                            if self.fps
                            else (_ for _ in ()).throw(
                                Exception("fps is not provided and set.")
                            )
                        )
                    ),
                    description="Processing Frames ...",
                    total=total_frames,
                    transient=True,
                    style="bar.back",
                )
            )
        )
        rich_print(
            "[bold magenta]Vidiopy[/bold magenta] - Video Frames Has Been Processed :thumbs_up:."
        )
        # Extract audio name without extension
        audio_name, _ = os.path.splitext(filename)

        # Set default values for ffmpeg options
        ffmpeg_options = {
            "preset": preset,
            **(ffmpeg_params if ffmpeg_params is not None else {}),
            **({"c:v": codec} if codec else {}),
            **({"b:v": bitrate} if bitrate else {}),
            **({"pix_fmt": pixel_format} if pixel_format else {}),
            **({"c:a": audio_codec} if audio_codec else {}),
            **({"ar": audio_fps} if audio_fps else {}),
            **({"b:a": audio_bitrate} if audio_bitrate else {}),
            **({"threads": threads} if threads else {}),
        }

        audio_file_name = None
        temp_video_file_name = None

        try:
            # Determine the fps to use
            fps_to_use = fps if fps else self.fps if self.fps else None

            # Create a temporary video file
            dir__, file__ = os.path.split(filename)
            temp_video_file = tempfile.NamedTemporaryFile(
                dir=dir__,
                suffix="video__temp__" + os.path.splitext(file__)[1],
                delete=False,
            )
            temp_video_file_name = temp_video_file.name
            temp_video_file.close()

            # Write video frames to the temporary file using ffmpegio
            with progress.Progress(transient=True) as progress_bar:
                current_frame = 0
                pbar = progress_bar.add_task(
                    description="Writing Video File",
                    total=total_frames,
                )

                def function_callback(status: dict, done: bool):
                    nonlocal current_frame
                    current_frame = status["frame"] - current_frame
                    progress_bar.update(pbar, completed=current_frame, refresh=True)

                ffmpegio.video.write(
                    temp_video_file_name,
                    fps_to_use,
                    video_np,
                    overwrite=over_write_output,
                    progress=function_callback,
                    **ffmpeg_options,
                )
                progress_bar.update(pbar, completed=True, visible=False)
            rich_print(
                "[bold magenta]Vidiopy[/bold magenta] - Video is Created :thumbs_up:"
            )
            if self.audio and audio:
                self._sync_audio_video_s_e_d()
                temp_audio_file = tempfile.NamedTemporaryFile(
                    suffix=".wav", prefix=audio_name + "_temp_audio_", delete=False
                )
                audio_file_name = temp_audio_file.name
                temp_audio_file.close()

                # Write audio to the temporary file
                self.audio.write_audiofile(audio_file_name)

                # Combine video and audio using ffmpeg
                with progress.Progress(transient=True) as progress_bar:
                    sp = progress_bar.add_task("Combining Video & Audio", total=None)
                    subprocess.run(
                        f'{config.FFMPEG_BINARY} -i {temp_video_file_name} -i {audio_file_name} -acodec copy {"-y" if over_write_output else ""} {filename}',
                        capture_output=True,
                        text=True,
                    )
                    progress_bar.update(sp, completed=True)
                rich_print(
                    f"[bold magenta]Vidiopy[/bold magenta] - ✔ Audio Video Combined Final video : - {filename} :thumbs_up:",
                    flush=True,
                )

            return self
        finally:
            if audio_file_name:
                os.remove(audio_file_name)
            # Rename temporary video file to the final filename if no audio is present
            if (not self.audio or not audio) and temp_video_file_name:
                os.replace(temp_video_file_name, filename)
                temp_video_file_name = None
                rich_print(
                    f"[bold magenta]Vidiopy[/bold magenta] - ✔ Final video : - {filename} :thumbs_up:",
                    flush=True,
                )
            if temp_video_file_name:
                os.remove(temp_video_file_name)

    def write_videofile_subclip(
        self,
        filename,
        start_t: int | float | None = None,
        end_t: int | float | None = None,
        fps=None,
        codec=None,
        bitrate=None,
        audio=True,
        audio_fps=44100,
        preset="medium",
        pixel_format=None,
        audio_codec=None,
        audio_bitrate=None,
        write_logfile=False,
        verbose=True,
        threads=None,
        ffmpeg_params: dict[str, str] | None = None,
        logger="bar",
        over_write_output=True,
    ) -> Self:
        clip = self.sub_clip_copy(start_t, end_t)
        clip.write_videofile(
            filename,
            fps,
            codec,
            bitrate,
            audio,
            audio_fps,
            preset,
            pixel_format,
            audio_codec,
            audio_bitrate,
            write_logfile,
            verbose,
            threads,
            ffmpeg_params,
            logger,
            over_write_output,
        )
        return self

    def write_image_sequence(
        self, nformat: str, fps: int | float | None = None, dir="."
    ) -> Self:
        def save_frame(frame: Image.Image, frame_number: int):
            frame.save(
                os.path.join(
                    dir, f"{frame_number:0{len(str(total_frames)) + 1}}{nformat}"
                )
            )

        if dir != "." and not os.path.exists(dir):
            os.makedirs(dir)

        if fps:
            frames_generator = self.iterate_frames_pil_t(fps)
            total_frames = (1 / fps) * self.duration if self.duration else None
        elif self.fps and self.duration:
            frames_generator = self.iterate_frames_pil_t(self.fps)
            total_frames = (1 / self.fps) * self.duration if self.duration else None
        else:
            raise ValueError(
                "Warning: FPS is not provided, and fps and duration are not set."
            )

        frame_number = 0
        for frame in progress.track(
            frames_generator,
            total=total_frames,
            description="Vidiopy - Writing Image Sequence :smiley:",
            transient=True,
        ):
            save_frame(frame, frame_number)
            frame_number += 1
        rich_print(
            "[bold magenta]Vidiopy[/bold magenta] - Image Sequence Has Been Written:thumbs_up:."
        )
        return self

    def save_frame(self, t, filename) -> Self:
        self.make_frame_pil(t).save(filename)
        return self

    def to_ImageClip(self, t):
        import ImageClips

        return ImageClips.Data2ImageClip(self.make_frame_pil(t))
