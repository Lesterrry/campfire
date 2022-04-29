'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021-2022
'''''''''''''''''''''''''''''

import yaml
import requests
import os

VERSION = "1.0.0 (290422)"

# Opening & parsing config file
def init():
	global CONFIG
	global SESSION
	path = os.path.dirname(os.path.realpath(__file__))
	with open(path + '/config.yaml') as config_file:
		CONFIG = yaml.safe_load(config_file)

	# Opening web session
	SESSION = requests.Session()

def reload():
	with open('config.yaml') as config_file:
		CONFIG = yaml.safe_load(config_file)
