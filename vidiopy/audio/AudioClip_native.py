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
import os
import pathlib
import re
from typing import Generator
from copy import copy as copy_
import ffmpegio
import numpy as np
from ..Clip import Clip

__all__ = [
    'AudioClip',
    'AudioFileCLip',
    'AudioArrayClip',
    'ConcatAudioClip',
    'CompositeAudioClip'
]


class AudioClip(Clip):

    def __init__(self, duration=None, fps=None):
        self.fps: int | None = fps
        self._original_dur: int | float | None = duration
        self._audio_data: np.ndarray | None = None
        self.channels: int | None = None
        self._st: int | float | None = None
        self._ed: int | float | None = None

    def __repr__(self):
        return f'<{self.__class__.__name__} channels={self.channels} duration={self.duration} fps={self.fps} start={self._st} end={self._ed} at {hex(id(self))}>'

    @property
    def audio_data(self) -> np.ndarray:
        if self._audio_data is None:
            raise ValueError('AudioClip._audio_data is None')
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
        raise AttributeError('Not Allowed to set duration')

    def set_duration(self, duration: int | float):
        self._original_dur = duration
        return self

    get_duration = duration

    @property
    def start(self) -> int | float | None:
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
    def end(self, end: int | float):
        self._ed = end

    def set_end(self, end: int | float):
        self._ed = end
        return self

    def get_frame_at_t(self, t: int | float) -> np.ndarray:
        if self.fps is None:
            raise ValueError('Frames per second (fps) is not set')
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        if self.duration is None:
            raise ValueError('Original duration is not set')

        # Calculate the Frame index using the duration, total_frames & time t
        frame_index = int((t / self.duration) * len(self._audio_data)) - 1
        return self._audio_data[frame_index]

    def iterate_frames_at_fps(self, fps: int | float | None = None) -> Generator[np.ndarray, None, None]:
        if fps is None:
            if self.fps is None:
                raise ValueError('Frames per second (fps) is not set')
            fps = self.fps
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        if self.duration is None:
            raise ValueError('Original duration is not set')

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        frame_index = 0
        while frame_index < len(self._audio_data):
            yield self._audio_data[frame_index]
            frame_index += int(original_fps / fps)

    def iterate_all_frames(self):
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        for frame in self._audio_data:
            yield frame

    def fl_frame_transform(self, func, *args, **kwargs):
        """Apply a function to each frame of the audio data
            frame=ndarray([chanel1: float, chanel2: float, ...])
        """
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        self._audio_data = np.array(
            [func(frame, *args, **kwargs) for frame in self._audio_data])
        return self

    def fl_clip_transform(self, func, *args, **kwargs):
        """Apply a function to the entire audio data
            frame=ndarray([chanel1: float, chanel2: float, ...])
        """
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        func(self, *args, **kwargs)
        return self

    def trim_audio_in_place(self, start: float | int | None = None, end: float | int | None = None):
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        if self.duration is None:
            raise ValueError('Original duration is not set')
        if start is None:
            start = self.start if self.start is not None else 0
        if end is None:
            end = self.start + \
                self.duration if self.start is not None and self.duration is not None else 0

        # Add check for end value
        if end > self.duration:
            raise ValueError(
                'End value cannot be greater than the original duration')

        # Calculate the original fps
        original_fps = len(self._audio_data) / self.duration

        # Calculate the frame index based on the original fps
        start_frame_index = int(start * original_fps)
        end_frame_index = int(end * original_fps)

        self._audio_data = self._audio_data[start_frame_index:end_frame_index]
        self._original_dur = end - start
        return self

    def trim_audio(self, start: float | int | None = None, end: float | int | None = None):
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        if self.duration is None:
            raise ValueError('Original duration is not set')
        if start is None:
            start = self.start if self.start is not None else 0
        if end is None:
            end = self.start + \
                self.duration if self.start is not None and self.duration is not None else start + self.duration

        # Add check for end value
        if end > self.duration:
            raise ValueError(
                'End value cannot be greater than the original duration')

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

    def write_audiofile(self, path: str, fps: int | None = None, overwrite=True, **kwargs):
        if fps is None:
            if self.fps is None:
                raise ValueError('Frames per second (fps) is not set')
            fps = self.fps
        if self._audio_data is None:
            raise ValueError('Audio data is not set')
        if self.duration is None:
            raise ValueError('Original duration is not set')
        if self.channels is None:
            raise ValueError('Channels is not set')

        # Convert the audio Data to the temp_Audio_Data using the duration & fps & _audio_data
        temp_audio_data = np.array([self.get_frame_at_t(
            t) for t in np.arange(0, self.duration, 1 / fps)])

        ffmpegio.audio.write(path, fps, temp_audio_data,
                             overwrite=overwrite, **kwargs)

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
        #             print(frame)
        #             writer.write(frame)
        # else:
        #     if os.path.isfile(path):
        #         raise ValueError(
        #             'File already exists. Please use a different filename or delete the existing file or put `overwrite=True`.')
        #     with ffmpegio.open(path, 'w', in_fps, rate=fps, **kwargs) as writer:
        #         for frame in self._audio_data:
        #             writer.write(frame)
        # return self


class AudioFileClip(AudioClip):
    def __init__(self, path: str | pathlib.Path):
        info = ffmpegio.probe.audio_streams_basic(path)[0]
        self.fps = info['sample_rate']
        self._original_dur = info['duration']
        super().__init__(self._original_dur, self.fps)
        self.path = path
        self.start = info['start_time']
        self.end = info['duration'] - info['start_time']
        self.channels = info['channels']
        self._audio_data = ffmpegio.audio.read(path)[1]


class AudioArrayClip(AudioClip):
    def __init__(self, audio_data: np.ndarray, fps: int | float, duration: int | float):
        self._audio_data = audio_data
        self.fps = fps
        self._original_dur = duration
        super().__init__(self._original_dur, self.fps)


class ConcatAudioClip(AudioClip):
    def __init__(self, audioclips: list[AudioClip]):
        self.audioclips = audioclips
        self.fps = audioclips[0].fps
        self._original_dur = sum(
            [clip.duration for clip in audioclips if clip.duration is not None])
        self._audio_data = np.concatenate(
            [clip.audio_data for clip in audioclips])
        super().__init__(self._original_dur, self.fps)


class CompositeAudioClip(AudioClip):
    def __init__(self, audioclips: list[AudioClip]):
        self.audioclips = audioclips
        self.fps = max(
            [clip.fps for clip in audioclips if clip.fps is not None])
        temp_durations = []
        for clip in audioclips:
            if clip.end is not None and clip.start is not None:
                temp_durations.append(clip.end - clip.start)
            elif clip.duration is not None:
                temp_durations.append(clip.duration)
            else:
                temp_durations.append(0)
        self._original_dur = durations = max(temp_durations)
        time_per_frame = 1 / self.fps
        clips = []
        for audio in audioclips:
            if audio.end is None:
                clips.append(audio.trim_audio(audio.start))
            else:
                clips.append(audio.trim_audio(audio.start, audio.end))
        audio_clip_list = []
        current_frame_time = 0.0
        while current_frame_time < durations:
            for clip in clips:
                audio_clip_list.append(clip.get_frame_at_t(current_frame_time))
            current_frame_time += time_per_frame
        self._audio_data = np.array(audio_clip_list)
