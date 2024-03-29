# VidioPy

![Vidiopy](https://gh-card.dev/repos/SohamTilekar/vidiopy.svg "Vidiopy")

</p>

VidioPy is a Python library in its early stages of development, intended as an alternative to Moviepy for basic video editing and manipulation. The goal is to provide a user-friendly interface for handling video files, applying basic transformations, and creating simple visual content.

## Installation

You can install VidioPy using the following command:

```bash
pip install git+https://github.com/SohamTilekar/VidioPy.git
```

or

```bash
pip install vidiopy
```

Note:

- Using the git comand version has many Advantages.
  - Bug Fixes.
  - Secure.
  - Latest.
- Using the dirct comand `pip install vidiopy` has many disadvantages.
  - Not Secure [repoted Issue #7](https://github.com/SohamTilekar/vidiopy/issues/7)
  - More Bugs.

## Usage

Here's a simple example of how to use VidioPy to create a video file:

```python
import vidiopy

video = vidiopy.VideoFileClip("path/to/video.mp4")
text = vidiopy.TextClip("Hello, world!", fontsize=70, color="white")
text.set_position(lambda t: (100, 50 + 10*t))
video = vidiopy.CompositeVideoClip([video, text])
video.write_videofile("output.mp4")
```

See the Detailed Documentation [here](https://sohamtilekar.github.io/vidiopy/)

## Contribution

We welcome contributions from the community to help us improve and expand VidioPy. Here's how you can contribute:

- Fixing bugs: Help us identify and resolve issues to ensure a stable and reliable library.
- Adding new features: Introduce new functionalities to make VidioPy more versatile and powerful.
- Improving documentation: Enhance the clarity and completeness of our documentation to make it more user-friendly.
- Providing feedback: Share your experiences, suggestions, and insights to help us shape the future development of VidioPy.

To contribute:

1. Read the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file.
1. Fork the repository.
1. Create a new branch for your feature, bug fix, or documentation improvement.
1. Make your changes and test them thoroughly.
1. Submit a pull request with a clear description of your changes.

## Disclaimer

**VidioPy is currently in the early stages of development and is not yet a complete product. Some features may be limited or incomplete. Currently, VidioPy does not support audio while writing video files, and there are no built-in video effects.** Use it at your own discretion, and feel free to report any issues, feature request or provide feedback.

## License

VidioPy is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Happy video editing with VidioPy!
