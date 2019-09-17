from os.path import isfile
from pathlib import Path
from typing import Iterable, Iterator


class Filer(object):

    """A class for gracefully handling file interactions

    Designed particularly for passing context in a Click program. 

    :METHODS:

    :read: Can check to see if the file exists, then returns an iterator of lines
    :write: Writes to the file, overwriting existing contents
    :append: Writes to the end of the file, preserving existing contents
    
    """

    def __init__(self, path: str) -> None:
        """Initialise the Filer

        :path: A Unix filepath to the desired file

        """
        self.path = path

    def _exists(self) -> None:
        """Hidden method to check file existence

        If the file does not exist, it is created

        :returns: None

        """
        if not isfile(self.path):
            Path(self.path).touch()

    def read(self, create: bool = True) -> Iterator[str]:
        """Read the lines of self.path

        :returns: A generator containing the individual lines of self.path

        """
        if create:
            self._exists()
        with open(self.path, "r") as file:
            for line in file:
                yield line.rstrip("\n")

    def write(self, ins: Iterable[str]) -> None:
        """Writes contents of ins to self.path.

        If the file exists, it overwrites.
        Multiple entries are concatenated by new lines - "\n"

        :ins: An iterable of strings to write to self.path
        :returns: None

        """
        with open(self.path, "w") as file:
            file.write("\n".join(ins))

    def append(self, ins: Iterable[str]) -> None:
        """Appends contents of ins to self.path.

        Contents of self.path will not be overwritten, if it exists.
        Multiple entries are concatenated by new lines - "\n"

        :ins: An iterable of strings to write to self.path
        :returns: None

        """
        with open(self.path, "a") as file:
            file.write("\n".join(ins))
