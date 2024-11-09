#!/usr/bin/python3
"""city module."""
from models.base_model import BaseModel

class City(BaseModel):
	"""class blue print
	Inherits from the BaseModel class"""
	
	state_id = ""
	name = ""
	
	def __init__(self, *args, **kwargs):
		"""init city"""
		super().__init__(*args, kwargs)

