import ffmpegio

__all__ = ["FFMPEG_BINARY", "FFPROBE_BINARY", "set_path"]

# Change Binary From Here
try:
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
except ffmpegio.path.FFmpegNotFound:
    FFMPEG_BINARY = None
    FFPROBE_BINARY = None


def set_path(ffmpeg_path: str | None = None, ffprobe_path: str | None = None):
    ffmpegio.set_path(ffmpeg_path, ffprobe_path)
    FFMPEG_BINARY = ffmpegio.get_path()
    FFPROBE_BINARY = ffmpegio.get_path(probe=True)
    return FFMPEG_BINARY, FFPROBE_BINARY
