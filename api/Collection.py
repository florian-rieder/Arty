"""
    Collection module
    Handles the datastructure of a collection, and saving and loading of
    metadata in a project folder.
"""
import os
import re
import json
import ntpath
import shutil
import builtins
from typing import Optional
from dataclasses import dataclass, field

from unidecode import unidecode
from dataclasses_json import config, dataclass_json
from kivy.logger import Logger


class CollectionManager():
    """ Summary
        -------
        Static class to manage the saving and loading of Collections.

        Methods
        -------
        load(path):
            loads a collection from a path.
        save(collection: Collection):
            saves a collection

        TODO
        ----
        - Make loading times faster
        - JSON format optimisation by minifying and aliasing the property
          names to take less space on disk.
        - Proof the loading so:
            1. we can have the absolute path to an image in a
               CollectionImage
            2. The system doesn't break when the user:
                - moves the directory between sessions
                - removes an image from the directory between sessions
                - drags an image from the work directory to the window
    """

    AUTHORIZED_IMAGE_FORMATS = (".jpg", ".jpeg", ".png", ".webp", ".tiff")
    META_EXTENSION = ".arty"
    VERSION = "Alpha-1.0"

    @classmethod
    def load(cls, path):
        """ Summary
            -------
            This function loads a collection from a path. If there is no
            collection here, create a new meta file

            Parameters
            ----------
            path: str
                path to the collection directory

            Returns
            -------
            collection: Collection
                the collection retrieved or created at the specified
                path

            Raises
            ------
            FileNotFoundError
                if the collection's work directory is not found

        """
        # check if the path given is valid
        if not os.listdir(path):
            raise FileNotFoundError

        # check if there is already a project file in this directory
        meta_filename = cls._get_meta_filename(path)

        if meta_filename:
            # if it's the case, load it.
            collection = cls.__load_meta(path)
        else:
            # if it's not the case, create a new one and start with a
            # default collection
            cls.__create_meta(path)
            # create a default collection
            collection = Collection(path, "Untitled Collection", list())

        # check the images in the directory and update the collection
        # and meta
        collection = cls.__check_files(collection)
        cls.__write_meta(collection)
        Logger.info("Collection: collection loaded")

        return collection

    @classmethod
    def save(cls, collection):
        """ Summary
            -------
            This method saves a collection to disk.

            Parameters
            ----------
            collection: Collection
                the Collection object to save
        """
        cls.__write_meta(collection)
        Logger.info("Collection: collection saved")


    @classmethod
    def __load_meta(cls, path):
        """ Summary
            -------
            Deserializes the data from the meta file and updates the
            collection.
        """
        # read the existing meta file
        meta_filename = cls._get_meta_filename(path)

        with open(os.path.join(path, meta_filename), "r") as meta:
            coll_json = meta.read()
            coll_dict = json.loads(coll_json)

        # retrieve the version of the collection
        try:
            version = coll_dict["v"]
        except KeyError as exc:
            raise KeyError(
                "Couldn't retrieve version from collection meta file"
            ) from exc

        if version != cls.VERSION:
            coll_json = cls.fix_version_conflict(coll_json)
            # reload the fixed json
            coll_dict = json.loads(coll_json)

        # now we are sure the data is clean, we can load the collection

        version = coll_dict["v"]

        # retrieve the collection list
        collection = [
            # cast each object in the JSON list to a CollectionImage
            # pylint says it's an error. Let's just say I disagree
            CollectionImage.from_dict(item) for item in coll_dict["c"]
        ]

        return Collection(path, version, collection)


    @classmethod
    def __check_files(cls, collection):
        """ Summary
            -------
            Runs through the files in the work directory and adds any
            image that is not yet in our collection. Removes any image
            whose file no longer exists -> data loss on renaming a file

            Returns
            -------
            checked_collection : Collection
                corrected collection (if new files are detected, they
                will be added to the collection, and the updated
                collection is returned)
        """
        # type safety check
        if not isinstance(collection, Collection):
            raise TypeError("collection must be of type Collection, not %s"
                % type(collection)
            )

        dir_contents = os.listdir(collection.work_directory)

        # filter the collection list to remove from the collection
        # references to files that no longer exist
        collection.collection = [i for i in collection.collection if i.filename in dir_contents]

        for filename in dir_contents:
            # reject all files with the wrong extension (case
            # insensitive)
            if filename.lower().endswith(cls.AUTHORIZED_IMAGE_FORMATS):
                new_image = CollectionImage(filename)

                # this works since we overloaded the equal operator in
                # CollectionImage !
                if new_image not in collection.collection:
                    # add the new image
                    collection.collection.append(new_image)

        return collection


    @classmethod
    def __write_meta(cls, collection):
        """ Serializes this collection and saves it in the project meta
            file in the work directory
        """
        # type safety check
        if not isinstance(collection, Collection):
            raise TypeError(
                "collection must be of type Collection, not %s"
                % type(collection)
            )

        meta_file_path = os.path.join(
            collection.work_directory,
            cls._get_meta_filename(collection.work_directory)
        )

        # create metadata file in the project directory
        with open(meta_file_path, "w") as meta_file:
            # convert the collection to JSON
            json_data = json.loads(collection.to_json())
            # convert to string and minify JSON file
            formatted_json = json.dumps(json_data, separators=(',', ':'))

            meta_file.write(formatted_json)


    @classmethod
    def __create_meta(cls, path):
        # default filename is collection.arty
        path = os.path.join(path, "collection" + cls.META_EXTENSION)
        open(path, "a").close()


    @classmethod
    def _get_meta_filename(cls, path):
        """
            Gets the first file with the correct extension. If none are
            found, returns False
        """
        for fname in os.listdir(path):
            if fname.endswith(cls.META_EXTENSION):
                return fname
        # if no collection meta file is found
        return False


    @classmethod
    def fix_version_conflict(cls, json_string):
        """ Summary
            -------
            Rules for upgrading older versions of a collection's meta
            to the current one.

            Arguments
            ---------
            json_string : str
                Outdated JSON string collected from the meta file
        """
        # turn the JSON into a dictionary for easy modifications
        coll_dict = json.loads(json_string)
        version = coll_dict["v"]

        if version == "Alpha-1.0":
            # upgrade the save file to the next version
            pass

        # turn the dictionary back to a JSON string
        json_string = json.dumps(coll_dict)

        return json_string

### end class CollectionManager


@dataclass_json
@dataclass
class Collection():
    """
        Summary
        -------
        Dataclass that represents a collection of images, that
        corresponds to a folder on the user's computer.

        Attributes
        ----------
        title : str, optional
            User entered name for the collection
        working_directory : str
            path to this collection's directory
        collection : list(CollectionImage), optional
            list of the images in the collection

        Methods
        -------
        get_collection()
            getter for the collection attribute
        set_collection(coll_list)
            setter for the collection attribute
        add_image(filename)
            add an image to the collection from source
        update_image(collection_image)
            update an image in the collection, if the image doesn't
            exist, throw an exception.
    """
    # the whole field(metadata=config(field_name=...)) shenanigans are
    # there to create aliases for the attribute's name in order for the
    # JSON file generated to save metadata to take less space on the
    # user's disk.
    work_directory :    str = field(
                            metadata=config(field_name="w"), default=""
                        )
    version :           str = field(
                            metadata=config(field_name="v"), default=""
                        )
    collection:         list = field(
                            metadata=config(field_name="c"),
                            default_factory=list
                        )

    def get_collection(self):
        """getter for the collection list"""
        return self.collection


    def set_collection(self, coll_list):
        """setter for the collection list"""
        self.collection = coll_list


    def add_image(self, source):
        """ Summary
            -------
            Function to add an image to the collection

            Returns
            -------
            CollectionImage
                The image that was inserted in the collection
        """

        # get the file name, using ntpath
        file_name = ntpath.basename(source)

        # check that the file sent is of accepted format
        if not file_name.lower().endswith(
            CollectionManager.AUTHORIZED_IMAGE_FORMATS
        ):
            raise ValueError("Unauthorized file format %s" % file_name)

        # copy the file to the working directory
        # NOTE: should verify if the user is not dragging a file from
        # the working directory
        try:
            shutil.copyfile(
                source,
                os.path.join(self.work_directory, file_name)
            )
        except shutil.SameFileError as err:
            raise ValueError(
                "This image already exists in the work directory %s" %
                file_name
            ) from err

        new_image = CollectionImage(file_name)

        if new_image in self.collection:
            raise ValueError(
                "This image already exists in the collection %s" %
                file_name
            )

        self.collection.append(new_image)

        return new_image


    def update_image(self, collection_image):
        """ Summary
            -------
            update an image in the collection, if the image doesn't
            exist, throw an exception.

            Arguments
            ---------
            collection_image: CollectionImage
                the image to update
            Raises
            ------
            Exception
                If the image to update doesn't exist in the collectin
        """
        if collection_image not in self.collection:
            raise Exception("Cannot update an image that doesn't exist in the collection.")
        for idx, image in enumerate(self.collection):
            if collection_image == image:
                self.collection[idx] = collection_image


    def get_absolute_path(self, collection_image):
        """ Summary
            -------
            Gives the absolute path to an image.

            Parameters
            ----------
            collection_image: CollectionImage
                an image

            Returns
            -------
            absolute_path: str
                absolute path to the image file
        """
        if not isinstance(collection_image, CollectionImage):
            raise ValueError("collection_image must be of type CollectionImage")

        return os.path.join(self.work_directory, collection_image.filename)

### end class Collection


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
        to_reference()
            generates a reference string (legend)

        NOTE
        ----
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
    """
    # the whole field(metadata=config(field_name=...)) shenanigans are
    # there to create aliases for the attribute's name in order for the
    # JSON file generated to save metadata to take less space on the
    # user's disk.
    filename :              str = field(metadata=config(field_name="f"))
    title :                 Optional[str] = field(
                                metadata=config(field_name="t"), default=""
                            )
    artist :                Optional[str] = field(
                                metadata=config(field_name="a"), default=""
                            )
    datation :              Optional[str] = field(
                                metadata=config(field_name="d"), default=""
                            )
    technique :             Optional[str] = field(
                                metadata=config(field_name="e"), default=""
                            )
    material :              Optional[str] = field(
                                metadata=config(field_name="m"), default=""
                            )
    conservation_site :     Optional[str] = field(
                                metadata=config(field_name="c"), default=""
                            )
    production_site :       Optional[str] = field(
                                metadata=config(field_name="p"), default=""
                            )
    dimensions :            Optional[str] = field(
                                metadata=config(field_name="x"), default=""
                            )
    notes:                  Optional[str] = field(
                                metadata=config(field_name="n"), default=""
                            )

    def to_reference(self):
        """ Formats the image metadata according to the guidelines at :
            https://www.unil.ch/files/live/sites/hart/files/shared/Espace_Etudiants/GPS_Guide_du_proseminaire.pdf

            NOTE
            ----
            Maybe allow for using different formattings ?
            This code assumes all fields are filled correctly
        """

        reference = "{artist_if_artist}{title}{production_site_if_no_artist}"\
            "{date}{technique}{dimensions}{conservation_site}".format(
            artist_if_artist = self.artist + ", " if self.artist else "",
            title = self.title + ", " if self.title else "Untitled,",
            production_site_if_no_artist = self.production_site + ", " if not self.artist else "",
            date = self.datation + ", " if self.datation else "",
            technique = self.technique + ", " if self.technique else "",
            dimensions = self.dimensions + ", " if self.dimensions else "",
            conservation_site = self.conservation_site
        )

        return reference


    def __eq__(self, other):
        """ overloads the == operator so that two CollectionImages with
            the same filename are considered the same image.
        """
        return self.filename == other.filename

### end class CollectionImage


class CollectionUtils():
    """ Summary
        -------
        A static class regrouping a bunch of utility methods regarding
        Collections

        Methods
        -------
        filter(img_list, mode="any", **kwargs)
            Filters a list of CollectionImages based on metadata
        sort(img_list, attribute)
            Sorts the images in a list of CollectionImages
    """

    @staticmethod
    def filter(img_list, mode="any", **kwargs):
        """ Summary
            -------
            Filters a list of CollectionImages based on metadata

            Arguments
            ---------
            img_list : list(CollectionImage)
                A list of CollectionImages to filter.
            mode : str, default='any'
                Selection method for the filter. Either 'any' or 'all'.
                It's basically an OR/AND operator between the specified
                fields.
                (e.g. any: artist OR title must match; all: artist
                AND title must match)
            kwargs:
                Any attribute of CollectionImage (multiple allowed)

            Returns
            -------
            filtered_list : list(CollectionImages)
                List filtered according to the given parameters

            Examples
            --------
            filtered_collection = collection.filter(
                mode="all",
                title="Mona Lisa", artist="Leonard"
            )

            TODO
            ----
            Add a proper method for filtering by datation, such as "get
            all artworks in a range of dates (e.g. 1000-1200)"
        """
        # type check our list
        if not all(isinstance(i, CollectionImage) for i in img_list):
            raise TypeError(
                "All elements of img_list must be of type CollecitionImage"
            )

        # check that the mode chosen is valid
        if mode not in ("any", "all"):
            raise ValueError("mode must be either 'any' or 'all'")

        # check that the fields entered are valid CollectionImage fields
        for attr in kwargs:
            if not hasattr(CollectionImage, attr):
                raise ValueError("CollectionImage has no attribute %s" % attr)

        # for each image in the collection, retain if at least one of
        # the arguments matches (with the in keyword)
        # Here it is better for performance and readability to use a
        # list comprehension instead of filter()
        # ...but not for debugging though...
        return [
            # for each image in the collection
            image for image in img_list
            # this wizardry in the line below allows for using either
            # the 'any' or 'all' python builtins from name
            if getattr(builtins, mode)(
                # retain if any/all arguments matches
                # (with the in keyword)
                [
                    # check if the value we're looking for is in this
                    # image's value (accent and case insensitive)...
                    unidecode(value).lower() in unidecode(getattr(image, attr)).lower()
                    # ...for each attribute we're filtering for...
                    for attr, value in kwargs.items()
                    # ...but only if the value we're filtering with is
                    # not empty, and the attribute is filled in the
                    # current image
                    # TODO: find out why an image with an empty field is
                    # retained when I specifically try to prevent it
                    # here...
                    if value.strip() != "" and getattr(image, attr) != ""
                ]
            )
        ]


    @classmethod
    def sort(cls, img_list, attribute, reverse=False):
        """ Summary
            -------
            Sorts the images in a list of CollectionImages

            Arguments
            ---------
            img_list: list(CollectionImage)
                A list of CollectionImage
            attribute: str
                Any attribute of Collection image
            reverse: bool, default=False
                reverse the sorting

            Returns
            -------
            sorted_collection : list(CollectionImage)
                sorted collection

            Notes
            -----
            Does it make sense to sort by multiple arguments ? If so,
            how does one do it ?
        """
        # type check our list
        if not all(isinstance(i, CollectionImage) for i in img_list):
            raise TypeError(
                "All elements of img_list must be of type CollecitionImage"
            )

        # check that the argument is valid
        if not hasattr(CollectionImage, attribute):
            raise ValueError("CollectionImage has no attribute %s" % attribute)

        # special case with dates
        if attribute == "datation":
            # return the list sorted by estimated numeric value of
            # datation string
            return sorted(
                img_list,
                key=lambda i: cls._datation_to_numeric(getattr(i, attribute)),
                reverse=reverse
            )

        # return the list sorted by the chosen criterion
        return sorted(
            img_list,
            key=lambda i: getattr(i, attribute).lower(),
            reverse=reverse
        )

    @classmethod
    def _datation_to_numeric(cls, datation_string):
        """ Summary
            -------
            Tries to estimate a numeric year value for datation strings
            for example:
            c. 1060 -> 1060
            IIè siècle av. j.-c. -> -200
            II-IIIè -> 100
            c. 1667-1668 -> 1667
            1666-8 -> 1666
            3-4ème siècle -> 200
            1667 -> 1667

            Notations:
            AP/AD can apply to all notations
            Estimated datation: 2 values given, centuries or years
                centuries: possible roman numerals
                    Note this little complication:
                           IIe s. AD -> 100
                           IIe s. AP -> -200
                year: no processing

            Returns
            -------
            int
                The estimated value of the input string. Returns 0 if
                nothing could be found
            Notes
            -----
            We could make it so that when we have two values, return the
            average of the two...

            TODO
            ----
            Implement management of quarter and half of century
            precisions:
                "2ème partie/moitié du IIème siècle" -> 150
                "3ème quart du XXème siècle" -> 1975
                "1er quart du 19ème siècle" -> 1800
                etc.
        """
        # detect AP/AD
        # NOTE: IN FRENCH !
        apad_regex = re.compile(
            r"((av\.?(ant)?)|(ap\.?(r[eè]s)?))\s?j\.?-?c\.?",
            flags=re.IGNORECASE
        )

        # detect numeric values (case sensitive)
        num_values = re.compile(r"\b[IVX]+|\b\d+")

        # detect if values are given in centuries
        century = re.compile(
            r"(\bsi[eè]cles?\b)|(\bs\.?\b)",
            flags=re.IGNORECASE
        )

        apad = 1

        # get AP/AD
        # AP -> negative number, AD -> positive number
        if re.search(apad_regex, datation_string):
            # check wether it is AP or AD
            apad = 1 if re.search(r"ap(?:r[eè]s)", datation_string) else -1

        values = list()

        # get all numeric values given in the string
        matches = re.findall(num_values, datation_string)
        if len(matches) > 0:
            # for each value
            for value in matches:
                # translate to int
                if re.match(r"[IVX]+", value):
                    values.append(cls._roman_to_int(value))
                else:
                    values.append(int(value))

        # check if the values are given in centuries
        if re.search(century, datation_string):
            # multiply each value by 100 (as each digit means a century)
            values = [i * 100 if apad == -1 else (i - 1) * 100 for i in values]

        # this is in case nothing was found
        if len(values) == 0:
            return 0

        # here we add the sign indicated by AP/AD
        return values[0] * apad

    @classmethod
    def _roman_to_int(cls, roman_numeral):
        """ Summary
            -------
            Converts roman numerals to int
            Entirely taken from :
            https://www.tutorialspoint.com/roman-to-integer-in-python

            Arguments
            ---------
            roman_numeral : str
                string of roman numerals (eg. 'XIII')

            Returns
            -------
            int
                decimal value of the roman numeral
        """
        roman = {
            'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,
            'IX':9,'XL':40,'XC':90,'CD':400,'CM':900
        }

        i = 0
        num = 0
        while i < len(roman_numeral):
            if i+1<len(roman_numeral) and roman_numeral[i:i+2] in roman:
                num+=roman[roman_numeral[i:i+2]]
                i+=2
            else:
                num+=roman[roman_numeral[i]]
                i+=1
        return num

### end class CollectionUtils
