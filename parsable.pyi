"""
Stub file for parsable module.

This file contains type annotations for the parsable module.
To use these type hints, ensure this .pyi file is in the same directory
as parsable.py or in your Python path.
"""

import sys
from typing import Any, Callable, Dict, List, Optional, ParamSpec, Tuple, TypeVar, Union, overload

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

__all__ = ['command', 'dispatch', 'at_top', 'find_entry_points', 'Parsable', 'parsable']

_A = ParamSpec('_A')
_B = TypeVar('_B')

VERBOSE: bool

_commands: List[Tuple[str, Tuple[Callable[..., Any], Callable[..., None]]]]
_bool_names: Dict[str, bool]
_parsers: Dict[type, Callable[[str], Any]]

def _parser(d: Any) -> Callable[[str], Any]: ...

def command(fun: Callable[_A, _B]) -> Callable[_A, _B]:
    """Decorator for parsable commands.
    
    Example:
    >>> from parsable import parsable
    >>> @parsable
    ... def cat(*filenames):
    ...     'Concatenate and print files'
    ...     for f in filenames:
    ...        print(open(f).read())
    """
    ...

def at_top(extra_depth: int = 0) -> bool:
    """Returns whether calling location is top-level parsable command.
    
    Example:
    >>> from parsable import parsable
    >>> @parsable
    ... def subroutine(arg=0):
    ...     'a subroutine'
    ...     result = arg + arg
    ...     if parsable.at_top():
    ...         print(result)
    ...     else:
    ...         return result
    """
    ...

def dispatch(argv: Optional[List[str]] = None) -> None:
    """Parses arguments to call a parsable command.
    
    Example:
    >>> from parsable import parsable
    >>> if __name__ == '__main__':
    ...     parsable.dispatch()
    """
    ...

def find_entry_points(
    package_name: str,
    package_dir: Optional[str] = None,
    pattern: str = r'\bparsable\b'
) -> Dict[str, List[str]]:
    """Finds parsable entry points during package setup.
    
    Example in setup.py:
        from setuptools import setup, find_packages
        from parsable import find_entry_points
        setup(
            name='example_package',
            packages=find_packages(),
            entry_points=find_entry_points('example_package'))
    """
    ...

class Parsable:
    """Collects parsable commands locally for optional dispatch.
    
    Example:
    >>> from parsable import parsable
    >>> parsable = parsable.Parsable()
    """
    
    _commands: List[Callable[..., Any]]
    
    def __init__(self) -> None: ...
    
    def command(self, /, fun: Callable[_A, _B]) -> Callable[_A, _B]: ...
    
    def dispatch(self, /, argv: Optional[List[str]] = None) -> None: ...
    
    @overload
    def __call__(self, /, fun: Callable[_A, _B]) -> Callable[_A, _B]: ...
    
    @overload
    def __call__(self, /, argv: List[str]) -> None: ...
    
    # Static method references
    at_top: Callable[[int], bool]
    find_entry_points: Callable[[str, Optional[str], str], Dict[str, List[str]]]
    
    # Self-reference (this is a bit unusual but matches your original code)
    Parsable: type[Parsable]

# Module-level parsable instance
parsable: Parsable 