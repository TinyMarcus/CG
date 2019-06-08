from tkinter import *
from math import *

fr = -0.70346742249839
to = 0.70346742249839

def errors(error_text):
    error = Tk()
    error.title('Ошибка!')
    error.geometry('300x80')

    lb_error_no_pts = Label(error, text = error_text, fg = 'red')
    lb_error_no_pts.pack(expand = 1)
    error.bind('<Escape>', lambda event: error.destroy())

    error.mainloop()

def find_dots(fr, to):
    # for i in range(len(main_arr)):
        # canvas.delete(main_arr[i])
    canvas.delete("all")
    points_array_parab = []
    points_array_plus_exp = []
    points_array_minus_exp = []
    points_array_result = []
    x = fr

    while (x <= to):
        x_par = x * 100
        y_par = 100 * x**2
        if x <= 0:
            y_pl_exp = exp(x)
            points_array_plus_exp.append([(500 + 100 * x), (300 - 100 * y_pl_exp)])
        if x >= 0:
            y_min_exp = exp(-x)
            points_array_minus_exp.append([(500 + 100 * x), (300 - 100 * y_min_exp)])
        points_array_parab.append([(500 + x_par), (300 - y_par)])
        x += 0.0005
    for i in range(len(points_array_parab)):
        main_arr.append(points_array_parab[i])
    for i in range(len(points_array_plus_exp)):
        main_arr.append(points_array_plus_exp[i])
    for i in range(len(points_array_minus_exp)):
        main_arr.append(points_array_minus_exp[i])
    # main_arr.append(points_array_parab)
    # points_array_minus_exp.reverse()
    # points_array_plus_exp.reverse()
    # main_arr.append(points_array_minus_exp)
    # main_arr.append(points_array_plus_exp)
    # canvas.create_polygon(main_arr, fill = 'blue', outline = 'blue', smooth = 1)

def draw_graphic():
    canvas.delete("all")
    canvas.create_polygon(main_arr, fill = 'blue', outline = 'blue', smooth = 1)

def replace():
    global undo_arr
    undo = []

    for i in main_arr:
        undo.append([i[0], i[1]])
    dx = replace_entry_dx.get()
    dy = replace_entry_dy.get()

    if dx != '' and dy != '':
        dx = float(dx)
        dy = float(dy)
        for i in range(len(main_arr)):
            main_arr[i][0] += dx
            main_arr[i][1] -= dy

        undo_arr = undo
        draw_graphic()
    else:
        errors("Вы не все ввели!")

def rotate():
    global undo_arr
    undo = []

    for i in main_arr:
        undo.append([i[0], i[1]])

    undo_arr = main_arr

    angle = rotate_entry_angle.get()
    x = rotate_entry_x.get()
    y = rotate_entry_y.get()

    if x != '' and y != '' and angle != '':
        angle = radians(float(angle))
        x = float(x) + 500
        y = float(y) + 300
        for i in range(len(main_arr)):
            n_y = y + (main_arr[i][1] - y) * cos(angle) - (main_arr[i][0] - x) * sin(angle)
            n_x = x + (main_arr[i][0] - x) * cos(angle) + (main_arr[i][1] - y) * sin(angle)
            main_arr[i][0] = n_x
            main_arr[i][1] = n_y

        undo_arr = undo
        draw_graphic()
    else:
        errors("Вы ввели не все данные!")

def scale():
    global undo_arr
    undo = []

    for i in main_arr:
        undo.append([i[0], i[1]])
    undo_arr = main_arr
    xm = scale_entry_x.get()
    ym = scale_entry_y.get()
    kx = scale_entry_kx.get()
    ky = scale_entry_ky.get()

    if xm != '' and ym != '' and kx != '' and ky != '':
        xm = float(xm) + 500
        ym = float(ym) + 300
        kx = float(kx)
        ky = float(ky)
        for dot in main_arr:
            dot[0] = (dot[0] * kx + (1 - kx) * xm)
            dot[1] = (dot[1] * ky + (1 - ky) * ym)
        undo_arr = undo
        draw_graphic()
    else:
        errors("Вы ввели не все данные!")

def undo():
    global main_arr, undo_arr
    main_arr = undo_arr
    draw_graphic()

def discard():
    global main_arr
    main_arr = []
    canvas.delete("all")
    find_dots(fr, to)
    draw_graphic()

def key_input(var):
    new = var.get()
    check = False
    FindDot = False
    FindSign = False
    FindZero = False

    for i in range(len(new)):
        if (i != 0 and new[i] in "+-"):
            FindSign = True
        if (not FindDot and i != 0 and new[i] == '0' and new[0] == '0') or\
           (not FindDot and i > 1 and new[i] == '0' and new[0] in '+-' and\
            new[1] == '0'):
            FindZero = True
        else:
            FindZero = False
        if (not (new[i] in "1234567890-+.")) or\
           (i > 0 and new[i] in "+-." and new[i-1] in "+-.") or\
           (FindDot and new[i] == '.') or (FindSign and new[i] in '+-') or\
           (FindZero and new[i] == '0'):
            check = True
            break
        #if new == '-0':
        #    new == 0
        if len(new) == 1 and new[0] == '+':
            break
        if new[i] == '.':
            FindDot = True
        if new[i] in '+-':
            FindDot = False
        if new[i] == '-' or new[i] == '+':
            FindSign = True
    if new == "" or new == "-" or not check:
        key_input.old = new
    else:
        var.set(key_input.old)
key_input.old = ""

def main():
    global graph
    global undo_arr
    undo_arr = []
    global main_arr
    main_arr = []
    root = Tk()
    root.title('Lab #2 by Ilyasov')
    root.geometry('1200x600')
    root.resizable(False, False)

    s_1 = StringVar()
    s_2 = StringVar()
    s_3 = StringVar()
    s_4 = StringVar()
    s_5 = StringVar()
    s_6 = StringVar()
    s_7 = StringVar()
    s_8 = StringVar()
    s_9 = StringVar()

    s_1.trace('w', lambda nm, idx, mode, var = s_1: key_input(var))
    s_2.trace('w', lambda nm, idx, mode, var = s_2: key_input(var))
    s_3.trace('w', lambda nm, idx, mode, var = s_3: key_input(var))
    s_4.trace('w', lambda nm, idx, mode, var = s_4: key_input(var))
    s_5.trace('w', lambda nm, idx, mode, var = s_5: key_input(var))
    s_6.trace('w', lambda nm, idx, mode, var = s_6: key_input(var))
    s_7.trace('w', lambda nm, idx, mode, var = s_7: key_input(var))
    s_8.trace('w', lambda nm, idx, mode, var = s_8: key_input(var))
    s_9.trace('w', lambda nm, idx, mode, var = s_9: key_input(var))

    global canvas
    canvas = Canvas(root, width = 1000, height = 600, bg = 'white')
    canvas.pack(side = 'left')

    find_dots(fr, to)
    draw_graphic()

    dx = DoubleVar()
    dx = ''
    dy = DoubleVar()
    dy = ''
    global replace_entry_dx
    global replace_entry_dy
    replace_label_dx = Label(root, text = 'dx:')
    replace_label_dx.place(x = 1005, y = 20)
    replace_entry_dx = Entry(root, width = 17, textvariable = s_1)
    replace_entry_dx.place(x = 1050, y = 20)

    replace_label_dy = Label(root, text = 'dy:')
    replace_label_dy.place(x = 1005, y = 50)
    replace_entry_dy = Entry(root, width = 17, textvariable = s_2)
    replace_entry_dy.place(x = 1050, y = 50)

    replace_button = Button(root, text = 'Переместить', width = 19, command = replace)
    replace_button.place(x = 1010, y = 80)

    label_line = Label(root, text = '___________________________')
    label_line.place(x = 1005, y = 120)

    global scale_entry_x
    global scale_entry_y
    global scale_entry_kx
    global scale_entry_ky
    xm = DoubleVar()
    xm = ''
    ym = DoubleVar()
    ym = ''
    kx = DoubleVar()
    kx = ''
    ky = DoubleVar()
    ky = ''
    scale_label_x = Label(root, text = 'xm:')
    scale_label_x.place(x = 1005, y = 160)
    scale_entry_x = Entry(root, width = 17, textvariable = s_3)
    scale_entry_x.place(x = 1050, y = 160)

    scale_label_y = Label(root, text = 'ym:')
    scale_label_y.place(x = 1005, y = 190)
    scale_entry_y = Entry(root, width = 17, textvariable = s_4)
    scale_entry_y.place(x = 1050, y = 190)

    scale_label_kx = Label(root, text = 'kx:')
    scale_label_kx.place(x = 1005, y = 220)
    scale_entry_kx = Entry(root, width = 17, textvariable = s_5)
    scale_entry_kx.place(x = 1050, y = 220)

    scale_label_ky = Label(root, text = 'ky:')
    scale_label_ky.place(x = 1005, y = 250)
    scale_entry_ky = Entry(root, width = 17, textvariable = s_6)
    scale_entry_ky.place(x = 1050, y = 250)

    scale_button = Button(root, text = 'Масштабировать', width = 19, command = scale)
    scale_button.place(x = 1010, y = 280)

    label_line = Label(root, text = '___________________________')
    label_line.place(x = 1005, y = 320)

    angle = DoubleVar()
    angle = ''
    x = DoubleVar()
    x = ''
    y = DoubleVar()
    y = ''
    global rotate_entry_x
    global rotate_entry_y
    global rotate_entry_angle
    rotate_label_x = Label(root, text = 'x:')
    rotate_label_x.place(x = 1005, y = 360)
    rotate_entry_x = Entry(root, width = 17, textvariable = s_7)
    rotate_entry_x.place(x = 1050, y = 360)

    rotate_label_y = Label(root, text = 'y:')
    rotate_label_y.place(x = 1005, y = 390)
    rotate_entry_y = Entry(root, width = 17, textvariable = s_8)
    rotate_entry_y.place(x = 1050, y = 390)

    rotate_label_angle = Label(root, text = 'Угол:')
    rotate_label_angle.place(x = 1005, y = 420)
    rotate_entry_angle = Entry(root, width = 17, textvariable = s_9)
    rotate_entry_angle.place(x = 1050, y = 420)

    rotate_button = Button(root, text = 'Повернуть', width = 19, command = rotate)
    rotate_button.place(x = 1010, y = 450)

    label_line = Label(root, text = '___________________________')
    label_line.place(x = 1005, y = 490)

    clear_button = Button(root, text = 'Шаг назад', width = 19, command = undo)
    clear_button.place(x = 1010, y = 520)

    undo_button = Button(root, text = 'Сбросить', width = 19, command = discard)
    undo_button.place(x = 1010, y = 560)

    root.bind('<Escape>', lambda event: root.destroy())
    root.mainloop()

if __name__ == '__main__':
    main()
