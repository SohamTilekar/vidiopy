import os
import ffmpegio

__all__ = ["FFMPEG_BINARY", "FFPROBE_BINARY", "set_path"]

FFMPEG_BINARY = None
FFPROBE_BINARY = None

try:
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
except Exception:
    try:
        if os.path.exists(
            os.path.join(os.path.expanduser("~"), "  ffmpeg", "ffmpeg")
        ) and os.path.exists(
            os.path.join(os.path.expanduser("~"), "  ffmpeg", "ffprobe")
        ):
            ffmpegio.set_path(os.path.join(os.path.expanduser("~"), "  ffmpeg"))
            FFMPEG_BINARY = os.path.join(os.path.expanduser("~"), "  ffmpeg", "ffmpeg")
            FFPROBE_BINARY = os.path.join(
                os.path.expanduser("~"), "  ffmpeg", "ffprobe"
            )
        elif os.path.exists(
            os.path.join(os.path.expanduser("~"), "ffmpeg", "ffmpeg.exe")
        ) and os.path.exists(
            os.path.join(os.path.expanduser("~"), "ffmpeg", "ffprobe.exe")
        ):
            ffmpegio.set_path(os.path.join(os.path.expanduser("~"), "ffmpeg"))
            FFMPEG_BINARY = os.path.join(os.path.expanduser("~"), "ffmpeg", "ffmpeg")
            FFPROBE_BINARY = os.path.join(os.path.expanduser("~"), "ffmpeg", "ffprobe")
        else:
            ...
    except Exception:
        ...


def set_path(ffmpeg_path: str | None = None, ffprobe_path: str | None = None):
    global FFMPEG_BINARY, FFPROBE_BINARY
    ffmpegio.set_path(ffmpeg_path, ffprobe_path)
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
    return FFMPEG_BINARY, FFPROBE_BINARY
