""" Collection module
    Handles the datastructure of a collection, and saving and loading of
    metadata in a project folder.
"""
import os
import json
import ntpath
import shutil
import builtins
from typing import Optional
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


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
    META_FILENAME = ".collection"

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
        if cls.META_FILENAME in os.listdir(path):
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


    @classmethod
    def __load_meta(cls, path):
        """ Summary
            -------
            Deserializes the data from the meta file and updates the
            collection

            NOTE
            ----
            I'm sure there's a better way to do this...
        """
        with open(os.path.join(path, cls.META_FILENAME), "r") as meta:
            coll_json = meta.read()
            coll_dict = json.loads(coll_json)

        # retrieve the title of the collection
        title = coll_dict["title"]

        # retrieve the collection list
        collection = [
            # cast each object in the JSON list to a CollectionImage
            # pylint says it's an error. Let's just say I disagree
            CollectionImage.from_dict(item) for item in coll_dict["collection"]
        ]

        return Collection(path, title, collection)


    @classmethod
    def __check_files(cls, collection):
        """ Runs through the files in the work directory and adds any
            image that is not yet in our collection.

            Returns
            -------
            checked_collection : Collection
                corrected collection (if new files are detected, they
                will be added to the collection, and the updated
                collection is returned)
        """
        # type safety check
        if not isinstance(collection, Collection):
            raise ValueError("collection must be of type Collection, not %s"
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
            raise ValueError(
                "collection must be of type Collection, not %s"
                % type(collection)
            )

        meta_file_path = os.path.join(
            collection.work_directory,
            cls.META_FILENAME
        )

        # create metadata file in the project directory
        with open(meta_file_path, "w") as meta_file:
            # convert the collection to JSON
            json_data = json.loads(collection.to_json())
            # format JSON file (temporary)
            formatted_json = json.dumps(json_data, indent=4)

            meta_file.write(formatted_json)


    @classmethod
    def __create_meta(cls, path):
        path = os.path.join(path, cls.META_FILENAME)
        open(path, "a").close()


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
    """
    work_directory : str
    title : str
    collection: list = field(default_factory=list)

    def get_collection(self):
        """getter for the collection list"""
        return self.collection


    def set_collection(self, coll_list):
        """setter for the collection list"""
        self.collection = coll_list
        CollectionManager.save(self)


    def add_image(self, source):
        """ Summary
            -------
            Function to add an image to the collection

            Returns
            -------
            CollectionImage
                The image that was inserted in the collection
        """
        # cleaning the input if necessary (format <b'path/to/file'>
        # coming from ArtyApp._on_file_drop())
        source = str(source.decode('utf-8'))
        if source.startswith("b'") and source.endswith("'"):
            source = source[2:-1]

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
            shutil.copyfile(source, os.path.join(self.work_directory, file_name))
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
        CollectionManager.save(self)

        return new_image


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


    def filter(self, mode="any", **kwargs):
        """ Summary
            -------
            Filters a collection based on metadata

            Arguments
            ---------
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

            Example
            -------
            filtered_collection = collection.filter(mode="all", title="Mona Lisa", artist="Leonard")
        """

        # check that the mode chosen is valid
        if mode not in ("any", "all"):
            raise ValueError("mode must be either 'any' or 'all'")

        # check that the fields entered are valid CollectionImage fields
        for attr in kwargs:
            if not hasattr(CollectionImage, attr):
                raise ValueError("CollectionImage has no attribute %s" % attr)

        # for each image in the collection, retain if at least one of
        # the arguments matches (with the in keyword)
        # Here it is better for performance and readability to use list
        # comprehensions instead of filter
        return [
            # for each image in the collection
            i for i in self.collection

            # this wizardry in the line below allows for using either
            # the 'any' or 'all' python builtins from name
            if getattr(builtins, mode)(
                #retain if any/all arguments matches (with the in keyword)
                [
                    # check if the value we're looking for is in this
                    # image's value (case insensitive)...
                    value.lower() in i.__getattribute__(attr).lower()
                    # ...for each attribute we're filtering for...
                    for attr, value in kwargs.items()
                    # ...but only if the attribute is filled in the
                    # current image
                    if i.__getattribute__(attr)
                ]
            )
        ]


    def sort(self, attribute, reverse=False):
        """ Summary
            -------
            Sorts the images in a collection.

            Arguments
            ---------
            attribute: str
                Any attribute of Collection image
            reverse: bool, default=False
                reverse the sorting

            Returns
            -------
            sorted_collection : list(CollectionImage)
                sorted collection

            NOTE
            ----
            Does it make sense to sort by multiple arguments ? If so,
            how does one do it ?
            Doesn't really work for dates though (if there are cases
            such as "c. 525" or "IIe siècle"). But the only solution to
            this, while allowing freedom for the user would be to create
            a whole processing engine to convert those notations to
            homogenous numeric values that we could then sort.
        """

        # check that the argument is valid
        if not hasattr(CollectionImage, attribute):
            raise ValueError("CollectionImage has no attribute %s" % attribute)

        # return the list sorted by the chosen criterion
        return sorted(
            self.collection,
            key=lambda i: i.__getattribute__(attribute),
            reverse=reverse
        )


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
            relative path to the file (eg. "image.png").
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
        user_notes : str, optional
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
        - Date format to discuss.
        - Other fields ?
        - Tag system ?
    """

    filename :              str
    title :                 Optional[str] = None
    artist :                Optional[str] = None
    year :                  Optional[str] = None
    technique :             Optional[str] = None
    conservation_site :     Optional[str] = None
    production_site :       Optional[str] = None
    dimensions :            Optional[str] = None
    user_notes:             Optional[str] = None

    def to_reference(self):
        """ Formats the image metadata according to the guidelines at :
            https://www.unil.ch/files/live/sites/hart/files/shared
            /Espace_Etudiants/GPS_Guide_du_proseminaire.pdf

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
            date = self.year + ", " if self.year else "",
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
