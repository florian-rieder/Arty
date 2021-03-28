""" Collection module
    Handles the saving and loading of metadata in a project folder
"""

import os
import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from CollectionImage import CollectionImage


AUTHORIZED_IMAGE_FORMATS = (".jpg", ".jpeg", ".png", ".webp", ".tiff")
META_FILENAME = ".collection"


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
        title : str
            User entered name for the collection
        working_directory : str
            path to this collection's directory
        collection : list(CollectionImage)
            list of the images in the collection

        Methods
        -------
        __post_init__()
        __initialize_collection()
        __write_meta()
        __load_meta()
    """
    title : str
    work_directory : str
    # ignore collection from dataclass __init__, we are going to
    # initialize it in the __post_init__ method.
    collection: list = field(default_factory=list, init=False)


    def __post_init__(self):
        """
        Summary
        -------
        Runs right after the __init__ function (handled by dataclass)

        Raises
        ------
        FileNotFoundError
            if the collection's work directory is not found
        """
        # check if the path given is valid
        if not os.listdir(self.work_directory):
            raise FileNotFoundError

        # check if there is already a project file in this directory
        if META_FILENAME in os.listdir(self.work_directory):
            self.__load_meta()
        else:
            self.__create_meta()

        # check the images in the directory and update the collection
        # and meta
        self.__check_files()
        self.__write_meta()


    def __load_meta(self):
        """ Deserializes the data from the meta file and updates the
        collection

        Notes
        -----
        In the current state of things, this throws the warning:

            RuntimeWarning: `NoneType` object value of non-optional
            type < all CollectionImage attributes > detected when
            decoding CollectionImage.

        There's probably stuff to study about dataclasses_json but
        for now it just works. Perhaps it has to do with the fact
        that for now most of them are None...
        """
        with open(os.path.join(self.work_directory, META_FILENAME), "r") as meta:
            coll_json = meta.read()
            coll_dict = json.loads(coll_json)

        self.title = coll_dict["title"]
        self.collection = [
            CollectionImage.from_dict(item) for item in coll_dict["collection"]
        ]


    def __check_files(self):
        """ Runs through the files in the work directory and adds any
            image that is not yet in our collection.
        """
        for filename in os.listdir(self.work_directory):
            # reject all files with the wrong extension (case
            # insensitive)
            if filename.lower().endswith(AUTHORIZED_IMAGE_FORMATS):
                new_image = CollectionImage(filename)

                # this works since we overloaded the equal operator in
                # CollectionImage !
                if new_image not in self.collection:
                    # add the new image
                    self.collection.append(new_image)


    def __write_meta(self):
        """ Serializes this collection and saves it in the project meta
            file in the work directory
        """
        # create metadata file in the project directory
        meta_file_path = os.path.join(self.work_directory, META_FILENAME)
        with open(meta_file_path, "w") as meta_file:
            json_data = json.loads(self.to_json())
            formatted_json = json.dumps(json_data, indent=4)
            meta_file.write(formatted_json)
    
    def __create_meta(self):
        path = os.path.join(self.work_directory, META_FILENAME)
        open(path, "a").close()
    
    def get_collection(self):
        return self.collection
    
    def set_collection(self, coll_list):
        self.collection = coll_list
        self.__write_meta()


if __name__ == "__main__":
    coll = Collection("test", "/Users/frieder/Documents/images")
    print(coll)
