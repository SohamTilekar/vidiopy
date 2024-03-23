from vidiopy.video.VideoClip import VideoClip


def crop(clip: VideoClip, x1: int, y1: int, x2: int, y2: int):
    clip.fl_frame_transform(lambda frame: frame[y1:y2, x1:x2])
    clip.size = (x2 - x1, y2 - y1)
    return clip
