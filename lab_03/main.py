from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QMessageBox
from math import *
import numpy as np
import sys
import time
# import breeze_resources

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 650, 650)
        self.canvas.setScene(self.scene)
        self.scene.window = self
        self.image = QImage(650, 650, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.pen = QPen()
        self.color_line = QColor(Qt.black)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(self.color_line)
        self.line_color.setScene(s)
        self.color_bground = QColor(Qt.white)
        self.line_drawing.clicked.connect(lambda: line_drawing(self))
        self.clean_all.clicked.connect(lambda : clear_all(self))
        self.btn_bg.clicked.connect(lambda: get_color_bg(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.sun_drawing.clicked.connect(lambda: sun_drawing(self))
        self.color_line_like_bg_button.clicked.connect(lambda: color_line_like_bg_color(self))
        self.CDA.setChecked(True)

def round_num(x):
    x += 0.5
    fl_x, int_x = modf(x)
    return int_x
    
# Функция необходимая для изменения интенсивности при использовании алгоритмов Брезенхема
# со сглаживанием и алгоритма Ву
def rgba2rgb(rgb_bg, rgb_color, alpha):
    temp = 1 - alpha
    
    return QColor(temp * rgb_bg[0] + alpha * rgb_color[0], \
                  temp * rgb_bg[1] + alpha * rgb_color[1], \
                  temp * rgb_bg[2] + alpha * rgb_color[2])

# Функция, возвращающая знак числа
def sign(x):
    if x == 0:
        return 0
    else:
        return x / abs(x)

# Алгоритм цифрового дифференциального анализатора
def CDA(window, point_1, point_2):
    point_1[0] = float(point_1[0])
    point_1[1] = float(point_1[1])
    point_2[0] = float(point_2[0])
    point_2[1] = float(point_2[1])
    d_x = abs(point_1[0] - point_2[0])
    d_y = abs(point_1[1] - point_2[1])

    length = max(d_x, d_y)

    if length == 0:
        window.image.setPixel(point_1[0], point_1[1], window.pen.color().rgb())
        return

    dX = (point_2[0] - point_1[0]) / length
    dY = (point_2[1] - point_1[1]) / length

    x = point_1[0] + 0.5 * sign(d_x)
    y = point_1[1] + 0.5 * sign(d_y)

    while (length > 0):
        window.image.setPixel(x, y, window.pen.color().rgba())
        x += dX
        y += dY
        length -= 1

# Алгоритм Брезенхема (целочисленный)
def bresenham_int(window, point_1, point_2):
    if point_1 == point_2:
        window,image.setPixel(point_1[0], point_1[1], window.pen.color().rgb())
        return
    point_1[0] = float(point_1[0])
    point_1[1] = float(point_1[1])
    point_2[0] = float(point_2[0])
    point_2[1] = float(point_2[1])
    d_x = point_2[0] - point_1[0]
    d_y = point_2[1] - point_1[1]
    s_x = sign(d_x)
    s_y = sign(d_y)
    d_x = abs(d_x)
    d_y = abs(d_y)
    x = point_1[0]
    y = point_1[1]

    chng = False

    if d_y > d_x:
        temp = d_x
        d_x = d_y
        d_y = temp
        chng = True

    e = 2 * d_y - d_x
    i = 1

    while (i <= d_x):
        window.image.setPixel(x, y, window.pen.color().rgb())
        if e >= 0:
            if chng != True:
                y += s_y
            else:
                x += s_x
            e -= (2 * d_x)

        if e < 0:
            if chng != True:
                x += s_x
            else:
                y += s_y
            e += (2 * d_y)
        i += 1

# Алгоритм Брезенхема (вещественный)
def bresenham_float(window, point_1, point_2):
    if point_1 == point_2:
        window.image.setPixel(point_1[0], point_1[1], window.pen.color().rgb())
        return
    point_1[0] = float(point_1[0])
    point_1[1] = float(point_1[1])
    point_2[0] = float(point_2[0])
    point_2[1] = float(point_2[1])
    d_x = point_2[0] - point_1[0]
    d_y = point_2[1] - point_1[1]
    s_x = sign(d_x)
    s_y = sign(d_y)
    d_x = abs(d_x)
    d_y = abs(d_y)
    x = point_1[0]
    y = point_1[1]

    chng = False

    if d_y > d_x:
        d_x, d_y = d_y, d_x
        chng = True

    m = d_y / d_x
    e = m - 0.5
    i = 1

    while i <= d_x:
        window.image.setPixel(x, y, window.pen.color().rgb())
        if e >= 0:
            if chng is True:
                x += s_x
            else:
                y += s_y
            e -= 1

        if e < 0:
            if chng is True:
                y += s_y
            else:
                x += s_x
            e += m
        i += 1

# Алгоритм Брезенхема с устранением ступенчатости (со сглаживанием)
def bresenham_smooth(window, point_1, point_2):
    if point_1 == point_2:
        window.image.setPixel(point_1[0], point_1[1], window.pen.color().rgb())
        return

    window.pen.setColor(window.color_line)
    point_1[0] = float(point_1[0])
    point_1[1] = float(point_1[1])
    point_2[0] = float(point_2[0])
    point_2[1] = float(point_2[1])
    d_x = point_2[0] - point_1[0]
    d_y = point_2[1] - point_1[1]
    s_x = sign(d_x)
    s_y = sign(d_y)
    d_x = abs(d_x)
    d_y = abs(d_y)
    x = point_1[0]
    y = point_1[1]

    try:
        m = d_y / d_x
    except ZeroDivisionError:
        m = 0
    
    intense = 1
    change = False

    if d_y > d_x:
        d_x, d_y = d_y, d_x
        change = True
        if m:
            m = 1 / m

    e = intense / 2
    m *= intense
    w = intense - m
    i = 1
    
    color_line = window.color_line.getRgb()
    bg_color = window.color_bground.getRgb()
    
    while i <= d_x:
        window.image.setPixel(x, y, rgba2rgb(bg_color, color_line, e).rgb())
        
        if e <= w:
            if change:
                y += s_y
            else:
                x += s_x
            e += m
        else:
            x += s_x
            y += s_y
            e -= w
        i += 1

# ============================================================================

# Функция, необходимая для отображения пикселя на холсте в алгоритме Ву
def draw_pixel(win, x_coord, y_coord, alpha, change, bg_color, color_line):
    if change:
        win.image.setPixel(y_coord, x_coord, rgba2rgb(bg_color, color_line, alpha).rgb())
    else:
        win.image.setPixel(x_coord, y_coord, rgba2rgb(bg_color, color_line, alpha).rgb())
    
# Алгоритм Ву Шаолиня
def algorithm_wu(win, p1, p2):
    if p1 == p2:
        win.image.setPixel(p1[0], p1[1], win.pen.color().rgb())
        return
    
    change = False
    xb = float(p1[0])
    yb = float(p1[1])
    xe = float(p2[0])
    ye = float(p2[1])
    
    if fabs(ye - yb) > fabs(xe - xb):
        xb, yb = yb, xb
        xe, ye = ye, xe
        change = True
    
    if xe < xb:
        xb, xe = xe, xb
        yb, ye = ye, yb
    
    d_x = xe - xb
    d_y = ye - yb
    grad = d_y / d_x
    
    x = xb
    y = yb
        
    color_line = win.color_line.getRgb()
    bg_color = win.color_bground.getRgb()
    
    while x <= xe:
        draw_pixel(win, x, y + 1, (y - int(y)), change, bg_color, color_line)
        draw_pixel(win, x, y, 1 - (y - int(y)), change, bg_color, color_line)
        y += grad
        x += 1
        
# ============================================================================

# Функция, выводящая линию на холст в зависимости от выбранного алгоритма
def line_drawing(window):
    bx = window.begin_x.text()
    by = window.begin_y.text()
    ex = window.end_x.text()
    ey = window.end_y.text()
    # clear_all(window)
    is_standart = False
    # window.image.fill(window.color_bground)
    if bx != '' and by != '' and ex != '' and ey != '':
        if window.CDA.isChecked():  
            start = time.clock()
            CDA(window, [bx, by], [ex, ey])
            end = time.clock()
        if window.bresenham_int.isChecked():
            start = time.clock()
            bresenham_int(window, [bx, by], [ex, ey])
            end = time.clock()
        if window.bresenham_float.isChecked():
            start = time.clock()
            bresenham_float(window, [bx, by], [ex, ey])
            end = time.clock()
        if window.bresenham_smooth.isChecked():
            start = time.clock()
            bresenham_smooth(window, [bx, by], [ex, ey])
            end = time.clock()
        if window.algorithm_wu.isChecked():
            start = time.clock()
            algorithm_wu(window, [bx, by], [ex, ey])
            end = time.clock()
        if window.librarian.isChecked():
            is_standart = True
            start = time.clock()
            window.scene.addLine(float(bx), float(by), float(ex), float(ey), window.pen)
            end = time.clock()
        if not is_standart:
            pix = QPixmap(650, 650)
            pix.convertFromImage(window.image)
            window.scene.addPixmap(pix)
    
        window.time_label.setText("{0:.4f} msc".format((end - start) * 1000))
    else:
        msg = QMessageBox()
        msg.setGeometry(450, 450, 800, 600)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Некорректные данные для построения линии!")
        msg.setWindowTitle("Ошибка!")
        msg.exec_()

# Функция, выводящая "солнце" на холст в зависимости от выбранного алгоритма
def sun_drawing(window):
    rad = window.spin_rad.text()
    spin = window.spin_angle.text()
    bx = 325
    by = 325
    # clear_all(window)
    # window.image.fill(window.color_bground)
    is_standart = False
    if rad != '' and spin != '' and spin != '0' and float(spin) > 0 and float(spin) <= 360:
        rad = float(rad)
        spin = float(spin)
        for i in np.arange(0, 360, spin):
            ex = cos(radians(i)) * rad + 325
            ey = sin(radians(i)) * rad + 325
            if window.CDA.isChecked():
                start = time.clock()
                CDA(window, [bx, by], [ex, ey])
                end = time.clock()
            if window.bresenham_int.isChecked():
                start = time.clock()
                bresenham_int(window, [bx, by], [ex, ey])
                end = time.clock()
            if window.bresenham_float.isChecked():
                start = time.clock()
                bresenham_float(window, [bx, by], [ex, ey])
                end = time.clock()
            if window.bresenham_smooth.isChecked():
                start = time.clock()
                bresenham_smooth(window, [bx, by], [ex, ey])
                end = time.clock()
            if window.algorithm_wu.isChecked():
                start = time.clock()
                algorithm_wu(window, [bx, by], [ex, ey])
                end = time.clock()
            if window.librarian.isChecked():
                is_standart = True
                start = time.clock()
                window.scene.addLine(float(bx), float(by), float(ex), float(ey), window.pen)
                end = time.clock()
    
        if not is_standart:
            pix = QPixmap(650, 650)
            pix.convertFromImage(window.image)
            window.scene.addPixmap(pix)
    
        window.time_label.setText("{0:.4f} msc".format((end - start) * 1000))
    else:
        msg = QMessageBox()
        msg.setGeometry(450, 450, 800, 600)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Некорректные данные для построения 'солнца'!")
        msg.setWindowTitle("Ошибка!")
        msg.exec_()

# Функция, меняющая цвет кисти, которой рисуется линия, на цвет фона
def color_line_like_bg_color(window):
    color = window.color_bground
    window.color_line = color
    window.pen.setColor(color)
    s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
    s.setBackgroundBrush(color)
    window.line_color.setScene(s)
#    window.hide()
    window.show()

# Функция, в которой выбирается цвет фона с Qt виджета
def get_color_bg(window):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.white, title='Цвет фона')
    if color.isValid():
        window.color_bground = color
        window.image.fill(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        window.bg_color.setScene(s)
#        window.scene.setBackgroundBrush(color)

# Функция, в которой выбирается цвет линии с Qt виджета
def get_color_line(window):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.black, title='Цвет линии')
    if color.isValid():
        window.color_line = color
        window.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        window.line_color.setScene(s)
        
# Функция очистки холста	
def clear_all(window):
    window.image.fill(Qt.color0)
    window.scene.clear()

# Главная функция
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
    
    
