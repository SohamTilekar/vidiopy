from setuptools import find_packages, setup
from pathlib import Path

with open(Path(r".\README.md")) as f:
    long_description = f.read()

setup(
    name='vidiopy',
    version='0.0.60',
    description='An Video Editing Library Similar to Moviepy.',
    long_description=long_description,
    author='Soham Tilekar',
    author_email='sohamtilekar233@gamil.com',
    # maintainer='Soham Tilekar',
    # maintainer_email='sohamtilekar233@gmail.com',
    url=r'https://github.com/SohamTilekar/vidiopy',
    package_dir={'': 'vidiopy'},
    classifiers=['', '', ''],
    license='MIT',
    
    long_description_content_type='text/markdown',
)