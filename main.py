#!/usr/bin/env python3
'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

VERSION = "0.1.3"

from colors import *
import core
import parse
import lifecycle
import time

print(f"Добро пожаловать в Campfire v{VERSION}")
print("Запуск сессии...")
lifecycle.init()
refresh_rate = lifecycle.CONFIG['refresh_rate']
print("Формирование рутины...")
routine = core.init_routine()
print("Сохранение типовых значений...")
default = parse.parse_all(True, routine)
for prod, stores in default.items():
		for store, info in stores.items():
			print(f"    {prod}@{store}: {'НЕСОД' if not info else ('СОД' if info == True else info)}")
print("Ожидание...")
time.sleep(refresh_rate)
print("\nЗапуск цикла...")

j = 0
while True:
	j += 1
	print(f"{CRR + ERS}{j} итерация... ", end="", flush=True)
	a = parse.parse_all(False, routine)
	if a != default:
		print(f"\n{MAG}ЕСТЬ ИЗМЕНЕНИЯ: {RES}", end="", flush=True)
		for prod, stores in a.items():
			for store, info in stores.items():
				b = info
				c = default[prod][store]
				if b != c:
					d = f" {prod}@{store}: {c} => {b}"
					print(d)
					if not core.notify(d, lifecycle.CONFIG):
						print(f"{RED}Ошибка отправки уведомления{RES}")
		default = a
	else:
		print(f"{CYN}БЕЗ ИЗМЕНЕНИЙ{RES}", end="", flush=True)
	time.sleep(refresh_rate)