def gray_scale(clip):
    clip.fl_frame_transform(lambda frame, *args, **kwargs: frame.convert('L'))


def blackwhite(clip):
    clip.fl_frame_transform(lambda frame, *args, **kwargs: frame.convert('1'))
