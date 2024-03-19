# AudioClip

> `#!py class` `#!py vidiopy.AudioClip`

: Bases: `#!py vidiopy.Clip`

    The AudioClip class represents an audio clip. It is a subclass of the Clip class.

    Parameters:

    :   
        - `#!py duration (int or float, optional)`: The duration of the audio clip. Defaults to `#!py None`.
        - `#!py fps (int, optional)`: Frames per second of the audio clip. Defaults to `#!py None`.

    Attributes:

    :   
        - `#!py fps: int | None`: The frames per second of the audio clip. Defaults to `#!py fps` Parameter.
        - `#!py _original_dur: int | float | None`: The original duration of the audio clip. Defaults to `#!py duration` Parameter.
        - `#!py _audio_data: np.ndarray | None`: The audio data of the clip. Defaults to `#!py None`.
        - `#!py channels: int | None`: The number of audio channels. Defaults to `#!py None`.
        - `#!py _st: int | float`: The start time of the audio clip. Defaults to `#!py 0.0`.
        - `#!py _ed: int | float | None`: The end time of the audio clip. Defaults to `#!py duration` Parameter.

    Properties:

    :   
        > `#!py audio_data: np.ndarray`

        :   This property gets the audio data. If the audio data is not set, it `#!py raises` a `#!py ValueError`.

            Returns:
            :   `#!py np.ndarray`: The audio data.

            Raises:
            :   `#!py ValueError`: If the audio data is not set.

            Example:
            :
                ```python
                >>> clip = AudioClip()
                >>> clip.audio_data = np.array([1, 2, 3])
                >>> print(clip.audio_data)
                array([1, 2, 3])
                ```

        > `#!py duration: int | float`

        :   This property gets the duration of the audio clip. The duration is represented in seconds and can be an `#!py integer`, a `#!py float`, or `#!py None` if the duration is not set.

            Note:
            :   You Can't Set the duration of the audio clip it is not allowed to change directly.

            Raises:
                `#!py AttributeError`: Always raises an `#!py AttributeError` if you try to set duration.

            Returns:
            :   `#!py int | float`: The duration of the audio clip.

            Example:
            :
                ```python
                >>> clip = AudioClip(duration=10)
                >>> print(clip.duration)
                10
                ```

        > `#!py start: int | float`

        :   This property gets the start time of the audio clip. The start time is represented in seconds and can be an `#!py integer` or a `#!py float`.

            Returns:
            :   `#!py int | float`: The start time of the audio clip.

            Example:
            :
                ```python
                >>> clip = AudioClip()
                >>> print(clip.start)
                0.0
                >>> clip.start = 5
                >>> print(clip.start)
                5
                ```

        > `#!py end: int | float | None`

        :   This property gets the end time of the audio clip. The end time is represented in seconds and can be an `#!py integer`, a `#!py float`, or `#!py None` if the end time is not set.

            Returns:
            :   `#!py int | float | None`: The end time of the audio clip.

            Example:
            :
                ```python
                >>> clip = AudioClip(duration=10)
                >>> print(clip.end)
                10
                >>> clip.end = 5
                >>> print(clip.end)
                5
                ```

    Methods:
    
    :   
        > `#!py def` `#!py set_data(self, audio_data: np.ndarray) -> Self`:

        :   
            This method sets the audio data and returns the instance of the class.

            Args:
            :   audio_data (np.ndarray): The audio data to set.

            Returns:
            :   AudioClip: The instance of the class.

            Example:
            :
                ```python
                    >>> clip = AudioClip()
                    >>> clip.set_data(np.array([1, 2, 3]))
                    >>> print(clip.audio_data)
                    array([1, 2, 3])
                ```

        > `#!py def` `#!py set_fps(self, fps: int | None) -> Self`:

        :   
            This method sets the frames per second (fps) for the audio clip and `#!py returns` the instance of the `#!py class`.

            Args:
            :   `#!py fps: int | None`: The frames per second to set. If `#!py None`, the fps will be unset.

            Returns:
            :   `#!py AudioClip`: `#!py Self` The Instance of the `#!py class`.

            Example:
            :
                ```python
                >>> clip = AudioClip()
                >>> clip.set_fps(30)
                >>> print(clip.fps)
                30
                ```

        > `#!py def` `#!py set_start(self, start: int | float) -> Self`:

        :   
            This method sets the start time of the audio clip and returns the instance of the class.
            The start time is represented in seconds and can be an `#!py integer` or a `#!py float`.

            Args:
            :   `#!py start: int | float`: The start time to set in seconds.

            Returns:
            :   `#!py AudioClip`: The instance of the class with the updated start time.

            Example:
            :
                ```python
                >>> clip = AudioClip()
                >>> clip.set_start(5)
                >>> print(clip.start)
                5
                ```

        > `#!py def` `#!py set_end(self, end: int | float | None) -> Self`:

        :   
            This method sets the end time of the audio clip and returns the instance of the class.
            The end time is represented in seconds and can be an `#!py integer`, a `#!py float`, or `#!py None` if the end time is not to be set.

            Args:
            :   `#!py end: int | float | None`: The end time to set in seconds.

            Returns:
            :   `#!py AudioClip`: The instance of the class with the updated end time.

            Example:
            :
                ```python
                >>> clip = AudioClip()
                >>> clip.set_end(10)
                >>> print(clip.end)
                10
                ```

        > `#!py def` `#!py get_frame_at_t(self, t: int | float) -> np.ndarray`:

        :   
            This method gets the audio frame at a specific time `t`. The time `t` is represented in seconds and can be an `#!py integer` or a `#!py float`.
            It calculates the frame index using the duration, total frames, and time `t`, and returns the audio data at that frame index.

            Args:
            :   `#!py t: int | float`: The time in seconds at which to get the audio frame.

            Returns:
            :   `#!py np.ndarray`: The audio data at the specified time.

            Raises:
            :   `#!py ValueError`: If frames per second (fps) is not set, audio data is not set, or original duration is not set.

        > `#!py def` `#!py iterate_frames_at_fps(self, fps: int | float | None = None) -> Generator[np.ndarray, None, None]:`

        :   
            This method generates audio frames at a specific frames per second (fps) rate. If no fps is provided, it uses the fps set in the AudioClip instance.
            It calculates the original fps using the duration and total frames, then generates frames at the specified fps rate.

            Args:
            :   `#!py fps (int | float | None, optional)`: The frames per second rate at which to generate frames. If not provided, the fps set in the AudioClip instance is used.

            Yields:
            :   `#!py np.ndarray`: The audio data at each frame.

            Raises:
            :   `#!py ValueError`: If frames per second (fps) is not set, audio data is not set, or original duration is not set.

        > `#!py def` `#!py iterate_all_frames(self) -> Generator[np.ndarray, None, None]:`

        :   
            This method generates all audio frames in the `#!py AudioClip` instance. It iterates over each frame in the audio data and `#!py yields` it.

            Yields:
            :   `#!py np.ndarray`: The audio data at each frame.

            Raises:
            :   `#!py ValueError`: If audio data is not set.

        > `#!py def` `#!py fl_frame_transform(self, func, *args, **kwargs) -> Self:`

        :   
            This method applies a function to each frame of the audio data. The function should take a frame (an ndarray of channel data) as its first argument,
            followed by any number of additional positional and keyword arguments.

            Args:
            :   - `#!py func (Callable)`: The function to apply to each frame. It should take a frame (an ndarray of channel data) as its first argument.
                - `#!py *args`: Additional positional arguments to pass to the function.
                - `#!py **kwargs`: Additional keyword arguments to pass to the function.

            Returns:
            :   `#!py AudioClip`: The instance of the class with the transformed audio data.

            Raises:
            :   `#!py ValueError`: If audio data is not set.

        > `#!py def` `#!py fl_clip_transform(self, func, *args, **kwargs) -> Self:`

        :   
            This method applies a function to the entire audio data. The function should take the AudioClip instance as its first argument,
            followed by any number of additional positional and keyword arguments.

            Args:
            :   - `#!py func (Callable)`: The function to apply to the audio data. It should take the AudioClip instance as its first argument.
                - `#!py *args`: Additional positional arguments to pass to the function.
                - `#!py **kwargs`: Additional keyword arguments to pass to the function.

            Returns:
            :   `#!py AudioClip`: The instance of the class with the transformed audio data.

            Raises:
            :   `#!py ValueError`: If audio data is not set.

        > `#!py def` `#!py fl_time_transform(self, func: Callable[[int | float], int | float]) -> Self:`

        :   
            This method applies a time transformation function to the `get_frame_at_t` method of the AudioClip instance.
            The transformation function should take a time (an integer or a float) as its argument and return a transformed time.

            The `get_frame_at_t` method is replaced with a new method that applies the transformation function to its argument before calling the original method.

            Args:
            :   `#!py func (Callable[[int | float], int | float])`: The time transformation function to apply. It should take a time (an integer or a float) as its argument and return a transformed time.

            Returns:
            :   `#!py AudioClip`: The instance of the class with the transformed `get_frame_at_t` method.

            Raises:
            :   `#!py ValueError`: If the `get_frame_at_t` method is not set.

        > `#!py def` `#!py sub_clip_copy(self, start: float | int | None = None, end: float | int | None = None) -> Self`

        :   This method creates a copy of the AudioClip instance and then creates a subclip from the audio clip starting from `start` to `end` in the copied instance.
            If `start` or `end` is not provided, it uses the start or end time set in the AudioClip instance. If neither is set, it uses 0 for start and the duration for end.

            It calculates the original frames per second (fps) using the duration and total frames, then calculates the start and end frame indices using the original fps.
            It then updates the audio data, original duration, end time, and start time of the copied AudioClip instance.

            Args:
            :   - `#!py start (float | int | None, optional)`: The start time of the subclip in seconds. If not provided, the start time set in the AudioClip instance is used. Defaults to `#!py None`.
                - `#!py end (float | int | None, optional)`: The end time of the subclip in seconds. If not provided, the end time set in the AudioClip instance is used. Defaults to `#!py None`.

            Returns:
            :   `#!py AudioClip`: A copy of the instance of the class with the updated audio data, original duration, end time, and start time.

            Raises:
            :   `#!py ValueError`: If audio data is not set, original duration is not set, or end time is greater than the original duration.

        > `#!py def` `#!py copy(self) -> Self`:

        :   This method creates a deep copy of the AudioClip instance and returns it. It uses the `copy_` function, which should be a deep copy function like `copy.deepcopy` in Python's standard library.

        Returns:
        :   `#!py AudioClip`: A deep copy of the instance of the class.

        Raises:
        :   `#!py ValueError`: If the `copy_` function is not set or does not correctly create a deep copy.

        > `#!py def` `#!py write_audiofile(self, path: str, fps: int | None = None, overwrite=True, show_log=False, **kwargs) -> None:`
        :   This method writes the audio data to an audio file at the specified path.
            It uses the frames per second (fps) if provided, otherwise it uses the fps set in the `#!py AudioClip` instance.
            It raises a `#!py ValueError` if fps is not set in either way.
            It also raises a `#!py ValueError` if audio data, original duration, or channels are not set.

            It creates a temporary audio data array by getting the frame at each time step from `#!py 0` to the end or duration with a step of `1/fps`.
            It then writes the temporary audio data to the audio file using the `#!py ffmpegio.audio.write` function.

            Args:
            :   - path (str): The path to write the audio file to.
                - fps (int | None, optional): The frames per second to use. If not provided, the fps set in the AudioClip instance is used. Defaults to None.
                - overwrite (bool, optional): Whether to overwrite the audio file if it already exists. Defaults to True.
                - show_log (bool, optional): Whether to show the log of the `ffmpegio.audio.write` function. Defaults to False.
                - **kwargs: Additional keyword arguments to pass to the `ffmpegio.audio.write` function.

            Raises:
            :   `#!py ValueError`: If fps is not set, audio data is not set, original duration is not set, or channels are not set.
