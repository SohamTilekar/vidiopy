# VideoFileClip

> `#!py class` `#!py vidiopy.VideoFileClip(filename: str, audio: bool = True, ffmpeg_options: dict | None = None)`

:   Bases: `#!py vidiopy.VideoClip`

    All Methods and properties of the `VideoClip` class are available.

    A video clip originating from a Video file.

    Parameters:
    :   
        > filename: str
        
        :   
            The name of the video file, as a string or a path-like object. It can have any extension supported by ffmpeg.
            ??? info "All Sported extensions"
                - .mp4
                - .avi
                - .mov
                - .mkv
                - .webm
                - .flv
                - .wmv
                - .3gp
                - .ogg
                - .ogv
                - .mts
                - .m2ts
                - .ts
                - .vob
                - .mpg
                - .mpeg
                - .m2v
                - .m4v
                - .mxf
                - .dv
                - .f4v
                - .gif
                - .mp3
                - .wav
                - .flac
                - .ogg
                - .m4a
                - .wma
                - .aac
                - .ac3
                - .alac
                - .aiff
                - .amr
                - .au
                - .mka
                - .mp2
                - .mpa
                - .opus
                - .ra
                - .tta
                - .wv
                - .weba
                - .webm
                - .webvtt
                - .srt
                ETC.

        > `#!py audio: bool` Default: `#!py True`

        :   
            Set to `#!py False` if the clip doesn’t have any audio or if you do not wish to read the audio.

        > `#!py ffmpeg_options: dict | None` Default: `#!py None`

        :   
            A dictionary of options to be passed to ffmpeg when generating the clip’s audio. If `#!py None`, the default options will be used. If you want to pass options to the video part of the clip, you will have to use the `#!py vidiopy.VideoFileClip.set_make_frame` method.

    Attributes:
    :   
        > `#!py clip`:
        
        :   The Numpy array of the clip’s video frames.

    > Read docs for `#!py Clip()` and `#!py VideoClip()` for other, more generic, attributes.

    Methods:
    :   
        > `#!py fl_frame_transform(self, func, *args, **kwargs) -> Self`:

        :   Applies a function to each frame of the video clip.

            This method iterates over each frame in the video clip, applies a function to it, and replaces the original frame with the result.

            Args:
            :   `#!py func (callable)`: The function to apply to each frame. It should take an Image as its first argument, and return an Image.
            :   `#!py *args`: Additional positional arguments to pass to func.
            :   `#!py **kwargs`: Additional keyword arguments to pass to func.

            Returns:
            :   `#!py Self`: Returns the instance of the class with updated frames.

            Raises:
            :   None

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> def invert_colors(image):
                ...     return ImageOps.invert(image)
                >>> video_clip.fl_frame_transform(invert_colors)
                ```

            Note:
            :   This method requires the start and end of the video clip to be set.

        > `#!py fl_clip_transform(self, func, *args, **kwargs) -> Self`:

        :   Applies a function to each frame of the video clip along with its timestamp.

            This method iterates over each frame in the video clip, applies a function to it and its timestamp, and replaces the original frame with the result.

            Args:
            :   `#!py func (callable)`: The function to apply to each frame. It should take an Image and a float (representing the timestamp) as its first two arguments, and return an Image.
            :   `#!py *args`: Additional positional arguments to pass to func.
            :   `#!py **kwargs`: Additional keyword arguments to pass to func.

            Returns:
            :   `#!py Self`: Returns the instance of the class with updated frames.

            Raises:
            :   None

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> def add_timestamp(image, timestamp):
                ...     draw = ImageDraw.Draw(image)
                ...     draw.text((10, 10), str(timestamp), fill="white")
                ...     return image
                >>> video_clip.fl_clip_transform(add_timestamp)
                ```

            Note:
            :   This method requires the fps of the video clip to be set.

        > `#!py make_frame_array(self, t: int | float) -> np.ndarray`:

        :   Generates a numpy array representation of a specific frame in the video clip.

            This method calculates the index of the frame for a specific time, retrieves the frame from the video clip, and converts it to a numpy array.

            Args:
            :   `#!py t (int | float)`: The time of the frame to convert.

            Returns:
            :   `#!py np.ndarray`: The numpy array representation of the frame.

            Raises:
            :   `#!py ValueError`: If the duration of the video clip is not set.

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> frame_array = video_clip.make_frame_array(10)
                ```

            Note:
            :   This method requires the duration of the video clip to be set.
        
        > `#!py make_frame_pil(self, t: int | float) -> Image.Image`:

        :   Generates a PIL Image representation of a specific frame in the video clip.

            This method calculates the index of the frame for a specific time, retrieves the frame from the video clip, and returns it as a PIL Image.

            Args:
            :   `#!py t (int | float)`: The time of the frame to convert.

            Returns:
            :   `#!py Image.Image`: The PIL Image representation of the frame.

            Raises:
            :   `#!py ValueError`: If the duration of the video clip is not set.

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> frame_image = video_clip.make_frame_pil(10)
                ```

            Note:
            :   This method requires the duration of the video clip to be set.
        
        > `#!py _import_video_clip(self, file_name: str, ffmpeg_options: dict | None = None) -> tuple`:

        :   Imports a video clip from a file using ffmpeg.

            This method reads a video file using ffmpeg, converts each frame to a PIL Image, and returns a tuple of the images and the fps of the video.

            Args:
            :   `#!py file_name (str)`: The name of the video file to import.
            :   `#!py ffmpeg_options (dict | None, optional)`: Additional options to pass to ffmpeg. Defaults to None.

            Returns:
            :   `#!py tuple`: A tuple of the frames as PIL Images and the fps of the video.

            Raises:
            :   None

            Example:
            :   
                ```python
                >>> video_clip = VideoClip()
                >>> frames, fps = video_clip._import_video_clip("video.mp4")
                ```

            Note:
            :   This method uses ffmpeg to read the video file. It is a private method and not intended for external use.
        