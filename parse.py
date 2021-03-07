'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

from bs4 import BeautifulSoup as bs
from colors import *
import lifecycle
import core
import subprocess

blacklist = []

def parse_all(warn: bool, routine):
	res = {}
	for prod, stores in routine['products'].items():
		res[prod] = {}
		at_least = False
		for store, info in stores.items():
			if (prod, store) in blacklist and lifecycle.CONFIG['one_fall_routine']:
				print(f"Игнорируется {prod}@{store}", end="\n" if warn else "; ", flush=not warn)
				res[prod][store] = {}
			else:
				at_least = True
				if info['ceremony'] == 'class_check':
					res[prod][store] = get_class_from_page(warn, (prod, store), info['headers'], **info['prop'])
				elif info['ceremony'] == 'lookup':
					res[prod][store] = lookup_page(warn, (prod, store), info['headers'], **info['prop'])
				elif info['ceremony'] == 'osa_lookup':
					res[prod][store] = osa_lookup_page(warn, (prod, store), **info['prop'])
				else:
					res[prod][store] = {}
	if at_least:
		return res
	else:
		a = "Рутина пуста, завершение работы"
		print(a)
		core.notify(a, lifecycle.CONFIG)

def decode(s: str):
	s = s.strip().encode("ascii", "ignore").decode()
	s = ''.join([c for c in s if c.isdigit()])
	return s

def get_class_from_page(warn: bool, label: (str, str), headers, url, status_class):
	page = get_page(warn, headers, url, label)
	if not page:
		return {}
	soup = bs(page.text, 'lxml')
	try:
		st = soup.find(class_=status_class).text.strip()
	except:
		if label in blacklist:
			if warn: print(f"parse: {ORG}Повторилась проблема с {label[0]}@{label[1]}{RES}")
		else:
			a = f"Не удалось обработать ресурс {label[0]}@{label[1]}"
			if warn: print(f"parse: {ORG}{a}{RES}")
			if not core.notify(a, lifecycle.CONFIG):
				print(f"{RED}Ошибка отправки уведомления{RES}")
			blacklist.append(label)
		return {}
	try: 
		blacklist.remove(label)
	except Exception:
		pass
	return st

def lookup_page(warn: bool, label: (str, str), headers, url, key):
	page = get_page(warn, headers, url, label)
	if not page:
		return False
	return key in page.text

def osa_lookup_page(warn: bool, label: (str, str), url, key):
	try:
		a = subprocess.check_output(['osascript', lifecycle.CONFIG["zipline_path"], url, key])
		if "true" in str(a): return True
		else: return False
	except Exception as e:
		b = f"Ошибка OSA: {e}"
		core.notify(b)
		print(f"parse: {RED}{b}{RES}")
		blacklist.append(label)

def get_page(warn: bool, headers, url, label: (str, str)):
	try:
		lifecycle.SESSION.headers.update(headers)
		page = lifecycle.SESSION.get(url)
	except Exception as e:
		if label in blacklist:
			print(f"parse: {RED}Повторилась проблема с {label[0]}@{label[1]} ({e}){RES}", end="\n" if warn else "; ", flush=not warn)
		else:
			a = f"Не удалось загрузить ресурс {label[0]}@{label[1]}: {e}"
			print(f"parse: {RED}{a}{RES}", end="\n" if warn else "; ", flush=not warn)
			if not core.notify(a, lifecycle.CONFIG):
				print(f"{RED}Ошибка отправки уведомления{RES}")
			blacklist.append(label)
		return {}
	if page.status_code != 200:
		if label in blacklist:
			print(f"parse: {ORG}Повторилась проблема с {label[0]}@{label[1]} (>{page.status_code}){RES}", end="\n" if warn else "; ", flush=not warn)
		else:
			a = f"Ресурс {label[0]}@{label[1]} вернул {page.status_code}"
			print(f"parse: {ORG}{a}{RES}", end="\n" if warn else "; ", flush=not warn)
			if not core.notify(a, lifecycle.CONFIG):
				print(f"{RED}Ошибка отправки уведомления{RES}")
			with open(f"records/{label[0]}@{label[1]}.html", "w") as file:
				file.write(page.text)
			blacklist.append(label)
		return {}
	try: 
		blacklist.remove(label)
	except Exception:
		pass
	return page