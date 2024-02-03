from typing import Callable, Union, Type
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
        self.clip, self.fps = self._import_video_clip(filename, ffmpeg_options)
        self.fps = float(self.fps)
        # Set video properties
        self.size = (video_data["width"], video_data["height"])
        self.start = 0.0
        # not all videos have a duration attribute in their metadata
        if video_data["duration"]:
            self.end = video_data["duration"]
            self._dur = video_data["duration"]
        else:
            self.end = len(self.clip) / self.fps
            self._dur = self.end
        # If audio is enabled, attach audio clip
        if audio:
            audio = AudioFileClip(filename, self._dur)
            audio.set_start(self.start).set_end(self.end)
            self.set_audio(audio)

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, filename={self.filename}, id={hex(id(self))},
        audio={(self.audio)})"""

    def __str__(self) -> str:
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, filename={self.filename}, id={hex(id(self))},
        audio={(self.audio)})"""

    #################
    # EFFECT METHODS#
    #################

    @requires_start_end
    def fl_frame_transform(self, func, *args, **kwargs) -> "VideoFileClip":
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame: Image.Image = func(frame, *args, **kwargs)
            clip.append(frame)
        self.clip = tuple(clip)
        return self

    @requires_fps
    def fl_clip_transform(self, func, *args, **kwargs) -> "VideoFileClip":
        td = 1 / self.fps
        frame_time = 0.0
        clip: list[Image.Image] = []
        for frame in self.clip:
            clip.append(func(frame, frame_time, *args, **kwargs))
            frame_time += td
        del self.clip
        self.clip = tuple(clip)
        return self

    def fx(self, func: Callable, *args, **kwargs) -> "VideoFileClip":
        # Apply an effect function directly to the clip
        self = func(self, *args, **kwargs)
        return self

    @requires_fps
    def sub_clip(
        self,
        t_start: Union[int, float, None] = None,
        t_end: Union[int, float, None] = None,
    ) -> "VideoFileClip":
        if t_end is None and t_start is None:
            return self
        if t_end is None:
            t_end = (
                self.end
                if self.end
                else (
                    self.duration
                    if self.duration
                    else (_ for _ in ()).throw(
                        ValueError("end or duration must be set.")
                    )
                )
            )
        if t_start is None:
            t_start = self.start if self.start else 0.0
        frames = []
        time_per_frame = 1 / self.fps
        current_frame_time = self.start

        while current_frame_time < t_end:
            frames.append(self.make_frame_pil(current_frame_time))
            current_frame_time += time_per_frame

        self.clip = tuple(frames)
        self.start = 0.0
        self.end = t_end
        self._dur = t_end - t_start
        return self

    @requires_fps
    def sub_clip_copy(
        self,
        t_start: Union[int, float, None] = None,
        t_end: Union[int, float, None] = None,
    ) -> "VideoFileClip":
        clip = self.copy()
        if t_end is None and t_start is None:
            return clip.copy()
        if t_end is None:
            t_end = (
                clip.end
                if clip.end
                else (
                    clip.duration
                    if clip.duration
                    else (_ for _ in ()).throw(
                        ValueError("end or duration must be set.")
                    )
                )
            )
        if t_start is None:
            t_start = clip.start if clip.start else 0.0
        frames = []
        time_per_frame = 1 / clip.fps
        current_frame_time = clip.start

        while current_frame_time < t_end:
            frames.append(clip.make_frame_pil(current_frame_time))
            current_frame_time += time_per_frame

        self.clip = tuple(frames)
        self.start = 0.0
        self.end = t_end
        self._dur = t_end
        return self

    @requires_duration
    def make_frame_array(self, t) -> np.ndarray:
        if self.duration is None:
            raise ValueError("Duration is Not Set.")
        time_per_frame = self.duration / len(self.clip)
        frame_index = t / time_per_frame
        frame_index = int(min(len(self.clip) - 1, max(0, frame_index)))
        return np.array(self.clip[frame_index])

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
        fps, frames = ffmpegio.video.read(file_name, **options)
        return tuple(Image.fromarray(frame) for frame in frames), fps
