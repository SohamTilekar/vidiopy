# Mixing clips

Video composition, also known as non-linear editing, is the fact of playing several clips together in a new clip. This video is a good example of what compositing you can do with VidioPy:

<!-- Adding youtube video in the markdown -->
<div style="display: flex; justify-content: center;">
    <iframe width="1280" height="720"  src="https://www.youtube.com/embed/rIehsqqYFEM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## <!-- stacking &--> Concatenating clips

Two simple ways of putting clips together is to concatenate them (to play them one after the other in a single long clip) <!-- or to stacking them (to them side by side in a single larger clip). -->

### Concatenating clips

Concatenation is done with the function `concatenate_videoclips`:

```python
from moviepy import VideoFileClip, ImageClip, concatenate_videoclips
clip1 = VideoFileClip("video.mp4").subclip(0,5)
clip2 = ImageClip("image.jpg").set_duration(5)
f_clip = concatenate_videoclips([clip1,clip2], fps=24, over_scale=True)
f_clip.write_videofile("output.mp4")
```


