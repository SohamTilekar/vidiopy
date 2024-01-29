from typing import override, Callable, Self
from PIL import Image
import ffmpegio
import numpy as np
from .VideoClip import VideoClip
from ..audio.AudioClip import AudioFileClip
from ..decorators import *


class VideoFileClip(VideoClip):
    def __init__(self, filename, audio=True, ffmpeg_options=None):
        super().__init__()

        self.filename = filename

        # Probe video streams and extract relevant information
        video_data = ffmpegio.probe.video_streams_basic(filename)[0]

        # Import video clip using ffmpeg
        self.clip = self._import_video_clip(filename, ffmpeg_options)

        # Set video properties
        self.fps: float = float(video_data["frame_rate"])
        self.size = (video_data["width"], video_data["height"])
        self.start = 0.0
        self.end = video_data["duration"]
        self._dur = float(self.end)
        # If audio is enabled, attach audio clip
        if audio:
            audio = AudioFileClip(filename, self._dur)
            audio.set_start(self.start).set_end(self.end)
            self.set_audio(audio)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} path={self.filename} start={self.start} end={self.end} fps={self.fps} size={self.size}, {id(self)}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} path={self.filename} start={self.start} end={self.end} fps={self.fps} size={self.size}"

    #################
    # EFFECT METHODS#
    #################

    @override
    @requires_start_end
    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame: Image.Image = func(frame, *args, **kwargs)
            clip.append(frame)
        self.clip = tuple(clip)
        return self

    @override
    def fl_clip_transform(self, func, *args, **kwargs):
        td = 1 / self.fps
        frame_time = 0.0
        clip: list[Image.Image] = []
        for frame in self.clip:
            clip.append(func(frame, frame_time, *args, **kwargs))
            frame_time += td
        del self.clip
        self.clip = tuple(clip)
        return self

    def fx(self, func: Callable, *args, **kwargs):
        # Apply an effect function directly to the clip
        self = func(self, *args, **kwargs)
        return self

    @override
    def sub_clip(
        self, t_start: int | float | None = None, t_end: int | float | None = None
    ) -> Self:
        if t_end is None and t_start is None:
            return self
        if t_end is None:
            t_end = (
                self.end
                if self.end
                else self.duration
                if self.duration
                else (_ for _ in ()).throw(ValueError("end or duration must be set."))
            )
        if t_start is None:
            t_start = self.start if self.start else 0.0
        frames = []
        time_per_frame = 1 / self.fps
        current_frame_time = self.start

        while current_frame_time <= t_end:
            frames.append(self.make_frame_pil(current_frame_time))
            current_frame_time += time_per_frame

        self.clip = tuple(frames)
        self.start = 0.0
        self.end = t_end
        self._dur = t_end - t_start
        return self

    @override
    def sub_clip_copy(
        self, t_start: int | float | None = None, t_end: int | float | None = None
    ) -> Self:
        clip = self.copy()
        if t_end is None and t_start is None:
            return clip.copy()
        if t_end is None:
            t_end = (
                clip.end
                if clip.end
                else clip.duration
                if clip.duration
                else (_ for _ in ()).throw(ValueError("end or duration must be set."))
            )
        if t_start is None:
            t_start = clip.start if clip.start else 0.0
        frames = []
        time_per_frame = 1 / clip.fps
        current_frame_time = clip.start

        while current_frame_time <= t_end:
            frames.append(clip.make_frame_pil(current_frame_time))
            current_frame_time += time_per_frame

        self.clip = tuple(frames)
        self.start = 0.0
        self.end = t_end
        self._dur = t_end
        return self

    @override
    @requires_duration
    def make_frame_array(self, t) -> np.ndarray:
        if self.duration is None:
            raise ValueError("Duration is Not Set.")
        time_per_frame = self.duration / len(self.clip)
        frame_index = t / time_per_frame
        frame_index = int(min(len(self.clip) - 1, max(0, frame_index)))
        return np.array(self.clip[frame_index])

    @override
    @requires_duration
    def make_frame_pil(self, t) -> Image.Image:
        if self.duration is None:
            raise ValueError("Duration is Not Set.")
        time_per_frame = self.duration / len(self.clip)
        frame_index = t / time_per_frame
        frame_index = int(min(len(self.clip) - 1, max(0, frame_index)))
        return self.clip[frame_index]

    def _import_video_clip(self, file_name, ffmpeg_options):
        options = {**(ffmpeg_options if ffmpeg_options else {})}
        return tuple(
            Image.fromarray(frame)
            for frame in ffmpegio.video.read(file_name, **options)[1]
        )
