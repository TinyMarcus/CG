from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 651, 651)
        self.mainview.setScene(self.scene)
        self.image = QImage(651, 651, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        
        self.bground_color = QColor(Qt.white)
        self.line_color = QColor(Qt.black)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(self.line_color)
        self.ln_color.setScene(s)
        self.draw_once.clicked.connect(lambda: draw_once(self))
        self.clean_all.clicked.connect(lambda: clear_all(self))
        self.btn_bground.clicked.connect(lambda: get_color_bground(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.draw_centr.clicked.connect(lambda: draw_centr(self))
        self.circle.clicked.connect(lambda: switch_to_circle(self))
        self.ellips.clicked.connect(lambda: switch_to_ellips(self))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.what)
        layout.addWidget(self.other)
        self.centr_x.setText("325")
        self.centr_y.setText("325")        
        self.color_line_like_bg_button.clicked.connect(lambda: color_line_like_bg_color(self))
        self.setLayout(layout)
        self.circle.setChecked(True)
        self.canon.setChecked(True)
        self.a.setDisabled(1)
        self.b.setDisabled(1)        
        
        #if (self.circle.isEnabled(0) == True):
        #    
        #    self.rad.setDisabled(0)            
        #elif (self.ellips.isEnabled() == True):
        #    self.rad.setDisabled(1)
        #    self.a.setDisabled(0)
        #    self.b.setDisabled(0)            

def round_num(x):
    x += 0.5
    x = int(x)
    return x

def switch_to_circle(window):
    window.rad.setDisabled(0)
    window.a.setDisabled(1)
    window.b.setDisabled(1)

def switch_to_ellips(window):
    window.rad.setDisabled(1)
    window.a.setDisabled(0)
    window.b.setDisabled(0)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def circle_canon(window, cx, cy, r):
    for x in range(0, r + 1, 1):
        y = round(sqrt(r ** 2 - x ** 2))
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())

    for y in range(0, r + 1, 1):
        x = round(sqrt(r ** 2 - y ** 2))
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())


def circle_param(window, cx, cy, r):
    l = round(pi * r / 2)  # длина четврети окружности
    l = int(l)
    for i in range(0, l + 1, 1):
        x = int(round(r * cos(i / r)))
        y = int(round(r * sin(i / r)))
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())

def circle_brez(window, cx, cy, r):
    x = 0   # задание начальных значений
    y = r
    d = 2 - 2 * r   # значение D(x,y)  при (0,R)
    while y >= 0:
        # высвечивание текущего пиксела
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())

        if d < 0:  # пиксель лежит внутри окружности
            buf = 2 * d + 2 * y - 1
            x += 1

            if buf <= 0:  # горизонтальный шаг
                d = d + 2 * x + 1
            else:  # диагональный шаг
                y -= 1
                d = d + 2 * x - 2 * y + 2

            continue

        if d > 0:  # пиксель лежит вне окружности
            buf = 2 * d - 2 * x - 1
            y -= 1

            if buf > 0:  # вертикальный шаг
                d = d - 2 * y + 1
            else:  # диагональный шаг
                x += 1
                d = d + 2 * x - 2 * y + 2

            continue

        if d == 0.0:  # пиксель лежит на окружности
            x += 1   # диагональный шаг
            y -= 1
            d = d + 2 * x - 2 * y + 2


def circle_middle(window, cx, cy, r):
    x = 0  # начальные значения
    y = r
    p = 5 / 4 - r  # (x + 1)^2 + (y - 1/2)^2 - r^2
    while True:
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())

        window.image.setPixel(cx - y, cy + x, window.pen.color().rgb())
        window.image.setPixel(cx + y, cy - x, window.pen.color().rgb())
        window.image.setPixel(cx - y, cy - x, window.pen.color().rgb())
        window.image.setPixel(cx + y, cy + x, window.pen.color().rgb())

        x += 1

        if p < 0:  # средняя точка внутри окружности, ближе верхний пиксел, горизонтальный шаг
            p += 2 * x + 1
        else:   # средняя точка вне окружности, ближе диагональный пиксел, диагональный шаг
            p += 2 * x - 2 * y + 5
            y -= 1

        if x > y:
            break


def ellips_canon(window, cx, cy, a, b):
    a = int(a)
    b = int(b)
    
    if a != 0 and b != 0:
        for x in range(0, a + 1, 1):
            y = round(b * sqrt(1.0 - x ** 2 / a / a))
            window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
            window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
            window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
            window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())

        for y in range(0, b + 1, 1):
            x = round(a * sqrt(1.0 - y ** 2 / b / b))
            window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
            window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
            window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
            window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())
    else:
        return


def ellips_param(window, cx, cy, a, b):
    m = max(a, b)
    l = round(pi * m / 2)
    l = int(l)
    for i in range(0, l + 1, 1):
        x = round(a * cos(i / m))
        y = round(b * sin(i / m))
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())


def ellips_brez(window, cx, cy, a, b):
    x = 0  # начальные значения
    y = b
    a = a ** 2
    d = round(b * b / 2 - a * b * 2 + a / 2)
    b = b ** 2
    while y >= 0:
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())
        if d < 0:  # пиксель лежит внутри эллипса
            buf = 2 * d + 2 * a * y - a
            x += 1
            if buf <= 0:  # горизотальный шаг
                d = d + 2 * b * x + b
            else:  # диагональный шаг
                y -= 1
                d = d + 2 * b * x - 2 * a * y + a + b

            continue

        if d > 0:  # пиксель лежит вне эллипса
            buf = 2 * d - 2 * b * x - b
            y -= 1

            if buf > 0:  # вертикальный шаг
                d = d - 2 * y * a + a
            else:  # диагональный шаг
                x += 1
                d = d + 2 * x * b - 2 * y * a + a + b

            continue

        if d == 0.0:  # пиксель лежит на окружности
            x += 1  # диагональный шаг
            y -= 1
            d = d + 2 * x * b - 2 * y * a + a + b

def ellips_middle(window, cx, cy, a, b):
    x = 0   # начальные положения
    y = b
    p = b * b - a * a * b + 0.25 * a * a   # начальное значение параметра принятия решения в области tg<1
    while 2 * (b ** 2) * x < 2 * a * a * y:  # пока тангенс угла наклона меньше 1
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())

        x += 1

        if p < 0:  # средняя точка внутри эллипса, ближе верхний пиксел, горизонтальный шаг
            p += 2 * b * b * x + b * b
        else:   # средняя точка вне эллипса, ближе диагональный пиксел, диагональный шаг
            y -= 1
            p += 2 * b * b * x - 2 * a * a * y + b * b

    #p += b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
    p += 3/4 * (a * a + b * b) - b * b * x - a * a * y
    # начальное значение параметра принятия решения в области tg>1 в точке (х + 0.5, y - 1) полседнего положения

    while y >= 0:
        window.image.setPixel(cx - x, cy + y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx - x, cy - y, window.pen.color().rgb())
        window.image.setPixel(cx + x, cy + y, window.pen.color().rgb())

        y -= 1

        if p > 0:
            p -= 2 * a * a * y - a * a
        else:
            x += 1
            p += 2 * b * b * x - 2 * a * a * y + a * a


def draw_once(window):
    is_standart = False
    #window.image.fill(window.color_bground) #TODO
    x = int(window.centr_x.text())
    y = int(window.centr_y.text())

    if window.circle.isChecked():     
        r = int(window.rad.text())  

        if window.canon.isChecked():
            circle_canon(window, x, y, r)
        if window.param.isChecked():
            circle_param(window, x, y, r)
        if window.brez.isChecked():
            circle_brez(window, x, y, r)
        if window.middle.isChecked():
            ellips_middle(window, x, y, r, r)
        if window.lib.isChecked():
            is_standart = True
            window.scene.addEllipse(x - r, y - r, r * 2, r * 2, window.pen)

    if window.ellips.isChecked():
        a = int(window.a.text())
        b = int(window.b.text())

        if window.canon.isChecked():
            ellips_canon(window, x, y, a, b)
        if window.param.isChecked():
            ellips_param(window, x, y, a, b)
        if window.brez.isChecked():
            ellips_brez(window, x, y, a, b)
        if window.middle.isChecked():
            ellips_middle(window, x, y, a, b)
        if window.lib.isChecked():
            is_standart = True
            window.scene.addEllipse(x - a, y - b, a * 2, b * 2, window.pen)


    if not is_standart:
        pix = QPixmap(651, 651)
        pix.convertFromImage(window.image)
        window.scene.addPixmap(pix)


def draw_centr(window):
   # window.image.fill(window.color_bground)
    is_standart = False
    x = int(window.centr_x.text())
    y = int(window.centr_y.text())
    d = int(window.dia.text())
    c = int(window.count.text())


    if window.circle.isChecked():
        for i in range(d, d * c + d, d):

            if window.canon.isChecked():
                circle_canon(window, x, y, i)
            if window.param.isChecked():
                circle_param(window, x, y, i)
            if window.brez.isChecked():
                circle_brez(window, x, y, i)
            if window.middle.isChecked():
                circle_middle(window, x, y, i)
            if window.lib.isChecked():
                is_standart = True
                window.scene.addEllipse(x - i, y - i, i * 2, i * 2, window.pen)

    if window.ellips.isChecked():
        a = int(window.a.text())
        b = int(window.b.text())
        for i in range(d, d * c + d, d):
            if window.canon.isChecked():
                ellips_canon(window, x, y, i * a / b, i * b / a)
            if window.param.isChecked():
                ellips_param(window, x, y, i * a / b, i * b / a)
            if window.brez.isChecked():
                ellips_brez(window, x, y, i * a / b, i * b / a)
            if window.middle.isChecked():
                ellips_middle(window, x, y, i * a / b, i * b / a)
            if window.lib.isChecked():
                is_standart = True
                if a < b:
                    window.scene.addEllipse(x - (i * a / b), y - (i * b / a) / 2, i * 2 * a / b, i * b / a, window.pen)
                if a > b:
                    window.scene.addEllipse(x - (i * a / b) / 2, y - (i * b / a), i * a / b, 2 * i * b / a, window.pen)                    


    if not is_standart:
        pix = QPixmap(651, 651)
        pix.convertFromImage(window.image)
        window.scene.addPixmap(pix)


def color_line_like_bg_color(window):
    color = window.bground_color
    window.color_line = color
    window.pen.setColor(color)
    s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
    s.setBackgroundBrush(color)
    window.ln_color.setScene(s)
#    window.hide()
    window.show()
    
def get_color_bground(window):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.white, title='Цвет фона')
    if color.isValid():
        window.bground_color = color
        window.image.fill(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        #window.mainview.setScene(s)
        window.bg_color.setScene(s)
        #window.scene.setBackgroundBrush(color)


def get_color_line(window):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.black, title='Цвет линии')            
    if color.isValid():
        window.color_line = color
        window.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        window.ln_color.setScene(s)


def clear_all(window):
    window.image.fill(Qt.color0)
    window.scene.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

