from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
import time
import random

tk = Tk()  # Создаём окно
tk.title('Турецкие шашки')  # Заголовок окна
board = Canvas(tk, width=795, height=795, bg='#FFFFFF')
tk.resizable(width=False, height=False)
board.pack()
app_running = True
tk.update()

hod_igroka = True
vozmozhnost_belih_shodit = False
vozmozhnost_chernih_shodit = False
white_count = 16
black_count = 16
vozm_b_zabrat_vverh = False
vozm_b_zabrat_vlevo = False
vozm_b_zabrat_vpravo = False
vozm_b_zabrat = False
vozm_b_d_zabrat_vverh = False
vozm_b_d_zabrat_vniz = False
vozm_b_d_zabrat_vlevo = False
vozm_b_d_zabrat_vpravo = False
vozm_b_d_zabrat = False
vozm_ch_zabrat_vniz = False
vozm_ch_zabrat_vlevo = False
vozm_ch_zabrat_vpravo = False
vozm_ch_zabrat = False
vozm_ch_d_zabrat_vverh = False
vozm_ch_d_zabrat_vniz = False
vozm_ch_d_zabrat_vlevo = False
vozm_ch_d_zabrat_vpravo = False
vozm_ch_d_zabrat = False

def izobrazheniya_figur():  # загружаем изображения фигур
    global figuri
    i1 = PhotoImage(file="res\\White.gif")
    i2 = PhotoImage(file="res\\Black.gif")
    i3 = PhotoImage(file="res\\WhiteDamka.gif")
    i4 = PhotoImage(file="res\\BlackDamka.gif")
    figuri = [0, i1, i2, i3, i4]


def novaya_igra():  # начинаем новую игру
    global pole

    pole = [[0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0]]

def Start_new():
    global white_count
    global black_count
    global hod_igroka
    if askyesno("Игра закончена","Хотите начать новую?"):
        novaya_igra()
        vivod(-1,-1)
        hod_igroka = True
        white_count = 16
        black_count = 16

def vivod(x_poz_1, y_poz_1):  # рисуем игровое поле
    global figuri
    global pole
    k = 100
    x = 0
    board.delete('all')

    while x < 8 * k:  # рисуем доску
        y = k
        while y < 8 * k:
            board.create_rectangle(x, y, x + k, y + k, fill="#deb887")
            y += k
        x += k
    x = 0
    while x < 8 * k:  # рисуем доску
        y = 0
        while y < 8 * k:
            board.create_rectangle(x, y, x + k, y + k, fill="#deb887")
            y += k
        x += k

    for y in range(8):  # рисуем стоячие пешки
        for x in range(8):
            z = pole[y][x]
            if z:
                if (x_poz_1, y_poz_1) != (x, y):  # стоячие пешки?
                    board.create_image(x * k, y * k, anchor=NW, image=figuri[z])


def vozmozhnost_belih_hodit(x, y): #метод, проверяющий белые шашки на доступность хода(что им ничего не преграждает путь)
    global vozmozhnost_belih_shodit
    global prev_b_coord_x
    global prev_b_coord_y
    if pole[x][y] == 1: # для белой не дамки
        if (pole[x - 1][y] == 0 and x > 0) or (y < 7 and pole[x][y + 1] == 0) or (pole[x][y - 1] == 0 and y > 0):
            vozmozhnost_belih_shodit = True
        else:
            vozmozhnost_belih_shodit = False
        prev_b_coord_x = x
        prev_b_coord_y = y
    elif pole[x][y] == 3: # для белой дамки
        if (x > 0 and pole[x-1][y] == 0) or (x < 7 and pole[x+1][y] == 0) or (y < 7 and pole[x][y + 1] == 0) or (pole[x][y - 1] == 0 and y > 0):
            vozmozhnost_belih_shodit = True
        else:
            vozmozhnost_belih_shodit = False
        prev_b_coord_x = x
        prev_b_coord_y = y


def vozmozhnost_chernih_hodit(x, y): #метод, проверяющий черные шашки на доступность хода(что им ничего не преграждает путь)
    global vozmozhnost_chernih_shodit
    global prev_ch_coord_x
    global prev_ch_coord_y

    if pole[x][y] == 2: # для черной не дамки
        if (pole[x + 1][y] == 0 and x < 7) or (y < 7 and pole[x][y + 1] == 0) or (pole[x][y - 1] == 0 and y > 0):
            vozmozhnost_chernih_shodit = True
        else:
            vozmozhnost_chernih_shodit = False
        prev_ch_coord_x = x
        prev_ch_coord_y = y
    elif pole[x][y] == 4: # для черной дамки
        if (x > 0 and pole[x - 1][y] == 0) or (x < 7 and pole[x + 1][y] == 0) or (y < 7 and pole[x][y + 1] == 0) or (pole[x][y - 1] == 0 and y > 0):
            vozmozhnost_chernih_shodit = True
        else:
            vozmozhnost_chernih_shodit = False
        prev_ch_coord_x = x
        prev_ch_coord_y = y

def belie_proverka():
    global vozm_b_zabrat_vverh
    global vozm_b_zabrat_vlevo
    global vozm_b_zabrat_vpravo
    global vozm_b_zabrat
    global vozm_b_d_zabrat_vverh
    global vozm_b_d_zabrat_vniz
    global vozm_b_d_zabrat_vlevo
    global vozm_b_d_zabrat_vpravo
    global vozm_b_d_zabrat

    for i in range(8):      # ищем на поле возможность случая забирания
        for j in range(8):
            if (pole[i][j] == 1 and i > 1) and (pole[i - 1][j] == 2 or pole[i - 1][j] == 4) and pole[i - 2][j] == 0: # для белой шашки вверх
                vozm_b_zabrat_vverh = True
                vozm_b_zabrat = True

            if (pole[i][j] == 1 and j > 1) and (pole[i][j - 1] == 2 or pole[i][j - 1] == 4) and pole[i][j - 2] == 0: # для белой шашки влево
                vozm_b_zabrat_vlevo = True
                vozm_b_zabrat = True

            if (pole[i][j] == 1 and j < 6) and (pole[i][j + 1] == 2 or pole[i][j+1] == 4) and pole[i][j + 2] == 0: # для белой шашки вправо
                vozm_b_zabrat = True
                vozm_b_zabrat_vpravo = True

            if i > 1 and pole[i][j] == 3: # для белой дамки вверх
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    count = 0
                    if pole[k][j] == 0 and ((k < 7 and pole[k + 1][j] == 2) or (k < 7 and pole[k + 1][j] == 4)) and (k < 6 and pole[k + 2][j] == 0 or k < 6 and pole[k + 2][j] == 3):
                        while pole[k][j] != 3:
                            if k < 7 and pole[i][j + 1] == 3:
                                vozm_b_d_zabrat_vlevo = True
                                vozm_b_d_zabrat = True
                                break
                            ch_count += 1
                            if k < 7:
                                k += 1
                            else:
                                break
                            if pole[k][j] == 0:
                                zero_count += 1
                            if pole[k][j] == 2 or pole[k][j] == 4:
                                count += 1
                            if count == 2:
                                break
                            if zero_count == ch_count - 2 and pole[k][j] == 3:
                                vozm_b_d_zabrat_vverh = True
                                vozm_b_d_zabrat = True
                            else:
                                vozm_b_d_zabrat_vverh = False
                        break

            if i < 7 and pole[i][j] == 3: # для белой дамки вниз
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    if pole[k][j] == 0 and ((k > 1 and pole[k - 1][j] == 2) or (k > 1 and pole[k - 1][j] == 4)):
                        while pole[k][j] != 3:
                            ch_count += 1
                            k -= 1
                            if pole[k][j] == 0:
                                zero_count += 1
                            if zero_count == ch_count - 2 and pole[k][j] == 3:
                                vozm_b_d_zabrat_vniz = True
                                vozm_b_d_zabrat = True
                            else:
                                vozm_b_d_zabrat_vniz = False
                        break

            if j > 1 and pole[i][j] == 3: # для белой дамки влево
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    count = 0
                    if pole[i][k] == 0 and ((k < 7 and pole[i][k + 1] == 2) or (k < 7 and pole[i][k + 1] == 4)) and (k < 6 and pole[i][k + 2] == 0 or k < 6 and pole[i][k + 2] == 3):
                        while pole[i][k] != 3:
                            if k < 7 and pole[i + 1][j] == 3:
                                vozm_b_d_zabrat_vlevo = True
                                vozm_b_d_zabrat = True
                                break
                            ch_count += 1
                            if k < 7:
                                k += 1
                            else:
                                break
                            if pole[i][k] == 0:
                                zero_count += 1
                            if pole[i][k] == 2 or pole[i][k] == 4:
                                count += 1
                            if count == 2:
                                break
                            if zero_count == ch_count - 2 and pole[i][k] == 3:
                                vozm_b_d_zabrat_vlevo = True
                                vozm_b_d_zabrat = True
                            elif vozm_b_d_zabrat_vlevo != True:
                                vozm_b_d_zabrat_vlevo = False

            if j < 7 and pole[i][j] == 3: # для белой дамки вправо
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    if pole[i][k] == 0 and ((k > 1 and pole[i][k - 1] == 2) or (k > 1 and pole[i][k - 1] == 4)):
                        while pole[i][k] != 3:
                            ch_count += 1
                            k -= 1
                            if pole[i][k] == 0:
                                zero_count += 1
                            if zero_count == ch_count - 2 and pole[i][k] == 3:
                                vozm_b_d_zabrat_vpravo = True
                                vozm_b_d_zabrat = True
                            else:
                                vozm_b_zabrat_vpravo = False
                        break

def chernie_proverka(): # аналогично с тем что выше
    global vozm_ch_zabrat_vniz
    global vozm_ch_zabrat_vlevo
    global vozm_ch_zabrat_vpravo
    global vozm_ch_zabrat
    global vozm_ch_d_zabrat_vverh
    global vozm_ch_d_zabrat_vniz
    global vozm_ch_d_zabrat_vlevo
    global vozm_ch_d_zabrat_vpravo
    global vozm_ch_d_zabrat

    for i in range(8):
        for j in range(8):
            if (pole[i][j] == 2 and i < 6) and (pole[i + 1][j] == 1 or pole[i + 1][j] == 3) and pole[i + 2][j] == 0:
                vozm_ch_zabrat_vniz = True
                vozm_ch_zabrat = True
            if (pole[i][j] == 2 and j > 1) and (pole[i][j - 1] == 1 or pole[i][j - 1] == 3) and pole[i][j - 2] == 0:
                vozm_ch_zabrat_vlevo = True
                vozm_ch_zabrat = True
            if (pole[i][j] == 2 and j < 6) and (pole[i][j + 1] == 1 or pole[i][j + 1] == 3) and pole[i][j + 2] == 0:
                vozm_ch_zabrat = True
                vozm_ch_zabrat_vpravo = True

            if i > 1 and pole[i][j] == 4:
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    count = 0
                    if pole[k][j] == 0 and ((k < 7 and pole[k + 1][j] == 1) or (k < 7 and pole[k + 1][j] == 3)) and (k < 6 and pole[k + 2][j] == 0 or k < 6 and pole[k + 2][j] == 4):
                        while pole[k][j] != 4:
                            if k < 7 and pole[i + 1][j] == 4:
                                vozm_ch_d_zabrat_vlevo = True
                                vozm_ch_d_zabrat = True
                                break
                            ch_count += 1
                            if k < 7:
                                k += 1
                            else:
                                break
                            if pole[k][j] == 0:
                                zero_count += 1
                            if pole[k][j] == 1 or pole[k][j] == 3:
                                count += 1
                            if count == 2:
                                break
                            if zero_count == ch_count - 2 and pole[k][j] == 4:
                                vozm_ch_d_zabrat_vverh = True
                                vozm_ch_d_zabrat = True
                            else:
                                vozm_ch_d_zabrat_vverh = False


            if i < 7 and pole[i][j] == 4:
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    if pole[k][j] == 0 and ((k > 1 and pole[k - 1][j] == 1) or (k > 1 and pole[k - 1][j] == 3)):
                        while pole[k][j] != 4:
                            ch_count += 1
                            k -= 1
                            if pole[k][j] == 0:
                                zero_count += 1
                            if zero_count == ch_count - 2 and pole[k][j] == 4:
                                vozm_ch_d_zabrat_vniz = True
                                vozm_ch_d_zabrat = True
                            else:
                                vozm_ch_d_zabrat_vniz = False
                        break

            if j > 1 and pole[i][j] == 4:
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    count = 0
                    if pole[i][k] == 0 and ((k < 7 and pole[i][k + 1] == 1) or (k < 7 and pole[i][k + 1] == 3)) and (k < 6 and pole[i][k + 2] == 0 or k < 6 and pole[i][k + 2] == 4):
                        while pole[i][k] != 4:
                            if k < 7 and pole[i][j + 1] == 4:
                                vozm_ch_d_zabrat_vlevo = True
                                vozm_ch_d_zabrat = True
                                break
                            ch_count += 1
                            if k < 7:
                                k += 1
                            else:
                                break
                            if pole[i][k] == 0:
                                zero_count += 1
                            if pole[i][k] == 1 or pole[i][k] == 3:
                                count += 1
                            if count == 2:
                                break
                            if zero_count == ch_count - 2 and pole[i][k] == 4:
                                vozm_ch_d_zabrat_vlevo = True
                                vozm_ch_d_zabrat = True
                            elif vozm_ch_d_zabrat_vlevo != True:
                                vozm_ch_d_zabrat_vlevo = False

            if j < 7 and pole[i][j] == 4:
                for k in range(8):
                    zero_count = 0
                    ch_count = 0
                    if pole[i][k] == 0 and ((k > 1 and pole[i][k - 1] == 1) or (k > 1 and pole[i][k - 1] == 3)):
                        while pole[i][k] != 4:
                            ch_count += 1
                            k -= 1
                            if pole[i][k] == 0:
                                zero_count += 1
                            if zero_count == ch_count - 2 and pole[i][k] == 4:
                                vozm_ch_d_zabrat_vpravo = True
                                vozm_ch_d_zabrat = True
                            else:
                                vozm_ch_zabrat_vpravo = False
                        break

def click_event(event):
    global hod_igroka
    global white_count
    global black_count
    global vozm_b_zabrat
    global vozm_b_zabrat_vverh
    global vozm_b_zabrat_vlevo
    global vozm_b_zabrat_vpravo
    global vozm_ch_zabrat
    global vozm_ch_zabrat_vniz
    global vozm_ch_zabrat_vlevo
    global vozm_ch_zabrat_vpravo
    global vozm_b_d_zabrat_vverh
    global vozm_b_d_zabrat_vniz
    global vozm_b_d_zabrat_vlevo
    global vozm_b_d_zabrat_vpravo
    global vozm_b_d_zabrat
    global vozm_ch_d_zabrat_vverh
    global vozm_ch_d_zabrat_vniz
    global vozm_ch_d_zabrat_vlevo
    global vozm_ch_d_zabrat_vpravo
    global vozm_ch_d_zabrat
    global prev_b_coord_x
    global prev_b_coord_y
    global prev_ch_coord_x
    global prev_ch_coord_y

    if 0 < event.x < 800 and 0 < event.y < 800:  # Если кликнули на доске
        x = event.y // 100  # Определяем строку на которую нажали
        y = event.x // 100  # Определяем столбец на который нажали

    if hod_igroka: # если ход белых
        if vozm_b_d_zabrat: # если у белых дамок есть возможность забрать черную шашку
            if vozm_b_d_zabrat_vverh:
                if pole[prev_b_coord_x][prev_b_coord_y] == 3 and prev_b_coord_x > 1 and pole[x][y] == 0 and prev_b_coord_y == y:
                    if x < prev_b_coord_x and x < 7 and pole[x + 1][y] == 2 or x < 7 and pole[x + 1][y] == 4:
                        ch_count = 0
                        not_zero_count = 0
                        prev_x = prev_b_coord_x
                        for k in range(prev_b_coord_x, x, -1): # проверяем все ли клетки на пути пустые
                            ch_count += 1
                            if pole[prev_b_coord_x][y] != 0:
                                not_zero_count += 1
                            prev_b_coord_x -= 1
                        if not_zero_count == 2: # если на пути ничего не мешает, то едим
                            pole[x][y] = 3
                            pole[prev_x][prev_b_coord_y] = 0
                            pole[x + 1][y] = 0
                            black_count -= 1
                            vivod(-1, -1)

            if vozm_b_d_zabrat_vniz:
                if pole[prev_b_coord_x][prev_b_coord_y] == 3 and prev_b_coord_x < 7 and pole[x][y] == 0 and prev_b_coord_y == y:
                    if x > prev_b_coord_x and pole[x - 1][y] == 2 or pole[x - 1][y] == 4:
                        ch_count = 0
                        not_zero_count = 0
                        prev_x = prev_b_coord_x
                        for k in range(x, prev_b_coord_x, -1):
                            ch_count += 1
                            if pole[prev_b_coord_x][y] != 0:
                                not_zero_count += 1
                            prev_b_coord_x += 1
                        if not_zero_count == 2:
                            pole[x][y] = 3
                            pole[prev_x][prev_b_coord_y] = 0
                            pole[x - 1][y] = 0
                            black_count -= 1
                            vivod(-1, -1)

            if vozm_b_d_zabrat_vlevo:
                if pole[prev_b_coord_x][prev_b_coord_y] == 3 and prev_b_coord_y > 1 and pole[x][y] == 0 and prev_b_coord_x == x:
                    if y < prev_b_coord_y and y < 7 and pole[x][y + 1] == 2 or y < 7 and pole[x][y + 1] == 4:
                        ch_count = 0
                        not_zero_count = 0
                        prev_y = prev_b_coord_y
                        for k in range(prev_b_coord_y, y, -1):
                            ch_count += 1
                            if pole[x][prev_b_coord_y] != 0:
                                not_zero_count += 1
                            prev_b_coord_y -= 1
                        if not_zero_count == 2:
                            pole[x][y] = 3
                            pole[prev_b_coord_x][prev_y] = 0
                            pole[x][y + 1] = 0
                            black_count -= 1
                            vivod(-1, -1)

            if vozm_b_d_zabrat_vpravo:
                if pole[prev_b_coord_x][prev_b_coord_y] == 3 and prev_b_coord_y < 6 and pole[x][y] == 0 and prev_b_coord_x == x:
                    if y > prev_b_coord_y and pole[x][y - 1] == 2 or pole[x][y - 1] == 4:
                        ch_count = 0
                        not_zero_count = 0
                        prev_y = prev_b_coord_y
                        for k in range(y, prev_b_coord_y, -1):
                            ch_count += 1
                            if pole[x][prev_b_coord_y] != 0:
                                not_zero_count += 1
                            prev_b_coord_y += 1
                        if not_zero_count == 2:
                            pole[x][y] = 3
                            pole[prev_b_coord_x][prev_y] = 0
                            pole[x][y - 1] = 0
                            black_count -= 1
                            vivod(-1, -1)

            vozm_b_d_zabrat = False
            belie_proverka()
            if vozm_b_d_zabrat == False:
                hod_igroka = False
        if vozm_b_zabrat: # если возможность белых не дамок забрать
            if vozm_b_zabrat_vverh:
                if pole[prev_b_coord_x][prev_b_coord_y] == 1 and prev_b_coord_x > 1 and (pole[prev_b_coord_x - 1][y] == 2 or pole[prev_b_coord_x - 1][y] == 4) and pole[x][y] == 0 and pole[x + 2][y] == 1 and prev_b_coord_x == x + 2 and prev_b_coord_y == y:
                    if prev_b_coord_x == 2 and x + 1 == 1 and x == 0: # если прыгнули на поле, превращающее в дамку
                        pole[x][y] = 3
                    else:
                        pole[x][y] = 1
                    pole[x + 2][y] = 0
                    pole[x + 1][y] = 0
                    black_count -= 1
                    vivod(-1, -1)

            if vozm_b_zabrat_vlevo:
                if pole[prev_b_coord_x][prev_b_coord_y] == 1 and prev_b_coord_y > 1 and (pole[prev_b_coord_x][prev_b_coord_y - 1] == 2 or pole[prev_b_coord_x][prev_b_coord_y - 1] == 4) and pole[x][y] == 0 and pole[prev_b_coord_x][prev_b_coord_y - 2] == 0 and prev_b_coord_x == x and prev_b_coord_y == y + 2:
                    pole[prev_b_coord_x][y + 2] = 0
                    pole[x][y + 1] = 0
                    pole[x][y] = 1
                    black_count -= 1
                    vivod(-1, -1)

            if vozm_b_zabrat_vpravo:
                if pole[prev_b_coord_x][prev_b_coord_y] == 1 and prev_b_coord_y < 6 and (pole[prev_b_coord_x][prev_b_coord_y + 1] == 2 or pole[prev_b_coord_x][prev_b_coord_y + 1] == 4) and pole[x][y] == 0 and pole[prev_b_coord_x][prev_b_coord_y + 2] == 0 and prev_b_coord_x == x and prev_b_coord_y == y - 2:
                    pole[prev_b_coord_x][y - 2] = 0
                    pole[x][y - 1] = 0
                    pole[x][y] = 1
                    black_count -= 1
                    vivod(-1, -1)
            vozm_b_zabrat = False

            belie_proverka()
            if vozm_b_d_zabrat == False and vozm_b_zabrat == False:
                hod_igroka = False
        belie_proverka()
        vozmozhnost_belih_hodit(x, y)
        if white_count == 0:
            messagebox.showinfo(title='Победа черных', message='Победили черные.', icon='info')
            hod_igroka = None
            Start_new()
        if vozmozhnost_belih_shodit: # если выбранная шашка может ходить(ей ничего не преграждает путь)
            if (pole[prev_b_coord_x][prev_b_coord_y] != 0 and prev_b_coord_y + 1 == y and prev_b_coord_x == x) or (prev_b_coord_y - 1 == y and prev_b_coord_x == x) or (prev_b_coord_x - 1 == x and prev_b_coord_y == y):  # Проверяем, сходили ли мы на одну клетку вертикально или горизонтально
                if pole[x][y] == 0 and vozm_b_zabrat == False and vozm_b_d_zabrat == False: # если эта клетка пустая и нету контроля для забирания(поедания)
                    if pole[prev_b_coord_x][prev_b_coord_y] == 1: # если сходили на поле, превращающее в дамку
                        if x == 0:
                            pole[x][y] = 3
                        else:
                            pole[x][y] = 1
                        pole[prev_b_coord_x][prev_b_coord_y] = 0
                        vivod(-1, -1)  # рисуем игровое поле
                        hod_igroka = False
            if pole[prev_b_coord_x][prev_b_coord_y] == 3 and pole[x][y] == 0 and vozm_b_zabrat == False and vozm_b_d_zabrat == False: # ходы для белой дамки
                if prev_b_coord_x > x and prev_b_coord_y == y:
                    ch_count = 0
                    not_zero_count = 0
                    prev_x = prev_b_coord_x
                    for k in range(prev_b_coord_x ,x ,-1): # проверка на пустой путь до выбранной клетки
                        ch_count += 1
                        if pole[prev_b_coord_x ][y] != 0:
                            not_zero_count +=1
                        prev_b_coord_x -= 1
                    if not_zero_count == 1:
                        pole[x][y] = 3
                        pole[prev_x][prev_b_coord_y] = 0
                        vivod(-1,-1)
                        hod_igroka = False
                if prev_b_coord_x < x and prev_b_coord_y == y:

                    ch_count = 0
                    not_zero_count = 0
                    prev_x = prev_b_coord_x
                    for k in range(prev_b_coord_x,x):
                        ch_count += 1
                        if pole[prev_b_coord_x][y] != 0:
                            not_zero_count +=1
                        prev_b_coord_x += 1
                    if not_zero_count == 1:
                        pole[x][y] = 3
                        pole[prev_x][prev_b_coord_y] = 0
                        vivod(-1, -1)
                        hod_igroka = False
                if prev_b_coord_y > y and prev_b_coord_x == x:
                    ch_count = 0
                    not_zero_count = 0
                    prev_y = prev_b_coord_y
                    for k in range(prev_b_coord_y,y,-1):
                        ch_count += 1
                        if pole[x][prev_b_coord_y] != 0:
                            not_zero_count +=1
                        prev_b_coord_y -= 1
                    if not_zero_count == 1:
                        pole[x][y] = 3
                        pole[prev_b_coord_x][prev_y] = 0
                        vivod(-1, -1)
                        hod_igroka = False
                if prev_b_coord_y < y and prev_b_coord_x == x:
                    ch_count = 0
                    not_zero_count = 0
                    prev_y = prev_b_coord_y
                    for k in range(prev_b_coord_y,y):
                        ch_count += 1
                        if pole[x][prev_b_coord_y] != 0:
                            not_zero_count +=1
                        prev_b_coord_y += 1
                    if not_zero_count == 1:
                        pole[x][y] = 3
                        pole[prev_b_coord_x][prev_y] = 0
                        vivod(-1, -1)
                        hod_igroka = False

##########################################################################################################################
##########################################################################################################################
##########################################################################################################################


    if not hod_igroka:
        if vozm_ch_d_zabrat:
            if vozm_ch_d_zabrat_vverh:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 4 and prev_ch_coord_x > 1 and pole[x][y] == 0 and prev_ch_coord_y == y:
                    if x < prev_ch_coord_x and x < 7 and pole[x + 1][y] == 1 or x < 7 and pole[x + 1][y] == 3:
                        ch_count = 0
                        not_zero_count = 0
                        prev_x = prev_ch_coord_x
                        for k in range(prev_ch_coord_x, x, -1):
                            ch_count += 1
                            if pole[prev_ch_coord_x][y] != 0:
                                not_zero_count += 1
                            prev_ch_coord_x -= 1
                        if not_zero_count == 2:
                            pole[x][y] = 4
                            pole[prev_x][prev_ch_coord_y] = 0
                            pole[x + 1][y] = 0
                            white_count -= 1
                            vivod(-1, -1)

            if vozm_ch_d_zabrat_vniz:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 4 and prev_ch_coord_x < 7 and pole[x][y] == 0 and prev_ch_coord_y == y:
                    if x > prev_ch_coord_x and pole[x - 1][y] == 1 or pole[x - 1][y] == 3:
                        ch_count = 0
                        not_zero_count = 0
                        prev_x = prev_ch_coord_x
                        for k in range(x, prev_ch_coord_x, -1):
                            ch_count += 1
                            if pole[prev_ch_coord_x][y] != 0:
                                not_zero_count += 1
                            prev_ch_coord_x += 1
                        if not_zero_count == 2:
                            pole[x][y] = 4
                            pole[prev_x][prev_ch_coord_y] = 0
                            pole[x - 1][y] = 0
                            white_count -= 1
                            vivod(-1, -1)

            if vozm_ch_d_zabrat_vlevo:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 4 and prev_ch_coord_y > 1 and pole[x][y] == 0 and prev_ch_coord_x == x:
                    if y < prev_ch_coord_y and y < 7 and pole[x][y + 1] == 1 or y < 7 and pole[x][y + 1] == 3:
                        ch_count = 0
                        not_zero_count = 0
                        prev_y = prev_ch_coord_y
                        for k in range(prev_ch_coord_y, y, -1):
                            ch_count += 1
                            if pole[x][prev_ch_coord_y] != 0:
                                not_zero_count += 1
                            prev_ch_coord_y -= 1
                        if not_zero_count == 2:
                            pole[x][y] = 4
                            pole[prev_ch_coord_x][prev_y] = 0
                            pole[x][y + 1] = 0
                            white_count -= 1
                            vivod(-1, -1)

            if vozm_ch_d_zabrat_vpravo:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 4 and prev_ch_coord_y < 6 and pole[x][y] == 0 and prev_ch_coord_x == x:
                    if y > prev_ch_coord_y and pole[x][y - 1] == 1 or pole[x][y - 1] == 3:
                        ch_count = 0
                        not_zero_count = 0
                        prev_y = prev_ch_coord_y
                        for k in range(y, prev_ch_coord_y, -1):
                            ch_count += 1
                            if pole[x][prev_ch_coord_y] != 0:
                                not_zero_count += 1
                            prev_ch_coord_y += 1
                        if not_zero_count == 2:
                            pole[x][y] = 4
                            pole[prev_ch_coord_x][prev_y] = 0
                            pole[x][y - 1] = 0
                            white_count -= 1
                            vivod(-1, -1)

            vozm_ch_d_zabrat = False
            chernie_proverka()
            if vozm_ch_d_zabrat == False:
                hod_igroka = True
        if vozm_ch_zabrat:
            if vozm_ch_zabrat_vniz:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 2 and prev_ch_coord_x < 6 and (pole[prev_ch_coord_x + 1][y] == 1 or pole[prev_ch_coord_x + 1][y] == 3) and pole[x][y] == 0 and pole[x - 2][y] == 2 and prev_ch_coord_x == x - 2 and prev_ch_coord_y == y:
                    if prev_ch_coord_x == 5 and x - 1 == 6 and x == 7:
                        pole[x][y] = 4
                    else:
                        pole[x][y] = 2
                    pole[x - 2][y] = 0
                    pole[x - 1][y] = 0
                    white_count -= 1
                    vivod(-1, -1)

            if vozm_ch_zabrat_vlevo:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 2 and prev_ch_coord_y > 1 and (pole[prev_ch_coord_x][prev_ch_coord_y - 1] == 1 or pole[prev_ch_coord_x][prev_ch_coord_y - 1] == 3) and pole[x][y] == 0 and pole[prev_ch_coord_x][prev_ch_coord_y - 2] == 0 and prev_ch_coord_x == x and prev_ch_coord_y == y + 2:
                    pole[prev_ch_coord_x][y + 2] = 0
                    pole[x][y + 1] = 0
                    pole[x][y] = 2
                    white_count -= 1
                    vivod(-1, -1)
            if vozm_ch_zabrat_vpravo:
                if pole[prev_ch_coord_x][prev_ch_coord_y] == 2 and prev_ch_coord_y < 6 and (pole[prev_ch_coord_x][prev_ch_coord_y + 1] == 1 or pole[prev_ch_coord_x][prev_ch_coord_y + 1] == 3) and pole[x][y] == 0 and pole[prev_ch_coord_x][prev_ch_coord_y + 2] == 0 and prev_ch_coord_x == x and prev_ch_coord_y == y - 2:
                    pole[prev_ch_coord_x][y - 2] = 0
                    pole[x][y - 1] = 0
                    pole[x][y] = 2
                    white_count -= 1
                    vivod(-1, -1)
            vozm_ch_zabrat = False
            chernie_proverka()
            if vozm_ch_zabrat == False and vozm_ch_d_zabrat == False:
                hod_igroka = True
        chernie_proverka()
        vozmozhnost_chernih_hodit(x, y)
        if black_count == 0:
            messagebox.showinfo(title='Победа белых', message='Победили белые.', icon='info')
            hod_igroka = None
            Start_new()
        if vozmozhnost_chernih_shodit:
            if (pole[prev_ch_coord_x][prev_ch_coord_y] != 0 and prev_ch_coord_y + 1 == y and prev_ch_coord_x == x) or (prev_ch_coord_y - 1 == y and prev_ch_coord_x == x) or (prev_ch_coord_x + 1 == x and prev_ch_coord_y == y):  # Проверяем, сходили ли мы на одну клетку вертикально или горизонтально
                if pole[x][y] == 0 and vozm_ch_zabrat == False and vozm_ch_d_zabrat == False:
                    if pole[prev_ch_coord_x][prev_ch_coord_y] == 2:
                        if x == 7:
                            pole[x][y] = 4
                        else:
                            pole[x][y] = 2
                        pole[prev_ch_coord_x][prev_ch_coord_y] = 0
                        vivod(-1, -1)  # рисуем игровое поле
                        hod_igroka = True
            if pole[prev_ch_coord_x][prev_ch_coord_y] == 4 and pole[x][y] == 0 and vozm_ch_zabrat == False and vozm_ch_d_zabrat == False:
                if prev_ch_coord_x > x and prev_ch_coord_y == y:
                    ch_count = 0
                    not_zero_count = 0
                    prev_x = prev_ch_coord_x
                    for k in range(prev_ch_coord_x, x, -1):
                        ch_count += 1
                        if pole[prev_ch_coord_x][y] != 0:
                            not_zero_count += 1
                        prev_ch_coord_x -= 1
                    if not_zero_count == 1:
                        pole[x][y] = 4
                        pole[prev_x][prev_ch_coord_y] = 0
                        vivod(-1, -1)
                        hod_igroka = True
                if prev_ch_coord_x < x and prev_ch_coord_y == y:
                    ch_count = 0
                    not_zero_count = 0
                    prev_x = prev_ch_coord_x
                    for k in range(prev_ch_coord_x, x):
                        ch_count += 1
                        if pole[prev_ch_coord_x][y] != 0:
                            not_zero_count += 1
                        prev_ch_coord_x += 1
                    if not_zero_count == 1:
                        pole[x][y] = 4
                        pole[prev_x][prev_ch_coord_y] = 0
                        vivod(-1, -1)
                        hod_igroka = True
                if prev_ch_coord_y > y and prev_ch_coord_x == x:
                    ch_count = 0
                    not_zero_count = 0
                    prev_y = prev_ch_coord_y
                    for k in range(prev_ch_coord_y, y, -1):
                        ch_count += 1
                        if pole[x][prev_ch_coord_y] != 0:
                            not_zero_count += 1
                        prev_ch_coord_y -= 1
                    if not_zero_count == 1:
                        pole[x][y] = 4
                        pole[prev_ch_coord_x][prev_y] = 0
                        vivod(-1, -1)
                        hod_igroka = True
                if prev_ch_coord_y < y and prev_ch_coord_x == x:
                    ch_count = 0
                    not_zero_count = 0
                    prev_y = prev_ch_coord_y
                    for k in range(prev_ch_coord_y, y):
                        ch_count += 1
                        if pole[x][prev_ch_coord_y] != 0:
                            not_zero_count += 1
                        prev_ch_coord_y += 1
                    if not_zero_count == 1:
                        pole[x][y] = 4
                        pole[prev_ch_coord_x][prev_y] = 0
                        vivod(-1, -1)
                        hod_igroka = True

izobrazheniya_figur()  # здесь загружаем изображения пешек
novaya_igra()  # начинаем новую игру
vivod(-1, -1)  # рисуем игровое поле
board.bind("<Button-1>", click_event)  # нажатие левой кнопки

mainloop()
