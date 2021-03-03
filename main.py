#!/usr/bin/env python3
'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

VERSION = "0.1.1"

from colors import * 
import time

print(f"Добро пожаловать в Campfire v{VERSION}")
print("Запуск сессии...")
from parse import *
from core import *
refresh_rate = CONFIG['refresh_rate']
print("Формирование рутины...")
routine = init_routine()
print("Сохранение типовых значений...")
default = parse_all(True, routine)
for prod, stores in default.items():
		for store, info in stores.items():
			print(f"    {prod}@{store}: {info.get('status', None)}")
print("\nЗапуск цикла...")
if not notify("Цикл запущен", CONFIG):
	print(f"{RED}Ошибка отправки уведомления{RES}")

j = 0
while True:
	j += 1
	start_time = time.time()
	print(f"{CRR + ERS}{j} итерация... ", end="", flush=True)
	a = parse_all(False, routine)
	if a != default:
		print(f"{CYN}ЕСТЬ ИЗМЕНЕНИЯ{RES}", end="", flush=True)
		for prod, stores in a.items():
			for store, info in stores.items():
				b = info.get('status', None)
				c = default[prod][store].get('status', None)
				if b != c: 
					print(f" {prod}@{store}: {c} => {b}", end="", flush=True)
		default = a
	else:
		print("БЕЗ ИЗМЕНЕНИЙ", end="", flush=True)
	time.sleep(refresh_rate - (start_time - time.time()))