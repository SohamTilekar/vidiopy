"""\
AudioClip_native.py - Audio Clips
=================================

This module contains the AudioClip class which is the base class for all audio clips. 
This class is a subclass of the Clip class. 

The following classes are defined:
    - AudioClip
    - AudioFileCLip
    - AudioArrayClip
    - ConcatAudioClip

"""
import pathlib
from typing import Generator
from copy import copy as copy_
import ffmpegio
import numpy as np
from ..Clip import Clip

__all__ = [
    "AudioClip",
    "AudioFileClip",
    "AudioArrayClip",
    "concatenate_audioclips",
    "composite_audioclips",
]


class AudioClip(Clip):
    def __init__(self, duration=None, fps=None):
        super().__init__()
        self.fps: int | None = fps
        self._original_dur: int | float | None = duration
        self._audio_data: np.ndarray | None = None
        self.channels: int | None = None
        self._st: int | float = 0.0
        self._ed: int | float | None = duration

    def __repr__(self):
        return f"""{self.__class__.__name__}(start={self.start}, end={self.end}, duration={self.duration}, fps={self.fps}, channels={self.channels}, id={hex(id(self))})"""

    def __str__(self):
        return f"""{self.__class__.__name__}(start={self.start}, end={self.end}, duration={self.duration}, fps={self.fps}, channels={self.channels})"""

    @property
    def audio_data(self) -> np.ndarray:
        if self._audio_data is None:
            raise ValueError("AudioClip._audio_data is None")
        return self._audio_data

    @audio_data.setter
    def audio_data(self, audio_data: np.ndarray):
        self._audio_data = audio_data

    def set_data(self, audio_data: np.ndarray):
        self._audio_data = audio_data
        return self

    @property
    def duration(self) -> int | float | None:
        return self._original_dur

    @duration.setter
    def duration(self, duration: int | float):
        raise AttributeError("Not Allowed to set duration")

    def set_duration(self, duration: int | float):
        self._original_dur = duration
        return self

    get_duration = duration

    @property
    def start(self) -> int | float:
        return self._st

    @start.setter
    def start(self, start: int | float):
        self._st = start

    def set_start(self, start: int | float):
        self._st = start
        return self

    @property
    def end(self) -> int | float | None:
        return self._ed

    @end.setter
    def end(self, end: int | float | None):
        self._ed = end

    def set_end(self, end: int | float | None):
        self._ed = end
        return self

    def get_frame_at_t(self, t: int | float) -> np.ndarray:
        if self.fps is None:
            raise ValueError("Frames per second (fps) is not set")
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None and self.end is None:
            raise ValueError("Original duration is not set")

        # Calculate the Frame index using the duration, total_frames & time t
        frame_index = int((t / (self.end or self.duration)) * len(self._audio_data)) - 1
        return self._audio_data[frame_index]

    def iterate_frames_at_fps(
        self, fps: int | float | None = None
    ) -> Generator[np.ndarray, None, None]:
        if fps is None:
            if self.fps is None:
                raise ValueError("Frames per second (fps) is not set")
            fps = self.fps
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None:
            raise ValueError("Original duration is not set")

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        frame_index = 0
        while frame_index < len(self._audio_data):
            yield self._audio_data[frame_index]
            frame_index += int(original_fps / fps)

    def iterate_all_frames(self):
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        for frame in self._audio_data:
            yield frame

    def fl_frame_transform(self, func, *args, **kwargs):
        """Apply a function to each frame of the audio data
        frame=ndarray([chanel1: float, chanel2: float, ...])
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        self._audio_data = np.array(
            [func(frame, *args, **kwargs) for frame in self._audio_data]
        )
        return self

    def fl_clip_transform(self, func, *args, **kwargs):
        """Apply a function to the entire audio data
        frame=ndarray([chanel1: float, chanel2: float, ...])
        """
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        func(self, *args, **kwargs)
        return self

    def trim_audio_in_place(
        self, start: float | int | None = None, end: float | int | None = None
    ):
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None:
            raise ValueError("Original duration is not set")
        if start is None:
            start = self.start if self.start is not None else 0
        if end is None:
            end = (
                self.start + self.duration
                if self.start is not None and self.duration is not None
                else 0
            )

        # Add check for end value
        if end > self.duration:
            raise ValueError("End value cannot be greater than the original duration")

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        start_frame_index = int(start * original_fps)
        end_frame_index = int(end * original_fps)

        self._audio_data = self._audio_data[start_frame_index:end_frame_index]
        self._original_dur = end - start
        return self

    def trim_audio(
        self, start: float | int | None = None, end: float | int | None = None
    ):
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None:
            raise ValueError("Original duration is not set")
        if start is None:
            start = self.start if self.start is not None else 0
        if end is None:
            end = (
                self.start + self.duration
                if self.start is not None and self.duration is not None
                else start + self.duration
            )

        # Add check for end value
        if end > self.duration:
            raise ValueError("End value cannot be greater than the original duration")

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        start_frame_index = int(start * original_fps)
        end_frame_index = int(end * original_fps)

        audio_data = self._audio_data[start_frame_index:end_frame_index]

        instance = self.copy()
        instance._audio_data = audio_data
        instance._original_dur = end - start
        return instance

    def copy(self):
        return copy_(self)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, end = key.start, key.stop
            return self.trim_audio(start, end)
        else:
            raise TypeError("Invalid argument type.")

    def write_audiofile(
        self, path: str, fps: int | None = None, overwrite=True, **kwargs
    ):
        if fps is None:
            if self.fps is None:
                raise ValueError("Frames per second (fps) is not set")
            fps = self.fps
        if self._audio_data is None:
            raise ValueError("Audio data is not set")
        if self.duration is None and self.end is None:
            raise ValueError("Original duration is not set")
        if self.channels is None:
            raise ValueError("Channels is not set")

        # Convert the audio Data to the temp_Audio_Data using the duration & fps & _audio_data
        temp_audio_data = np.array(
            [
                self.get_frame_at_t(t)
                for t in np.arange(0, self.end or self.duration, 1 / fps)
            ]
        )
        ffmpegio.audio.write(path, fps, temp_audio_data, overwrite=overwrite, **kwargs)

        # # Calculating the in_fps of the audio data using the audio length and the duration
        # in_fps = len(self._audio_data) // self.duration

        # if overwrite:
        #     if os.path.isfile(path):
        #         os.remove(path)
        #     with ffmpegio.open(url_fg=path,
        #                        mode='wa',
        #                        rate_in=in_fps,
        #                        rate=fps,
        #                        **kwargs) as writer:
        #         for frame in self._audio_data:
        #             writer.write(frame)
        # else:
        #     if os.path.isfile(path):
        #         raise ValueError(
        #             'File already exists. Please use a different filename or delete the existing file or put `overwrite=True`.')
        #     with ffmpegio.open(path, 'w', in_fps, rate=fps, **kwargs) as writer:
        #         for frame in self._audio_data:
        #             writer.write(frame)
        # return self


class SilenceClip(AudioClip):
    def __init__(self, duration: int | float, fps: int = 44100, channels: int = 1):
        self.fps = fps
        self._original_dur: int | float = duration
        super().__init__(self._original_dur, self.fps)
        self.channels = channels
        self._audio_data = np.zeros((int(duration * self.fps), self.channels))


class AudioFileClip(SilenceClip):
    def __init__(self, path: str | pathlib.Path, duration: int | float | None = None):
        info = ffmpegio.probe.audio_streams_basic(path)
        if not info:
            self.fps = 44100
            self.channels = 1
            duration = (
                duration
                if duration
                else (_ for _ in ()).throw(
                    ValueError("Audio is empty and duration is not provided")
                )
            )
            super().__init__(duration, self.fps, self.channels)
        else:
            info = info[0]
            self.fps = info["sample_rate"]
            self._original_dur = info["duration"]
            self.channels = info["channels"]
            super().__init__(info["duration"], info["sample_rate"], info["channels"])
            self.path = path
            self.start = info["start_time"]
            self.end = info["duration"] - info["start_time"]
            self._audio_data = ffmpegio.audio.read(path)[1]


class AudioArrayClip(AudioClip):
    def __init__(self, audio_data: np.ndarray, fps: int, duration: int | float):
        self.fps = fps
        self._original_dur = duration
        super().__init__(self._original_dur, self.fps)
        self.channels = audio_data.shape[1]
        self._audio_data = audio_data


def concatenate_audioclips(
    clips: list[AudioClip], fps: int | None = 44100
) -> AudioClip | AudioArrayClip:
    """Concatenate multiple audio clips into a single audio clip"""
    if len(clips) == 0:
        raise ValueError("No clips to concatenate")
    if len(clips) == 1:
        return clips[0].copy()
    clip: list[np.ndarray] = []
    fps = fps if fps else max([c.fps if c.fps else 0 for c in clips])
    if not fps:
        raise ValueError("No fps value found place set fps value or fps value in clips")
    duration = sum(
        [
            c.end - c.start
            if c.end
            else c.duration
            if c.duration
            else (_ for _ in ()).throw(ValueError(""))
            for c in clips
        ]
    )
    channels: int = max(
        [
            c.channels
            if c.channels
            else (_ for _ in ()).throw(ValueError("clip channels is not set"))
            for c in clips
        ]
    )
    for c in clips:
        c_channels: int = (
            c.channels
            if c.channels
            else (_ for _ in ()).throw(ValueError("clip channels is not set"))
        )
        dif_channels = channels - c_channels
        for f in c.iterate_frames_at_fps(fps):
            clip.append(np.concatenate((f, [f.mean()] * dif_channels)))
    return AudioArrayClip(np.asarray(clip), fps, duration)


def composite_audioclips(clips: list[AudioClip], fps: int | None = 44100):
    fps = fps if fps else max([c.fps if c.fps else 0 for c in clips])
    if not fps:
        raise ValueError("No fps value found place set fps value or fps value in clips")
    duration = max(
        [
            c.end - c.start
            if c.end
            else c.duration - c.start
            if c.duration
            else (_ for _ in ()).throw(ValueError(""))
            for c in clips
        ]
    )
    if not duration:
        raise ValueError(
            "No duration value found place set duration value or duration value in clips"
        )
    channels: int = max(
        [
            c.channels
            if c.channels
            else (_ for _ in ()).throw(ValueError("clip channels is not set"))
            for c in clips
        ]
    )
    if not channels:
        raise ValueError(
            "No channels value found place set channels value or channels value in clips"
        )
    td = 1 / fps
    t = 0.0
    frames = []
    while t < duration:
        frame_ch = []
        for c in clips:
            if (
                c.start < t < c.end
                if c.end
                else c.duration
                if c.duration
                else (_ for _ in ()).throw(ValueError("audio clip duration is not set"))
            ):
                c_frame = c.get_frame_at_t(t)
                extend_num = channels - len(c_frame)
                frame_ch.append(
                    np.concatenate((c_frame, [c_frame.mean()] * extend_num))
                )
        frames.append(np.sum(frame_ch, axis=0))
        t += td
    return AudioArrayClip(np.array(frames), fps, duration)
