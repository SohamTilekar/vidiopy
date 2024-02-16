# Getting started to use VidioPy

## Advantages and limitations

MoviePy has been developed with the following goals in mind:

Advantages:

- Simple syntax for cutting, concatenations, title insertions, video compositing, video processing, and creation of custom effects.
- Same syntax for all operating systems (Linux, MacOX, Windows).
- Flexible : You have total control over the frames of the video and audio, and creating your own effects is easy as Py.
- Fast : you can batch operations as much as you want, backend in ffmpeg, pillow, numpy, etc. for speed.
- Supports most video formats and codecs. & Question Support.

limitations:

- still in development.
- less documentation & Features.

## How Vidiopy works

Vidiopy Uses the [ffmpeg](https://www.ffmpeg.org/) library to read and write video files. The processing of the different media is is proceed using modules like Numpy,  opencv, Pillow, ETC.

## Example code

```python
from vidiopy import VideoFileClip, TextClip

# Load myHolidays.mp4 and trimming it to 10 seconds. 50s to 60s.
clip = VideoFileClip("myHolidays.mp4").subclip(50,60)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("My Holidays 2013", font_size=70, txt_color='white', bg_color='gray', font=r'path/to/font.ttf')
txt_clip = txt_clip.set_pos('center', 'right').set_duration(10)

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a video file in any format
video.write_videofile("myHolidays_edited.webm")
video.write_videofile("myHolidays_edited.mp4")
video.write_videofile("myHolidays_edited.avi")
video.write_videofile("myHolidays_edited.mkv")

# Writing single frame
video.save_frame("frame.png", t=0.5) # t= time in seconds

# Writing Image Sequence
video.write_image_sequence("image%03d.png", fps=24) # %03d are placeholders for the numbers 001, 002, 003, etc. fps = frames per second
video.write_image_sequence("image%03d.jpg", fps=24) # %03d are placeholders for the numbers 001, 002, 003, etc. fps = frames per second
video.write_image_sequence("image%03d.bmp", fps=24) # %03d are placeholders for the numbers 001, 002, 003, etc. fps = frames per second
```
