import subprocess
import shutil
import ffmpegio
import platform
import os
import tempfile
import zipfile
import requests

__all__ = ['FFMPEG_BINARY', 'FFPROBE_BINARY', 'set_path']

# Change Binary From Here
FFMPEG_BINARY = None
FFPROBE_BINARY = None


BASE_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'binary')


def set_ffmpeg_ffprobe_binary(binary: tuple[None | str, None | str] = (None, None)):
    def download_and_extract_zip(url, output_folder):
        response = requests.get(url)
        response.raise_for_status()
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile('wb', suffix='ffmpeg-release-full.zip', delete=False) as file:
                file.write(response.content)
                temp_file_path = file.name  # Get the path before closing the file

            with zipfile.ZipFile(temp_file_path, 'r') as zip_file:
                zip_file.extract(
                    'ffmpeg-6.1.1-essentials_build/bin/ffmpeg.exe', output_folder)
                zip_file.extract(
                    'ffmpeg-6.1.1-essentials_build/bin/ffprobe.exe', output_folder)
                zip_file.close()

            shutil.move(os.path.join(
                output_folder, 'ffmpeg-6.1.1-essentials_build', 'bin', 'ffmpeg.exe'), output_folder)
            shutil.move(os.path.join(
                output_folder, 'ffmpeg-6.1.1-essentials_build', 'bin', 'ffprobe.exe'), output_folder)

            return os.path.join(output_folder, 'ffmpeg.exe'), os.path.join(output_folder, 'ffprobe.exe')
        finally:
            shutil.rmtree(os.path.join(
                output_folder, 'ffmpeg-6.1.1-essentials_build'))
            if temp_file_path:
                os.remove(temp_file_path)

    system_info = platform.system()
    if binary[0] and binary[1]:
        ffmpegio.set_path(binary[0], binary[1])
        return binary
    elif system_info == 'Windows' and not binary[0] and not binary[1]:
        binary = (os.path.join(BASE_DIR, 'ffmpeg.exe'),
                  os.path.join(BASE_DIR, 'ffprobe.exe'))
        try:
            ffmpegio.set_path(*binary)
            return binary
        except Exception:
            ...
        binary = ('ffmpeg.exe', 'ffprobe.exe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...
        arch, _ = platform.architecture()
        if arch == "64bit":
            try:
                FULL_RELEASE_URL = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
                binary = download_and_extract_zip(FULL_RELEASE_URL, BASE_DIR)
                ffmpegio.set_path(*binary)
                return binary
            except ValueError:
                print("Warning: ffmpeg binary is not set.")
        elif arch == "3bit":
            print("Warning: ffmpeg binary is not set.")
    elif system_info == 'Linux' and not binary[0] and not binary[1]:
        # TODO: Test it.
        # TODO: Add Support to download binary from https://johnvansickle.com/ffmpeg/ or else where.
        binary = (os.path.abspath(os.path.join('binary', 'ffmpeg')),
                  os.path.abspath(os.path.join('binary', 'ffprobe')))
        try:
            ffmpegio.set_path(*binary)
            return binary
        except:
            ...
        binary = ('ffmpeg', 'ffprobe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...
        try:
            subprocess.run(['sudo', 'apt', 'install', 'ffmpeg'], check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(
                ['sudo', 'apt-get', 'install', 'ffmpeg'], check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['sudo', 'pacman', '-S', 'ffmpeg'], check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['sudo', 'dnf', 'install', 'ffmpeg'], check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['yum', 'install', 'epel-release'], check=True)
            subprocess.run(['sudo', 'yum', 'localinstall', '--nogpgcheck',
                           'https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm'], check=True)
            subprocess.run(['yum', 'install', 'ffmpeg',
                           'fmpeg-devel'], check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        try:
            subprocess.run(['sudo', 'zypper', 'addrepo', '-cfp', '90',
                           'https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/', 'packman'], check=True)
            subprocess.run(['sudo', 'zypper', 'refresh'], check=True)
            subprocess.run(['sudo', 'zypper', 'install',
                           '--from', 'packman', 'ffmpeg'], check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...

        print("Warning: ffmpeg binary is not set.")
    elif system_info == 'Darwin' and not binary[0] and not binary[1]:
        # TODO: Test it.
        try:
            ffmpegio.set_path(f'{BASE_DIR}/ffmpeg', f'{BASE_DIR}/ffprobe')
        except (FileNotFoundError, subprocess.CalledProcessError):
            ...
        binary = ('ffmpeg', 'ffprobe')
        try:
            ffmpegio.set_path(*binary)
            return binary
        except (ValueError):
            ...
        try:
            subprocess.run('brew install ffmpeg', shell=True, check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            try:
                subprocess.run('xcode-select --install',
                               shell=True, check=True)
                subprocess.run('brew  install ffmpeg', shell=True, check=True)
                subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                               shell=True, check=True)
                ffmpegio.set_path(*binary)
                return binary
            except (FileNotFoundError, subprocess.CalledProcessError):
                ...
        try:
            subprocess.run('sudo port install ffmpeg', shell=True, check=True)
            ffmpegio.set_path(*binary)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError):
            try:
                subprocess.run('xcode-select --install',
                               shell=True, check=True)
                subprocess.run('sudo port install ffmpeg',
                               shell=True, check=True)
                ffmpegio.set_path(*binary)
                return binary
            except (FileNotFoundError, subprocess.CalledProcessError):
                ...
        ffmpeg_temp_filename = ''
        ffprobe_temp_filename = ''
        try:
            macos_ffmpeg_binary_api_url = r'https://evermeet.cx/ffmpeg/getrelease/zip'
            macos_ffprobe_binary_api_url = r'https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip'
            import urllib.request
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                ffmpeg_temp_filename = temp_file.name
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                ffprobe_temp_filename = temp_file.name
            with urllib.request.urlopen(macos_ffmpeg_binary_api_url) as response, open(ffmpeg_temp_filename, 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            with urllib.request.urlopen(macos_ffprobe_binary_api_url) as response, open(ffprobe_temp_filename, 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            with zipfile.ZipFile(ffmpeg_temp_filename, 'r') as zip_file:
                zip_file.extract('ffmpeg', os.path.join(BASE_DIR, 'ffmpeg'))
                zip_file.close()
            with zipfile.ZipFile(ffprobe_temp_filename, 'r') as zip_file:
                zip_file.extract('ffprobe', os.path.join(BASE_DIR, 'ffprobe'))
                zip_file.close()
            ffmpegio.set_path(BASE_DIR)
            return (os.path.join(BASE_DIR, 'ffmpeg'),
                    os.path.join(BASE_DIR, 'ffprobe'))
        except (ffmpegio.errors.FFmpegError,
                FileNotFoundError,
                subprocess.CalledProcessError):
            if os.path.exists(ffmpeg_temp_filename):
                os.remove(ffmpeg_temp_filename)
            if os.path.exists(ffprobe_temp_filename):
                os.remove(ffprobe_temp_filename)
        print("Warning: ffmpeg binary is not set.")
    else:
        print("Warning: ffmpeg binary is not set.")
    return None, None


FFMPEG_BINARY, FFPROBE_BINARY = set_ffmpeg_ffprobe_binary(
    (FFMPEG_BINARY,
     FFPROBE_BINARY)
)

del set_ffmpeg_ffprobe_binary
del BASE_DIR
del platform
del zipfile


def set_path(
        ffmpeg_path: str | None = None,
        ffprobe_path: str | None = None):
    ffmpegio.set_path(ffmpeg_path, ffprobe_path)
