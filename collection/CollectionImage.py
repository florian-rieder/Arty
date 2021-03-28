""" Represents an image in the corpus, with all its metadata
"""

from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CollectionImage():
    """
        Summary
        -------
        Dataclass that represents one image in a collection.
        It contains a pointer to the file on disk, and a set of
        metadata.

        Attributes
        ----------
        filename : str
            the local file name, not the path to the file.
            (eg. "image.png")

        Methods
        -------
        __eq__
            overloads the == operator

        Notes
        -----
        Date format to discuss
    """

    filename :              str
    title :                 Optional[str] = None
    artist :                Optional[str] = None
    year :                  Optional[str] = None
    support :               Optional[str] = None
    technique :             Optional[str] = None
    conservation_site :     Optional[str] = None

    def __eq__(self, other):
        """ overloads the == operator so that two CollectionImages with
            the same filename are considered the same image.
        """
        return self.filename == other.filename
