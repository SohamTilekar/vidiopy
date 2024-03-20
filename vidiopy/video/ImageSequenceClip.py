import os
import math
from pathlib import Path
from typing import Callable
from PIL import Image
import numpy as np
from ..decorators import *
from .VideoClip import VideoClip


class ImageSequenceClip(VideoClip):
    """
    A class used to represent a sequence of images as a video clip.

    This class extends the VideoClip class and provides additional functionality for handling sequences of images. It allows for the creation of a video clip from a sequence of images, with the ability to specify the frames per second (fps) and duration of the clip. The sequence of images can be provided as a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory. The class also provides methods for importing the image sequence, generating a numpy array or PIL Image representation of a specific frame in the clip, and applying a function to each frame of the clip.

    Attributes:
        clip (tuple[Image.Image, ...]): The sequence of images as a tuple of PIL Images.
        fps (int | float | None): The frames per second of the clip.
        _dur (int | float | None): The duration of the clip in seconds.
        audio (optional): The audio of the clip.

    Methods:
        __init__(sequence, fps=None, duration=None, audio=None): Initializes an instance of the ImageSequenceClip class.
        __eq__(other): Checks if this instance is equal to another instance.
        _import_image_sequence(sequence): Imports an image sequence from a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory.
        make_frame_array(t): Generates a numpy array representation of a specific frame in the clip.
        make_frame_pil(t): Generates a PIL Image representation of a specific frame in the clip.
        fl_frame_transform(func, *args, **kwargs): Applies a function to each frame of the clip.
        fl_clip_transform(func, *args, **kwargs): Applies a function to each frame of the clip along with its timestamp.
    """

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
        """
        Initializes an instance of the ImageSequenceClip class.

        This method imports an image sequence from the specified sequence, sets the fps and duration of the image sequence clip, and sets the audio of the image sequence clip if specified.

        Args:
            sequence (str | Path | tuple[Image.Image, ...] | tuple[np.ndarray, ...] | tuple[str | Path, ...]): The sequence to import. It can be a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory.
            fps (int | float | None, optional): The frames per second of the image sequence clip. If not specified, it is calculated from the duration and the number of images in the sequence.
            duration (int | float | None, optional): The duration of the image sequence clip in seconds. If not specified, it is calculated from the fps and the number of images in the sequence.
            audio (optional): The audio of the image sequence clip. If not specified, the image sequence clip will have no audio.

        Raises:
            ValueError: If neither fps nor duration is specified.
            ValueError: If not all images in the sequence have the same size.

        Example:
            >>> image_sequence_clip = ImageSequenceClip(("image1.jpg", "image2.jpg"), fps=24)

        Note:
            This method uses the _import_image_sequence method to import the image sequence and the set_audio method to set the audio of the image sequence clip.
        """
        # method body goes here
        super().__init__()

        self.clip: tuple[Image.Image, ...] = self._import_image_sequence(sequence)
        # Check if the images have the same size
        for i in range(1, len(self.clip)):
            if self.clip[i].size != self.clip[0].size:
                raise ValueError("All images must have the same size.")
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

    def __eq__(self, other) -> bool:
        if not hasattr(self, "clip"):
            return False
        return (
            isinstance(other, VideoClip)
            and self.fps == other.fps
            and self.size == other.size
            and self.start == other.start
            and self.end == other.end
            and self.duration == other.duration
            and self.audio == other.audio
            and self.clip == other.clip
        )

    def _import_image_sequence(
        self,
        sequence: (
            str | Path | tuple[str | Path] | tuple[Image.Image] | tuple[np.ndarray]
        ),
    ) -> tuple[Image.Image, ...]:
        """
        Imports an image sequence from a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory.

        This method checks the type of the sequence argument and imports the image sequence accordingly. If the sequence is a tuple of PIL Images, it returns the sequence as is. If the sequence is a tuple of numpy arrays, it converts each numpy array to a PIL Image. If the sequence is a tuple of paths to images, it opens each image and returns a tuple of PIL Images. If the sequence is a path to a directory, it opens all images in the directory and returns a tuple of PIL Images.

        Args:
            sequence (str | Path | tuple[str | Path] | tuple[Image.Image] | tuple[np.ndarray]): The sequence to import. It can be a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory.

        Returns:
            tuple[Image.Image, ...]: The imported image sequence as a tuple of PIL Images.

        Raises:
            TypeError: If the sequence is not a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory.

        Example:
            >>> image_sequence_clip = ImageSequenceClip()
            >>> image_sequence = image_sequence_clip._import_image_sequence(("image1.jpg", "image2.jpg"))

        Note:
            This method uses the PIL Image class to open images and convert numpy arrays to images.
        """
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
    def make_frame_array(self, t: int | float) -> np.ndarray:
        """
        Generates a numpy array representation of a specific frame in the image sequence clip.

        This method calculates the index of the frame for a specific time, retrieves the frame from the image sequence clip, and converts it to a numpy array.

        Args:
            t (int | float): The time of the frame to convert.

        Returns:
            np.ndarray: The numpy array representation of the frame.

        Raises:
            None

        Example:
            >>> image_sequence_clip = ImageSequenceClip()
            >>> frame_array = image_sequence_clip.make_frame_array(10)

        Note:
            This method uses the duration or end of the image sequence clip to calculate the time per frame.
        """
        time_per_frame = (self.duration if self.duration else self.end) / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return np.array(self.clip[frame_index])

    @requires_duration_or_end
    def make_frame_pil(self, t: int | float) -> Image.Image:
        """
        Generates a PIL Image representation of a specific frame in the image sequence clip.

        This method calculates the index of the frame for a specific time, retrieves the frame from the image sequence clip, and returns it as a PIL Image.

        Args:
            t (int | float): The time of the frame to convert.

        Returns:
            Image.Image: The PIL Image representation of the frame.

        Raises:
            ValueError: If neither the duration nor the end of the image sequence clip is set.

        Example:
            >>> image_sequence_clip = ImageSequenceClip()
            >>> frame_image = image_sequence_clip.make_frame_pil(10)

        Note:
            This method uses either the duration or the end of the image sequence clip to calculate the time per frame.
        """
        if self.duration is None and self.end is None:
            raise ValueError("either duration or end must be set")
        time_per_frame = (self.duration if self.duration else self.end) / len(self.clip)
        frame_index = math.floor(t / time_per_frame)
        frame_index = min(len(self.clip) - 1, max(0, frame_index))
        return self.clip[frame_index]

    def fl_frame_transform(
        self, func: Callable[..., Image.Image], *args, **kwargs
    ) -> "ImageSequenceClip":
        """
        Applies a function to each frame of the image sequence clip.

        This method iterates over each frame in the image sequence clip, applies a function to it, and replaces the original frame with the result. The function is expected to take a PIL Image as its first argument and return a PIL Image.

        Args:
            func (Callable[..., Image.Image]): The function to apply to each frame. It should take a PIL Image as its first argument and return a PIL Image.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            ImageSequenceClip: The current instance of the ImageSequenceClip class.

        Raises:
            None

        Example:
            >>> image_sequence_clip = ImageSequenceClip()
            >>> image_sequence_clip.fl_frame_transform(lambda frame: frame.rotate(90))

        Note:
            This method modifies the current instance of the ImageSequenceClip class in-place.
        """
        clip: list[Image.Image] = []
        for frame in self.clip:
            frame = func(frame, *args, **kwargs)
            clip.append(frame)
        self.clip = tuple(clip)
        return self

    @requires_fps
    def fl_clip_transform(
        self, func: Callable[..., Image.Image], *args, **kwargs
    ) -> "ImageSequenceClip":
        """
        Applies a function to each frame of the image sequence clip along with its timestamp.

        This method iterates over each frame in the image sequence clip, applies a function to it and its timestamp, and replaces the original frame with the result. The function is expected to take a PIL Image and a float as its first two arguments and return a PIL Image.

        Args:
            func (Callable[..., Image.Image]): The function to apply to each frame. It should take a PIL Image and a float as its first two arguments and return a PIL Image.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            ImageSequenceClip: The current instance of the ImageSequenceClip class.

        Raises:
            ValueError: If the fps of the image sequence clip is not set.

        Example:
            >>> image_sequence_clip = ImageSequenceClip()
            >>> image_sequence_clip.fl_clip_transform(lambda frame, t: frame.rotate(90 * t))

        Note:
            This method modifies the current instance of the ImageSequenceClip class in-place.
        """
        td = 1 / self.fps
        frame_time = 0.0
        clip = []
        for frame in self.clip:
            clip.append(func(frame, frame_time, *args, **kwargs))
            frame_time += td
        del self.clip
        self.clip = tuple(clip)
        return self
