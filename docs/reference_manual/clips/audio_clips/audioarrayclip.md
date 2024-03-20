# AudioArrayClip

> `#!py class` `#!py vidiopy.AudioArrayClip`

:   Bases: `#!py vidiopy.AudioClip`

    AudioArrayClip is a class that represents an audio clip from an array. It extends the AudioClip class.

    Parameters:
    
    :   
        - `#!py audio_data: np.ndarray`: The audio data.
        - `#!py fps: int`: The sample rate of the audio clip.
        - `#!py duration: int | float`: The duration of the audio clip.

    Example:

    :   ```python
        import numpy as np
        import vidiopy

        audio_data = np.random.uniform(-1, 1, 44100 * 3) # 3 seconds of random audio
        audio_clip = vidiopy.AudioArrayClip(audio_data, fps=44100)
        ```