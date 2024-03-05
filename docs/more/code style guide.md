# code style guide

## functions and methods docstrings

### function and method docstring template

```python linenums="1"
"""\
A Brief Description of the Function or Method

#### Parameters:
    - `param1` `type`: -
        The first Doc.
    - `param2` `type[type, type]`: -
        The second Doc.
    - `param3` `(type, optional, ...)`: -
        The third Doc.
    - `param4` `(type, optional, default=None)`: -
        The fourth Doc.
    - `*param5` `(type, optional, ...)`: -
        The fifth Doc.
    - `**param6` `(type, optional, ...)`: -
        The sixth Doc.

#### returns: # if return Multiple things
    - `int`: - an a xyz.
    - `float`: - an a abc

#### return: `int` # if return Single thing
    Doc goes here.

#### return: `None` # if do not return anything

#### raises: # add if needed
    - `Error`: - if xyz.
    - `Exception`: - if abc.

#### Note: # add if needed
    - xyz
    - More notes.

#### Warning: # add if needed
    - xyz
    - More warnings.

#### examples:
    example 1 :

    \`\`\`python
    >>> code
    output
    \`\`\`
    example 2 :

    \`\`\`python
    code # explain
    \`\`\`
    - More examples.

#### TODO: # add if needed
    - xyz
    - More TODOs.

#### [function reference manual](https://github.com/SohamTilekar/vidiopy/blob/master/docs/...)

"""
```

### function and method docstring conventions

- Docstrings are always triple quoted strings use `"""` not `'''`.
- add a blank line after the docstring.
- use the #### for the sections.
- add as much detail as possible.
- add the link to Function or Method Reference manuel.

## class docstrings

### class docstring template

```python linenums="1"
"""\
A Brief Description of the Class

properties:
    - `property1`: - a short 1 line description of the property.
    - `property2`: - a short 1 line description of the property.

methods:
    - `method1`: - a short 1 line description of the method.
    - `method2`: - a short 1 line description of the method.

abstract methods:
    - `method1`: - a short 1 line description of the method.
    - `method2`: - a short 1 line description of the method.

#### Note: # add if needed
    - xyz
    - More notes.

#### Warning: # add if needed
    - xyz
    - More warnings.

#### examples:
    example 1 :
    \`\`\`python
    >>> code
    output
    \`\`\`

    example 2 :
    \`\`\`python
    code # explain
    \`\`\`
    - More examples.
"""
```

### class docstring conventions

- Docstrings are always triple quoted strings use `"""` not `'''`.
- add a blank line after the docstring.
- use the #### for the sections.
- add as much detail as possible.

## Comments

- Use as less comments as possible.
- Use comments where code is not self explanatory or weird.
