#!/usr/bin/python3
"""amenity module."""
from models.base_model import BaseModel

class Amenity(BaseModel):
        """Blue print of amenity class.
        Inherits from the BaseModel class"""

        # public insatnce
        name = ""

        def __init__(self, *args, **kwargs):
                """init amenity"""
                super().__init__(*args, **kwargs)
