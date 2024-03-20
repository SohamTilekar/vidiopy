# Concatenating Audio Clips

> `#!py def` `#!py concatenate_audioclips(clips: list[AudioClip], fps: int | None = 44100) -> AudioClip | AudioArrayClip:`

:   Concatenates multiple audio clips into a single audio clip.

    Parameters:
    
    :   - `#!py clips: list[AudioClip]`: A list of AudioClip objects to be concatenated.
        - `#!py fps (int, optional)`: The frames per second (fps) for the output AudioClip. If not provided, it defaults to 44100, or the maximum fps value found in the input clips.

    Returns:
    
    :   `#!py AudioClip | AudioArrayClip`: The concatenated AudioClip. If the input clips have different channels, the output `#!py AudioClip` will have the maximum number of channels found in the input clips, and the missing channels in the other clips will be filled with the mean value of their existing channels.

    Raises:
    
    :   `#!py ValueError`: If no clips are provided, or if no fps value is found or set, or if a clip's channels are not set.

    Note:
    
    :   - The duration of the output `#!py AudioClip` is the sum of the durations of the input clips.
        - If a clip's end time is set, it is used to calculate its duration; otherwise, its duration attribute is used.
        - If neither is set, a `#!py ValueError` is `#!py raised`.

# Compositing Audio Clips

> `#!py def` `#!py composite_audioclips(clips: list[AudioClip], fps: int | None = 44100, use_bg_audio: bool = False) -> AudioArrayClip:`

:   Composites multiple audio clips into a single audio clip.

    Parameters:
    
    :   - `#!py clips: list[AudioClip]`: A list of AudioClip objects to be composited.
        - `#!py fps (int, optional)`: The frames per second (fps) for the output AudioClip. If not provided, it defaults to the maximum fps value found in the input clips.
        - `#!py use_bg_audio (bool, optional)`: If True, the first clip in the list is used as the background audio. The remaining clips are overlaid on top of this background audio. If False, a SilenceClip of the maximum duration found in the clips is used as the background audio.

    Returns:
    
    :   `#!py AudioArrayClip`: The composited AudioClip. The output AudioClip will have the maximum number of channels found in the input clips, and the missing channels in the other clips will be filled with the mean value of their existing channels.

    Raises:
    
    :   `#!py ValueError`: If no clips are provided, or if no fps value is found or set, or if a clip's channels are not set, or if no duration is found or set in the clips when use_bg_audio is False.

    Note:
    
    :   - The duration of the output `#!py AudioClip` is the duration of the background audio.
        - If a clip's end time is set, it is used to calculate its duration; otherwise, its duration attribute is used.
        - If neither is set, a `#!py ValueError` is `#!py raised`.