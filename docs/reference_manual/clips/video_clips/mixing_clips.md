# CompositeVideoCLip

> `#!py def` `#!py composite_videoclips(clips: Sequence[VideoClip], fps: int | float | None = None, bg_color: tuple[int, ...] = (0, 0, 0, 0), use_bg_clip: bool = False, audio: bool = True, audio_fps=44100)`

:   Composites multiple video clips into a single video clip.

    This `#!py function` takes a `#!py sequence` of video clips and composites them into a single video clip. The clips are layered on top of each other in the order they appear in the `#!py sequence`. The background of the composite clip can be a solid color or the first clip in the `#!py sequence`. The `#!py function` also handles the positioning of each clip in the composite clip and the audio of the composite clip.

    Args:

    :   - `#!py clips: Sequence[VideoClip]`: The `#!py sequence` of video clips to composite.
        - `#!py fps (int | float | None, optional)`: The frames per second of the composite clip. If not specified, it is set to the maximum fps of the clips in the `#!py sequence` or raises a ValueError if none of the clips have fps set.
        - `#!py bg_color (tuple[int, ...], optional)`: The background color of the composite clip as a tuple of integers representing RGBA values. Default is (0, 0, 0, 0) which is transparent.
        - `#!py use_bg_clip (bool, optional)`: Whether to use the first clip in the `#!py sequence` as the background of the composite clip. Default is False.
        - `#!py audio (bool, optional)`: Whether to include audio in the composite clip. If True, the audio of the clips in the `#!py sequence` is also composited. Default is True.
        - `#!py audio_fps (int, optional)`: The frames per second of the audio of the composite clip. Default is 44100.

    Returns:
    :   `#!py ImageSequenceClip`: The composite video clip as an instance of the `#!py ImageSequenceClip` class.

    Raises:
    :   - `#!py ValueError`: If neither fps nor duration is set for any of the clips in the `#!py sequence`.
        - `#!py ValueError`: If the position of a clip in the composite clip is not specified correctly.
        - `#!py TypeError`: If the position of a clip in the composite clip is not of the correct type.

    Example:
    :   
        ```python
        >>> clip1 = VideoClip(...)
        >>> clip2 = VideoClip(...)
        >>> composite_clip = composite_videoclips([clip1, clip2], fps=24)
        ```

    Note:
    :   This `#!py function` uses the `#!py `#!py ImageSequenceClip` class to create the composite video clip and the composite_audioclips `#!py function` to composite the audio of the clips.


# ConcatenateVideoClips

> `#!py def` `#!py concatenate_videoclips(clips: Sequence[VideoClip], transparent: bool = False, fps: int | float | None = None, scaling_strategy: str = "scale_same", transition: (     VideoClip | Callable[[Image.Image, Image.Image, int | float], VideoClip] | None ) = None, audio: bool = True, audio_fps: int | None = None):`
    
:   Concatenates multiple video clips into a single video clip.

    This function takes a sequence of video clips and concatenates them into a single video clip. The clips are appended one after the other in the order they appear in the sequence. The function also handles the scaling of each clip in the concatenated clip and the audio of the concatenated clip.

    Args:
    :   - `#!py clips (Sequence[VideoClip])`: The sequence of video clips to concatenate.
        - `#!py transparent (bool, optional)`: Whether to use a transparent background for the concatenated clip. Default is False.
        - `#!py fps (int | float | None, optional)`: The frames per second of the concatenated clip. If not specified, it is set to the maximum fps of the clips in the sequence or raises a ValueError if none of the clips have fps set.
        - `#!py scaling_strategy (bool |` None, optional): The scaling strategy to use for the clips in the concatenated clip. If 'scale_up', the clips are scaled up to fit the size of the concatenated clip. If 'scale_down', the clips are scaled down to fit the size of the concatenated clip. If 'scale_same', the clips are not scaled. Default is 'scale_same'.
        - `#!py transition (VideoClip | Callable[[Image.Image, Image.Image, int | float], VideoClip] | None, optional)`: The transition to use between the clips in the concatenated clip. If a VideoClip, it is used as the transition. If a callable, it is called with the last frame of the previous clip, the first frame of the next clip, and the duration of the transition to generate the transition. If None, no transition is used. Default is None.
        - `#!py audio (bool, optional)`: Whether to include audio in the concatenated clip. If True, the audio of the clips in the sequence is also concatenated. Default is True.
        - `#!py audio_fps (int | None, optional)`: The frames per second of the audio of the concatenated clip. Default is None.

    Returns:
    :   `#!py ImageSequenceClip`: The concatenated video clip as an instance of the `#!py ImageSequenceClip` class.

    Raises:
        - `#!py ValueError`: If neither fps nor duration is set for any of the clips in the sequence.
        - `#!py ValueError`: If the size of a clip in the concatenated clip is not specified correctly.
        - `#!py TypeError`: If the scaling strategy of a clip in the concatenated clip is not of the correct type.

    Example:
    :   
        ```python
        >>> clip1 = VideoClip(...)
        >>> clip2 = ImageClip(...)
        >>> concatenated_clip = concatenate_videoclips([clip1, clip2], fps=24)
        ```

    Note:
    :   This function uses the `#!py ImageSequenceClip` class to create the concatenated video clip and the concatenate_audioclips function to concatenate the audio of the clips.
