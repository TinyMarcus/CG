from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPen, QColor
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 711, 661)
        self.canvas.setScene(self.scene)
        
        self.cutter_color = QColor(Qt.black)
        self.line_color = QColor(Qt.blue)
        self.cut_line_color = QColor(Qt.red)
        
        self.polygon = list()
        self.lines = list()
        self.cur_line = list()
        
        self.full_polygon = False
        self.isConvex = False
        self.direction = -1
        
        self.add_line_bt.clicked.connect(lambda: add_line_bt(self))
        self.add_cut_bt.clicked.connect(lambda: add_cut_bt(self))
        self.del_cut_bt.clicked.connect(lambda: del_cutter(self))
        self.close_bt.clicked.connect(lambda: close_cutter())
        self.cut_bt.clicked.connect(lambda: cut_line(self))
        self.paral_bt.clicked.connect(lambda: add_paral(self))
        
        
        self.color_cut_line_bt.clicked.connect(lambda: get_cut_line_color(self))
        self.clear_bt.clicked.connect(lambda: clear(self))
        
        self.first_color_buttons()
    
    def first_color_buttons(self):
        self.color_cut_line_bt.setStyleSheet("background-color:rgb" \
                                         + color_in_str(self.cut_line_color.getRgb()))

class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            add_cut_event(event.scenePos())
        elif event.buttons() == Qt.LeftButton:
            add_line_event(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            close_cutter()

def add_line_event(p):
    global window
    window.cur_line.append(p)
    if len(window.cur_line) == 2:
        add_line(QLineF(window.cur_line[0], window.cur_line[1]))
        window.cur_line = list()

def add_paral_line(win):
    global window
    
    num = int(window.paral_num.text())
    print(window.polygon[num], window.polygon[num-1])
    koef = (-(window.polygon[num].y() - window.polygon[num-1].y())) / (window.polygon[num].x() - window.polygon[num-1].x())
    print(koef)


def add_paral(win):
    if len(win.polygon) == 0:
        QMessageBox.warning(win, "Внимание!", "Не введен отсекатель!")
        return
    
    
    num = window.paral_num.text()

    if num == "":
        return

    num = int(num)

    delta_x = win.polygon[num].x() - win.polygon[num-1].x()
    delta_y = -(win.polygon[num].y() - win.polygon[num-1].y())

    delta_one = delta_x * 0.25
    delta_two = delta_y * 0.25

    koef = (delta_y / delta_x)

    x1 = (win.polygon[num-1].x() - 30 * koef) + delta_one
    y1 = (win.polygon[num-1].y() - 30) - delta_two
    x2 = (win.polygon[num].x() - 30 * koef) - delta_one
    y2 = (win.polygon[num].y() - 30) + delta_two

    line = QLineF(x1, y1, x2, y2)
    add_line(line)

    x1 = (win.polygon[num-1].x() + 30 * koef) + delta_one
    y1 = (win.polygon[num-1].y() + 30) - delta_two
    x2 = (win.polygon[num].x() + 30 * koef) - delta_one
    y2 = (win.polygon[num].y() + 30) + delta_two

    line = QLineF(x1, y1, x2, y2)
    add_line(line)

def add_line_bt(win):
    x1 = float(win.x1_line.text())
    y1 = float(win.y1_line.text())
    x2 = float(win.x2_line.text())
    y2 = float(win.y2_line.text())

    line = QLineF(x1, y1, x2, y2)
    add_line(line)

def add_line(line):
    global window
    window.lines.append(line)
    cut(window)

def add_cut_event(p):
    global window
    add_cut(p)

def add_cut_bt(win):
    x = float(win.x_cut.text())
    y = float(win.y_cut.text())

    add_cut(QPointF(x, y))


def add_cut(p):
    global window

    if window.full_polygon:
        QMessageBox.warning(window, "Ошибка", "Отсекатель уже введен!")
        return

    window.polygon.append(p)
    size = len(window.polygon)

    if size > 1:
        window.scene.addLine(QLineF(window.polygon[size - 2], window.polygon[size - 1]), QPen(window.cutter_color))

def cut(window):
    window.scene.clear()
    
    for j in range(len(window.lines)):
        window.scene.addLine(window.lines[j], QPen(window.line_color))
    
    for i in range(len(window.polygon) - 1):
        window.scene.addLine(QLineF(window.polygon[i], window.polygon[i + 1]), QPen(window.cutter_color))

    if window.full_polygon:
        if not window.isConvex:
            QMessageBox().warning(window, "Ошибка", "Многоугольник невыпуклый")
            return
        
     
def cut_line(window):
    for line in window.lines:
        cyrus_beck_algo(window.polygon, line, window.direction, window)

     
def close_cutter():
    global window
    
    size = len(window.polygon)
    if size > 2:
        add_cut(window.polygon[0])
        window.full_polygon = True
        isConvex, _sign = is_convex(window.polygon)
        
        if isConvex:
            window.isConvex = True
            window.direction = _sign
        else:
            window.isConvex = False
            QMessageBox().warning(window, "Ошибка", "Многоугольник невыпуклый")

def del_cutter(window):
    window.polygon = list()
    window.full_polygon = False
    window.scene.clear()
    draw_all_lines(window)

def draw_all_lines(window):
    for line in window.lines:
        window.scene.addLine(line, QPen(window.line_color))

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

def get_cut_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cut_line_color = color
        window.color_cut_line_bt.setStyleSheet("background-color:rgb" \
                                               + color_in_str(window.cut_line_color.getRgb()))

def clear(window):
    window.scene.clear()
    window.lines = list()
    window.cur_line = list()
    window.polygon = list()
    window.full_polygon = False
    window.isConvex = False
    window.direction = - 1

def sign(x):
    if x == 0:
        return 0
    
    return x / fabs(x)

def is_convex(polygon):
    size = len(polygon)
    array_vector = list()
    _sign = 0
    
    if size < 3:
        return False, _sign

    for i in range(1, size):
        if i < size - 1:
            ab = QPointF(polygon[i].x() - polygon[i - 1].x(), polygon[i].y() - polygon[i - 1].y())
            bc = QPointF(polygon[i + 1].x() - polygon[i].x(), polygon[i + 1].y() - polygon[i].y())
        else:
            ab = QPointF(polygon[i].x() - polygon[i - 1].x(), polygon[i].y() - polygon[i - 1].y())
            bc = QPointF(polygon[1].x() - polygon[0].x(), polygon[1].y() - polygon[0].y())
        
        array_vector.append(ab.x() * bc.y() - ab.y() * bc.x())

    exist_sign = False
    for i in range(len(array_vector)):
        if array_vector[i] == 0:
            continue
        
        if exist_sign:
            if sign(array_vector[i]) != _sign:
                return False, _sign
        else:
            _sign = sign(array_vector[i])
            exist_sign = True

    return True, _sign

def scalar(p_1, p_2):
    return p_1.x() * p_2.x() + p_1.y() * p_2.y()

def cyrus_beck_algo(polygon, line, n, window):
    t_beg = 0
    t_end = 1
    
    D = QPointF(line.p2().x() - line.p1().x(), line.p2().y() - line.p1().y())
    
    for i in range(len(polygon) - 1):
        N = QPointF(-n * (polygon[i + 1].y() - polygon[i].y()), n * (polygon[i + 1].x() - polygon[i].x()))
        W = QPointF(line.p1().x() - polygon[i].x(), line.p1().y() - polygon[i].y())
        
        
        Dscalar = scalar(D, N)
        Wscalar = scalar(W, N)
        
        if Dscalar == 0:
            if Wscalar >= 0:
                continue
            elif Wscalar < 0:
                return
        else:
            t = - Wscalar / Dscalar
            
            if Dscalar > 0:
                if t > 1:
                    return
                else:
                    t_beg = max(t_beg, t)
            elif Dscalar < 0:
                if t < 0:
                    return
                else:
                    t_end = min(t_end, t)

    if t_beg <= t_end:
        window.scene.addLine(line.p1().x() + (line.p2().x() - line.p1().x()) * t_end,
                             line.p1().y() + (line.p2().y() - line.p1().y()) * t_end,
                             line.p1().x() + (line.p2().x() - line.p1().x()) * t_beg,
                             line.p1().y() + (line.p2().y() - line.p1().y()) * t_beg,
                             QPen(window.cut_line_color))

def main():
    global window
    
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
