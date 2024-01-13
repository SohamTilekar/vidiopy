
def crop(clip, left: int, upper: int, right: int, lower: int):
    clip.fl_image(lambda frame: frame.crop((left, upper, right, lower)))
    clip.size = (right - left, upper - lower)
    return clip


if __name__ == '__main__':
    SystemExit()