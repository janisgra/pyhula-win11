import os
import sys

# Apply Python 3.13+ compatibility patches automatically
if sys.version_info >= (3, 13):
	try:
		# Try to import and apply compatibility patches
		import struct
		import array
		
		# Store original struct.pack
		_original_pack = struct.pack
		
		def _safe_struct_pack(format_string, *values):
			"""Safe struct.pack wrapper for Python 3.13+ compatibility"""
			converted_values = []
			format_chars = format_string.replace('<', '').replace('>', '').replace('!', '').replace('=', '').replace('@', '')
			
			for i, (fmt_char, value) in enumerate(zip(format_chars, values)):
				if value is None:
					converted_values.append(0)
				elif fmt_char in 'bBhHiIlLqQ':  # Integer formats
					if isinstance(value, str):
						try:
							converted_values.append(int(value))
						except ValueError:
							converted_values.append(ord(value[0]) if value else 0)
					elif isinstance(value, float):
						converted_values.append(int(value))
					else:
						int_val = int(value)
						# Apply bounds checking for unsigned byte format
						if fmt_char == 'B' and int_val > 255:
							int_val = 255
						elif fmt_char == 'B' and int_val < 0:
							int_val = 0
						converted_values.append(int_val)
				else:
					converted_values.append(value)
			
			return _original_pack(format_string, *converted_values)
		
		# Replace struct.pack with safe version
		struct.pack = _safe_struct_pack
		
		# Apply array.fromstring compatibility patch
		if not hasattr(array.array, 'fromstring'):
			_original_array = array.array
			
			class _CompatibleArray(_original_array):
				"""Array class with fromstring() compatibility for Python 3.13"""
				
				def fromstring(self, s):
					"""Compatibility method for array.fromstring()"""
					if isinstance(s, str):
						s = s.encode('latin-1')
					return self.frombytes(s)
			
			array.array = _CompatibleArray
		
	except Exception:
		# Silently continue if patching fails
		pass

from .userapi import *

# Version information
__version__ = '1.13.1'

def get_version():
	try:
		version_path = os.path.dirname(os.path.realpath(__file__)) + '\\pypack\\version.ini'
		with open(version_path, 'rb') as f:
			version = f.read()
		return version.decode().strip()
	except:
		return __version__
