'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021-2022
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
				core.safe_print(f"Игнорируется {prod}@{store}", end="\n" if warn else "; ", flush=not warn)
				res[prod][store] = {}
			else:
				at_least = True
				if info['ceremony'] == 'class-check':
					res[prod][store] = get_class_from_page(warn, (prod, store), info['headers'], **info['prop'])
				elif info['ceremony'] == 'lookup':
					res[prod][store] = lookup_page(warn, (prod, store), info['headers'], **info['prop'])
				elif info['ceremony'] == 'osa-lookup':
					res[prod][store] = osa_lookup_page(warn, (prod, store), **info['prop'])
				elif info['ceremony'] == 'code-check':
					res[prod][store] = get_page_code(warn, (prod, store), info['headers'], **info['prop'])
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
	with open(f"records/{label[0]}@{label[1]}.html", "w") as file:
		file.write(page.text)
	try:
		st = soup.find(class_=status_class).text.strip()
	except Exception as e:
		if label in blacklist:
			if warn: 
				print(f"parse: {ORG}Повторилась проблема с {label[0]}@{label[1]} ({e}){RES}")
		else:
			a = f"Не удалось обработать ресурс {label[0]}@{label[1]} ({e})"
			if warn:
				print(f"parse: {ORG}{a}{RES}")
			core.notify(a, lifecycle.CONFIG)
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

def osa_lookup_page(warn: bool, label: (str, str), url, soldout_key, in_stock_key):
	try:
		a = subprocess.check_output(['osascript', lifecycle.CONFIG["zipline_path"], url, soldout_key, in_stock_key])
		if "sold_out" in str(a): return "СОЛДАУТ"
		elif "in_stock" in str(a): return "В ПРОДАЖЕ"
		elif "time_out" in str(a): return "ТАЙМАУТ"
		else: raise ValueError(f"OSA returned {str(a)}")
	except Exception as e:
		b = f"Ошибка OSA: {e}"
		core.notify(b, lifecycle.CONFIG)
		print(f"parse: {RED}{b}{RES}")
		blacklist.append(label)

def get_page_code(warn: bool, label: (str, str), headers, url):
	try:
		lifecycle.SESSION.headers.update(headers)
		page = lifecycle.SESSION.get(url)
	except Exception as e:
		if label in blacklist:
			if warn:
				print(f"parse: {RED}Повторилась проблема с {label[0]}@{label[1]} ({e}){RES}", end="\n" if warn else "; ", flush=not warn)
		else:
			a = f"Не удалось загрузить ресурс {label[0]}@{label[1]}: {e}"
			if warn:
				print(f"parse: {RED}{a}{RES}", end="\n", flush=True)
			core.notify(a, lifecycle.CONFIG)
			blacklist.append(label)
		return {}
	try:
		blacklist.remove(label)
	except Exception:
		pass
	return page.status_code

def get_page(warn: bool, headers, url, label: (str, str)):
	try:
		lifecycle.SESSION.headers.update(headers)
		page = lifecycle.SESSION.get(url)
	except Exception as e:
		if label in blacklist:
			if warn:
				print(f"parse: {RED}Повторилась проблема с {label[0]}@{label[1]} ({e}){RES}", end="\n" if warn else "; ", flush=not warn)
		else:
			a = f"Не удалось загрузить ресурс {label[0]}@{label[1]}: {e}"
			if warn:
				print(f"parse: {RED}{a}{RES}", end="\n", flush=True)
			core.notify(a, lifecycle.CONFIG)
			blacklist.append(label)
		return {}
	if page.status_code != 200:
		if label in blacklist:
			print(f"parse: {ORG}Повторилась проблема с {label[0]}@{label[1]} (>{page.status_code}){RES}", end="\n" if warn else "; ", flush=not warn)
		else:
			a = f"Ресурс {label[0]}@{label[1]} вернул {page.status_code}"
			if warn:
				print(f"parse: {ORG}{a}{RES}", end="\n", flush=True)
			core.notify(a, lifecycle.CONFIG)
			with open(f"records/{label[0]}@{label[1]}.html", "w") as file:
				file.write(page.text)
			blacklist.append(label)
		return {}
	try:
		blacklist.remove(label)
	except Exception:
		pass
	return page
