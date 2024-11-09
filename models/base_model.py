#!/usr/bin/env python3
"""The BaseModel module.
Creates the basemodel class from which other classes
in the project will inherit"""

import models
import uuid
from datetime import datetime

class BaseModel:
    """Blueprint of the base class model"""
    def __init__(self, *args, **kwargs):
        """Initialization of the class using dictionary
        attributes if given."""
        # check if kwargs is not empty
        if kwargs:
            for key, value in kwargs.items():
                # ignore __class__ attribute
                if key == "__class__":
                    continue
                # convert created_at and updated_at to string objects
                if key in ("created_at", "updated_at") and isinstance(value, str):
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Method to return a string representation
        of the instance"""
        return f"[{self.__class__.__name__}] ({self.id} {self.__dict__}"

    def save(self):
        """Method to update the updated_at attribute with
        the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Method to return a dictionary of the instance
        created
        """
        return {
            **self.__dict__,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }


