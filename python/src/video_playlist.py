"""A video playlist class."""

from collections import OrderedDict


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name: str):
        self._videos = OrderedDict()
        self._name = name

