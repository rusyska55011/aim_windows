# -*- coding: utf-8 -*-

import win32gui
import win32api
import ctypes
import keyboard
import time

dc = win32gui.GetDC(0)
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

middle_x = screensize[0] // 2
middle_y =  screensize[1] // 2

# Функция чтения файла с сохраненными настройками
def file_read():
    f = open('settings.txt', 'r')
    lines = f.readlines()
    c = []
    total = ''
    for i in lines[0].split('\n')[0] + ",":
        if i == ",":
            c.append(int(total))
            total = ''
        else:
            total += i
    r = lines[1].split('\n')[0]
    o = lines[2].split('\n')[0]
    l = lines[3].split('\n')[0]
    f.close
    return c,r,o,l

# Функция перезаписи файла с сохраненными настройками
def file_create(c, r, o, l):
    f = open('settings.txt', 'w')
    f.write(str(c) + '\n')
    f.write(str(r) + '\n')
    f.write(str(o) + '\n')
    f.write(str(l))
    f.close()
    return c,r,o,l

# Цикл ожидания. Во время работы считывает кнопку "=", после чего идет перезапись файла с настройками
# Если кнопка не считана, условие с перезаписью не срабатывает
print("Для перехода в настройки нажмите клавишу '+' ('='). Автоматический запуск через 5 секунд...")
for i in range(0, 1000):
    if keyboard.is_pressed('='):
        print('Выберите цвет прицела (В формате RGB, через запятую каждый аргумент, к примеру: 255,0,0 или 100,50,242)')
        c = str(input())
        print('Выберите радиус точки прицела')
        r = int(input())
        print('Выберите отступ (верхней, нижней, левой, правой) линий вокруг приела. Отсутуп осущ. от нулевых координат. Если хотите играть с точкой, нажмите 0')
        o = int(input())
        if o == 0:
            break
        else:
            print('Выберите длинну линий')
            l = int(input())
        file_create(c,r,o,l)
        break
    time.sleep(5 / 1000)

# Считывание файла, возвращает 4 аргумента (1й арг - список с 3мя значениями), которые переписываем в переменную
Read = file_read()

c = win32api.RGB(Read[0][0], Read[0][1], Read[0][2])
r = int(Read[1])
o = int(Read[2])
l = int(Read[3])

print('Ваши настрокий:')
print('Цвет прицела в RGB:', Read[0][0], Read[0][1], Read[0][2])
print('Радиус точки прицела:', r)
print('Отступ линий прицела:', o)
print('Длина прицела:', l)

# Бесконечный цикл отрисовки прицела
while True:
    # При нажатии кнопки "-" активируется бесконечный цикл, который ничего не делает,
    # кроме того как ждет нажатия "=", чтобы выйти из цикла и вернуться к основному циклу
    if keyboard.is_pressed('-'):
        while True:
            if keyboard.is_pressed('='):
                break

    y = middle_y
    x = middle_x

    # Отрисовка одного пикселя, если радиус == 1
    if r == 1:
        win32gui.SetPixel(dc, x, y, c)
    else:
        # Отрисовка точки
        for z in range(0, r * 2):
            for i in range(0, r):
                win32gui.SetPixel(dc, x - r + z, y - i, c)
                win32gui.SetPixel(dc, x - r + z, y + i, c)
        if o == 0:
            continue
        else:
            # Отрисовка линий по горизонтали и вертикали
            for z in range(0, r):
                for i in range(0, l):
                    win32gui.SetPixel(dc, x + o + i, y + z, c)
                    win32gui.SetPixel(dc, x + o + i, y - z, c)
                    win32gui.SetPixel(dc, x - o - i, y + z, c)
                    win32gui.SetPixel(dc, x - o - i, y - z, c)

                    win32gui.SetPixel(dc, x + z, y + o + i, c)
                    win32gui.SetPixel(dc, x - z, y + o + i, c)
                    win32gui.SetPixel(dc, x + z, y - o - i, c)
                    win32gui.SetPixel(dc, x - z, y - o - i, c)

