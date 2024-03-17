# VideoClip

> `#!py class` `#!py vidiopy.VideoClip.VideoClip`

:   Base: `#!py vidiopy.Clip.Clip`
    
    A VideoClip is a Base Class for all Video And Image clips (`#!py VideoFileClip`, `#!py ImageClip` and `#!py ImageSequenceClip`)

    See `#!py VideoFileClip`, `#!py ImageClip` etc. for more user-friendly classes.

    Attributes:
    :   > _st: `#!py float | int`
        
        :   The start time of the clip (in seconds).

        > _ed: `#!py float | int | None`

        :   The end time of the clip (in seconds).

        > _dur: `#!py float | int | None`

        :   The Duration of the clip (in seconds).

            ??? warning "Warning: Not Real Duration"
                It Many not equal to `#!py video.end - video.start`.
                It is the Original Duration In which Video Is imported or any thing else.
        
        > fps: `#!py float | int | None`

        :   The FPS(Frame per Second) of the Video.

        > size: `#!py tuple[int, int]`

        :   The size of the clip, (width,height), in pixels.

        > audio: `#!py AudioClip | None`

        :   Audio in the Video.

        > pos: `#!py Callable[[float | int], tuple[int | str | float, int | str | float]]`

        : A function `#!py t->(x,y)` where x,y is the position of the clip when it is composed with other clips. See VideoClip.set_pos for more details.

        > relative_pos: `#!py bool`

        : A Bool Which Determine whether the pos will output a relative position or in pixel.

    Properties:
    :   > start: `#!py float | int`
        
        :   The start time of the clip (in seconds).

        > end: `#!py float | int | None`

        :   The end time of the clip (in seconds).

        > duration: `#!py float | int | None`

        :   The Duration of the clip (in seconds).

            ??? warning "Warning: Not Real Duration"
                It Many not equal to `#!py video.end - video.start`.
                It is the Original Duration In which Video Is imported or any thing else.
        
        > width | w: `#!py int`

        :   The width of the clip, in pixels.

        > height | h: `#!py int`

        :   The height of the clip, in pixels.

        > aspect_ratio: `#!py Fraction`

        :   The aspect ratio of the clip, (width / height).

    methods:
    :   > `#!py set_start(self, value: int | float) -> VideoClip`

        :   The set_start method is used to set the start time of the video clip.
            It Changes _st attribute of the VideoClip.

            Args:
            :   `#!py value: int | float`: The start time of the video clip.

            Returns:
            :   `#!py VideoClip`: The instance of the VideoClip after setting the start time.

        > `#!py set_end(self, value: int | float) -> VideoClip`

        :   The set_end method is used to set the end time of the video clip.
            It Changes _ed attribute of the VideoClip.

            Args:
            :   `#!py value: int | float`: The end time of the video clip.

            Returns:
            :   `#!py VideoClip`: The instance of the VideoClip after setting the end time.

        > `#!py set_duration(self, value: int | float) -> VideoClip`

        :   Setter for the duration of the video clip.
            it raises a ValueError since duration is not allowed to be set.
            but you can change the duration using `#!py clip._dur = value` or the `#!py _set_duration` method.

            Args:
            :   `#!py dur: int | float`: The duration to set for the video clip.

            Returns:
            :   `#!py NoReturn`: Raises a `#!py ValueError` since duration is not allowed to be set.

            Raises:
            :   `#!py ValueError`: If an attempt is made to set the duration, a `#!py ValueError` is raised.
        
        > `#!py _set_duration(self, value: int | float) -> VideoClip`

        :   Private method to set the duration of the video clip.
            It Changes _dur attribute of the VideoClip.

            Args:
            :   `#!py value: int | float`: The duration to set for the video clip.

            Returns:
            :   `#!py VideoClip`: The instance of the `#!py VideoClip` after setting the duration.

        > `#!py set_position(self, pos: (tuple[int | float | str, int | float | str] | list[int | float | str] | Callable[[float | int], tuple[int | float | str, int | float | str]]), relative=False) -> Self:`

        :   Sets the position of the video clip.
            This is useful for the concatenate method, where the position of the video clip is used  to set it on other clip.
            This method allows the position of the video clip to be set either as a fixed tuple of coordinates, or as a function that returns a tuple of coordinates at each time. The position can be set as absolute or relative to the size of the clip using the relative.

            Note:
            :   - It Should Be the coordinates of the Video on the top left corner.
                - If relative is True, the position should be between the 0.0 & 1.0.
                - If relative is False, the position should be between the 0 & width or height of the video.


            Parameters:
            :   `#!py pos: tuple | Callable`: The position to set for the video clip. This can be either:
                :   - a tuple of two integers or floats, representing the x and y coordinates of the position, or
                    - a callable that takes a single float or integer argument (representing the time) and returns a tuple of two integers or floats, representing the x and y coordinates of the position.
                `#!py relative (bool, optional)`: Whether the position is relative to the size of the clip. If True, the position is interpreted as a fraction of the clip's width and height. Defaults to False.

            Raises:
            :   `#!py TypeError`: If `pos` is not a tuple or a callable.

            Returns:
            :   `#!py self`: Returns the instance of the class.
        
        > `#!py set_audio(self, audio: AudioClip | None) -> Self`:

        :   Sets the audio for the video clip.

            This method assigns the provided audio clip to the video clip. If the audio clip is not `#!py None`,
            it also sets the start and end times of the audio clip to match the video clip's start and end times.

            Parameters:
            :   `#!py audio: AudioClip | None`: The audio clip to be set to the video clip. If `#!py None`, no audio is set.

            Returns:
            :   `#!py Self`: Returns the instance of the class with updated audio clip.

        > `#!py without_audio(self) -> Self`:
            
        :   Removes the audio from the current VideoClip instance.

            This method sets the 'audio' attribute of the VideoClip instance to None, effectively removing any audio that the clip might have.

            Returns:
            :   VideoClip: The same instance of the VideoClip but without any audio. This allows for method chaining.

            Example:
            :   
                ```python
                >>> clip = VideoClip(...)
                >>> clip_without_audio = clip.without_audio()
                ```

            Note:
            :   This method modifies the VideoClip instance in-place. If you want to keep the original clip with audio, consider making a copy before calling this method.

        > `#!py set_fps(self, fps: int | float) -> Self`:
        
        :   Set the frames per second (fps) for the video clip.

            This method allows you to set the fps for the video clip. The fps value
            determines how many frames are shown per second during playback. A higher
            fps value results in smoother video playback.

            Parameters:
            :   `#!py fps: int | float`: The frames per second value to set. This can be an integer
                or a float. For example, a value of 24 would mean 24 frames are shown per second.

            Raises:
            :   `#!py TypeError`: If the provided fps value is not an integer or a float.

            Returns:
            :   `#!py Self`: Returns the instance of the class, allowing for method chaining.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> clip.set_fps(24)
                ```
        
        > `#!py make_frame_array(self, t) -> np.ndarray`:

        :   Generate a frame at time `t` as a NumPy array.

            This method is intended to be overridden in subclasses. It should return
            a NumPy array representing the frame at the given time.

            Parameters:
            :   `#!py t: float`: The time at which to generate the frame.

            Raises:
            :   `#!py NotImplementedError`: If the method is not overridden in a subclass.

            Returns:
            :   `#!py np.ndarray`: A NumPy array representing the frame at time `t`.

            Example:
            :   
                ```python
                >>> clip = VideoClipSubclass()
                >>> frame = clip.make_frame_array(0.5)
                ```
        
        > `#!py make_frame_pil(self, t) -> np.ndarray`:

        :   Generate a frame at time `t` as a NumPy array.

            This method is intended to be overridden in subclasses. It should return
            a PIL representing the frame at the given time.

            Parameters:
            :   `#!py t: float`: The time at which to generate the frame.

            Raises:
            :   `#!py NotImplementedError`: If the method is not overridden in a subclass.

            Returns:
            :   `#!py np.ndarray`: A NumPy array representing the frame at time `t`.

            Example:
            :   
                ```python
                >>> clip = VideoClipSubclass()
                >>> frame = clip.make_frame_pil(0.5)
                ```

        > `#!py get_frame(self, t: int | float, is_pil=None) -> np.ndarray | Image.Image`:

        :   Get a frame at time `t`.

            This method returns a frame at the given time `t`. The frame can be returned
            as a NumPy array or a PIL Image, depending on the value of `is_pil`.

            Parameters:
            :   `#!py t: int | float`: The time at which to get the frame.
                `#!py is_pil (bool, optional)`: If `#!py True`, the frame is returned as a PIL Image. If `#!py False` or None, the frame is returned as a NumPy array. Defaults to None.

            Raises:
            :   `#!py ValueError`: If `is_pil` is not `#!py True`, `#!py False`, or None.

            Returns:
            :   `#!py np.ndarray | Image.Image`: The frame at time `t` as a NumPy array or a PIL Image.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> frame_array = clip.get_frame(0.5)
                >>> frame_pil = clip.get_frame(0.5, is_pil=True)
                ```

        > `#!py iterate_frames_pil_t(self, fps: int | float) -> Generator[Image.Image, Any, None]`:

        :   Iterate over frames as PIL Images at a given frames per second (fps).

            This method generates frames at a given fps as PIL Images. The frames are
            generated from the start of the clip to the end or duration, whichever is set.

            Parameters:
            :   `#!py fps: int | float`: The frames per second at which to generate frames.

            Raises:
            :   `#!py ValueError`: If neither end nor duration is set.

            Yields:
            :   `#!py Image.Image`: The next frame as a PIL Image.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> for frame in clip.iterate_frames_pil_t(24):
                ...     # Do something with frame
                ```

        > `#!py iterate_frames_array_t(self, fps: int | float) -> Generator[np.ndarray, Any, None]`:

        :   Iterate over frames as NumPy arrays at a given frames per second (fps).

            This method generates frames at a given fps as NumPy arrays. The frames are
            generated from the start of the clip to the end or duration, whichever is set.

            Parameters:
            :   `#!py fps: int | float`: The frames per second at which to generate frames.

            Raises:
            :   `#!py ValueError`: If neither end nor duration is set.

            Yields:
            :   `#!py np.ndarray`: The next frame as a NumPy array.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> for frame in clip.iterate_frames_array_t(24):
                ...     # Do something with frame
                ```

        > `#!py sub_clip_copy(self, t_start: int | float | None = None, t_end: int | float | None = None) -> Self`:

        :   Returns a subclip of the clip.__copy__, starting at time t_start (in seconds).

            Parameters:
            :   `#!py t_start: int | float | None, optional`: The start time of the subclip in seconds. Defaults to None.
            :   `#!py t_end: int | float | None, optional`: The end time of the subclip in seconds. Defaults to None.

            Returns:
            :   `#!py Self`: The subclip of the clip.

            Raises:
            :   `#!py NotImplementedError`: If the method is not overridden in a subclass.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> subclip = clip.sub_clip_copy(t_start=1.5, t_end=3.5)
                ```

        > `#!py sub_clip(self, t_start: int | float | None = None, t_end: int | float | None = None) -> Self`:

        :   Returns a subclip of the clip, starting at time t_start and ending at time t_end.

            Parameters:
            :   `#!py t_start: int | float | None, optional`: The start time of the subclip in seconds. Defaults to None.
            :   `#!py t_end: int | float | None, optional`: The end time of the subclip in seconds. Defaults to None.

            Returns:
            :   `#!py Self`: The subclip of the clip.

            Raises:
            :   `#!py NotImplementedError`: If the method is not overridden in a subclass.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> subclip = clip.sub_clip(t_start=1.5, t_end=3.5)
                ```

        > `#!py fl_frame_transform(self, func, *args, **kwargs) -> Self`:

        :   Apply a frame transformation function to each frame of the video clip.

            This method calls the provided function `func` on each frame of the clip and applies the transformation.
            The transformed frames are then stored in a list and assigned back to the clip.

            Parameters:
            :   `#!py func`: The frame transformation function to be applied.
            :   `#!py *args`: Additional positional arguments to be passed to the transformation function.
            :   `#!py **kwargs`: Additional keyword arguments to be passed to the transformation function.

            Returns:
            :   `#!py Self`: The modified video clip object.

            Example:
            :   
                ```python
                >>> def grayscale(frame):
                >>>     # Convert frame to grayscale
                >>>     return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                >>>
                >>> clip = VideoClip()
                >>> clip.fl_frame_transform(grayscale)
                ```

            Note:
            :   This method is meant to be overridden in the subclass. If not overridden, it raises a NotImplementedError.
            :   The transformation function `func` should accept a single frame as the first argument and return the transformed frame.

        > `#!py fl_time_transform(self, func_t: Callable[[int | float], int | float]) -> Self`:

        :   Apply a time transformation function to the clip.

            This method modifies the `make_frame_array` and `make_frame_pil` methods
            to apply a time transformation function `func_t` to the time `t` before
            generating the frame. This can be used to speed up, slow down, or reverse
            the clip, among other things.

            If the clip has audio, the same time transformation is applied to the audio.

            Parameters:
            :   `#!py func_t (Callable[[int | float], int | float])`: The time transformation function to apply. This function should take a time `t` and return a new time.

            Returns:
            :   `#!py Self`: Returns the instance of the class, allowing for method chaining.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> clip.fl_time_transform(lambda t: 2*t)  # Speed up the clip by a factor of 2
                ```

        > `#!py fx(self, func: Callable[..., Self], *args, **kwargs) -> Self`:

        :   Apply an effect function to the clip.

            This method applies an effect function `func` to the clip. The effect function
            should take the clip as its first argument, followed by any number of positional
            and keyword arguments.

            The effect function should return a new clip, which is then returned by this method.

            Parameters:
            :   `#!py func (Callable[..., Self])`: The effect function to apply. This function should take the clip as its first argument, followed by any number of positional and keyword arguments.
            :   `#!py *args`: Positional arguments to pass to the effect function.
            :   `#!py **kwargs`: Keyword arguments to pass to the effect function.

            Returns:
            :   `#!py Self`: The new clip returned by the effect function.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> clip.fx(effect_function, arg1, arg2, kwarg1=value1)
                ```

        > `#!py sub_fx(self, func: Callable[..., Self], *args, start_t: int | float | None = None, end_t: int | float | None = None, **kwargs) -> Self`:

        :   Apply an effect function to a subclip of the clip.

            This method creates a subclip from `start_t` to `end_t`, applies an effect
            function `func` to the subclip, and returns the modified subclip.

            The effect function should take the clip as its first argument, followed by
            any number of positional and keyword arguments.

            Parameters:
            :   `#!py func (Callable[..., Self])`: The effect function to apply. This function should take the clip as its first argument, followed by any number of positional and keyword arguments.
            :   `#!py *args`: Positional arguments to pass to the effect function.
            :   `#!py start_t (int | float | None, optional)`: The start time of the subclip. If None, the start of the clip is used. Defaults to None.
            :   `#!py end_t (int | float | None, optional)`: The end time of the subclip. If None, the end of the clip is used. Defaults to None.
            :   `#!py **kwargs`: Keyword arguments to pass to the effect function.

            Returns:
            :   `#!py Self`: The modified subclip.

            Example:
            :   
                ```python
                >>> clip = VideoClip()
                >>> subclip = clip.sub_fx(effect_function, arg1, arg2, start_t=1, end_t=2, kwarg1=value1)
                ```

        > `#!py _sync_audio_video_s_e_d(self) -> Self`:

        :   Synchronizes the audio and video start, end, and duration attributes.

            This method is used to ensure that the audio and video parts of a clip are in sync.
            It sets the start, end, and original duration of the audio to match the video.

            Returns:
            :   `#!py Self`: Returns the instance of the class with updated audio attributes.

            Raises:
            :   None

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> video_clip._sync_audio_video_s_e_d()
                ```

            Note:
            :   This is an internal method, typically not meant to be used directly by the user.

        > `#!py write_videofile(self, filename, fps=None, codec=None, bitrate=None, audio=True, audio_fps=44100, preset="medium", pixel_format=None, audio_codec=None, audio_bitrate=None, threads=None, ffmpeg_params: dict[str, str] | None = None, logger="bar", over_write_output=True) -> Self`:

        :   Writes the video clip to a file.

            This method generates video frames, processes them, and writes them to a file.
            If audio is present in the clip, it is also written to the file.

            Args:
            :   `#!py filename (str)`: The name of the file to write.
            :   `#!py fps (int, optional)`: The frames per second to use for the output video. If not provided, the fps of the video clip is used.
            :   `#!py codec (str, optional)`: The codec to use for the output video.
            :   `#!py bitrate (str, optional)`: The bitrate to use for the output video.
            :   `#!py audio (bool, optional)`: Whether to include audio in the output video. Defaults to True.
            :   `#!py audio_fps (int, optional)`: The frames per second to use for the audio. Defaults to 44100.
            :   `#!py preset (str, optional)`: The preset to use for the output video. Defaults to "medium".
            :   `#!py pixel_format (str, optional)`: The pixel format to use for the output video.
            :   `#!py audio_codec (str, optional)`: The codec to use for the audio.
            :   `#!py audio_bitrate (str, optional)`: The bitrate to use for the audio.
            :   `#!py threads (int, optional)`: The number of threads to use for writing the video file.
            :   `#!py ffmpeg_params (dict[str, str] | None, optional)`: Additional parameters to pass to ffmpeg.
            :   `#!py logger (str, optional)`: The logger to use. Defaults to "bar".
            :   `#!py over_write_output (bool, optional)`: Whether to overwrite the output file if it already exists. Defaults to True.

            Returns:
            :   `#!py Self`: Returns the instance of the class.

            Raises:
            :   `#!py Exception`: If fps is not provided and not set in the video clip.

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> video_clip.write_videofile("output.mp4")
                ```

            Note:
            :   This method uses ffmpeg to write the video file.

        > `#!py write_videofile_subclip(self, filename, start_t: int | float | None = None, end_t: int | float | None = None, fps=None, codec=None, bitrate=None, audio=True, audio_fps=44100, preset="medium", pixel_format=None, audio_codec=None, audio_bitrate=None, write_logfile=False, verbose=True, threads=None, ffmpeg_params: dict[str, str] | None = None, logger="bar", over_write_output=True) -> Self`:

        :   Writes a subclip of the video clip to a file.

            This method generates video frames for a specific part of the video (subclip), processes them, and writes them to a file.
            If audio is present in the clip, it is also written to the file.

            Args:
            :   `#!py filename (str)`: The name of the file to write.
            :   `#!py start_t (int | float | None, optional)`: The start time of the subclip. If not provided, the start of the video is used.
            :   `#!py end_t (int | float | None, optional)`: The end time of the subclip. If not provided, the end of the video is used.
            :   `#!py fps (int, optional)`: The frames per second to use for the output video. If not provided, the fps of the video clip is used.
            :   `#!py codec (str, optional)`: The codec to use for the output video.
            :   `#!py bitrate (str, optional)`: The bitrate to use for the output video.
            :   `#!py audio (bool, optional)`: Whether to include audio in the output video. Defaults to True.
            :   `#!py audio_fps (int, optional)`: The frames per second to use for the audio. Defaults to 44100.
            :   `#!py preset (str, optional)`: The preset to use for the output video. Defaults to "medium".
            :   `#!py pixel_format (str, optional)`: The pixel format to use for the output video.
            :   `#!py audio_codec (str, optional)`: The codec to use for the audio.
            :   `#!py audio_bitrate (str, optional)`: The bitrate to use for the audio.
            :   `#!py write_logfile (bool, optional)`: Whether to write a logfile. Defaults to False.
            :   `#!py verbose (bool, optional)`: Whether to print verbose output. Defaults to True.
            :   `#!py threads (int, optional)`: The number of threads to use for writing the video file.
            :   `#!py ffmpeg_params (dict[str, str] | None, optional)`: Additional parameters to pass to ffmpeg.
            :   `#!py logger (str, optional)`: The logger to use. Defaults to "bar".
            :   `#!py over_write_output (bool, optional)`: Whether to overwrite the output file if it already exists. Defaults to True.

            Returns:
            :   `#!py Self`: Returns the instance of the class.

            Raises:
            :   `#!py Exception`: If fps is not provided and not set in the video clip.

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> video_clip.write_videofile_subclip("output.mp4", start_t=10, end_t=20)
                ```

            Note:
            :   This method uses ffmpeg to write the video file.

        > `#!py write_image_sequence(self, nformat: str, fps: int | float | None = None, dir=".") -> Self`:

        :   Writes the frames of the video clip as an image sequence.

            This method generates video frames, processes them, and writes them as images to a directory.
            The images are named by their frame number and the provided format.

            Args:
            :   `#!py nformat (str)`: The format to use for the output images.
            :   `#!py fps (int | float | None, optional)`: The frames per second to use for the output images. If not provided, the fps of the video clip is used.
            :   `#!py dir (str, optional)`: The directory to write the images to. Defaults to the current directory.

            Returns:
            :   `#!py Self`: Returns the instance of the class.

            Raises:
            :   `#!py ValueError`: If fps is not provided and fps and duration are not set in the video clip.

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> video_clip.write_image_sequence("png", fps=24, dir="frames")
                ```

            Note:
            :   This method uses ffmpeg to write the images.

        > `#!py save_frame(self, t: int | float, filename: str) -> Self`:

        :   Saves a specific frame of the video clip as an image.

            This method generates a video frame for a specific time, processes it, and writes it as an image to a file.

            Args:
            :   `#!py t (int | float)`: The time of the frame to save.
            :   `#!py filename (str)`: The name of the file to write.

            Returns:
            :   `#!py Self`: Returns the instance of the class.

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> video_clip.save_frame(10, "frame10.png")
                ```

            Note:
            :   This method uses ffmpeg to write the image.

        > `#!py to_ImageClip(self, t: int | float)`:

        :   Converts a specific frame of the video clip to an ImageClip.

            This method generates a video frame for a specific time, processes it, and converts it to an ImageClip.

            Args:
            :   `#!py t (int | float)`: The time of the frame to convert.

            Returns:
            :   `#!py Data2ImageClip`: The converted ImageClip.

            Raises:
            :   None

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> image_clip = video_clip.to_ImageClip(10)
                ```

            Note:
            :   This method uses ffmpeg to generate the frame and then converts it to an ImageClip.

