"""Utility functions"""
import inspect
from typing import Any


def filter_kwargs_for_init(cls, kwargs: dict[str, Any], skip_additionally: list[str] = ()):
    """filter provided dictionary to leave only those keys, which are met in constructor of the cls"""

    sig = inspect.signature(cls.__init__)
    valid_params = set(sig.parameters) - {'self'}
    return {k: v for k, v in kwargs.items() if k in valid_params and k not in skip_additionally}
