"""This module manages the configuration of ffmpeg and ffprobe binaries."""

import os
from typing_extensions import Union
import ffmpegio

__all__ = ["FFMPEG_BINARY", "FFPROBE_BINARY", "set_path"]

FFMPEG_BINARY = None
FFPROBE_BINARY = None

try:
    try:
        FFMPEG_BINARY = ffmpegio.get_path()
        FFPROBE_BINARY = ffmpegio.get_path(probe=True)
    except Exception:
        ffmpegio.set_path(os.path.join(__file__, "binary"))
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


def set_path(
    ffmpeg_path: Union[str, None] = None, ffprobe_path: Union[str, None] = None
):
    """
    Sets the paths for the ffmpeg and ffprobe binaries.

    This function sets the paths for the ffmpeg and ffprobe binaries in the global variables FFMPEG_BINARY and FFPROBE_BINARY.
    If the paths are not provided, it uses the default paths set in the ffmpegio library.

    Parameters:
    ffmpeg_path (str | None): The path to the ffmpeg binary. If None, the default ffmpeg path is used.
    ffprobe_path (str | None): The path to the ffprobe binary. If None, the default ffprobe path is used.

    Returns:
    tuple: A tuple containing the paths to the ffmpeg and ffprobe binaries.

    Raises:
    RuntimeError: If Failed to auto-detect ffmpeg and ffprobe executable.
    ValueError: If the given paths are not valid.
    """
    global FFMPEG_BINARY, FFPROBE_BINARY
    ffmpegio.set_path(ffmpeg_path, ffprobe_path)
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
    return FFMPEG_BINARY, FFPROBE_BINARY
