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
        title : str, optional
            title of the image
        artist : str, optional
            artist name
        year : str, optional
            production year (eg. "c. 1875")
        technique : str, optional
            technique (eg. "Oil on canvas")
        conservation_site : str, optional
            conservation site (eg. "Musée du Louvre, Paris")
        production_site : str, optional
            production site
        dimensions : str, optional
            dimensions of the work (eg. "300x200cm" or "20x30x25cm")

        Methods
        -------
        __eq__
            overloads the == operator

        NOTE
        ----
        Date format to discuss

        TODO
        ----
        JSON format optimisation by minifying and aliasing the property
        names to take less space on disk.
    """

    filename :              str
    title :                 Optional[str] = None
    artist :                Optional[str] = None
    year :                  Optional[str] = None
    technique :             Optional[str] = None
    conservation_site :     Optional[str] = None
    production_site :       Optional[str] = None
    dimensions :            Optional[str] = None

    def to_reference(self):
        """ Formats the image metadata according to the guidelines at :
            https://www.unil.ch/files/live/sites/hart/files/shared
            /Espace_Etudiants/GPS_Guide_du_proseminaire.pdf

            NOTE
            ----
            Maybe allow for using different formattings ?
            This code assumes all fields are filled correctly
        """
        ref_string = "{artist_if_artist}{title}{production_site_if_no_artist}{date}{technique}{dimensions}{conservation_site}".format(
            artist_if_artist = self.artist + ", " if self.artist else "",
            title = self.title + ", ", # TODO: see about italics
            production_site_if_no_artist = self.production_site + ", " if not self.artist else "",
            date = self.year + ", ",
            technique = self.technique + ", ",
            dimensions = self.dimensions + ", ",
            conservation_site = self.conservation_site
        )

        return ref_string


    def __eq__(self, other):
        """ overloads the == operator so that two CollectionImages with
            the same filename are considered the same image.
        """
        return self.filename == other.filename
