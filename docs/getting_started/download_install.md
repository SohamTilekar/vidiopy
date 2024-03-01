# Download and Installation

## Installation

### Using pip

If you're utilizing pip, installation is a breeze. Just execute the following command:

```bash linenums="1"
pip install vidiopy
```

??? warning "Warning: Requires setuptools"

    In case setuptools isn't installed, rectify this by using:
    ```bash linenums="1"
    pip install setuptools
    ```

### Using Source

1. Download the source code from the [GitHub repository](https://github.com/SohamTilekar/vidiopy).
2. Unzip the downloaded file into a designated folder.
3. Run the following command in the terminal:

```bash linenums="1"
python setup.py install
```

## Dependencies

VidioPy relies on the following Python packages:

<div class="annotate" markdown>
- [rich](https://github.com/Textualize/rich) (1)
{ .annotate }

- [numpy](https://numpy.org/) (2)
{ .annotate }

- [ffmpegio](https://github.com/python-ffmpegio/python-ffmpegio) (3)
{ .annotate }

- [pillow](https://pypi.org/project/pillow/) (4)
{ .annotate }
</div>

1. rich is a Python library for rich text and beautiful formatting in the terminal. It is used for displaying progress bars and other rich text in the terminal.
2. numpy is a Python library for numerical computing. It is used for handling arrays and matrices.
3. ffmpegio is a Python library for reading and writing video files using ffmpeg. It is used for reading and writing video files.
4. pillow is a Python library for image processing. It is used for reading, writing and modifying image files.

Pip will automatically install these dependencies for you during installation. If installing from source, manual installation of these dependencies is required.

VidioPy also depends on ffmpeg and ffprobe. It will attempt to download these binaries globally or place them in the `vidiopy/binary` directory if not found in the system's PATH or global variables. If the automatic download fails, you can manually download them from [here](https://ffmpeg.org/download.html) and place them in the `vidiopy/binary` folder or set them in global variables.

For those who prefer more control over paths, you can specify the locations of ffmpeg and ffprobe using the `#!python vidiopy.set_path()` function after importing vidiopy:

``` py linenums="1"
import vidiopy
vidiopy.set_path(ffmpeg_path="path/to/ffmpeg", ffprobe_path="path/to/ffprobe")
```

Alternatively, you can pass the path of the folder containing ffmpeg and ffprobe:

``` py linenums="1"
import vidiopy
vidiopy.set_path(ffmpeg_path="path/to/folder/containing/ffmpeg & ffprobe")
```
