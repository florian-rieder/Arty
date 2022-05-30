import re
from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json


# pylint: disable=too-many-instance-attributes
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
            Relative path to the file (eg. "image.png").
        title : str, optional
            Title of the image
        artist : str, optional
            Artist name
        datation : str, optional
            Production datation (eg. "c. 1875")
        technique : str, optional
            Technique (eg. "Painting", "Sculpture"...)
        material : str, optional
            Material (eg. "Oil on canvas", "Marble"...)
        conservation_site : str, optional
            Conservation site (eg. "Musée du Louvre, Paris")
        production_site : str, optional
            Production site
        dimensions : str, optional
            Dimensions of the work (eg. "300x200cm" or "20x30x25cm")
        notes : str, optional
            Text block for the user to write anything they want

        Methods
        -------
        to_legend()
            generates a reference string (legend)

        Notes
        -----
        - filename is deliberately a relative path, this prevents
          everything from breaking in the case the directory is moved.
          To get the absolute path, use:
            collection.get_absolute_path(collection_image)
          or other os.path.join barbaric things.
          This is not particularily clean but for now I don't really
          know how to do better.
        - Date format to discuss.
        - Other fields ?
        - Tag system ?
        - To add fields, remember to also add them in CollectionPanel !
    """
    # the whole field(metadata=config(field_name=...)) shenanigans are
    # there to create aliases for the attribute's name in order for the
    # JSON file generated to save metadata to take less space on the
    # user's disk.
    filename :              str
    title :                 Optional[str] = ""
    artist :                Optional[str] = ""
    datation :              Optional[str] = ""
    technique :             Optional[str] = ""
    material :              Optional[str] = ""
    conservation_site :     Optional[str] = ""
    production_site :       Optional[str] = ""
    dimensions :            Optional[str] = ""
    style :                 Optional[str] = ""
    source :                Optional[str] = ""
    notes:                  Optional[str] = ""

    def to_legend(self, style_name="CHICAGO"):
        """ Summary
            -------
            Formats the image metadata according to the guidelines in
            the "Guide du proséminaire" [1]

            Arguments
            ---------
            style_name : key in CollectionUtils.LEGEND_STYLES

            Notes
            -----
            TODO: allow for more text formatting (italics, bold...)

            References
            ----------
            [1] https://www.unil.ch/files/live/sites/hart/files/shared/Espace_Etudiants/GPS_Guide_du_proseminaire.pdf
        """
        from api.CollectionUtils import CollectionUtils

        # rules for replacing style tokens
        formatting = {
            "artist": self.artist,
            "title": self.title if self.title else "Untitled",
            "title_italic": "[i]" + self.title + "[/i]"  if self.title else "[i]Untitled[/i]",
            "datation": self.datation,
            "technique": self.technique,
            "material": self.material,
            "dimensions": self.dimensions,
            "conservation_site": self.conservation_site,
            "production_site": self.production_site,
            "production_site_if_no_artist": self.production_site if not self.artist else "",
        }

        style = CollectionUtils.LEGEND_STYLES[style_name]

        tokens = [m.group(1) for m in re.finditer(r"{(\w+)}", style)]
        # replace tokens if the formatted value exists, else skip
        formatted_tokens = [formatting[t] for t in tokens if formatting[t]]

        legend = ", ".join(formatted_tokens)

        return legend


    def __eq__(self, other):
        """ overloads the == operator so that two CollectionImages with
            the same filename are considered the same image.
        """
        return self.filename == other.filename
