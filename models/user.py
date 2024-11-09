#!/usr/bin/python3
"""user module."""

from models.base_model import BaseModel

class User(BaseModel):
	"""Blue print of the user class.
	Inherits from the BaseModel class"""

	# public class atributes
	email = ""
	password = ""
	first_name = ""
	last_name = ""
	
	def __init__(self, *args, **kwargs):
		"""initialize the user class"""
		super().__init__(*args, **kwargs) #calls methods from the BaseModel class
	

