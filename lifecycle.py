'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

import core
import yaml
import requests

#Opening & parsing config file
def init():
	global CONFIG
	global SESSION
	try:
		with open('config.yaml') as config_file:
			CONFIG = yaml.safe_load(config_file)
	except Exception as e:
		core.handle_error("lifecycle", f"Ошибка чтения файла конфигурации: {e}")

	#Opening web session
	SESSION = requests.Session()