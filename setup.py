from setuptools import setup, find_packages
from pathlib import Path

with open(Path(r".\README.md")) as f:
    long_description = f.read()

__version__ = "0.2.12"

setup(
    name='vidiopy',
    version=__version__,
    description='An Video Editing Library Similar to Moviepy.',
    long_description=long_description,
    author='Soham Tilekar',
    author_email='sohamtilekar233@gamil.com',
    # maintainer='Soham Tilekar',
    # maintainer_email='sohamtilekar233@gmail.com',
    url=r'https://github.com/SohamTilekar/vidiopy',
    packages=find_packages(exclude=("venv", "test", ".vscode", ".idea")),
    project_urls={
        "Homepage": "https://github.com/SohamTilekar/vidiopy/",
        "Source": "https://github.com/SohamTilekar/vidiopy/",
        "Tracker": "https://github.com/SohamTilekar/vidiopy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "License :: OSI Approved :: MIT No Attribution License (MIT-0)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Multimedia :: Graphics :: Editors",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    license='MIT License',
    long_description_content_type='text/markdown',
    install_requires=['rich', 'pydub', 'numpy', 'ffmpegio', 'pillow', 'decorator'],
    include_package_data=True,
    python_requires=">=3.11, <=3.12.1",
)