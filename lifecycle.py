'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

import yaml
import requests

VERSION = "0.1.6 (070321), Nested"

#Opening & parsing config file
def init():
	global CONFIG
	global SESSION
	with open('config.yaml') as config_file:
		CONFIG = yaml.safe_load(config_file)

	#Opening web session
	SESSION = requests.Session()

def reload():
	with open('config.yaml') as config_file:
		CONFIG = yaml.safe_load(config_file)