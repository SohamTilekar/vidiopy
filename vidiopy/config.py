from multiprocessing.dummy import shutdown
import subprocess
from timeit import timeit
import shutil
import ffmpegio
import platform
import os
import tempfile
import zipfile
import requests


# Change Binary From Here
FFMPEG_BINARY = None
FFPROBE_BINARY = None


def download_and_extract_zip(url, output_folder):
    response = requests.get(url)
    response.raise_for_status()
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile('wb', suffix='ffmpeg-release-full.zip', delete=False) as file:
            file.write(response.content)
            temp_file_path = file.name  # Get the path before closing the file

        with zipfile.ZipFile(temp_file_path, 'r') as zip_file:
            zip_file.extract('ffmpeg-6.1.1-essentials_build/bin/ffmpeg.exe',
                             output_folder)
            zip_file.extract('ffmpeg-6.1.1-essentials_build/bin/ffprobe.exe',
                             output_folder)
            zip_file.close()
        shutil.move(
            output_folder+r'\ffmpeg-6.1.1-essentials_build\bin\ffmpeg.exe', output_folder)
        shutil.move(
            output_folder+r'\ffmpeg-6.1.1-essentials_build\bin\ffprobe.exe', output_folder)
        return output_folder+r'\ffmpeg.exe', output_folder+r'\ffprobe.exe'
    finally:
        shutil.rmtree(output_folder+r'\ffmpeg-6.1.1-essentials_build')
        if temp_file_path:
            os.remove(temp_file_path)


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
        except Exception:
            ...
        arch, _ = platform.architecture()
        if arch == "64bit":
            try:
                FULL_RELEASE_URL = r'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
                binary = download_and_extract_zip(FULL_RELEASE_URL, BASE_DIR)
                ffmpegio.set_path(*binary)
                return binary
            except ValueError:
                print("Warning: ffmpeg binary is not set.")
        elif arch == "3bit":
            # TODO: Add 32bit support I do not have 32 os if any one has then add it and test it
            # try:
            #     FULL_RELEASE_URL = r'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
            #     binary = download_and_extract_zip(FULL_RELEASE_URL, BASE_DIR)
            #     ffmpegio.set_path(*binary)
            #     return binary
            # except ValueError:
            #     ...
            print("Warning: ffmpeg binary is not set.")
    elif system_info == 'Linux' and not binary[0] and not binary[1]:
        # TODO: Test it.
        binary = ('ffmpeg', 'ffprobe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...
        binary = (os.path.abspath(r'binary\ffmpeg'),
                  os.path.abspath(r'binary\ffprobe'))
        try:
            ffmpegio.set_path(*binary)
            return binary
        except:
            ...
        try:
            subprocess.run(['sudo', 'apt', 'install', 'ffmpeg'], check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['sudo', 'pacman', '-S', 'ffmpeg'], check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['sudo', 'dnf', 'install', 'ffmpeg'], check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['yum', 'install', 'epel-release'], check=True)
            subprocess.run(['yum', 'install', 'ffmpeg'], check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        print("Warning: ffmpeg binary is not set.")
    elif system_info == 'Darwin' and not binary[0] and not binary[1]:
        # TODO: Test it.
        binary = ('ffmpeg', 'ffprobe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...

        try:
            subprocess.run('brew install ffmpeg', shell=True, check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            try:
                subprocess.run('xcode-select --install',
                               shell=True, check=True)
                subprocess.run('brew  install ffmpeg', shell=True, check=True)
                subprocess.run(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    shell=True, check=True)
                return binary
            except (FileNotFoundError, subprocess.CalledProcessError):
                ...

        try:
            subprocess.run('sudo port install ffmpeg', shell=True, check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            try:
                subprocess.run('xcode-select --install',
                               shell=True, check=True)
                subprocess.run('sudo port install ffmpeg',
                               shell=True, check=True)
                return binary
            except (FileNotFoundError, subprocess.CalledProcessError):
                ...
        print("Warning: ffmpeg binary is not set.")
    else:
        print("Warning: ffmpeg binary is not set.")


set_ffmpeg_ffprobe_binary((FFMPEG_BINARY or None, FFPROBE_BINARY))
del set_ffmpeg_ffprobe_binary


def set_path(
        ffmpeg_path: str | None = None,
        ffprobe_path: str | None = None):
    ffmpegio.set_path(ffmpeg_path, ffprobe_path)
