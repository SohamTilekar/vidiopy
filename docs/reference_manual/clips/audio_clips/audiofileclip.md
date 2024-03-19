# AudioFileClip

> `#!py class` `vidiopy.AudioFileClip`

:   
    Bases: `vidiopy.SilenceClip`

    AudioFileClip is a class that represents an audio file. It extends the SilenceClip class.

    Parameters:
    :   
        - `#!py path: str | pathlib.Path`: The path to the audio file.
        - `#!py duration (int | float | None, optional)`: The duration of the audio file. If not provided, it will be calculated from the audio file.

    Raises:
    :   
        - `#!py ValueError`: If the audio file is empty and duration is not provided.