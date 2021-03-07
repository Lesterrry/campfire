'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

import requests
import urllib
import yaml
import lifecycle
from colors import *

def handle_error(module: str, text: str):
	print(f"{module}: {RED}{text}{RES}")
	exit(0)

def notify(text: str, conf):
	if lifecycle.CONFIG['notify']:
		try:
			a = requests.get(conf['notification_url'].replace("{TEXT}", f"{lifecycle.CONFIG['device_name']}: {text}"))
		except:
			return False
		return a.status_code == 200
	return True

def init_routine():
	#Opening & parsing index file
	try:
		with open('index.yaml') as f:
			a = yaml.safe_load(f)
			return a
	except:
		handle_error("core", "Ошибка чтения файла индекса")
