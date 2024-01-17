import ffmpegio
import platform
import os
import tempfile
import shutil
import py7zr
import requests


# Change Binary From Here
FFMPEG_BINARY = None
FFPROBE_BINARY = None


def set_ffmpeg_ffprobe_binary(binary: tuple[None | str, None | str] = (None, None)):
    system_info = platform.system()
    if binary[0] and binary[1]:
        ffmpegio.set_path(binary[0], binary[1])
        return binary
    elif system_info == 'Windows' and not binary[0] and not binary[1]:
        binary = ('ffmpeg.exe', 'ffprobe.exe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...
        BASE_DIR = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'binary')
        binary = (os.path.join(BASE_DIR, 'ffmpeg.exe'),
                  BASE_DIR+r'\ffprobe.exe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except:
            ...
        arch, _ = platform.architecture()
        if arch == "64bit":
            try:
                # FULL_RELEASE_URL = r'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z'
                # binary = download_and_extract_7z(FULL_RELEASE_URL, BASE_DIR)
                # ffmpegio.set_path(binary)
                return binary, BASE_DIR+'\\ffprobe.exe'
            except ValueError:
                print("Warning: ffmpeg binary is not set.")
        elif arch == "3bit":
            print("Warning: ffmpeg binary is not set.")
    elif system_info == 'Linux' and not binary[0] and not binary[1]:
        binary = ('ffmpeg', 'ffprobe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...

    elif system_info == 'Darwin' and not binary[0] and not binary[1]:
        binary = ('ffmpeg', 'ffprobe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...
    else:
        print("Warning: ffmpeg binary is not set.")


print(set_ffmpeg_ffprobe_binary((FFMPEG_BINARY, FFPROBE_BINARY)))
ffmpegio.video.read(r'D:\soham_code\vidiopy\media\chaplin.mp4')
