#!/usr/bin/python3

from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
	obj = all_objs[obj_id]
	print(obj)

print("-- Create a new Amenity -- ")
my_amenity = Amenity()
my_amenity.name = "wifi"
my_amenity.save()
print(my_amenity)
