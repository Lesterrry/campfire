'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

import requests
import yaml
from bs4 import BeautifulSoup as bs
import datetime
import os
from colors import *

#Opening & parsing config file
global CONFIG
try:
	with open('config.yaml') as config_file:
		CONFIG = yaml.safe_load(config_file)
except:
	print(f"parse: {RED}Ошибка чтения файла конфигурации{RES}")
	exit(0)

#Opening web session
session = requests.Session()
try:
	session.headers.update(CONFIG['headers'])
except:
	print(f"parse: {RED}Ошибка применения заголовков{RES}")
	exit(0)

def init_routine():
	#Opening & parsing index file
	try:
		with open('index.yaml') as f:
			a = yaml.safe_load(f)
			return a
	except:
		print(f"parse: {RED}Ошибка чтения файла индекса{RES}")
		exit(0)

def decode(s: str):
	s = s.strip().encode("ascii", "ignore").decode()
	s = ''.join([c for c in s if c.isdigit()])
	return s

def parse_page(warn: bool, label: (str, str), url, status_class, price_class):
	try:
		page = session.get(url)
	except:
		print(f"parse: {RED}Не удалось загрузить ресурс {label[0]}@{label[1]}{RES}", end="\n" if warn else "; ", flush=not warn)
		return {}
	if page.status_code != 200:
		print(f"parse: {ORG}Ресурс {label[0]}@{label[1]} вернул {page.status_code}{RES}", end="\n" if warn else "; ", flush=not warn)
		if page.status_code == 403:
			with open("info.html", "w") as file:
				file.write(page.text)
		return {}
	soup = bs(page.text, 'lxml')
	try:
		st = soup.find(class_=status_class).text.strip()
	except:
		if warn: print(f"parse: {ORG}Не удалось обработать ресурс {url}{RES}")
		return {}
	try:
		price = decode(soup.find(class_=price_class).text.strip())
	except:
		if warn: print(f"parse: {ORG}Проблема с ценой ресурса {url}{RES}")
		price = 0
	return {'status': st, "price": price}

def parse_all(warn: bool, routine):
	res = {}
	for prod, stores in routine['products'].items():
		res[prod] = {}
		for store, info in stores.items():
			res[prod][store] = parse_page(warn, (prod, store), **info)
	return res
