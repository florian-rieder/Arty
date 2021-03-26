import os
import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


AUTHORIZED_IMAGE_FORMATS = (".jpg", ".jpeg", ".png", ".webp", ".tiff")
META_FILENAME = "collection.arty"

@dataclass_json
@dataclass
class Collection():
    title : str
    work_directory : str
    collection: list = field(default_factory=list, init=False)
    

    def __post_init__(self):
        # check if the path given is valid
        if not os.listdir(self.work_directory):
            raise FileNotFoundError
        
        self.__initialize_collection()
        self.__create_meta()
    

    def __initialize_collection(self):
        for filename in os.listdir(self.work_directory):
            # reject all files with the wrong extension
            if filename.lower().endswith(AUTHORIZED_IMAGE_FORMATS):
                self.collection.append(CollectionImage(filename))
            

    def __create_meta(self):
        # create metadata file in the project directory
        meta_file_path = os.path.join(self.work_directory, META_FILENAME)
        with open(meta_file_path, "w") as meta_file:
            json_data = json.loads(self.to_json())
            formatted_json = json.dumps(json_data, indent=4)
            meta_file.write(formatted_json)


        # make that file hidden -- doesn't work
        # st = os.stat(meta_file_path)
        # os.chflags(meta_file_path, st.st_flags ^ stat.UF_HIDDEN)
        # on windows i guess ? -- also doesn't work
        # p = os.popen('attrib +h ' + META_FILENAME)
        # p.close()

@dataclass_json
@dataclass
class CollectionImage():
        # filename is the local file name, not the path to the file
        filename : str
        title : str = None
        artist : str = None
        year : str = None
        support : str = None
        technique : str = None
        conservation_site : str = None
        

if __name__ == "__main__":
    coll = Collection("test", "/Users/frieder/Documents/images")