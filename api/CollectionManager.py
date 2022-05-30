import json
import os

from kivy.logger import Logger

from api.Collection import Collection
from api.CollectionImage import CollectionImage
from api.CollectionUtils import CollectionUtils


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

    META_EXTENSION = ".arty"

    ### IMPORTANT
    # When doing changes to the .arty file :
    # Change the version number
    VERSION = "Alpha-1.1"
    # By the way, I don't think using app-wide versioning nomenclature
    # in here is the best idea. We should go back to something separate
    # from app versioning.

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
        Logger.info("Collection: Collection loaded")

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
        Logger.info("Collection: Collection saved")


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

        try:
            version = coll_dict["version"]
        except KeyError:
            version = coll_dict["v"]

        if version == "Alpha-1.0":
            # upgrade the save file to the next version

            # rename a key :
            # mydict[k_new] = mydict.pop(k_old)

            # revert minification
            coll_dict["work_directory"] = coll_dict.pop("w")

            coll_dict["version"] = "Alpha-1.0.1"
            coll_dict.pop("v")

            updated_coll = list()
            for image_meta in coll_dict["c"]:
                updated_image_meta = {
                    "filename": image_meta["f"],
                    "title": image_meta["t"],
                    "artist": image_meta["a"],
                    "datation": image_meta["d"],
                    "technique": image_meta["e"],
                    "material": image_meta["m"],
                    "conservation_site": image_meta["c"],
                    "production_site": image_meta["p"],
                    "dimensions": image_meta["x"],
                    "style": image_meta["S"],
                    "source": image_meta["s"],
                    "notes": image_meta["n"],
                }
                updated_coll.append(updated_image_meta)
            
            coll_dict.pop("c")
            coll_dict["collection"] = updated_coll


        if version == "Alpha-1.0.1":
            # upgrade the save file to the next version
            pass


        # turn the dictionary back to a JSON string
        json_string = json.dumps(coll_dict)

        return json_string


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
            version = coll_dict["version"]
        except KeyError as exc:
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

        version = coll_dict["version"]

        # retrieve the collection list
        collection = [
            # cast each object in the JSON list to a CollectionImage
            # pylint: disable=no-member
            CollectionImage.from_dict(item) for item in coll_dict["collection"]
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
            if filename.lower().endswith(CollectionUtils.AUTHORIZED_IMAGE_FORMATS):
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
            #formatted_json = json.dumps(json_data, separators=(',', ':'))
            #prettified
            formatted_json = json.dumps(json_data, indent=4)

            if not formatted_json.strip():
                # prevent data from being erased
                raise RuntimeError("Tried to write an empty Collection")

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
