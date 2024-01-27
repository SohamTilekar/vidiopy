from functools import wraps


def requires_duration(f):
    """ Decorator that raises an error if the clip has no duration."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.duration:
            raise ValueError("Attribute 'duration' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_duration_or_end(f):
    """ Decorator that raises an error if the clip has no duration or end."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.duration and not clip.end:
            raise ValueError("Attribute 'duration' or 'end' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_size(f):
    """ Decorator that raises an error if the clip has no size."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.size:
            raise ValueError("Attribute 'size' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_fps(f):
    """ Decorator that raises an error if the clip has no fps."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.fps:
            raise ValueError("Attribute 'fps' not set or `fps=0`")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_start(f):
    """ Decorator that raises an error if the clip has no start."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.start:
            raise ValueError("Attribute 'start' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_end(f):
    """ Decorator that raises an error if the clip has no end."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.end:
            raise ValueError("Attribute 'end' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_start_end(f):
    """ Decorator that raises an error if the clip has no start or end."""

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.start and not clip.end:
            raise ValueError("Attribute 'start' or 'end' not set")
        else:
            return f(clip, *a, **k)

    return wrapper
