import os
import tempfile
import platform
import subprocess
import shutil
import urllib.request
import zipfile
import ffmpegio
from rich.progress import Progress

__all__ = ["FFMPEG_BINARY", "FFPROBE_BINARY", "set_path", "install_ffmpeg"]


def download_url(url, output_path):
    response = urllib.request.urlopen(url)
    total_size = int(response.headers["content-length"])

    with Progress() as progress:
        task_id = progress.add_task("[cyan]Downloading...", total=total_size)
        with open(output_path, "wb") as f:
            for chunk in read_in_chunks(response):
                f.write(chunk)
                progress.update(task_id, advance=len(chunk))


def read_in_chunks(file, chunk_size=1024 * 1024):  # default chunk size is 1 MB
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data


# Change Binary From Here
try:
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
except ffmpegio.path.FFmpegNotFound:
    if os.path.exists(
        os.path.join(os.path.expanduser("~"), "ffmpeg", "ffmpeg")
    ) and os.path.join(os.path.expanduser("~"), "ffmpeg", "ffprobe"):
        FFMPEG_BINARY, FFPROBE_BINARY, _ = ffmpegio.set_path(
            os.path.join(os.path.expanduser("~"), "ffmpeg")
        )
    elif os.path.exists(
        os.path.join(os.path.expanduser("~"), "ffmpeg", "ffmpeg.exe")
    ) and os.path.join(os.path.expanduser("~"), "ffmpeg", "ffprobe.exe"):
        FFMPEG_BINARY, FFPROBE_BINARY, _ = ffmpegio.set_path(
            os.path.join(os.path.expanduser("~"), "ffmpeg")
        )
    else:
        FFMPEG_BINARY, FFPROBE_BINARY = None, None


def install_ffmpeg():
    # check the operating system
    if platform.system() == "Windows":
        url = r"https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        # Using urllib install the ffmpeg zip file to the temp file

        file = ""
        dir_path = ""
        try:
            file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            file.close()
            download_url(url, file.name)
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
                if os.path.exists(os.path.join(dir_path, "ffmpeg.exe")):
                    os.remove(os.path.join(dir_path, "ffmpeg.exe"))
                if os.path.exists(os.path.join(dir_path, "ffprobe.exe")):
                    os.remove(os.path.join(dir_path, "ffprobe.exe"))
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
    elif platform.system() == "Linux":
        try:
            subprocess.run("sudo apt install ffmpeg", check=True)
        except Exception as e:
            try:
                subprocess.run("sudo apt-get install ffmpeg", check=True)
            except Exception as e:
                ...
            else:
                return "ffmpeg", "ffprobe"
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
    elif platform.system() == "Darwin":
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
    else:
        raise Exception("Unsupported Operating System")


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
        except ValueError:
            ...
    elif platform.system() == "Darwin":
        try:
            FFMPEG_BINARY, FFPROBE_BINARY = set_path(
                os.path.join(os.path.expanduser("~"), "ffmpeg")
            )
        except ffmpegio.path.FFmpegNotFound:
            ...
        except ValueError:
            ...
