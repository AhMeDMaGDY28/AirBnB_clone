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
        """Save objects to the JSON file."""
        json_dict = {}
        for key, value in self.all().items():
            json_dict[key] = value.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(json_dict, file)

    def reload(self):
        """Reload objects from the JSON file if it exists."""
        from models.base_model import BaseModel
        try:
            with open(self.__file_path, "r") as fp:
                json_dict = json.load(fp)
        except Exception:
            return
        for key, value in json_dict.items():
            self.all()[key] = eval(key.split(".")[0])(**value)