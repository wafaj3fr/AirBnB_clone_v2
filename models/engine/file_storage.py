#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                    print(cls)
                except Exception as ex:
                    print('cls not valid: ', ex)
            cls_dict = {}
            for k, v in self.__objects.items():
                if cls == type(v)::
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        temp = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
                for key in jo.items():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**key))
        except FileNotFoundError:
            pass
        
    def delete(self, obj=None):
        """ Deletes obj from objects if it's inside """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except(AttributeError, KeyError):
            pass

    def close(self):
        """calls reload() to deserialize json file to objects"""
        self.reload()
