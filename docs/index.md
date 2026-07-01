# 🎬 VidioPy

[![PyPI version](https://badge.fury.io/py/vidiopy.svg)](https://badge.fury.io/py/vidiopy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VidioPy** is a modern, Pythonic video editing and manipulation library. Born as a robust alternative to MoviePy, it aims to provide a cleaner, highly extensible interface for developers looking to programmatically edit videos, generate dynamic content, and composite multimedia assets.

Whether you're building automated video generation tools, adding text overlays, or creating simple video effects, VidioPy gives you the reliable building blocks to do it effortlessly.

---

## 📖 Table of Contents

- 📥 **[Download & Install](getting_started/download_install.md)**
- 🚀 **[Getting Started](getting_started/quick_presentation.md)**
- 📚 **[Reference Manual](reference_manual/reference_manual.md)**

---

## ✨ Features

- **Intuitive API**: Chainable methods and straightforward class structures (`VideoClip`, `AudioClip`, `TextClip`, etc.).
- **Media Compositing**: Overlay text, images, and other videos to build complex scenes.
- **Audio & Video Integration**: First-class support for audio mixing and manipulation alongside your video frames.
- **Programmatic Effects**: Apply mathematical transformations and lambda functions to video frames dynamically over time.
- **Familiar Tools Under the Hood**: Built on top of `numpy`, `Pillow`, and `ffmpegio` for blazing fast frame manipulations.

---

## 🚀 Quick Start

Creating your first video with VidioPy is as simple as:

```python
import vidiopy

# 1. Load an existing video
video = vidiopy.VideoFileClip("path/to/video.mp4")

# 2. Create a text overlay
text = vidiopy.TextClip("Hello, VidioPy!", fontsize=70, color="white")

# 3. Animate the text to move downwards over time
text = text.set_position(lambda t: (100, 50 + 10 * t))

# 4. Composite the text over the video
final_video = vidiopy.CompositeVideoClip([video, text])

# 5. Export the result
final_video.write_videofile("output.mp4")
```

---

## 🤝 Contributing

VidioPy is a community-driven project and we would love your help! Whether you want to fix bugs, propose new features, or improve the documentation, all contributions are welcome.

To get started:
1. Check out our [Contribution Guidelines](more/CONTRIBUTING.md).
2. Fork the repository and create your feature branch.
3. Make your changes and test them thoroughly.
4. Submit a Pull Request!

---

## ⚠️ Disclaimer

**VidioPy is currently in the active early stages of development.** 
While the core features work wonderfully, you might find some edge cases or missing capabilities compared to older libraries. We encourage you to use it, test it, and report any bugs or feature requests in the Issues tab!

---

## 📜 License

VidioPy is open-sourced software licensed under the [MIT License](https://opensource.org/licenses/MIT).
