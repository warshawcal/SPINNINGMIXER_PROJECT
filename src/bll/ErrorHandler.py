import traceback
import os
import glob
import sys

class ErrorHandlerContext:

	def __init__(self, debug_mode, function_name):
		self.debug_mode = debug_mode
		self.function_name = function_name

	def __enter__(self):
		self.log = None

	def __exit__(self,exc_type,exc_value,traceback_):

		# exc_lines = traceback.format_exc().split("\n")
		# try:
		# 	punchline = exc_lines[-2]
		# except:
		# 	punchline = None

		# if self.debug_mode:
		# 	print("\n\n EXIT FUNCTION IN ERROR HANDLER PINGED")
		# 	print(str(exc_type).strip())
		# 	print(str(type(exc_type)).strip())

		# if (exc_type is None and exc_value is None and traceback_ is None):
		# 	return

		# if str(exc_type).strip() == "<class 'SystemExit'>":
		# 	print("\n\n SystemExit Detected.\n\n")
		# 	### DO STUFF ###
		# 	return
			
		# if str(punchline).strip() == "KeyboardInterrupt":
		# 	print("\n\n SIGKILL Detected.\n\n")
		# 	### DO STUFF ###
		# 	sys.exit()
		# 	return

		# else:

		exc_lines = traceback.format_exc().split("\n")
		try:
			punchline = exc_lines[-2]
		except:
			punchline = None

		if self.debug_mode:
			print("\n\n JARVIS ERROR DETECTED: " + \
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