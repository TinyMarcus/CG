from tkinter import *
from pandas import *
import funcs

def clear():
    '''Clearing screen'''
    if len(array_points) > 0:
        try:
            for i in range(len(array_points)):
                canvas.delete(array_points[i])
        except:
            errors(' Точек нет!')
        try:
            canvas.delete(triangle_a)
            canvas.delete(in_circle_a)
        except:
            print('')

def errors(error_text):
    '''Outputing errors'''
    error = Tk()
    error.title('Ошибка!')
    error.geometry('500x80')

    lb_error_no_pts = Label(error, text = error_text, fg = 'red')
    lb_error_no_pts.pack(expand = 1)
    error.bind('<Escape>', lambda event: error.destroy())

    error.mainloop()

def table_pts(all_points):
    '''Outputing table with all points'''
    global table

    if len(all_points) > 0:
        size = '350x' + str(len(all_points) * 50)

        table = Tk()
        table.title('Таблица точек')
        table.geometry(size)

        tb = DataFrame(all_points, columns = ['x', 'y'])
        lb = Label(table, text = str(tb))
        lb.place(x = 0, y = 0)
        table.bind('<Escape>', lambda event: table.destroy())

        table.mainloop()
    else:
        errors('Таблица пуста!')

def create_pts(k, all_points):
    '''Building and drawing all points'''

    for i in range(len(all_points)):
        pts_text = canvas.create_text((540 + all_points[i][0] * k), 320 - all_points[i][1] * k,
                                       text = (str(i) + '.' + '(' + str(all_points[i][0]) + ', '
                                       + str(all_points[i][1]) + ')'), fill = 'black')
        pts = canvas.create_oval((500 + all_points[i][0] * k - 5), (300 - all_points[i][1] * k - 5),
                                 (500 + all_points[i][0] * k + 5),
                                 (300 - all_points[i][1] * k + 5), outline = 'red', fill = 'red', width = 1)
        array_points.append(pts)
        array_points.append(pts_text)

def get_pts(all_points):
    '''Drawing points and triangle with square'''
    global in_circle_a
    global triangle_a
    global pts
    global answer
    global k
    global text_x
    global text_y

    if len(all_points) > 2:
        calc_pts, trian_square = funcs.find_answer(all_points)
        #print(calc_pts)

        k = 50
        max = -1000000

        if 0 not in calc_pts:
            for i in range(len(calc_pts)):
                for j in range(len(calc_pts[i])):
                    #print(abs(calc_pts[i][j]))
                    if abs(calc_pts[i][j]) > max:
                        max = abs(calc_pts[i][j])


            k = 270 / max
            #if (max >= 500):
            #    k = 0.3
            #elif (max >= 20 and max <= 40):
            #    k = 3
            #elif (max <= 7):
            #    k = 30

            #print(k, max)

        if 0 not in calc_pts:
            answer = Tk()
            answer.title('Результаты')
            answer.geometry('350x200')
            answer.resizable(False, False)

            center_ic = funcs.center_in_circle(calc_pts)
            radius_ic = funcs.find_radius_in_circle(calc_pts)
            #print(radius_ic)

            x1 = 500 + (center_ic[0] - radius_ic) * k
            y1 = 300 - (center_ic[1] - radius_ic) * k
            x2 = 500 + (center_ic[0] + radius_ic) * k
            y2 = 300 - (center_ic[1] + radius_ic) * k

            #print(center_ic[0], i, x2, y2)

            #print(x1, y1, x2, y2)

            triangle_x1 = 500 + calc_pts[0][0] * k
            triangle_y1 = 300 - calc_pts[0][1] * k
            triangle_x2 = 500 + calc_pts[1][0] * k
            triangle_y2 = 300 - calc_pts[1][1] * k
            triangle_x3 = 500 + calc_pts[2][0] * k
            triangle_y3 = 300 - calc_pts[2][1] * k

            a, b, c = funcs.sides_len(calc_pts[0], calc_pts[1], calc_pts[2])

            triangle_a = canvas.create_polygon([triangle_x1, triangle_y1],
                                               [triangle_x2, triangle_y2],
                                               [triangle_x3, triangle_y3], fill = 'green')
            #print(x1[0])

            in_circle_a = canvas.create_oval(x1[0], y1[0], x2[0], y2[0], outline = 'blue',
                                             fill = 'blue', width = 2)
            lb = Label(answer, text = 'Результирующие точки')
            lb.place(x = 90, y = 10)

            indexes = [0, 0, 0]

            for i in range(len(calc_pts)):
                indexes[i] = all_points.index(calc_pts[i])

            in_circle = funcs.square_in_circle(calc_pts[0], calc_pts[1], calc_pts[2])
            tr_square = funcs.triangle_square(a, b, c)

            table_result_points = DataFrame(calc_pts, columns = ['x', 'y'], index = indexes)
            res_points = Label(answer, text = str(table_result_points))
            res_points.place(x = 150, y = 30)

            lb_square_in_circle = Label(answer, text = 'Площадь вписанной окружности: ')
            lb_square_in_circle.place(x = 10, y = 130)
            square_inwr_circle = Label(answer, text = str(round(in_circle, 3)))
            square_inwr_circle.place(x = 270, y = 130)

            lb_square_triangle = Label(answer, text = 'Площадь треугольника: ')
            lb_square_triangle.place(x = 10, y = 150)
            square_tr = Label(answer, text = str(round(tr_square, 3)))
            square_tr.place(x = 270, y = 150)
            square_tr = 0

            lb_square_difference = Label(answer, text = 'Разность площадей: ')
            lb_square_difference.place(x = 10, y = 170)
            square_diff = Label(answer, text = str(round(abs(tr_square - in_circle), 3)))
            square_diff.place(x = 270, y = 170)

            create_pts(k, all_points)
            answer.bind('<Escape>', lambda event: answer.destroy())

            answer.mainloop()
        else:
            create_pts(k, all_points)
            errors('Треугольник вырожденный!')
    elif len(all_points) > 0 and len(all_points) < 3:
        create_pts(50, all_points)
        errors('Недостаточное количество точек для построения треугольника!')

def input_data(points_array):
    '''Filtering information that was inputed'''
    points_array = points_array.split(';')

    for i in range(len(points_array)):
        if points_array[i] != '':
            if len(points_array[i].split(' ')) <= 1 and len(points_array[i].split(',')) == 2:
                if points_array[i].split(',')[0] != '' and points_array[i].split(',')[1] != '' \
                and [float(points_array[i].split(',')[0]), float(points_array[i].split(',')[1])] \
                not in all_points:
                    all_points.append([float(points_array[i].split(',')[0]), float(points_array[i].split(',')[1])])
    q = -500

    # for x in range(25):
    #     k = x * 40
    #     canvas.create_line(k + 20, 600, k + 20, 0, width = 1, fill = 'grey')
    #     q += 40
    #
    # q = -300
    #
    # for y in range(15):
    #     k = y * 40
    #     canvas.create_line(0, k + 20, 1000, k + 20, width = 1, fill = 'grey')
    #     q += 40

    canvas.create_line(500, 0, 500, 600, width = 2, arrow = FIRST, fill = 'black')
    canvas.create_line(0, 300, 1000, 300, width = 2, arrow = LAST, fill = 'black')
    canvas.create_text(490, 310, text = '0', fill = 'black')

def start(points_array):
    '''Calculating triangle'''
    canvas.delete('all')
    input_data(points_array)
    get_pts(all_points)

def delete_all_pts():
    '''Deleting all points and clearing the screen'''
    clear()
    all_points.clear()

def add_and_reset(points_array):
    '''Adding points and recalculating'''
    if points_array != '':
        clear()
        start(points_array)
    else:
        errors('Вы ничего не ввели!')

def delete_pts(points_array):
    '''Deleting uneccessary points'''
    #if points_array != '':
    #print(len(points_array))
    if len(points_array) > 1:
        points_array = list(points_array.split(','))
        points_arr = []
        points_arr.append([float(points_array[0]), float(points_array[1])])
        count = 0

        #print(points_arr)
        for i in range(len(points_arr)):
            if points_arr[i] in all_points:
                all_points.remove(points_arr[i])
                count += 1
        if count > 0:
            clear()
            get_pts(all_points)
        else:
            errors('Такой точки нет!')
    else:
        errors('Вы ничего не ввели!')

def edit_points(points_array):
    '''Editing points by user'''
    #print(len(points_array))
    if len(points_array) > 5:
        points_array = list(points_array.split(':'))
        delete_array = []
        for i in range(len(points_array)):
            if points_array[i] != '':
                delete_array.append([float(points_array[i].split(',')[0]),
                                     float(points_array[i].split(',')[1])])
        if delete_array[0] in all_points:
            all_points[all_points.index(delete_array[0])] = delete_array[1]
            clear()
            get_pts(all_points)
        else:
            errors('Такой точки нет!')
    else:
        errors('Вы ничего не ввели!')

# ==============================================================================

def key_input(var):
    '''Filtering inputing in Entry windows'''

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

# ==============================================================================

def main():
    '''Main function'''

    root = Tk()
    root.title('Lab #1 by Ilyasov')
    root.geometry('1280x600')
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
    s_10 = StringVar()
    s_11 = StringVar()
    s_12 = StringVar()

    s_1.trace('w', lambda nm, idx, mode, var = s_1: key_input(var))
    s_2.trace('w', lambda nm, idx, mode, var = s_2: key_input(var))
    s_3.trace('w', lambda nm, idx, mode, var = s_3: key_input(var))
    s_4.trace('w', lambda nm, idx, mode, var = s_4: key_input(var))
    s_5.trace('w', lambda nm, idx, mode, var = s_5: key_input(var))
    s_6.trace('w', lambda nm, idx, mode, var = s_6: key_input(var))
    s_7.trace('w', lambda nm, idx, mode, var = s_7: key_input(var))
    s_8.trace('w', lambda nm, idx, mode, var = s_8: key_input(var))
    s_9.trace('w', lambda nm, idx, mode, var = s_9: key_input(var))
    s_10.trace('w', lambda nm, idx, mode, var = s_10: key_input(var))
    s_11.trace('w', lambda nm, idx, mode, var = s_11: key_input(var))
    s_12.trace('w', lambda nm, idx, mode, var = s_12: key_input(var))

    global canvas
    canvas = Canvas(root, width = 1000, height = 600, bg = 'white')
    canvas.pack(side = 'left')

    global all_points
    all_points = []

    global array_points
    array_points = []

    # q = -500
    #
    # for x in range(25):
    #     k = x * 40
    #     canvas.create_line(k + 20, 600, k + 20, 0, width = 1, fill = 'grey')
    #     q += 40
    #
    # q = -300
    #
    # for y in range(15):
    #     k = y * 40
    #     canvas.create_line(0, k + 20, 1000, k + 20, width = 1, fill = 'grey')
    #     q += 40


    canvas.create_line(500, 0, 500, 600, width = 2, arrow = FIRST, fill = 'black')
    canvas.create_line(0, 300, 1000, 300, width = 2, arrow = LAST, fill = 'black')
    canvas.create_text(490, 310, text = '0', fill = 'black')

    label_points = Label(root, text = 'X')
    label_points.place(x = 1060, y = 10)

    label_points = Label(root, text = 'Y')
    label_points.place(x = 1200, y = 10)

    entry_pts_x1 = Entry(root, width = 11, textvariable = s_1)
    entry_pts_x1.place(x = 1020, y = 30)

    entry_pts_y1 = Entry(root, width = 11, textvariable = s_2)
    entry_pts_y1.place(x = 1160, y = 30)

    entry_pts_x2 = Entry(root, width = 11, textvariable = s_3)
    entry_pts_x2.place(x = 1020, y = 60)

    entry_pts_y2 = Entry(root, width = 11, textvariable = s_4)
    entry_pts_y2.place(x = 1160, y = 60)

    entry_pts_x3 = Entry(root, width = 11, textvariable = s_5)
    entry_pts_x3.place(x = 1020, y = 90)

    entry_pts_y3 = Entry(root, width = 11, textvariable = s_6)
    entry_pts_y3.place(x = 1160, y = 90)

    button_find_result = Button(root, text = 'Найти', width = 26)
    button_find_result.bind('<Button-1>', lambda event: start(str(entry_pts_x1.get()) + ',' + str(entry_pts_y1.get()) + ';' + str(entry_pts_x2.get())
    + ',' + str(entry_pts_y2.get()) + ';' + str(entry_pts_x3.get()) + ',' + str(entry_pts_y3.get())))
    button_find_result.place(x = 1020, y = 120)

    button_add_pts = Button(root, text = 'Добавить точки', width = 26)
    button_add_pts.bind('<Button-1>', lambda event: add_and_reset(str(entry_pts_x1.get()) + ',' + str(entry_pts_y1.get()) + ';' + str(entry_pts_x2.get())
    + ',' + str(entry_pts_y2.get()) + ';' + str(entry_pts_x3.get()) + ',' + str(entry_pts_y3.get())))
    button_add_pts.place(x = 1020, y = 160)

    button_tab = Button(root, text = 'Вывести таблицу значений', width = 26)
    button_tab.bind('<Button-1>', lambda event: table_pts(all_points))
    button_tab.place(x = 1020, y = 200)

    button_clean = Button(root, text = 'Удалить все точки', width = 26)
    button_clean.bind('<Button-1>', lambda event: delete_all_pts())
    button_clean.place(x = 1020, y = 240)

    label_points = Label(root, text = '_________________________________')
    label_points.place(x = 1020, y = 275)

    entry_pts_x = Entry(root, width = 11, textvariable = s_7)
    entry_pts_x.place(x = 1020, y = 330)

    entry_pts_y = Entry(root, width = 11, textvariable = s_8)
    entry_pts_y.place(x = 1160, y = 330)

    label_points = Label(root, text = 'X')
    label_points.place(x = 1060, y = 310)

    label_points = Label(root, text = 'Y')
    label_points.place(x = 1200, y = 310)

    button_delete = Button(root, text = 'Удалить точку', width = 26)
    button_delete.bind('<Button-1>', lambda event: delete_pts(str(entry_pts_x.get())
                       + ',' + str(entry_pts_y.get())))
    button_delete.place(x = 1020, y = 360)

    label_points = Label(root, text = '_________________________________')
    label_points.place(x = 1020, y = 390)

    label_points = Label(root, text = 'Старые значения: ')
    label_points.place(x = 1020, y = 420)

    label_points = Label(root, text = 'X')
    label_points.place(x = 1060, y = 440)

    label_points = Label(root, text = 'Y')
    label_points.place(x = 1200, y = 440)

    entry_points_x4 = Entry(root, width = 11, textvariable = s_9)
    entry_points_x4.place(x = 1020, y = 460)

    entry_points_y4 = Entry(root, width = 11, textvariable = s_10)
    entry_points_y4.place(x = 1160, y = 460)

    label_points = Label(root, text = 'Новые значения: ')
    label_points.place(x = 1020, y = 490)

    label_points = Label(root, text = 'X')
    label_points.place(x = 1060, y = 510)

    label_points = Label(root, text='Y')
    label_points.place(x = 1200, y = 510)

    entry_points_x5 = Entry(root, width = 11, textvariable = s_11)
    entry_points_x5.place(x = 1020, y = 530)

    entry_points_y5 = Entry(root, width = 11, textvariable = s_12)
    entry_points_y5.place(x = 1160, y = 530)

    btn_add = Button(root, text = 'Редактировать точку', width = 26)
    btn_add.bind('<Button-1>', lambda event: edit_points(str(entry_points_x4.get()) + ',' + str(entry_points_y4.get()) +
                 ':' + str(entry_points_x5.get()) + ',' + str(entry_points_y5.get())))
    btn_add.place(x = 1020, y = 560)
    root.bind('<Escape>', lambda event: root.destroy())

    root.mainloop()

if __name__ == '__main__':
    main()
