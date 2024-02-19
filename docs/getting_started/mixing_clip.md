# Mixing clips

Video composition, also known as non-linear editing, is the fact of playing several clips together in a new clip. This video is a good example of what compositing you can do with VidioPy:

<!-- Adding youtube video in the markdown -->
<div style="display: flex; justify-content: center;">
    <iframe width="1280" height="720"  src="https://www.youtube.com/embed/rIehsqqYFEM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## stacking & Concatenating clips

Two simple ways of putting clips together is to concatenate them (to play them one after the other in a single long clip) or to stacking them (to them side by side in a single larger clip).

### Concatenating clips

Concatenating clips is done using the `concatenate_videoclips` function. This function takes a list of clips and returns a new clip that plays them one after the other:

```python
from vidiopy import ImageClip, VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("path/to/video1.mp4")
clip2 = VideoFileClip("path/to/video2.mp4")
clip3 = ImageClip("path/to/Image.png")

final_clip = concatenate_videoclips([clip1, clip2, clip3], fps=24) # fps is optional if not provided it will use the highest fps of the clips.
final_clip.write_videofile("path/to/output/video.mp4")
```

### Stacking clips or compositing_clips

Stacking clips is done using the `compositing_clips` function. This function takes a list of clips and returns a new clip that plays them side by side:

```python
from vidiopy import ImageClip, VideoFileClip, composite_videoclips

clip1 = VideoFileClip("path/to/video1.mp4")
clip2 = VideoFileClip("path/to/video2.mp4")
clip2.set_end(5) # it will play for 5 seconds
clip3 = ImageClip("path/to/Image.png")
clip3.set_start(5) # it will start playing after 5 seconds

final_clip = compositing_clips([clip1, clip2, clip3], fps=24) # fps is optional if not provided it will use the highest fps of the clips.
final_clip.write_videofile("path/to/output/video.mp4")
```
