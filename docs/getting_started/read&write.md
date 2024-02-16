# Reading/Writing Video & Audio

## Reading Video from file

The first step of video editing is to reading them from file. this Van be Done using `vidiopy.VideoFileClip` class. This class takes the path of the video file as input and returns a video which inherits from `VideoClip` class.

```python
import vidiopy
video = vidiopy.VideoFileClip("path/to/video.extension") # you can perform the operations on the video object
video_without_audio = vidiopy.VideoFileClip("path/to/video.extension", audio=False) # defaults to `audio=True`
```

if the video do not have the audio then it will create a silence clip

## Writing Video to file

To Write the Video we can use the `write_videofile` function inside the `VideoClip`.
Other clip type inherent it from the `VideoClip`.

```python
import vidiopy
video = vidiopy.VideoFileClip("path/to/video.extension")
video.write_videofile("path/to/output/video.extension", fps=30) # fps is optional it will default use the fps of the video if it is set
```

## Reading Audio from file

To read the audio from the file we can use the `AudioFileClip` class. This class takes the path of the audio file as input and returns a audio which inherits from `AudioClip` class.

```python
import vidiopy
audio = vidiopy.AudioFileClip("path/to/audio.extension")
```

## Writing Audio to file

To Write the Audio we can use the `write_audiofile` function inside the `AudioClip`.
Other clip type inherent it from the `AudioClip`.

```python
import vidiopy
audio = vidiopy.AudioFileClip("path/to/audio.extension")
audio.write_audiofile("path/to/output/audio.extension")
```
