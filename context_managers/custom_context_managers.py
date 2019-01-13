"""
Book: Clean code in python.
Chapter: Context managers, p30.
"""
import contextlib


# 1st Option: Using __enter__, __exit__ magic methods
class CustomContextManager:
	def __init__(self):
		self.returned_object = 3

	def __enter__(self):
		print("Executing preconditions")
		# Return statement is optional. Use it only if you need to
		# use the returned_object inside the with block.
		return self.returned_object

	def __exit__(self, exc_type, ex_value, ex_traceback):
		print("Executing postconditions")

with CustomContextManager() as returned_object:
	print(f"This is the object returned by __enter__: {returned_object}")


# 2nd Option: Using contextlib.contextmanager decorator
@contextlib.contextmanager
def CustomContextManager():
	print("Executing preconditions")
	returned_object = 3
	# Same as before, yielding a specific value is optional. Use it only
	# if you need to use the returned_object inside the with block.
	yield returned_object
	print("Executing postconditions")

with CustomContextManager() as returned_object:
	print(f"This is the object returned by __enter__: {returned_object}")


# 3rd Option: Using contextlib.ContextDecorator
# This method doesn't support the with statement so use it only if
# you don't need to access the returned_object in the context manager.
class CustomContextManager(contextlib.ContextDecorator):
	def __enter__(self):
		print("Executing preconditions")

	def __exit__(self, exc_type, ex_value, ex_traceback):
		print("Executing postconditions")

@CustomContextManager()
def decorated_function():
	print("There is no returned_object object")

decorated_function()
