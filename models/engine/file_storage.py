#!/usr/bin/python3
"""FileStorage module for storing objects in JSON format."""

import json


class FileStorage:
    """A class for storing objects in JSON format."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Get all stored objects.

        Returns:
            dict: A dictionary containing all stored objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to the storage.

        Args:
            obj: The object to be added.
        """
        key = f"{type(obj).__name__}.{obj.id}"
        self.all()[key] = obj

    def save(self):
        """Save objects to the JSON file"""
        json_dict = {}
        for key, value in self.all().items():
            json_dict[key] = value.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(json_dict, file, indent=4)

    def reload(self):
        """Reload objects from the JSON file if it exists."""
        from models.base_model import BaseModel
        from models.user import User
        from models.amenity import Amenity
        from models.city import City
        from models.state import State
        from models.review import Review
        from models.place import Place

        try:
            with open(self.__file_path, "r", encoding="utf-8") as fp:
                json_dict = json.load(fp)
        except Exception:
            return
        for key, value in json_dict.items():
            self.all()[key] = eval(key.split(".")[0])(**value)
