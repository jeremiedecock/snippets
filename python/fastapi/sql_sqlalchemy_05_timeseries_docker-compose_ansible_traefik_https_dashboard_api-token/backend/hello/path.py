"""
This module contains common tools related to (file) paths.
"""

__all__ = ['expand_path']

import os

def expand_path(path):
    """Expand `~` constructs and return an absolute path.

    On Unix operating systems (Linux, MacOSX, ...),
    `~` is a shortcut for the curent user's home directory
    (e.g. "/home/jack" for "jack").

    Example
    -------

    Lets assume we are on a Unix system,
    the current user is "jack" and the current path is "/bar".

    >>> expand_path("~/foo")
    "/home/jack/foo"

    >>> expand_path("baz")
    "/bar/baz"

    >>> expand_path("../tmp")
    "/tmp"

    Parameters
    ----------
    path : str
        The `path` to expand.

    Returns
    -------
    str
        The absolute and expanded `path`.
    """
    if path is not None:
        path = os.path.expanduser(path)  # to handle "~/..." paths
        path = os.path.abspath(path)     # to handle relative paths
        return path
    else:
        return None
