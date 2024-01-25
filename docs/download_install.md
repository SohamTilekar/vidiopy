# Download and Installation

## Installation

### Using pip

If you're utilizing pip, installation is a breeze. Just execute the following command:

```bash
pip install vidiopy
```

In case setuptools isn't installed, rectify this by using:

```bash
pip install setuptools
```

### Using Source

1. Download the source code from the [GitHub repository](https://github.com/SohamTilekar/vidiopy).
2. Unzip the downloaded file into a designated folder.
3. Run the following command in the terminal:

```bash
python setup.py install
```

## Dependencies

VidioPy relies on the following Python packages:

1. [rich](https://github.com/Textualize/rich)
2. [numpy](https://numpy.org/)
3. [ffmpegio](https://github.com/python-ffmpegio/python-ffmpegio)
4. [pillow](https://pypi.org/project/pillow/)
5. [decorator](https://pypi.org/project/decorator/)

Pip will automatically install these dependencies for you during installation. If installing from source, manual installation of these dependencies is required.

VidioPy also depends on ffmpeg and ffprobe. It will attempt to download these binaries globally or place them in the `vidiopy/binary` directory if not found in the system's PATH or global variables. If the automatic download fails, you can manually download them from [here](https://ffmpeg.org/download.html) and place them in the `vidiopy/binary` folder or set them in global variables.

For those who prefer more control over paths, you can specify the locations of ffmpeg and ffprobe using the `vidiopy.set_path()` function after importing vidiopy:

```python
import vidiopy
vidiopy.set_path(ffmpeg_path="path/to/ffmpeg", ffprobe_path="path/to/ffprobe")
```

Alternatively, you can pass the path of the folder containing ffmpeg and ffprobe:

```python
import vidiopy
vidiopy.set_path(ffmpeg_path="path/to/folder/containing/ffmpeg & ffprobe")
```
