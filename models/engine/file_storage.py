#!/usr/bin/env python3
"""File storage module."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


class FileStorage:
    """Blueprint of the filestorage class.
    Handles the serialization and deserialization of instances to
    and from JSON file."""
    """class attributes"""

    # path to the json file for storage
    __file_path = "file.json"
    # Dict to store all objects in memory
    __objects = {}

    # Methods
    def all(self):
        """Returns the dictionary __objects
        containing all instances"""
        return FileStorage.__objects

    def new(self, obj):
        """
        To set a new object in __object
        with <obj class name>.id.
        :param obj:
        :return:
        """
        class_name = type(obj).__name__
        obj_id = obj.id
        key = f"{class_name}.{obj_id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serialize the __object to json file and
        store in the __file_path
        :return:
        """
        new_obj_dict = {}
        for key, obj in FileStorage.__objects.items():
            new_obj_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(new_obj_dict, f)

    def reload(self):
        """Deserialization of the JSON file back to objects"""
        try:
            with open(FileStorage.__file_path, 'r', encoding="UTF-8") as f:
                object_load = json.load(f)
                new_obj_dict = {}
                for key, dict_obj in object_load.items():
                    class_name = key.split(".")[0]
                    obj = eval(class_name)(**dict_obj)
                    new_obj_dict[key] = obj
                FileStorage.__objects = new_obj_dict
        except FileNotFoundError:
            pass

