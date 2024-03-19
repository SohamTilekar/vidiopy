# ImageClip

> `#!py class` `#!py vidiopy.ImageClip(image: str | Path | Image.Image | np.ndarray | None = None, fps: int | float | None = None, duration: int | float | None = None)`

:   Bases: `#!py vidiopy.VideoClip`

    All Methods and properties of the `#!py VideoClip` `#!py class` are available.

    A `#!py class` representing a video clip generated from a single image.

    Parameters:
    
    :   - `#!py image: str | Path | Image.Image | np.ndarray | None`: The image to use for the video clip. If `#!py None`, an empty video clip is created.
        - `#!py fps: int | float | None`: The frames per second of the video clip. If `#!py None`, the fps is set to 30.
        - `#!py duration: int | float | None`: The duration of the video clip in seconds. If `#!py None`, the duration is set to 1.

    Attributes:

    :   - `#!py image: Image.Image`: The image used for the video clip.
        - Other attributes are inherited from the `#!py VideoClip` `#!py class`.

    Methods:

    :   > `#!py _import_image(self, image) -> Image.Image`:

        :   Import the image from various sources.

            Does not made for external use.

            Parameters:
            :   `#!py image (str | Path | Image.Image | np.ndarray)`: Input image data.

            Returns:
            :   `#!py Image.Image`: The imported image data.

            This is a private method and not intended for external use.

        > You Can Use `#!py set_duration()` & duration property to change _dur.

        > `#!py fl_frame_transform(self, func, *args, **kwargs) -> Self`:

        :   Apply a frame transformation function to the image.

            Parameters:
            :   `#!py func (Callable)`: The frame transformation function.
            :   `#!py *args`: Additional positional arguments for the function.
            :   `#!py **kwargs`: Additional keyword arguments for the function.

            Returns:
            :   `#!py ImageClip`: A new ImageClip instance with the transformed image.

            Note:
            :   This method modifies the current ImageClip instance in-place.

            Example Usage:
            :   
                ```python
                image_clip = ImageClip(image_path, fps=30, duration=5.0)
                transformed_clip = image_clip.fl_frame_transform(resize, width=640, height=480)
                ```

        > `#!py fl_frame_transform(self, func, *args, **kwargs) -> Self`:

        :   Apply a frame transformation function to the image.

            Parameters:
            :   `#!py func (Callable)`: The frame transformation function.
            :   `#!py *args`: Additional positional arguments for the function.
            :   `#!py **kwargs`: Additional keyword arguments for the function.

            Returns:
            :   `#!py ImageClip`: A new ImageClip instance with the transformed image.

            Note:
            :   This method modifies the current ImageClip instance in-place.

            Example Usage:
            :   
                ```python
                image_clip = ImageClip(image_path, fps=30, duration=5.0)
                transformed_clip = image_clip.fl_frame_transform(resize, width=640, height=480)
                ```

        > `#!py fl_clip_transform(self, func, *args, **kwargs) -> Self`:

        :   Raise a ValueError indicating that fl_clip is not applicable for ImageClip.

            The Clip should be converted to VideoClip using `to_video_clip` method first.

            Parameters:
            :   `#!py func`: Unused.
            :   `#!py *args`: Unused.
            :   `#!py **kwargs`: Unused.

            Returns:
            :   `#!py ImageClip`: The current ImageClip instance.

            Raises:
            :   `#!py ValueError`: This method is not applicable for ImageClip.

            Example Usage:
            :   
                ```python
                image_clip = ImageClip(image_path, fps=30, duration=5.0)
                image_clip.fl_clip(some_function)  # Raises ValueError
                ```

        > `#!py fx(self, func: Callable, *args, **kwargs)`:

        :   Apply a generic function to the ImageClip.

            Parameters:
            :   `#!py func (Callable)`: The function to apply.
            :   `#!py *args`: Additional positional arguments for the function.
            :   `#!py **kwargs`: Additional keyword arguments for the function.

            Returns:
            :   `#!py ImageClip`: The current ImageClip instance.

            Note:
            :   This method modifies the current ImageClip instance in-place.

            Example Usage:
            :   
                ```python
                def custom_function(image):
                    # Some custom processing on the image
                    return modified_image

                image_clip = ImageClip(image_path, fps=30, duration=5.0)
                image_clip.fx(custom_function, some_arg=42)
                ```

        > `#!py sub_fx(self, func, *args, start_t: int | float | None = None, end_t: int | float | None = None, **kwargs) -> Self`:

        :   Apply a custom function to the Image Clip.

            Note:
            :   Before using the `sub_fx` method, you need to convert the image clip to a video clip using `to_video_clip()` function.

            Args:
            :   `#!py func`: The custom function to apply to the Image Clip.
            :   `#!py *args`: Additional positional arguments to pass to the custom function.
            :   `#!py start_t (int | float | None)`: The start time of the subclip in seconds. If None, the subclip starts from the beginning.
            :   `#!py end_t (int | float | None)`: The end time of the subclip in seconds. If None, the subclip ends at the last frame.
            :   `#!py **kwargs`: Additional keyword arguments to pass to the custom function.

            Returns:
            :   `#!py Self`: The modified ImageClips instance.

            Example:
            :   
                ```python
                # Convert the image clip to a video clip
                video_clip = image_clip.to_video_clip()

                # Apply a custom function to the video clip
                modified_clip = video_clip.sub_fx(custom_function, start_t=2, end_t=5)
                ```

            Raises:
            :   `#!py ValueError`: If the method is called on an Image Clip instead of a Video Clip.

        > `#!py sub_clip_copy(self, start: int | float | None = None, end: int | float | None = None) -> Self`:

        :   Create a copy of the current clip and apply sub-clip operation.
            Read more about sub-clip operation in the `sub_clip` method.

            Args:
            :   `#!py start (int | float | None)`: Start time of the sub-clip in seconds.
                If None, the sub-clip starts from the beginning of the original clip.
            :   `#!py end (int | float | None)`: End time of the sub-clip in seconds.
                If None, the sub-clip ends at the end of the original clip.

            Returns:
            :   `#!py Self`: A new instance of the clip with the sub-clip applied.

            Example:
            :   
                ```python
                image_clip = ImageClip(image_path, fps=30, duration=5.0)
                sub_clip = image_clip.sub_clip_copy(start=2, end=5)
                ``` 
        
        > `#!py sub_clip(self, start: int | float | None = None, end: int | float | None = None) -> Self`:

        :   Returns a sub-clip of the current clip.

            Args:
            :   `#!py start (int | float | None, optional)`: The start time of the sub-clip in seconds. Defaults to None.
            :   `#!py end (int | float | None, optional)`: The end time of the sub-clip in seconds. Defaults to None.

            Returns:
            :   `#!py Self`: The sub-clip.

            Note:
            :   It modifies the current clip in-place.
                If both `start` and `end` are None, the original clip is returned.
                If `start` is None, it defaults to 0.
                If `end` is None, it defaults to the end time of the original clip.

            Example:
            :   
                ```python
                image_clip = ImageClip(image_path, fps=30, duration=5.0)
                image_clip.sub_clip(start=2, end=5)
                ```

        > `#!py make_frame_array(self, t)`:

        :   Gives the numpy array representation of the image at a given time.

            Args:
            :   `#!py t (float)`: The timestamp of the frame.

            Returns:
            :   `#!py numpy.ndarray`: The numpy array representation of the image.

            Raises:
            :   `#!py ValueError`: If the image is not set.

        > `#!py make_frame_pil(self, t) -> Image.Image`:

        :   Returns the image frame at a given time.

            Args:
            :   `#!py t (float)`: The time at which to retrieve the frame.

            Returns:
            :   `#!py PIL.Image.Image`: The image frame at the given time.

            Raises:
            :   `#!py ValueError`: If the image is not set.

        > `#!py to_video_clip(self, fps=None, duration=None)`:

        :   Convert `ImageClip` to `VideoClip`

            If fps or duration is not provided, it defaults to the corresponding attribute
            of the ImageClip instance. If those attributes are not available, a ValueError is raised.

            Parameters:
            :   `#!py fps (float, optional)`: Frames per second of the resulting video clip.
                If not provided, it defaults to the fps attribute of the ImageClip instance.
                If that is also not available, a ValueError is raised.
            :   `#!py duration (float, optional)`: Duration of the resulting video clip in seconds.
                If not provided, it defaults to the duration attribute of the ImageClip instance.
                If that is also not available, a ValueError is raised.

            Returns:
            :   `#!py ImageSequenceClip`: A VideoClip subclass instance generated from the ImageClip frames.

            Raises:
            :   `#!py ValueError`: If fps or duration is not provided and the corresponding attribute is not available.

            Note:
            :   The `to_video_clip` method returns an instance of the `ImageSequenceClip` class,
                which is a subclass of the `VideoClip` Class.

            Example Usage:
            :   
                ```python
                # Example Usage
                image_clip = ImageClip()
                video_clip = image_clip.to_video_clip(fps=24, duration=10.0)
                video_clip.sub_fx(custom_function, start_t=2, end_t=5)
                ```

# Data2ImageClip

> `#!py class` `#!py vidiopy.Data2ImageClip(data: np.ndarray | Image.Image, fps: int | float | None = None, duration: int | float | None = None)`

:   Bases: `#!py vidiopy.ImageClip`

    A class representing a video clip generated from raw data (numpy array or PIL Image).

    It extends the `#!py ImageClip` class and allows users to create video clips from raw data, supporting either numpy arrays or PIL Images as input.

    Parameters:

    :   - `#!py data (np.ndarray or PIL Image)`: The raw data to be converted into a video clip.
        - `#!py fps (int | float | None)`: Frames per second of the video. If not provided, it will be inherited from the parent class (ImageClip) or set to the default value.
        - `#!py duration (int | float | None)`: Duration of the video in seconds. If not provided, it will be inherited from the parent class (ImageClip) or set to the default value.

    Attributes:

    :   - `#!py image (PIL Image)`: The PIL Image representation of the provided data.
        - `#!py size (tuple)`: The size (width, height) of the image.

    Methods:

    :   > `#!py _import_image(self, image) -> Image.Image`:

        :   Private method to convert the provided data (numpy array or PIL Image) into a PIL Image.

            Parameters:
            :   `#!py image (np.ndarray or PIL Image)`: The raw data to be converted.

            Returns:
            :   `#!py Image.Image`: The PIL Image representation of the provided data.

            Raises:
            :   `#!py TypeError`: If the input type is not supported (neither numpy array nor PIL Image).

    Example Usage:

    :   
        ```python
        # Import necessary libraries

        # Create a Data2ImageClip instance from a numpy array
        data_array = np.random.randint(0, 255, size=(480, 640, 3), dtype=np.uint8)
        video_clip = Data2ImageClip(data=data_array, fps=30, duration=5)

        # Create a Data2ImageClip instance from a PIL Image
        from PIL import Image
        data_image = Image.new('RGB', (640, 480), color='red')
        video_clip = Data2ImageClip(data=data_image, fps=24, duration=10)
        ```

    Note:

    :   The `#!py Data2ImageClip` class extends the `#!py ImageClip`. It allows users to create video clips from raw data, supporting either numpy arrays or PIL Images as input.

<style>
    .color-box {
        display: inline-block;
        border: 1px solid gray;
        height: 18px;
        width: 18px;
    }
</style>

# ColorClip

> `#!py class` `#!py vidiopy.ColorClip(color: str | tuple[int, ...], mode="RGBA", size=(1, 1), fps=None, duration=None)`

:   Bases: #!py vidiopy.Data2ImageClip
    
    A video clip class with a solid color.

    It extends the `#!py Data2ImageClip` class and allows users to create video clips with a solid color.

    Parameters:

    :   - `#!py color: str | tuple[int, ...]`: Color of the image. It can be a color name (e.g., 'red', 'blue') or RGB tuple.

            ??? info "Available Color Names"
                - <div class="color-box" style="background-color: #f0f8ff;"></div> `#!css aliceblue: "#f0f8ff"`,<br>
                - <div class="color-box" style="background-color: #faebd7;"></div> `#!css antiquewhite: "#faebd7"`,<br>
                - <div class="color-box" style="background-color: #00ffff;"></div> `#!css aqua: "#00ffff"`,<br>
                - <div class="color-box" style="background-color: #7fffd4;"></div> `#!css aquamarine: "#7fffd4"`,<br>
                - <div class="color-box" style="background-color: #f0ffff;"></div> `#!css azure: "#f0ffff"`,<br>
                - <div class="color-box" style="background-color: #f5f5dc;"></div> `#!css beige: "#f5f5dc"`,<br>
                - <div class="color-box" style="background-color: #ffe4c4;"></div> `#!css bisque: "#ffe4c4"`,<br>
                - <div class="color-box" style="background-color: #000000;"></div> `#!css black: "#000000"`,<br>
                - <div class="color-box" style="background-color: #ffebcd;"></div> `#!css blanchedalmond: "#ffebcd"`,<br>
                - <div class="color-box" style="background-color: #0000ff;"></div> `#!css blue: "#0000ff"`,<br>
                - <div class="color-box" style="background-color: #8a2be2;"></div> `#!css blueviolet: "#8a2be2"`,<br>
                - <div class="color-box" style="background-color: #a52a2a;"></div> `#!css brown: "#a52a2a"`,<br>
                - <div class="color-box" style="background-color: #deb887;"></div> `#!css burlywood: "#deb887"`,<br>
                - <div class="color-box" style="background-color: #5f9ea0;"></div> `#!css cadetblue: "#5f9ea0"`,<br>
                - <div class="color-box" style="background-color: #7fff00;"></div> `#!css chartreuse: "#7fff00"`,<br>
                - <div class="color-box" style="background-color: #d2691e;"></div> `#!css chocolate: "#d2691e"`,<br>
                - <div class="color-box" style="background-color: #ff7f50;"></div> `#!css coral: "#ff7f50"`,<br>
                - <div class="color-box" style="background-color: #6495ed;"></div> `#!css cornflowerblue: "#6495ed"`,<br>
                - <div class="color-box" style="background-color: #fff8dc;"></div> `#!css cornsilk: "#fff8dc"`,<br>
                - <div class="color-box" style="background-color: #dc143c;"></div> `#!css crimson: "#dc143c"`,<br>
                - <div class="color-box" style="background-color: #00ffff;"></div> `#!css cyan: "#00ffff"`,<br>
                - <div class="color-box" style="background-color: #00008b;"></div> `#!css darkblue: "#00008b"`,<br>
                - <div class="color-box" style="background-color: #008b8b;"></div> `#!css darkcyan: "#008b8b"`,<br>
                - <div class="color-box" style="background-color: #b8860b;"></div> `#!css darkgoldenrod: "#b8860b"`,<br>
                - <div class="color-box" style="background-color: #a9a9a9;"></div> `#!css darkgray: "#a9a9a9"`,<br>
                - <div class="color-box" style="background-color: #a9a9a9;"></div> `#!css darkgrey: "#a9a9a9"`,<br>
                - <div class="color-box" style="background-color: #006400;"></div> `#!css darkgreen: "#006400"`,<br>
                - <div class="color-box" style="background-color: #bdb76b;"></div> `#!css darkkhaki: "#bdb76b"`,<br>
                - <div class="color-box" style="background-color: #8b008b;"></div> `#!css darkmagenta: "#8b008b"`,<br>
                - <div class="color-box" style="background-color: #556b2f;"></div> `#!css darkolivegreen: "#556b2f"`,<br>
                - <div class="color-box" style="background-color: #ff8c00;"></div> `#!css darkorange: "#ff8c00"`,<br>
                - <div class="color-box" style="background-color: #9932cc;"></div> `#!css darkorchid: "#9932cc"`,<br>
                - <div class="color-box" style="background-color: #8b0000;"></div> `#!css darkred: "#8b0000"`,<br>
                - <div class="color-box" style="background-color: #e9967a;"></div> `#!css darksalmon: "#e9967a"`,<br>
                - <div class="color-box" style="background-color: #8fbc8f;"></div> `#!css darkseagreen: "#8fbc8f"`,<br>
                - <div class="color-box" style="background-color: #483d8b;"></div> `#!css darkslateblue: "#483d8b"`,<br>
                - <div class="color-box" style="background-color: #2f4f4f;"></div> `#!css darkslategray: "#2f4f4f"`,<br>
                - <div class="color-box" style="background-color: #2f4f4f;"></div> `#!css darkslategrey: "#2f4f4f"`,<br>
                - <div class="color-box" style="background-color: #00ced1;"></div> `#!css darkturquoise: "#00ced1"`,<br>
                - <div class="color-box" style="background-color: #9400d3;"></div> `#!css darkviolet: "#9400d3"`,<br>
                - <div class="color-box" style="background-color: #ff1493;"></div> `#!css deeppink: "#ff1493"`,<br>
                - <div class="color-box" style="background-color: #00bfff;"></div> `#!css deepskyblue: "#00bfff"`,<br>
                - <div class="color-box" style="background-color: #696969;"></div> `#!css dimgray: "#696969"`,<br>
                - <div class="color-box" style="background-color: #696969;"></div> `#!css dimgrey: "#696969"`,<br>
                - <div class="color-box" style="background-color: #1e90ff;"></div> `#!css dodgerblue: "#1e90ff"`,<br>
                - <div class="color-box" style="background-color: #b22222;"></div> `#!css firebrick: "#b22222"`,<br>
                - <div class="color-box" style="background-color: #fffaf0;"></div> `#!css floralwhite: "#fffaf0"`,<br>
                - <div class="color-box" style="background-color: #228b22;"></div> `#!css forestgreen: "#228b22"`,<br>
                - <div class="color-box" style="background-color: #ff00ff;"></div> `#!css fuchsia: "#ff00ff"`,<br>
                - <div class="color-box" style="background-color: #dcdcdc;"></div> `#!css gainsboro: "#dcdcdc"`,<br>
                - <div class="color-box" style="background-color: #f8f8ff;"></div> `#!css ghostwhite: "#f8f8ff"`,<br>
                - <div class="color-box" style="background-color: #ffd700;"></div> `#!css gold: "#ffd700"`,<br>
                - <div class="color-box" style="background-color: #daa520;"></div> `#!css goldenrod: "#daa520"`,<br>
                - <div class="color-box" style="background-color: #808080;"></div> `#!css gray: "#808080"`,<br>
                - <div class="color-box" style="background-color: #808080;"></div> `#!css grey: "#808080"`,<br>
                - <div class="color-box" style="background-color: #008000;"></div> `#!css green: "#008000"`,<br>
                - <div class="color-box" style="background-color: #adff2f;"></div> `#!css greenyellow: "#adff2f"`,<br>
                - <div class="color-box" style="background-color: #f0fff0;"></div> `#!css honeydew: "#f0fff0"`,<br>
                - <div class="color-box" style="background-color: #ff69b4;"></div> `#!css hotpink: "#ff69b4"`,<br>
                - <div class="color-box" style="background-color: #cd5c5c;"></div> `#!css indianred: "#cd5c5c"`,<br>
                - <div class="color-box" style="background-color: #4b0082;"></div> `#!css indigo: "#4b0082"`,<br>
                - <div class="color-box" style="background-color: #fffff0;"></div> `#!css ivory: "#fffff0"`,<br>
                - <div class="color-box" style="background-color: #f0e68c;"></div> `#!css khaki: "#f0e68c"`,<br>
                - <div class="color-box" style="background-color: #e6e6fa;"></div> `#!css lavender: "#e6e6fa"`,<br>
                - <div class="color-box" style="background-color: #fff0f5;"></div> `#!css lavenderblush: "#fff0f5"`,<br>
                - <div class="color-box" style="background-color: #7cfc00;"></div> `#!css lawngreen: "#7cfc00"`,<br>
                - <div class="color-box" style="background-color: #fffacd;"></div> `#!css lemonchiffon: "#fffacd"`,<br>
                - <div class="color-box" style="background-color: #add8e6;"></div> `#!css lightblue: "#add8e6"`,<br>
                - <div class="color-box" style="background-color: #f08080;"></div> `#!css lightcoral: "#f08080"`,<br>
                - <div class="color-box" style="background-color: #e0ffff;"></div> `#!css lightcyan: "#e0ffff"`,<br>
                - <div class="color-box" style="background-color: #fafad2;"></div> `#!css lightgoldenrodyellow: "#fafad2"`,<br>
                - <div class="color-box" style="background-color: #90ee90;"></div> `#!css lightgreen: "#90ee90"`,<br>
                - <div class="color-box" style="background-color: #d3d3d3;"></div> `#!css lightgray: "#d3d3d3"`,<br>
                - <div class="color-box" style="background-color: #d3d3d3;"></div> `#!css lightgrey: "#d3d3d3"`,<br>
                - <div class="color-box" style="background-color: #ffb6c1;"></div> `#!css lightpink: "#ffb6c1"`,<br>
                - <div class="color-box" style="background-color: #ffa07a;"></div> `#!css lightsalmon: "#ffa07a"`,<br>
                - <div class="color-box" style="background-color: #20b2aa;"></div> `#!css lightseagreen: "#20b2aa"`,<br>
                - <div class="color-box" style="background-color: #87cefa;"></div> `#!css lightskyblue: "#87cefa"`,<br>
                - <div class="color-box" style="background-color: #778899;"></div> `#!css lightslategray: "#778899"`,<br>
                - <div class="color-box" style="background-color: #778899;"></div> `#!css lightslategrey: "#778899"`,<br>
                - <div class="color-box" style="background-color: #b0c4de;"></div> `#!css lightsteelblue: "#b0c4de"`,<br>
                - <div class="color-box" style="background-color: #ffffe0;"></div> `#!css lightyellow: "#ffffe0"`,<br>
                - <div class="color-box" style="background-color: #00ff00;"></div> `#!css lime: "#00ff00"`,<br>
                - <div class="color-box" style="background-color: #32cd32;"></div> `#!css limegreen: "#32cd32"`,<br>
                - <div class="color-box" style="background-color: #faf0e6;"></div> `#!css linen: "#faf0e6"`,<br>
                - <div class="color-box" style="background-color: #ff00ff;"></div> `#!css magenta: "#ff00ff"`,<br>
                - <div class="color-box" style="background-color: #800000;"></div> `#!css maroon: "#800000"`,<br>
                - <div class="color-box" style="background-color: #66cdaa;"></div> `#!css mediumaquamarine: "#66cdaa"`,<br>
                - <div class="color-box" style="background-color: #0000cd;"></div> `#!css mediumblue: "#0000cd"`,<br>
                - <div class="color-box" style="background-color: #ba55d3;"></div> `#!css mediumorchid: "#ba55d3"`,<br>
                - <div class="color-box" style="background-color: #9370db;"></div> `#!css mediumpurple: "#9370db"`,<br>
                - <div class="color-box" style="background-color: #3cb371;"></div> `#!css mediumseagreen: "#3cb371"`,<br>
                - <div class="color-box" style="background-color: #7b68ee;"></div> `#!css mediumslateblue: "#7b68ee"`,<br>
                - <div class="color-box" style="background-color: #00fa9a;"></div> `#!css mediumspringgreen: "#00fa9a"`,<br>
                - <div class="color-box" style="background-color: #48d1cc;"></div> `#!css mediumturquoise: "#48d1cc"`,<br>
                - <div class="color-box" style="background-color: #c71585;"></div> `#!css mediumvioletred: "#c71585"`,<br>
                - <div class="color-box" style="background-color: #191970;"></div> `#!css midnightblue: "#191970"`,<br>
                - <div class="color-box" style="background-color: #f5fffa;"></div> `#!css mintcream: "#f5fffa"`,<br>
                - <div class="color-box" style="background-color: #ffe4e1;"></div> `#!css mistyrose: "#ffe4e1"`,<br>
                - <div class="color-box" style="background-color: #ffe4b5;"></div> `#!css moccasin: "#ffe4b5"`,<br>
                - <div class="color-box" style="background-color: #ffdead;"></div> `#!css navajowhite: "#ffdead"`,<br>
                - <div class="color-box" style="background-color: #000080;"></div> `#!css navy: "#000080"`,<br>
                - <div class="color-box" style="background-color: #fdf5e6;"></div> `#!css oldlace: "#fdf5e6"`,<br>
                - <div class="color-box" style="background-color: #808000;"></div> `#!css olive: "#808000"`,<br>
                - <div class="color-box" style="background-color: #6b8e23;"></div> `#!css olivedrab: "#6b8e23"`,<br>
                - <div class="color-box" style="background-color: #ffa500;"></div> `#!css orange: "#ffa500"`,<br>
                - <div class="color-box" style="background-color: #ff4500;"></div> `#!css orangered: "#ff4500"`,<br>
                - <div class="color-box" style="background-color: #da70d6;"></div> `#!css orchid: "#da70d6"`,<br>
                - <div class="color-box" style="background-color: #eee8aa;"></div> `#!css palegoldenrod: "#eee8aa"`,<br>
                - <div class="color-box" style="background-color: #98fb98;"></div> `#!css palegreen: "#98fb98"`,<br>
                - <div class="color-box" style="background-color: #afeeee;"></div> `#!css paleturquoise: "#afeeee"`,<br>
                - <div class="color-box" style="background-color: #db7093;"></div> `#!css palevioletred: "#db7093"`,<br>
                - <div class="color-box" style="background-color: #ffefd5;"></div> `#!css papayawhip: "#ffefd5"`,<br>
                - <div class="color-box" style="background-color: #ffdab9;"></div> `#!css peachpuff: "#ffdab9"`,<br>
                - <div class="color-box" style="background-color: #cd853f;"></div> `#!css peru: "#cd853f"`,<br>
                - <div class="color-box" style="background-color: #ffc0cb;"></div> `#!css pink: "#ffc0cb"`,<br>
                - <div class="color-box" style="background-color: #dda0dd;"></div> `#!css plum: "#dda0dd"`,<br>
                - <div class="color-box" style="background-color: #b0e0e6;"></div> `#!css powderblue: "#b0e0e6"`,<br>
                - <div class="color-box" style="background-color: #800080;"></div> `#!css purple: "#800080"`,<br>
                - <div class="color-box" style="background-color: #663399;"></div> `#!css rebeccapurple: "#663399"`,<br>
                - <div class="color-box" style="background-color: #ff0000;"></div> `#!css red: "#ff0000"`,<br>
                - <div class="color-box" style="background-color: #bc8f8f;"></div> `#!css rosybrown: "#bc8f8f"`,<br>
                - <div class="color-box" style="background-color: #4169e1;"></div> `#!css royalblue: "#4169e1"`,<br>
                - <div class="color-box" style="background-color: #8b4513;"></div> `#!css saddlebrown: "#8b4513"`,<br>
                - <div class="color-box" style="background-color: #fa8072;"></div> `#!css salmon: "#fa8072"`,<br>
                - <div class="color-box" style="background-color: #f4a460;"></div> `#!css sandybrown: "#f4a460"`,<br>
                - <div class="color-box" style="background-color: #2e8b57;"></div> `#!css seagreen: "#2e8b57"`,<br>
                - <div class="color-box" style="background-color: #fff5ee;"></div> `#!css seashell: "#fff5ee"`,<br>
                - <div class="color-box" style="background-color: #a0522d;"></div> `#!css sienna: "#a0522d"`,<br>
                - <div class="color-box" style="background-color: #c0c0c0;"></div> `#!css silver: "#c0c0c0"`,<br>
                - <div class="color-box" style="background-color: #87ceeb;"></div> `#!css skyblue: "#87ceeb"`,<br>
                - <div class="color-box" style="background-color: #6a5acd;"></div> `#!css slateblue: "#6a5acd"`,<br>
                - <div class="color-box" style="background-color: #708090;"></div> `#!css slategray: "#708090"`,<br>
                - <div class="color-box" style="background-color: #708090;"></div> `#!css slategrey: "#708090"`,<br>
                - <div class="color-box" style="background-color: #fffafa;"></div> `#!css snow: "#fffafa"`,<br>
                - <div class="color-box" style="background-color: #00ff7f;"></div> `#!css springgreen: "#00ff7f"`,<br>
                - <div class="color-box" style="background-color: #4682b4;"></div> `#!css steelblue: "#4682b4"`,<br>
                - <div class="color-box" style="background-color: #d2b48c;"></div> `#!css tan: "#d2b48c"`,<br>
                - <div class="color-box" style="background-color: #008080;"></div> `#!css teal: "#008080"`,<br>
                - <div class="color-box" style="background-color: #d8bfd8;"></div> `#!css thistle: "#d8bfd8"`,<br>
                - <div class="color-box" style="background-color: #ff6347;"></div> `#!css tomato: "#ff6347"`,<br>
                - <div class="color-box" style="background-color: #40e0d0;"></div> `#!css turquoise: "#40e0d0"`,<br>
                - <div class="color-box" style="background-color: #ee82ee;"></div> `#!css violet: "#ee82ee"`,<br>
                - <div class="color-box" style="background-color: #f5deb3;"></div> `#!css wheat: "#f5deb3"`,<br>
                - <div class="color-box" style="background-color: #ffffff;"></div> `#!css white: "#ffffff"`,<br>
                - <div class="color-box" style="background-color: #f5f5f5;"></div> `#!css whitesmoke: "#f5f5f5"`,<br>
                - <div class="color-box" style="background-color: #ffff00;"></div> `#!css yellow: "#ffff00"`,<br>
                - <div class="color-box" style="background-color: #9acd32;"></div> `#!css yellowgreen: "#9acd32"`,<br>
 
        - `#!py mode: str`: Mode to use for the image. Default is 'RGBA'.
        - `#!py size: tuple`: Size of the image in pixels (width, height). Default is (1, 1) for changing size afterwards.
        - `#!py fps: float, optional`: Frames per second for the video clip.
        - `#!py duration: float, optional`: Duration of the video clip in seconds.

    Attributes:

    :   - `#!py color: str | tuple[int, ...]`: The color of the video clip.
        - `#!py mode: str`: The mode of the video clip.
        - Other attributes are inherited from the `#!py Data2ImageClip` `#!py class`.

    Methods:

    :   > `#!py set_size(self, size: tuple[int, int])`:

        :   Set the size of the video clip.

            Parameters:
            :   `#!py size: tuple[int, int]`: New size of the video clip in pixels (width, height).

            Example Usage:
            :   
                ```python
                color_clip.set_size((800, 600))
                ```

    Example Usage:

    :   
        ```python
        # Create a red square video clip (500x500, 30 FPS, 5 seconds):
        red_square = ColorClip(color='red', size=(500, 500), fps=30, duration=5)

        # Create a blue fullscreen video clip (1920x1080, default FPS and duration):
        blue_fullscreen = ColorClip(color='blue', size=(1920, 1080))

        # Create a green transparent video clip (RGBA mode, 800x600):
        green_transparent = ColorClip(color=(0, 255, 0, 0), mode='RGBA', size=(800, 600))
        ```


#TextClip

`#!py class` `#!py vidiopy.TextClip(text: str, font_pth: None | str = None, font_size: int = 20, txt_color: str | tuple[int, ...] = (255, 255, 255, 0), bg_color: str | tuple[int, ...] = (0, 0, 0, 0), fps=None, duration=None)`

:   Bases: #!py vidiopy.Data2ImageClip

    A class representing a text clip to be used in video compositions.

    Parameters:

    :   - `#!py text (str)`: The text content to be displayed in the clip.
        - `#!py font_pth (None | str, optional)`: The file path to the TrueType font file (.ttf). If None, the default system font is used. Defaults to None.
        - `#!py font_size (int, optional)`: The font size for the text. Defaults to 20.
        - `#!py txt_color (str | tuple[int, ...], optional)`: The color of the text specified as either a string (e.g., 'white') or a tuple representing RGBA values. Defaults to (255, 255, 255, 0) (fully transparent white).
        - `#!py bg_color (str | tuple[int, ...], optional)`: The background color of the text clip, specified as either a string (e.g., 'black') or a tuple representing RGBA values. Defaults to (0, 0, 0, 0) (fully transparent black).
        - `#!py fps (float, optional)`: Frames per second of the video. If None, the value is inherited from the parent class. Defaults to None.
        - `#!py duration (float, optional)`: Duration of the video clip in seconds. If None, the value is inherited from the parent class. Defaults to None.

    Attributes:

    :   - `#!py font (PIL.ImageFont.FreeTypeFont)`: The font object used for rendering the text.
        - `#!py image (PIL.Image.Image)`: The image containing the rendered text.
        - `#!py fps (float)`: Frames per second of the video clip.
        - `#!py duration (float)`: Duration of the video clip in seconds.
        - Other attributes are inherited from the `#!py Data2ImageClip` `#!py class`.

    Example Usage:

    :   
        ```python
        # Create a TextClip with custom text and styling
        text_clip = TextClip("Contribute to Vidiopy", font_size=30, txt_color='red', bg_color='blue', fps=24, duration=5.0)

        # Use the text clip in a video composition
        composition = CompositeVideoClip([other_clip, text_clip])
        composition.write_videofile("output.mp4", codec='libx264', fps=24)
        ```
