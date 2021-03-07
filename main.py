#!/usr/bin/env python3
'''''''''''''''''''''''''''''
COPYRIGHT FETCH DEVELOPMENT,

2021
'''''''''''''''''''''''''''''

from colors import *
import core
import parse
import lifecycle
import time
import os

print(f"Добро пожаловать в Campfire v{lifecycle.VERSION}")
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
print("\nЗапуск цикла...")

j = 0
r = 0
while True:
	x = refresh_rate - r
	print(f"Осталось: {'' if x >= 10 else '0'}{x}м  {CRB(15)}", end="", flush=True)
	r += 1
	if r == refresh_rate:
		r = 0
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
						d = f" {prod}@{store}: {'НЕСОД' if not c else ('СОД' if c == True else c)} => {'НЕСОД' if not b else ('СОД' if b == True else b)}"
						print(d)
						core.reload()
						if lifecycle.CONFIG['siren'] and b != dict() and b != True and b != False:
							os.system(f"osascript {lifecycle.CONFIG['siren_path']}")
						if not core.notify(d, lifecycle.CONFIG):
							print(f"{RED}Ошибка отправки уведомления{RES}")
			default = a
		else:
			print(f"{CYN}БЕЗ ИЗМЕНЕНИЙ{RES} ", end="", flush=True)
	time.sleep(60)