#pylint: disable=invalid-name
"""
    Collection module
    -----------------
    Handles the datastructure of a collection
"""
import ntpath
import os
import shutil
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


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
    work_directory :    str
    version :           str
    collection:         list = field(default_factory=list)

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

        from api.CollectionImage import CollectionImage
        from api.CollectionUtils import CollectionUtils

        # get the file name, using ntpath
        file_name = ntpath.basename(source)

        # check that the file sent is of accepted format
        if not file_name.lower().endswith(
            CollectionUtils.AUTHORIZED_IMAGE_FORMATS
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
            raise ValueError(
                "Cannot update an image that doesn't exist in the collection."
            )

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
        from api.CollectionImage import CollectionImage
        if not isinstance(collection_image, CollectionImage):
            raise ValueError(
                "collection_image must be of type CollectionImage"
            )

        return os.path.join(self.work_directory, collection_image.filename)
