import os
import math
from pathlib import Path
from typing import Callable, Self, Any
from PIL import Image
import PIL
import numpy as np
from ..decorators import *
from .VideoClip import VideoClip


class ImageSequenceClip(VideoClip):
    def __init__(
        self,
        sequence: (
            str
            | Path
            | tuple[Image.Image, ...]
            | tuple[np.ndarray, ...]
            | tuple[str | Path, ...]
        ),
        fps: int | float | None = None,
        duration: int | float | None = None,
        audio=None,
    ):
        super().__init__()

        self.clip: tuple[Image.Image, ...] = self._import_image_sequence(sequence)
        if fps is not None and duration is not None:
            self.fps = fps
            self._dur = duration
        elif fps is None and duration is not None:
            self.fps = len(self.clip) / duration
            self._dur = duration
        elif duration is None and fps is not None:
            self.fps = fps
            self._dur = len(self.clip) / fps
        else:
            raise ValueError("You must specify either fps or duration.")

        if audio is not None:
            self.set_audio(audio)

    def _import_image_sequence(
        self,
        sequence: (
            str | Path | tuple[str | Path] | tuple[Image.Image] | tuple[np.ndarray]
        ),
    ) -> tuple[Image.Image, ...]:
        if isinstance(sequence, tuple):
            if isinstance(sequence[0], Image.Image):
                return sequence
            elif isinstance(sequence[0], np.ndarray):
                return tuple(map(Image.fromarray, sequence))
            elif isinstance(sequence[0], (str, Path)) or (
                hasattr(sequence[0], "read") and callable(getattr(sequence[0], "read"))
            ):
                return tuple(map(Image.open, sequence))
            raise TypeError(
                "The sequence should contain either PIL images or paths to images or numpy array."
            )
        elif isinstance(sequence, (str, Path)):
            # use set comprehension to remove duplicates
            files = [
                os.path.join(sequence, file)
                for file in os.listdir(sequence)
                if os.path.isfile(os.path.join(sequence, file))
                and os.path.splitext(file)[1].lower()
                in set(Image.registered_extensions().keys())
            ]
            files.sort()
            return tuple(map(Image.open, files))
        raise TypeError(
            "The argument must be either a tuple of PIL images or paths to images or a path to a directory."
        )

    @requires_duration_or_end
    def make_frame_array(self, t) -> np.ndarray:
        time_per_frame = (self.duration if self.duration else self.end) / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return np.array(self.clip[frame_index])

    @requires_duration_or_end
    def make_frame_pil(self, t) -> Image.Image:
        if self.duration is None and self.end is None:
            raise ValueError("either duration or end must be set")
        time_per_frame = (self.duration if self.duration else self.end) / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return self.clip[frame_index]

    def fl_frame_transform(
        self,
        func: Callable[[Image.Image, tuple[Any], dict[str, Any]], Image.Image],
        *args,
        **kwargs
    ) -> Self:
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame = func(frame, *args, **kwargs)
            clip.append(frame)
        self.clip = tuple(clip)
        return self

    @requires_fps
    def fl_clip_transform(self, func, *args, **kwargs):
        td = 1 / self.fps
        frame_time = 0.0
        clip = []
        for frame in self.clip:
            clip.append(func(frame, frame_time, *args, **kwargs))
            frame_time += td
        del self.clip
        self.clip = tuple(clip)
        return self
