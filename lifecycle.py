'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

import yaml
import requests

VERSION = "0.1.8 (130321), Nested"

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
