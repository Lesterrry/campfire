'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

import requests
import urllib

def notify(text: str, conf):
	try:
		a = requests.get(conf['notification_url'].replace("{TEXT}", text))
	except:
		return False
	return a.status_code == 200