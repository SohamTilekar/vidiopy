# ImageSequenceClip

> `#!py class` `#!py vidiopy.VideoClip.ImageSequenceClip`

:   Bases: `#!py vidiopy.VideoClip.VideoClip(sequence, fps=None, duration=None, audio=None)`
    
    A class used to represent a sequence of images as a video clip. This class extends the VideoClip class and provides additional functionality for handling sequences of images.

    Attributes:
    :   - `#!py clip (tuple[Image.Image, ...])`: The sequence of images as a tuple of PIL Images.

        - It inherits all the attributes from the `VideoClip` class.

    Parameters:
    :   - `#!py sequence (str | Path | tuple[Image.Image, ...] | tuple[np.ndarray, ...] | tuple[str | Path, ...])`: The sequence to import. It can be a tuple of PIL Images, paths to images, numpy arrays, or a path to a directory.
        - `#!py fps (int | float | None, optional)`: The frames per second of the image sequence clip. If not specified, it is calculated from the `duration` and the number of images in the `sequence`.
        - `#!py duration (int | float | None, optional)`: The duration of the image sequence clip in seconds. If not specified, it is calculated from the `fps` and the number of images in the `sequence`.
        - `#!py audio (optional)`: The audio of the image sequence clip. If not specified, the image sequence clip will have no audio.

    Methods:
    :   > `#!py make_frame_array(t)`

        :   Generates a numpy array representation of a specific frame in the image sequence clip.

            This method calculates the index of the frame for a specific time, retrieves the frame from the image sequence clip, and converts it to a numpy array.

            **Parameters**:
            - `#!py t (int | float)`: The time of the frame to convert.

            **Returns**:
            - `#!py np.ndarray`: The numpy array representation of the frame.

            **Requires**:
            - `#!py duration` or `#!py end` to be set.

        > `#!py make_frame_pil(t)`

        :   Generates a PIL Image representation of a specific frame in the image sequence clip.

            This method calculates the index of the frame for a specific time, retrieves the frame from the image sequence clip, and returns it as a PIL Image.

            **Parameters**:
            - `#!py t (int | float)`: The time of the frame to convert.

            **Returns**:
            - `#!py Image.Image`: The PIL Image representation of the frame.

            **Raises**:
            - `#!py ValueError`: If neither the `duration` nor the `end` of the image sequence clip is set.

            **Requires**:
            - `#!py duration` or `#!py end` to be set.

        > `#!py fl_frame_transform(func, *args, **kwargs)`

        :   Applies a function to each frame of the image sequence clip.

            This method iterates over each frame in the image sequence clip, applies a function to it, and replaces the original frame with the result. The function is expected to take a PIL Image as its first argument and return a PIL Image.

            **Parameters**:
            - `#!py func (Callable[..., Image.Image])`: The function to apply to each frame. It should take a PIL Image as its first argument and return a PIL Image.
            - `#!py *args`: Additional positional arguments to pass to the function.
            - `#!py **kwargs`: Additional keyword arguments to pass to the function.

            **Returns**:
            - `#!py ImageSequenceClip`: The current instance of the `ImageSequenceClip` class.

            **Example**:
            ```python
            >>> image_sequence_clip = ImageSequenceClip()
            >>> image_sequence_clip.fl_frame_transform(lambda frame: frame.rotate(90))
            ```

        > `#!py fl_clip_transform(func, *args, **kwargs)`

        :   Applies a function to each frame of the image sequence clip along with its timestamp.

            This method iterates over each frame in the image sequence clip, applies a function to it and its timestamp, and replaces the original frame with the result. The function is expected to take a PIL Image and a float as its first two arguments and return a PIL Image.

            **Parameters**:
            - `#!py func (Callable[..., Image.Image])`: The function to apply to each frame. It should take a PIL Image and a float as its first two arguments and return a PIL Image.
            - `#!py *args`: Additional positional arguments to pass to the function.
            - `#!py **kwargs`: Additional keyword arguments to pass to the function.

            **Returns**:
            - `#!py ImageSequenceClip`: The current instance of the `ImageSequenceClip` class.

            **Raises**:
            - `#!py ValueError`: If the `fps` of the image sequence clip is not set.

            **Requires**:
            - `#!py fps` to be set.

            **Example**:
            ```python
            >>> image_sequence_clip = ImageSequenceClip()
            >>> image_sequence_clip.fl_clip_transform(lambda frame, t: frame.rotate(90 * t))
            ```