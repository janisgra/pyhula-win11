import os
from .userapi import *

def get_version():
	version_path = os.path.dirname(os.path.realpath(__file__)) + '\\pypack\\version.ini'

	with open(version_path, 'rb') as f:
		version = f.read()
	return version.decode()
