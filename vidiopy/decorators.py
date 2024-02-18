"""
This module contains decorators that can be used to enforce attribute requirements on functions.

The decorators in this module are used to wrap functions that require specific attributes in their first argument (clip).
If the required attributes are not set or are None, the decorators will raise a ValueError.
"""

from functools import wraps

# Decorator implementations...
from functools import wraps


def requires_duration(f):
    """
    Decorator that raises an error if the clip has no 'duration' attribute.

    This decorator is used to wrap functions that require a 'duration' attribute in their first argument (clip).
    If the 'duration' attribute is not set or is None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has a 'duration' attribute.

    Returns:
    function: The wrapped function which will raise an error if the 'duration' attribute is not set in the clip.

    Raises:
    ValueError: If the 'duration' attribute is not set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.duration:
            raise ValueError("Attribute 'duration' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_duration_or_end(f):
    """
    Decorator that raises an error if the clip has neither 'duration' nor 'end' attribute.

    This decorator is used to wrap functions that require either a 'duration' or 'end' attribute in their first argument (clip).
    If both 'duration' and 'end' attributes are not set or are None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has a 'duration' or 'end' attribute.

    Returns:
    function: The wrapped function which will raise an error if neither the 'duration' nor 'end' attribute is set in the clip.

    Raises:
    ValueError: If neither the 'duration' nor 'end' attribute is set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.duration and not clip.end:
            raise ValueError("Attribute 'duration' or 'end' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_size(f):
    """
    Decorator that raises an error if the clip has no 'size' attribute.

    This decorator is used to wrap functions that require a 'size' attribute in their first argument (clip).
    If the 'size' attribute is not set or is None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has a 'size' attribute.

    Returns:
    function: The wrapped function which will raise an error if the 'size' attribute is not set in the clip.

    Raises:
    ValueError: If the 'size' attribute is not set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.size:
            raise ValueError("Attribute 'size' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_fps(f):
    """
    Decorator that raises an error if the clip has no 'fps' attribute.

    This decorator is used to wrap functions that require an 'fps' attribute in their first argument (clip).
    If the 'fps' attribute is not set or is None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has an 'fps' attribute.

    Returns:
    function: The wrapped function which will raise an error if the 'fps' attribute is not set in the clip.

    Raises:
    ValueError: If the 'fps' attribute is not set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.fps:
            raise ValueError("Attribute 'fps' not set or `fps=0`")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_start(f):
    """
    Decorator that raises an error if the clip has no 'start' attribute.

    This decorator is used to wrap functions that require a 'start' attribute in their first argument (clip).
    If the 'start' attribute is not set or is None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has a 'start' attribute.

    Returns:
    function: The wrapped function which will raise an error if the 'start' attribute is not set in the clip.

    Raises:
    ValueError: If the 'start' attribute is not set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.start:
            raise ValueError("Attribute 'start' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_end(f):
    """
    Decorator that raises an error if the clip has no 'end' attribute.

    This decorator is used to wrap functions that require an 'end' attribute in their first argument (clip).
    If the 'end' attribute is not set or is None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has an 'end' attribute.

    Returns:
    function: The wrapped function which will raise an error if the 'end' attribute is not set in the clip.

    Raises:
    ValueError: If the 'end' attribute is not set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.end:
            raise ValueError("Attribute 'end' not set")
        else:
            return f(clip, *a, **k)

    return wrapper


def requires_start_end(f):
    """
    Decorator that raises an error if the clip has no 'start' or 'end' attribute.

    This decorator is used to wrap functions that require both 'start' and 'end' attributes in their first argument (clip).
    If either the 'start' or 'end' attribute is not set or is None, the decorator will raise a ValueError.

    Parameters:
    f (function): The function to be wrapped. This function should have a first argument (clip) that has both 'start' and 'end' attributes.

    Returns:
    function: The wrapped function which will raise an error if either the 'start' or 'end' attribute is not set in the clip.

    Raises:
    ValueError: If either the 'start' or 'end' attribute is not set in the clip.
    """

    @wraps(f)
    def wrapper(clip, *a, **k):
        if not clip.start and not clip.end:
            raise ValueError("Attribute 'start' or 'end' not set")
        else:
            return f(clip, *a, **k)

    return wrapper
