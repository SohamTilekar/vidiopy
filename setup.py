from setuptools import find_packages, setup
from pathlib import Path

with open(Path(r".\README.md")) as f:
    long_description = f.read()

setup(
    name='vidiopy',
    version='0.0.60',
    description='An Video Editing Library Similar to Moviepy.',
    long_description=long_description,
    package_dir={'': 'vidiopy'},
    long_description_content_type='text/markdown',
    url=r""
)