import os
import tempfile
import platform
import subprocess
import shutil
import urllib.request
import zipfile
import ffmpegio

__all__ = ["FFMPEG_BINARY", "FFPROBE_BINARY", "set_path", "install_ffmpeg"]

# Change Binary From Here
try:
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
except ffmpegio.path.FFmpegNotFound:
    FFMPEG_BINARY = None
    FFPROBE_BINARY = None


def install_ffmpeg():
    # check the operating system

    if platform.platform() == "Windows":
        url = r"https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        # Using urllib install the ffmpeg zip file to the temp file

        file = ""
        dir_path = ""
        try:
            file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            file.write(urllib.request.urlopen(url).read())
            file.flush()
            file.close()
            # Extract the zip file
            zip_ref = zipfile.ZipFile(file.name, "r")
            try:
                dir_path = os.path.join(os.path.expanduser("~"), "ffmpeg")
                os.makedirs(dir_path, exist_ok=True)
                zip_ref.extract(
                    "ffmpeg-6.1.1-essentials_build/bin/ffmpeg.exe",
                    dir_path,
                )
                zip_ref.extract(
                    "ffmpeg-6.1.1-essentials_build/bin/ffprobe.exe",
                    dir_path,
                )
            finally:
                zip_ref.close()
        except Exception as e:
            raise
        finally:
            if dir_path:
                shutil.move(
                    os.path.join(
                        dir_path, r"ffmpeg-6.1.1-essentials_build\bin\ffmpeg.exe"
                    ),
                    dir_path,
                )
                shutil.move(
                    os.path.join(
                        dir_path, r"ffmpeg-6.1.1-essentials_build\bin\ffprobe.exe"
                    ),
                    dir_path,
                )
            if file:
                name = file.name
                file.close()
                os.remove(name)
        return os.path.join(dir_path, "ffmpeg.exe"), os.path.join(
            dir_path, "ffprobe.exe"
        )
    elif platform.platform() == "Linux":
        try:
            subprocess.run("sudo apt install ffmpeg", check=True)
        except Exception as e:
            ...
        else:
            return "ffmpeg", "ffprobe"
        try:
            subprocess.run(
                "sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm",
                check=True,
            )
            subprocess.run("sudo dnf install ffmpeg ffmpeg-devel", check=True)
        except Exception as e:
            ...
        else:
            return "ffmpeg", "ffprobe"
        try:
            subprocess.run("sudo pacman -S ffmpeg", check=True)
            subprocess.run("yay -S ffmpeg-git", check=True)
            subprocess.run("yay -S ffmpeg-full-git", check=True)
        except Exception as e:
            raise
        else:
            return "ffmpeg", "ffprobe"
    elif platform.platform() == "Darwin":
        try:
            subprocess.run("brew install ffmpeg", check=True)
            return "ffmpeg", "ffprobe"
        except Exception as e:
            try:
                subprocess.run("xcode-select --install", check=True)
                subprocess.run(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    check=True,
                )
                subprocess.run("brew install ffmpeg", check=True)
                return "ffmpeg", "ffprobe"
            except Exception as e:
                tmp_file = ""
                tmp_file2 = ""
                try:
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
                    tmp_file2 = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
                    tmp_file.write(
                        urllib.request.urlopen(
                            r"https://evermeet.cx/ffmpeg/get/zip"
                        ).read()
                    )
                    tmp_file2.write(
                        urllib.request.urlopen(
                            r"https://evermeet.cx/ffmpeg/get/ffprobe/zip"
                        ).read()
                    )
                    tmp_file.flush()
                    tmp_file2.flush()
                    tmp_file.close()
                    tmp_file2.close()
                    # Extract the zip file
                    with zipfile.ZipFile(tmp_file.name, "r") as zip_ref:
                        zip_ref.extract("ffmpeg", os.path.expanduser(r"~\ffmpeg"))
                    with zipfile.ZipFile(tmp_file2.name, "r") as zip_ref:
                        zip_ref.extract("ffprobe", os.path.expanduser(r"~\ffmpeg"))
                    return os.path.join(
                        os.path.expanduser(r"~\ffmpeg"), r"ffmpeg"
                    ), os.path.join(os.path.expanduser(r"~\ffmpeg"), r"ffprobe")
                except Exception as e:
                    raise
                finally:
                    if tmp_file:
                        os.remove(tmp_file.name)
                    if tmp_file2:
                        os.remove(tmp_file2.name)
                    if tmp_file:
                        tmp_file.close()
                    if tmp_file2:
                        tmp_file2.close()


def set_path(ffmpeg_path: str | None = None, ffprobe_path: str | None = None):
    global FFMPEG_BINARY, FFPROBE_BINARY
    ffmpegio.set_path(ffmpeg_path, ffprobe_path)
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
    return FFMPEG_BINARY, FFPROBE_BINARY


if FFMPEG_BINARY is None or FFPROBE_BINARY is None:
    if platform.system() == "Windows":
        try:
            FFMPEG_BINARY, FFPROBE_BINARY = set_path(
                os.path.join(os.path.expanduser("~"), "ffmpeg")
            )
        except ffmpegio.path.FFmpegNotFound:
            ...
    elif platform.system() == "Darwin":
        try:
            FFMPEG_BINARY, FFPROBE_BINARY = set_path(
                os.path.join(os.path.expanduser("~"), "ffmpeg")
            )
        except ffmpegio.path.FFmpegNotFound:
            ...
