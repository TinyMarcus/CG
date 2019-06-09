from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPen, QColor
import sys
import numpy as np

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 711, 661)
        self.canvas.setScene(self.scene)
        
        self.cutter_color = QColor(Qt.black)
        self.polygon_color = QColor(Qt.blue)
        self.cut_polygon_color = QColor(Qt.red)
        
        self.cutter_figure = list()
        self.figures = list()
        self.current_figure = list()
        
        self.full_polygon = False
        self.isConvex = False
        self.direction = -1
        
        self.add_pol_bt.clicked.connect(lambda: add_polygon_sb(self))
        self.add_cut_bt.clicked.connect(lambda: add_cutter_sb(self))
        self.del_cut_bt.clicked.connect(lambda: del_cutter(self))
        self.close_bt.clicked.connect(lambda: close_cutter())
        self.cut_bt.clicked.connect(lambda: cut(self))
        
        self.color_cut_polygon_bt.clicked.connect(lambda: get_cut_polygon_color(self))
        self.clear_bt.clicked.connect(lambda: clear(self))

        self.first_color_buttons()
        
    def first_color_buttons(self):
        self.color_cut_polygon_bt.setStyleSheet("background-color:rgb" + color_in_str(self.cut_polygon_color.getRgb()))

class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            add_cutter_event(event.scenePos())
        elif  event.buttons() == Qt.RightButton and event.modifiers() == Qt.ControlModifier:
            close_cutter()
        elif event.buttons() == Qt.LeftButton:
            add_polygon_event(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            close_polygon()

def add_polygon_event(point):
    add_polygon(point)

def add_polygon_sb(window):
    x = float(window.x_pol.text())
    y = float(window.y_pol.text())
    
    add_polygon(QPointF(x, y))

def add_polygon(point):
    global window
    window.current_figure.append(point)
    cut_all(window)

def add_cutter_event(point):
    add_cutter(point)

def add_cutter_sb(window):
    x = float(window.x_cut.text())
    y = float(window.y_cut.text())
    
    add_cutter(QPointF(x, y))

def add_cutter(point):
    global window
    
    if window.full_polygon:
        QMessageBox.warning(window, "Ошибка", "Отсекатель уже введен")
        return

    window.cutter_figure.append(point)
    size = len(window.cutter_figure)

    if size > 1:
        window.scene.addLine(QLineF(window.cutter_figure[size - 2], window.cutter_figure[size - 1]), QPen(window.cutter_color))

def cut_all(window):
    window.scene.clear()
    
    for figure in window.figures:
        for i in range(len(figure) - 1):
            window.scene.addLine(QLineF(figure[i], figure[i + 1]), QPen(window.polygon_color))

    for i in range(len(window.cutter_figure) - 1):
        window.scene.addLine(QLineF(window.cutter_figure[i], window.cutter_figure[i + 1]), QPen(window.cutter_color))

    if len(window.current_figure) > 1:
        for i in range(len(window.current_figure) - 1):
            window.scene.addLine(QLineF(window.current_figure[i], window.current_figure[i + 1]), QPen(window.polygon_color))

    if window.full_polygon:
        if not window.isConvex:
            QMessageBox().warning(window, "Ошибка", "Многоугольник невыпуклый")
            return

def close_cutter():
    global window
    
    size = len(window.cutter_figure)
    if size > 2:
        add_cutter(window.cutter_figure[0])
        window.full_polygon = True
        isConvex, _sign = is_convex(window.cutter_figure)
        
        if isConvex:
            window.isConvex = True
            window.direction = _sign
            cut_all(window)
        else:
            window.isConvex = False
            QMessageBox().warning(window, "Ошибка", "Многоугольник невыпуклый")

def close_polygon():
    global window
    
    size = len(window.current_figure)
    if size > 2:
        add_polygon(window.current_figure[0])
        window.figures.append(window.current_figure)
        window.current_figure = list()

def del_cutter(window):
    if len(window.cutter_figure) == 0:
        QMessageBox.warning(window, "Предупреждение", "Нет введенного отсекателя")
        return
    
    window.cutter_figure = list()
    window.full_polygon = False
    cut_all(window)

def del_last_polygon(window):
    if len(window.current_figure) != 0:
        window.current_figure = list()
    elif len(window.figures) != 0:
        window.figures.pop()
    else:
        QMessageBox.warning(window, "Предупреждение", "Нет введенных многоугольников")
        return
    cut_all(window)

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

def get_cut_polygon_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cut_polygon_color = color
        window.color_cut_polygon_bt.setStyleSheet("background-color:rgb" \
                                                  + color_in_str(window.cut_polygon_color.getRgb()))
        cut_all(window)

def clear(window):
    window.scene.clear()
    window.figures = list()
    window.current_figure = list()
    window.cutter_figure = list()
    window.full_polygon = False
    window.isConvex = False
    window.direction = -1

def cut(window):
    for figure in window.figures:
        new_polygon = algo(window, figure, window.cutter_figure)
        for i in range(len(new_polygon) - 1):
            window.scene.addLine(QLineF(new_polygon[i], new_polygon[i + 1]), QPen(window.cut_polygon_color, 2))

def sign(x):
    if x == 0:
        return 0
    return x / fabs(x)


def is_convex(figure):
    size = len(figure)
    vector2d = list()
    check_sign = 0
    
    if size < 3:
        return False, check_sign
    
    for i in range(1, size):
        if i < size - 1:
            ab = QPointF(figure[i].x() - figure[i - 1].x(), figure[i].y() - figure[i - 1].y())
            bc = QPointF(figure[i + 1].x() - figure[i].x(), figure[i + 1].y() - figure[i].y())
        else:
            ab = QPointF(figure[i].x() - figure[i - 1].x(), figure[i].y() - figure[i - 1].y())
            bc = QPointF(figure[1].x() - figure[0].x(), figure[1].y() - figure[0].y())
        
        vector2d.append(ab.x() * bc.y() - ab.y() * bc.x())
    
    exist_sign = False
    for i in range(len(vector2d)):
        if vector2d[i] == 0:
            continue
        
        if exist_sign:
            if sign(vector2d[i]) != check_sign:
                return False, check_sign
        else:
            check_sign = sign(vector2d[i])
            exist_sign = True

    return True, check_sign

def visible(p0, p1, p2):
    Pab1 = (p0.x() - p1.x()) * (p2.y() - p1.y())
    Pab2 = (p0.y() - p1.y()) * (p2.x() - p1.x())
    
    return sign(Pab1 - Pab2)

def fact_sech(p0, pk, w1, w2):
    vis_1 = visible(p0, w1, w2)
    vis_2 = visible(pk, w1, w2)
    
    if (vis_1 < 0 and vis_2 > 0) or (vis_1 > 0 and vis_2 < 0):
        return True
    
    return False

def intersection(p1, p2, w1, w2):
    k = np.arange(4).reshape((2, 2))
    k[0][0] = p2.x() - p1.x()
    k[0][1] = w1.x() - w2.x()
    k[1][0] = p2.y() - p1.y()
    k[1][1] = w1.y() - w2.y()
    
    p = np.arange(2).reshape((2, 1))
    p[0][0] = w1.x() - p1.x()
    p[1][0] = w1.y() - p1.y()
    
    k = np.linalg.inv(k)
    param = k.dot(p)
    
    return QPointF(p1.x() + (p2.x() - p1.x()) * param[0][0],
                   p1.y() + (p2.y() - p1.y()) * param[0][0])

def algo(window, figure_tmp, cutter_figure):
    figure = figure_tmp.copy()
    Np = len(figure)
    Nw = len(cutter_figure)
    
    S = QPointF()
    F = QPointF()
    for i in range(Nw - 1):
        Nq = 0
        Q = list()
        
        for j in range(Np):
            if j != 0:
                if fact_sech(S, figure[j], cutter_figure[i], cutter_figure[i + 1]):
                    I = intersection(S, figure[j], cutter_figure[i], cutter_figure[i + 1])
                    Q.append(I)
                    Nq += 1
            else:
                F = figure[j]
        
            S = figure[j]
            is_visible = visible(S, cutter_figure[i], cutter_figure[i + 1])
            
            if (is_visible >= 0 and window.direction == -1) or (is_visible <= 0 and window.direction == 1):
                Q.append(S)
                Nq += 1
        if Nq != 0:
            if fact_sech(S, F, cutter_figure[i], cutter_figure[i + 1]):
                I = intersection(S, F, cutter_figure[i], cutter_figure[i + 1])
                Q.append(I)
                Nq += 1
        
        Np = Nq
        figure = Q.copy()
    
    if len(figure) > 0:
        figure.append(figure[0])
    
    return figure


def main():
    global window
    
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
