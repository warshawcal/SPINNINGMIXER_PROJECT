import traceback
import os
import glob
import sys

"""
This file is to create an error_handler decorator that we can wrap around all of our functions
instead of adding try/except blocks all over the place.
"""
class ErrorHandlerContext:

	def __init__(self, debug_mode, function_name):
		self.debug_mode = debug_mode
		self.function_name = function_name

	def __enter__(self):
		self.log = None

	def __exit__(self,exc_type,exc_value,traceback_):

		exc_lines = traceback.format_exc().split("\n")
		try:
			punchline = exc_lines[-2]
		except:
			punchline = None

		if (exc_type is None and exc_value is None and traceback_ is None):
			return

		elif str(exc_type).strip() == "<class 'SystemExit'>":
			if self.debug_mode:
				print("\n\n SystemExit Detected.\n\n")
			### DO STUFF ###
			return
			
		elif str(punchline).strip() == "KeyboardInterrupt":
			if self.debug_mode: 
				print("\n\n SIGKILL Detected.\n\n")
			### DO STUFF ###
			return

		else:
			if self.debug_mode:
					print("\n\n JARVIS ERROR HANDLER REPORT: " + \
						" \n\nFUNCTION: "  + "\n"  + str(self.function_name)+ \
						" \n\nEXC TYPE: "  + "\n"  + str(exc_type) 			+ \
						" \n\nEXC VALUE: " + "\n"  + str(exc_value) 		+ \
						" \n\nPUNCHLINE: " + "\n"  + str(punchline) 		+ \
						" \n\nERROR TRACEBACK: "   + "\n" + str(traceback_)   )
		return

def error_handler(debug_mode,function_name):
	# https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator
	def actual_decorator(f):
		def wrapper(*args, **kwargs):
			with ErrorHandlerContext(debug_mode, function_name) as context:
				return f(*args, **kwargs)
		return wrapper
	return actual_decorator

#EOF