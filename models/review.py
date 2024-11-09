#!/usr/bin/python3

from models.base_model import BaseModel

class Review(BaseModel):
	"""Blue print of the review class.
	Inherits from the BaseModel"""
	
	# public class attributes
	place_id = ""
	user_id = ""
	text = ""
	
	def __init__(self, *args, **kwargs):
		"""init review"""
		super().__init__(*args, **kwargs)
