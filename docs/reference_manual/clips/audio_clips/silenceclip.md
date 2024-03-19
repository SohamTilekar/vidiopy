# Silence Clip

> `#!py class` `vidiopy.SilenceClip`

:   
    Bases: `vidiopy.AudioClip`

    SilenceClip is a subclass of AudioClip that represents a silent audio clip.

    It inherits from AudioClip therefore it has all the methods and attributes of AudioClip.

    Parameters:
    :   
        - `#!py duration: int | float`: The duration of the audio clip.
        - `#!py fps (int, optional)`: The frames per second of the audio clip. Default is `#!py 44100`.
        - `#!py channels (int, optional)`: The number of audio channels. Default is `#!py 1`.

