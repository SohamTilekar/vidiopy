def crop(clip, x1: int, y1: int, x2: int, y2: int):
    clip.fl_frame_transform(lambda frame, box: frame.crop(box), (x1, y1, x2, y2))
    clip.size = (x2 - x1, y2 - y1)
    return clip
