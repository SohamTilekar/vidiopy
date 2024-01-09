from typing import Callable, Self
import numpy as np
from copy import copy

class Clip():
    def __init__(self) -> None:
        self.audio = None

    def fx(self, function: Callable[..., Self], *args, **kwargs) -> Self:
        return function(self, *args, *kwargs)
    
    def copy(self):
        newclip = copy(self)
        if hasattr(self, 'audio'):
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
        ...