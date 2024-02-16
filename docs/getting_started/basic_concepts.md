# Basic Concepts

There are 2 main types of clip in VidioPY: `VideoClip` and `AudioClip`. The first one is used for videos and the second one for Audio. Both of them are based on the `Clip` class, which is the base class for all clips in VidioPY.

They can be modified (cut, slowed down, darkened…) or put mixed with clips to form new clips, they can be written to files (as a MP4, a GIF, a MP3, etc.).
VideoClips for instance can be created from a video file, an image, a text, or a custom animation. They can have an audio track (which is an AudioClip).

A clip can be modified using one of moviepy’s numerous effects (like in `clip.resize(width="360")`, `clip.subclip(t1,t2)`, or `clip.fx(vidiopy.brightness, 1.5)`) or using a user-implemented effect. VidioPY implements many functions (like `clip.fl_frame_transform`, `clip.fl_clip_transform`, `clip.fl_time_transform`, `clip.fx`, etc.) which make it very easy to code your own effect in a few lines.

## VideoClip

### Creating a VideoClip

There are many ways to create a VideoClip. The most common way is to load a video file using `VideoFileClip`:

```python
from vidiopy import VideoFileClip
clip = VideoFileClip("path/to/video.mp4")
```

You can also create a VideoClip from an image:

```python
from vidiopy import ImageClip
clip = ImageClip("path/to/image.png")
```

### Modifying a VideoClip

There are may attributes of the VideoClip class, some of them are:
fps, duration, size, audio, start, end, start, etc.

You can set them using the `set` methods relative to the attribute you want to set.

```python
clip = clip.set_duration(10) # Not Allowed for the VideoClips only for the ImageClips
clip = clip.set_fps(24) # Should be int or float
clip = clip.set_start(5) # Use Full for the Compositing & Concatenating Video Clip. More in the Mixing clips Section
clip = clip.set_end(15) # Use Full for the Compositing & Concatenating Video Clip. More in the Mixing clips Section
audio = AudioClip("path/to/audio.mp3")
clip = clip.set_audio(audio) # Set the audio of the clip. use full for the ImageClips.
...
```

### Applying Effects to a VideoClip

There are May effects that can be applied to the VideoClip. Some of them are:
resize, crop, subclip, fx, etc.

```python
clip = resize(clip, width=360) # Resize the clip to the given width
clip = crop(clip, x1=10, y1=10, x2=100, y2=100) # Crop the clip to the given dimensions
clip = clip.subclip(t1=5, t2=10) # Cut the clip to the given duration
clip = clip.fx(vidiopy.brightness, 1.5) # Apply the brightness effect to the clip
...
```

### Exporting a VideoClip

You can write a VideoClip to a file using the `write_videofile` method:

```python
clip.write_videofile("path/to/output/video.mp4") # Write the clip to a file
clip.write_videofile_subclip("path/to/output/video.mp4", start_t=5, end_t=10) # Write the subclip to a file
clip.write_image_sequence(nformat=".png", dir="images") # Write the clip to a file as an image sequence
clip.save_frame("path/to/output/frame.png", t=5) # Save the frame of the clip to a file
```

## AudioClip

### Creating an AudioClip

There are many ways to create an AudioClip. The most common way is to load an audio file using `AudioFileClip` or `SilenceClip`:

```python
from vidiopy import AudioFileClip
clip = AudioFileClip("path/to/audio.mp3") # Create an audio clip from a file Also accept video file it will extract the audio from the video file
clip = SilenceClip(duration=10) # Create a silent audio clip
```

### Modifying an AudioClip

There are may attributes of the AudioClip class, some of them are:
audio_data, fps, start, end, etc.

You can set them using the `set` methods relative to the attribute you want to set.

```python
clip.fps = 24 # Set the fps of the clip
clip.start = 5 # Set the start time of the clip
clip.end = 15 # Set the end time of the clip
clip.audio_data = audio_data # Set the audio data of the clip
...
```

### Applying Effects to an AudioClip

There are May effects that can be applied to the AudioClip. Some of them are:
audio_normalize, sub_clip, etc.

```python
clip = clip.sub_clip(start=5, end=10) # Cut the clip to the given duration
clip = audio_normalize(clip) # Apply the normalize effect to the clip
...
```

### Exporting an AudioClip

You can write an AudioClip to a file using the `write_audiofile` method:

```python
clip.write_audiofile("path/to/output/audio.mp3") # Write the clip to a file
```
