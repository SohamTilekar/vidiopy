from typing import Callable, Self
from copy import copy


class Clip:
    """
    The Clip class represents a media clip that can be manipulated and processed.
    Which is the base class for all media clips in the library.
    """

    def fx(self, func: Callable[..., Self], *args, **kwargs) -> Self:
        """
        Apply a function to the current instance and return the result.

        This method allows for the application of any callable to the current instance of the class.
        The callable should take the instance as its first argument, followed by any number of positional and keyword arguments.

        Parameters:
            func (Callable[..., Self]): The function to apply. This should take the instance as its first argument.
            *args: Variable length argument list for the function.
            **kwargs: Arbitrary keyword arguments for the function.

        Returns:
            Self: The result of applying the function to the instance.

        Example:
            >>> clip = Clip()
            >>> def do(instance):
            ...     # Do something with instance.
            ...     return instance.
            ...
            >>> new_clip = clip.fx(do)
        """
        return func(self, *args, **kwargs)

    def copy(self):
        """
        Creates a deep copy of the current Clip object.

        This method creates a new instance of the Clip object, copying all the attributes of the current object into the new one.
        If the current object has an 'audio' attribute, it also creates a deep copy of this 'audio' object and assigns it to the 'audio' attribute of the new Clip object.

        Returns:
            Clip: A new Clip object that is a deep copy of the current object.
        """
        newclip = copy(self)
        if hasattr(self, "audio"):
            newclip.audio = copy(self.audio)
        return newclip

    def close(self):
        """
        Release any resources that are in use.
        """

        #    Implementation note for subclasses:
        #
        #    * Memory-based resources can be left to the garbage-collector.
        #    * However, any open files should be closed, and subprocesses
        #      should be terminated.
        #    * Be wary that shallow copies are frequently used.
        #      Closing a Clip may affect its copies.
        #    * Therefore, should NOT be called by __del__().

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
