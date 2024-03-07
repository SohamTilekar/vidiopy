# Clip

> `#!py class` `#!py vidiopy.Clip.Clip`

:    Bases: `#!py object`
    
    A Clip is the base class for all the clips (`#!py VideoClip` and `#!py AudioClip`).

    > `#!py fx(func, *args, **kwargs)`
    
    :   Apply a function to the current instance and return the result.

        This method allows for the application of any callable to the current instance of the class.
        The callable should take the instance as its first argument, followed by any number of positional and keyword arguments.

        Parameters:
        :   - `#!py func: (Callable[..., Self])`: The function to apply. This should take the instance as its first argument.
            - `#!py *args`: Variable length argument list for the function.
            - `#!py **kwargs`: Arbitrary keyword arguments for the function.

        Returns:
        :   - `#!py Self`: The result of applying the function to the instance.

        Example:
        :   
            ```python
            >>> clip = Clip()
            >>> def do(instance):
            ...     # Do something with instance.
            ...     return instance.
            ...
            >>> new_clip = clip.fx(do)
            ```
    
    > `#!py copy()`
    
    :   Creates a deep copy of the current Clip object.

        This method creates a new instance of the Clip object, copying all the attributes of the current object into the new one.
        If the current object has an 'audio' attribute, it also creates a deep copy of this 'audio' object and assigns it to the 'audio' attribute of the new Clip object.

        Returns:
        :   `#!py Clip`: A new Clip object that is a deep copy of the current object.

    > `#!py close()`
    
    :   Release any resources that are in use.


    > `#!py __enter__()`

    :   Enter the context manager.

    > `#!py __exit__()`

    :   Exit the context manager.
