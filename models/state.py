#!/usr/bin/python3
"""state module."""
from models.base_model import BaseModel

class State(BaseModel):
	"""Blue print of the state class
	Inherits from the BaseModel"""
	
	# public insatnce attribute
	name = ""
	
	def __init__(self, *args, **kwargs):
		"""init state"""
		super().__init__(*args, **kwargs)
