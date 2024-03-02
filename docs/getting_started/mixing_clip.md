# Mixing clips

Video composition, also known as non-linear editing, is the fact of playing several clips together in a new clip. This video is a good example of what compositing you can do with VidioPy:

<!-- Adding youtube video in the markdown -->
<style>
    /* Styles for the container */
    .container {
        position: relative;
        padding-top: 56.25%; /* 16:9 aspect ratio */
    }

    /* Styles for the responsive iframe */
    .responsive-iframe {
        position: absolute;
        top: 10%;
        left: 10%;
        width: 90%;
        height: 90%;
    }
</style>
<div class="container">
    <iframe class="responsive-iframe" src="https://www.youtube.com/embed/rIehsqqYFEM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## compositing / Concatenating clips

Two simple ways of putting clips together is to concatenate them (to play them one after the other in a single long clip) or to compositing (to them side by side in a single larger clip).

### Concatenating clips

Concatenating means playing the clips one after the other in a single long clip. The function `concatenate_videoclips` takes a list of clips and returns a new clip that is the concatenation of all the clips in the list.
Concatenation is done with the function `concatenate_videoclips`:

```python linenums="1"
from vidiopy import VideoFileClip, ImageClip, concatenate_videoclips
clip1 = VideoFileClip("video.mp4").subclip(0,5)
clip2 = ImageClip("image.jpg").set_duration(5)
f_clip = concatenate_videoclips([clip1,clip2], fps=24, over_scale=True)
f_clip.write_videofile("output.mp4")
```

The f_clip is a clip that plays the clips 1, and 2 one after the other. Note that the clips do not need to be the same size. If they aren't they will all appear centered in a clip large enough to contain the biggest of them, with optionally a color of your choosing to fill the borders. You have many other options there (see the doc of the function).

### Compositing Clip

Compositing is done with the function `composite_videoclips`:

```python
video = CompositeVideoClip([clip1,clip2,clip3])
```

Now video plays `clip1`, and `clip2` on top of `clip1`, and `clip3` on top of `clip1`, and `clip2`. For instance, if `clip2` and `clip3` have the same size as `clip1`, then only `clip3`, which is on top, will be visible in the video… unless `clip3` and clip2 have masks which hide parts of them. Note that by default the composition has the size of the largest clip or first if `bg_clip=True`.

### Starting and stopping times

In a CompositionClip, all the clips start to play at a time that is specified by the clip.start attribute. You can set this starting time as follows:

clip1 = clip1.with_start(5) # start after 5 seconds
So for instance your composition will look like

```python linenums="1"
video = CompositeVideoClip([clip1, # starts at t=0
                            clip2.with_start(5), # start at t=5s
                            clip3.with_start(9)]) # start at t=9s
```

In the example above, maybe clip2 will start before clip1 is over.

### Positioning clips

If clip2 and clip3 are smaller than clip1, you can decide where they will appear in the composition by setting their position. Here we indicate the coordinates of the top-left pixel of the clips:

```python linenums="1"
video = CompositeVideoClip([clip1,
                           clip2.with_position((45,150)),
                           clip3.with_position((90,100))])
```

There are many ways to specify the position:

```python linenums="1"
clip2.with_position((45,150)) # x=45, y=150 , in pixels

clip2.with_position("center") # automatically centered

# clip2 is horizontally centered, and at the top of the picture
clip2.with_position(("center","top"))

# clip2 is vertically centered, at the left of the picture
clip2.with_position(("left","center"))

# clip2 is at 40% of the width, 70% of the height of the screen:
clip2.with_position((0.4,0.7), relative=True)

# clip2's position is horizontally centered, and moving down!
clip2.with_position(lambda t: ('center', 50+t) )
```

When indicating the position keep in mind that the `y` coordinate has its zero at the top of the picture:

<div style="display: flex; justify-content: center;">
    <img src="https://moviepy.readthedocs.io/en/latest/_images/videoWH.jpeg" alt="videoWH" style="width: 50%; height: auto;" />
</div>

### Compositing audio clips

When you mix video clips together, MoviePy will automatically compose their respective audio tracks to form the audio track of the final clip, so you don’t need to worry about compositing these tracks yourself.

If you want to make a custom audiotrack from several audio sources: audioc clips can be mixed together with CompositeAudioClip and concatenate_audioclips:

```python linenums="1"
from moviepy import *
# ... make some audio clips aclip1, aclip2, aclip3
concat = concatenate_audioclips([aclip1, aclip2, aclip3])
compo = CompositeAudioClip([aclip1.multiply_volume(1.2),
                            aclip2.with_start(5), # start at t=5s
                            aclip3.with_start(9)])
```
