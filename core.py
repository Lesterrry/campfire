'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021-2022
'''''''''''''''''''''''''''''

import requests
import urllib
import yaml
import lifecycle
from colors import *
import os

def handle_error(module: str, text: str):
	print(f"{module}: {RED}{text}{RES}")
	exit(1)

def cronitor_ping():
	if lifecycle.CONFIG['cronitor_integrated']:
		requests.get(f"https://cronitor.link/p/{lifecycle.CONFIG['cronitor_key']}/{lifecycle.CONFIG['cronitor_id']}?host={lifecycle.CONFIG['device_name']}", timeout=10)
def notify(text: str, conf):
	if lifecycle.CONFIG['notify']:
		try:
			a = requests.get(conf['notification_url'].replace("{TEXT}", f"({lifecycle.CONFIG['device_name']}) {text}"), timeout=10)
		except:
			return False
		return a.status_code == 200
	return True
def safe_print(*message, end: str = "\n", flush: bool = False):
	if not lifecycle.CONFIG['silent']:
		print(*message, end=end, flush=flush)
def init_routine():
	#Opening & parsing index file
	try:
		path = os.path.dirname(os.path.realpath(__file__))
		with open(path + '/index.yaml') as f:
			a = yaml.safe_load(f)
			return a
	except Exception as e:
		handle_error("core", f"Ошибка чтения файла индекса ({e})")
