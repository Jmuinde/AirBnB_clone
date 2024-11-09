#!/usr/bin/python3
""" The console module.
"""
import cmd 
import os
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review

classes = {"BaseModel": BaseModel, "User": User, "State": State, "Amenity": Amenity, 
		"City": City, "Place" : Place, "Review" : Review}


class HBNBCommand(cmd.Cmd):
	"""The class blueprint.
	inherits from the cmd module"""

	prompt = '(hbnb) '

	# Methods
	def do_clear(self, line):
		"""clears the console screen."""
		 
		# For windows 
		if os.name == 'nt':
			_ = os.system('cls')

		# for Unix/Linux/Mac
		else:
			_ = os.system('clear')

	def do_quit(self, line):
		"""command to exit the program"""
		return True

	def do_EOF(self, line):
		"""Exit the program"""
		return True

	def emptyline(self):
		"""Handles empty input; overrides to do nothing."""
		return False

	def do_create(self, arg):
		"""Creates a new class instance"""
		arguments = arg.split()
		if len(arguments) == 0:
			print("** class name missing **")
			return False
		if arguments[0] in classes:
			object = classes[arguments[0]]() # Create a new instance of the specified class
		else:
			print("** class doesn't exist **")
			return False
		print(object.id)
		object.save()

	def do_show(self, arg):
		"""Prints the string representation of an insatnce
		based on the class name and id"""
		arguments = arg.split()
		# check if the class name is provided.
		if len(arguments) == 0:
			print(" ** class name missing **")
			return False
		# check if class name provided dose exist
		if arguments[0] not in classes:
			print(" ** class doesn't exist **")
			return False

		# check if instance id is missing 
		if len(arguments) < 2:
			print(" ** insatnce id missing **")
			return False

		# check if the insatnce exists in storage
		instance_key = f"{arguments[0]}.{arguments[1]}"
		if instance_key in models.storage.all():
			print(models.storage.all()[instance_key])

		else:
			print(" ** no instance found **")

	def do_destroy(self, arg):
		"""Deletes an instance based on the class name and id"""
		arguments = arg.split()
		
		# check if the class name is missing 
		if len(arguments) == 0:
			print(" ** class name missing **")
			return False
		# Check if class name provided exists
		if arguments[0] not in classes:
			print(" ** class doesn't exist **")
			return False
		# check if argument id is present
		if len(arguments) < 2:
			print(" ** instance id is missing **")
			return False
		# check if the instance exists in storage 
		instance_key = f"{arguments[0]}.{arguments[1]}"

		# delete instance if present in storage
		if instance_key in models.storage.all():
			del models.storage.all()[instance_key]
			models.storage.save()
		else:
			print(" ** no instance found **")
	
	def do_all(self, arg):
		"""Prints instance representation of all or base on class name"""
		arguments = arg.split()
		
		if len(arguments) > 0:
			class_name = arguments[0]
			if class_name not in classes:
				print("** class doesn't exist **")
				return False

		objects = models.storage.all()
		all_instances = []

		if len(arguments) > 0 :
			all_instances = [str(obj) for key, obj in objects.items() if key.startswith(class_name)]
		else:
			all_instances = [str(obj) for obj in objects.values()]
		print(all_instances)

	
	def do_update(self, arg):
		"""Updates an instance based on class name and id. 
		Updates and attribute or adds one if it does not exist"""
		arguments = arg.split()
		
		# Restrict multiple updating/ addition of attribute at ones
		if len(arguments) > 4:
			print("** only one attribute can be updated at a time **")
			return False
		
		# Check if class name is missing
		if len(arguments) == 0:
			print("** class name missing **")
			return False


		# Check if class name doesn't exist
		if arguments[0] not in classes:
			print(" ** class doesn't exist ** ")
			return False
		# Check if id is missing
		if len(arguments) < 2: 
			print(" ** instance id missing ** ")
			return False
		# construct the instance key
		instance_key = f"{arguments[0]}.{arguments[1]}"
		# check if instance does exists
		if instance_key not in models.storage.all():
			print("** no instance found **")
			return False

		# check if attribute name is provided
		if len(arguments) < 3:
			print("** attribute name missing **")
			return False
		# check if attribute value is provided
		if len(arguments) < 4:
			print("** value missing **")
			return False

		#Retrieve the object from storage
		obj = models.storage.all()[instance_key]

		# Extract attribute name and value
		attribute_name = arguments[2]
		attribute_value = arguments[3]

		# Skipe restricted attributes
		if attribute_name in ["id", "created_at", "updated_at"]:
			print("** restricted attribute **")
			return False

		# Ensure attribute type cassting is applicable
		if hasattr(obj, attribute_name):
			attr_type = type(getattr(obj, attribute_name))
			try:
				attribute_value = attr_type(attribute_value) # Try to cast new value to the type exisitign
			except (ValueError, TypeError):
				# if casting fails, stores the new value as is 
				pass
		else:
			attribute_value = str(attribute_value) # if attribute does not exist store a string by defult
		# Set the attribute and save object
		setattr(obj, attribute_name, attribute_value)
		obj.save()
	
	def default(self, line):
		"""Handel <class name>.all() and other commands."""
		if "." in line:
			class_name, command = line.split(".", 1)
			if command == "all()":
				self.do_all(class_name)

		# Handle <class_name>.count()
			elif command == "count()":
				if class_name in classes:
				# count instances of the specified class
					count = sum(1 for key in models.storage.all() if key.startswith(class_name + "."))
					print(count)
				else:
					print(f"** class doesn't exist **")
			# Handle <class_name>.show(<id>)
			elif command.startswith("show(") and command.endswith(")"):
				if class_name not in classes:
					print("** class doesn't exist **")
					return False
				# Extract the ID between parentheses
				instance_id = command[5:-1].strip("\"'")
				# Pass parsed arguments to do_show
				self.do_show(f"{class_name} {instance_id}")
		
			# Handle <class_name>.destroy(id)

			elif command.startswith("destroy(") and command.endswith(")"):
				if class_name not in classes:
					print("** class doesn't exist **")
					return False
				# Extract the ID between parenthesis
				instance_id = command[8:-1].strip("\"'")
				self.do_destroy(f"{class_name} {instance_id}")

			# Handle <class_name>.update(<id>, <attribute name>, <attribute value>)
			elif command.startswith("update(") and command.endswith(")"):
				if class_name not in classes:
					print("** class doesn't exist **")
					return False

			# Extract the arguments within the parenthesis			
				args = command[7: -1].split(", ")
			# Debug: print the extracted arguments
				print(f"Debug - Extracted args: {args}")
			
				if len(args) < 3:
					print("** attribute name missing **" if len(args) == 1 else "** value missing **")
					return False
			# Handle quotes in the arguments 
				instance_id = args[0].strip("\"'")
				attr_name = args[1].strip("\"'")
				attr_value = args[2].strip("\"'")
				
			# Debug: print the parsed command arguments
				print(f"Debug: class_name={class_name},instance_id={instance_id}, attr_name={attr_name},attr_value={attr_value}")

			# Pass parsed arguments to do_update
				self.do_update(f"{class_name} {instance_id} {attr_name} {attr_value}")
			else:
				print("*** Unkown syntax: {line}")

		else:
			print(f"*** Unknown syntax: {line}")
				

if __name__ == '__main__':
	"""Ensures that the program only runs when
	called by name"""
	HBNBCommand().cmdloop()

