'''
python setup.py build
'''

import Cython.Build
import distutils.core
import os
import struct
from setuptools import setup, find_packages
def get_data_files(file_dir):
	data_files_dir = {}
	for root, dirs, files in os.walk(file_dir):  
		#print(root) #当前目录路径  
		#print(dirs) #当前路径下所有子目录  
		#print(files) #当前路径下所有非目录子文件
		if root not in data_files_dir:
			data_files_dir[root] = []
			
		for f in files:
			if f == '.gitignore':
				continue
			data_files_dir[root].append(root[2:]+'\\'+f)
	
	#print(data_files_dir)
	data_files = []
	for path in data_files_dir:
		data_files.append(('Lib\\site-packages\\pyhula\\'+path[13:], data_files_dir[path]))
	#data_files_set = [root]
	return data_files

name = 'pyhula'
version = '1.1.4'
description = "Hula package"
author = 'HighGreat'
author_email = 'highgreat@hg-fly.com'

commandprocessor = Cython.Build.cythonize('./src/pyhula/pypack/fylo/commandprocessor.py')[0]
config = Cython.Build.cythonize('./src/pyhula/pypack/fylo/config.py')[0]
controlserver = Cython.Build.cythonize('./src/pyhula/pypack/fylo/controlserver.py')[0]
mavlink = Cython.Build.cythonize('./src/pyhula/pypack/fylo/mavlink.py')[0]
msganalyzer = Cython.Build.cythonize('./src/pyhula/pypack/fylo/msganalyzer.py')[0]
mavanalyzer = Cython.Build.cythonize('./src/pyhula/pypack/fylo/mavanalyzer.py')[0]
stateprocessor = Cython.Build.cythonize('./src/pyhula/pypack/fylo/stateprocessor.py')[0]
taskprocessor = Cython.Build.cythonize('./src/pyhula/pypack/fylo/taskprocessor.py')[0]
uwb = Cython.Build.cythonize('./src/pyhula/pypack/fylo/uwb.py')[0]

buffer = Cython.Build.cythonize('./src/pyhula/pypack/system/buffer.py')[0]
command = Cython.Build.cythonize('./src/pyhula/pypack/system/command.py')[0]
communicationcontroller = Cython.Build.cythonize('./src/pyhula/pypack/system/communicationcontroller.py')[0]
communicationcontrollerfactory = Cython.Build.cythonize('./src/pyhula/pypack/system/communicationcontrollerfactory.py')[0]
dancecontroller = Cython.Build.cythonize('./src/pyhula/pypack/system/dancecontroller.py')[0]
dancefileanalyzer = Cython.Build.cythonize('./src/pyhula/pypack/system/dancefileanalyzer.py')[0]

datacenter = Cython.Build.cythonize('./src/pyhula/pypack/system/datacenter.py')[0]
event = Cython.Build.cythonize('./src/pyhula/pypack/system/event.py')[0]
mavcrc = Cython.Build.cythonize('./src/pyhula/pypack/system/mavcrc.py')[0]
network = Cython.Build.cythonize('./src/pyhula/pypack/system/network.py')[0]
networkcontroller = Cython.Build.cythonize('./src/pyhula/pypack/system/networkcontroller.py')[0]
serialcontroller = Cython.Build.cythonize('./src/pyhula/pypack/system/serialcontroller.py')[0]
state = Cython.Build.cythonize('./src/pyhula/pypack/system/state.py')[0]
system = Cython.Build.cythonize('./src/pyhula/pypack/system/system.py')[0]
taskcontroller = Cython.Build.cythonize('./src/pyhula/pypack/system/taskcontroller.py')[0]



# action_funtion = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/action_funtion.py')[0]
# getBoundry = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/getBoundry.py')[0]
# output_pos = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/output_pos.py')[0]
# parsejson = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/parsejson.py')[0]
# print_struct = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/print_struct.py')[0]
# op_seq_judgment = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/op_seq_judgment.py')[0]
# judgeBoundary = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/judgeBoundary.py')[0]
# matxtreader = Cython.Build.cythonize('./src/pyhula/pypack/system/dance/matxtreader.py')[0]



ext_modules = [commandprocessor, config, controlserver, mavlink, msganalyzer, mavanalyzer,	stateprocessor, taskprocessor, 
uwb, buffer, command, communicationcontroller, communicationcontrollerfactory, dancecontroller, dancefileanalyzer, 
 datacenter, event, mavcrc, network, networkcontroller, serialcontroller, state, system, taskcontroller, 
 ]
# action_funtion, getBoundry, output_pos, parsejson, print_struct, op_seq_judgment, judgeBoundary, 
# matxtreader

mat_data = [('Lib/site-packages/pyhula/pypack/system/dance', [
'src/pyhula/pypack/system/dance/arrow-anticlockwise.matxt',
'src/pyhula/pypack/system/dance/arrow-circle.matxt',
'src/pyhula/pypack/system/dance/arrow-clockwise.matxt',
'src/pyhula/pypack/system/dance/arrow-land.matxt',
'src/pyhula/pypack/system/dance/arrow-shuriken.matxt',
'src/pyhula/pypack/system/dance/arrow-square.matxt',
'src/pyhula/pypack/system/dance/circle-anticlockwise.matxt',
'src/pyhula/pypack/system/dance/circle-arrow.matxt',
'src/pyhula/pypack/system/dance/circle-clockwise.matxt',
'src/pyhula/pypack/system/dance/circle-land.matxt',
'src/pyhula/pypack/system/dance/circle-shuriken.matxt',
'src/pyhula/pypack/system/dance/circle-square.matxt',
'src/pyhula/pypack/system/dance/landing.matxt',
'src/pyhula/pypack/system/dance/shuriken-anticlockwise.matxt',
'src/pyhula/pypack/system/dance/shuriken-arrow.matxt',
'src/pyhula/pypack/system/dance/shuriken-circle.matxt',
# 'src/pyhula/pypack/system/dance/shuriken-clockwise.matxt',
# 'src/pyhula/pypack/system/dance/shuriken-land.matxt',
# 'src/pyhula/pypack/system/dance/shuriken-square.matxt',+
# 'src/pyhula/pypack/system/dance/square-anticlockwise.matxt',
# 'src/pyhula/pypack/system/dance/square-arrow.matxt',
# 'src/pyhula/pypack/system/dance/square-circle.matxt',
# 'src/pyhula/pypack/system/dance/square-clockwise.matxt',
# 'src/pyhula/pypack/system/dance/square-land.matxt',
# 'src/pyhula/pypack/system/dance/square-shuriken.matxt',
# 'src/pyhula/pypack/system/dance/square-wave.matxt',
# 'src/pyhula/pypack/system/dance/takeoff.matxt',
# 'src/pyhula/pypack/system/dance/takeoff-arrow.matxt',
# 'src/pyhula/pypack/system/dance/takeoff-circle.matxt',
# 'src/pyhula/pypack/system/dance/takeoff-shuriken.matxt',
# 'src/pyhula/pypack/system/dance/takeoff-square.matxt',
# 'src/pyhula/pypack/system/dance/takeoff-wave.matxt'
])]

dancefile_data = [('Lib/site-packages/pyhula/pypack/dancefile', [])]

ini_data = [('Lib/site-packages/pyhula/pypack', ['src/pyhula/pypack/log.ini', 'src/pyhula/pypack/version.ini'])]

# if struct.calcsize('P') == 4:   
#     danceviewsoftware = get_data_files('.\src\pyhula\FyloPlayer32')
# else:
#     danceviewsoftware = get_data_files('.\src\pyhula\FyloPlayer')
danceviewsoftware = [('Lib/site-packages/pyhula', ['src/pyhula/f09-lite-trans/f09-ffmpeg-lib.dll'])]
classifiers = [
"Intended Audience :: Education",
"Development Status :: 2 - Pre-Alpha", 
"Programming Language :: Python",
"Programming Language :: Python :: 3",
#"Programming Language :: Python :: 3.5",0
"Programming Language :: Python :: 3.6",
"Programming Language :: Python :: 3.7",
"Programming Language :: Python :: 3.8",
"Programming Language :: Python :: 3.9",
"Programming Language :: Python :: 3.10",
"Programming Language :: Python :: 3 :: Only",
"Operating System :: Microsoft :: Windows",
#"Operating System :: MacOS",
]

with open("requirements.txt") as f:
    requirements = f.read().splitlines()
distutils.core.setup(
name = name,
version = version,
description = description,
long_description = open('./readmewhl.md', encoding='utf-8').read(),
long_description_content_type = 'text/markdown',
author = author,
author_email = author_email,
packages = ['pyhula'],
package_dir = {'pyhula':'src/pyhula'},
ext_modules = ext_modules,
# data_files = danceviewsoftware + dancefile_data + ini_data + mat_data,
data_files = ini_data ,
install_requires = requirements,
package_data={'pyhula': ['f09-lite-trans/*']},
python_requires = '>=3.6',
classifiers = classifiers,
extras_require ={
	   'docs': [
            'sphinx>=3.0.0,<4.0.0',  # 文档生成依赖
        ]
}
)
