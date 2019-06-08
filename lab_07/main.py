from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint, QLineF
import time

blue = Qt.blue
red = Qt.red
now = None

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 781, 781)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(781, 781, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.line_color = QColor(Qt.blue)
        self.cut_line_color = QColor(Qt.red)
        self.bars.clicked.connect(lambda : set_bars(self))
        self.clear_bt.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        self.on_bars.clicked.connect(lambda: add_bars(self))
#        self.color_line_bt.clicked.connect(lambda: get_line_color(self))
        self.color_algo_bt.clicked.connect(lambda: get_cut_line_color(self))
        self.lines = []
        self.cur_line = []
        self.clip = None
        self.point_now = None
        self.input_bars = False
        self.input_rect = False
        self.pen = QPen(blue)
        self.first_color_buttons()
        
    def first_color_buttons(self):
        self.color_algo_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(self.cut_line_color.getRgb()))

class Scene(QtWidgets.QGraphicsScene):

    def mousePressEvent(self, event):
        add_point(event.scenePos())

    def mouseMoveEvent(self, event):
        global now, w
        if w.input_rect:
            if now is None:
                now = event.scenePos()
            else:
                self.removeItem(self.itemAt(now, QTransform()))
                p = event.scenePos()
                self.addRect(now.x(), now.y(), abs(now.x() - p.x()), abs(now.y() - p.y()))

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")


def set_bars(win):
    if win.input_bars:
        win.input_bars = False
        win.rect.setDisabled(False)
        win.clear_bt.setDisabled(False)
        win.paint.setDisabled(False)
        win.on_bars.setDisabled(False)
    else:
        win.input_bars = True
        win.rect.setDisabled(True)
        win.clear_bt.setDisabled(True)
        win.paint.setDisabled(True)
        win.on_bars.setDisabled(True)


def set_rect(win):
    if win.input_rect:
        win.input_rect = False
        win.bars.setDisabled(False)
        win.clear_bt.setDisabled(False)
        win.paint.setDisabled(False)
        win.on_bars.setDisabled(False)
    else:
        win.input_rect = True
        win.bars.setDisabled(True)
        win.clear_bt.setDisabled(True)
        win.paint.setDisabled(True)
        win.on_bars.setDisabled(True)


def add_row(win):
    win.table.insertRow(win.table.rowCount())


def add_point(point):
    global w
    if w.input_bars:
        if w.point_now is None:
            w.point_now = point
        else:
            w.lines.append([[w.point_now.x(), w.point_now.y()],
                            [point.x(), point.y()]])

            add_row(w)
            i = w.table.rowCount() - 1
            item_b = QTableWidgetItem("[{0}, {1}]".format(w.point_now.x(), w.point_now.y()))
            item_e = QTableWidgetItem("[{0}, {1}]".format(point.x(), point.y()))
            w.table.setItem(i, 0, item_b)
            w.table.setItem(i, 1, item_e)
            w.scene.addLine(w.point_now.x(), w.point_now.y(), point.x(), point.y(), w.pen)
            w.point_now = None


def clean_all(win):
    global now
    now = None
    win.scene.clear()
    win.table.clear()
    win.lines = []
    win.image.fill(Qt.white)
    r = win.table.rowCount()
    for i in range(r, -1, -1):
        win.table.removeRow(i)
        

def end_codes(dot, cutter):
    code = [0, 0, 0, 0]
    if dot[0] < cutter[0]:
        code[0] = 1
    if dot[0] > cutter[1]:
        code[1] = 1
    if dot[1] < cutter[2]:
        code[2] = 1
    if dot[1] > cutter[3]:
        code[3] = 1

    return code


def clipping(win):
    buf = win.scene.itemAt(now, QTransform()).rect()
    win.clip = [buf.left(), buf.right(), buf.top(),  buf.bottom()]
    for b in win.lines:
        pass
        win.pen.setColor(win.cut_line_color)
        my_alg(b, win.clip, win)
        win.pen.setColor(win.line_color)


def logical_multiplication(code_1, code_2):
    p = 0
    for i in range(4):
        p += code_1[i] & code_2[i]

    return p


def check_appearance(line, cutter):
    s1 = sum(end_codes(line[0], cutter))
    s2 = sum(end_codes(line[1], cutter))

    wid = 0

    if not s1 and not s2:
        wid = 1
    else:
        l = logical_multiplication(end_codes(line[0], cutter), end_codes(line[1], cutter))
        if l != 0:
            wid = -1

    return wid


def my_alg(line, cutter, window):
    Fl = -1
    m = 1

    if (line[1][0] - line[0][0] != 0):
        m = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
        if m == 0:
            Fl = 1
        else:
            Fl = 0

    for i in range(4):
        wid = check_appearance(line, cutter)
        code_1 = end_codes(line[0], cutter)
        code_2 = end_codes(line[1], cutter)
        if (wid == -1):
            return
        elif (wid == 1):
            window.scene.addLine(line[0][0], line[0][1], line[1][0], line[1][1], window.pen)
            return

        if code_1[i] == code_2[i]:
            continue

        if code_1[i] == 0:
            tmp = line[0]
            line[0] = line[1]
            line[1] = tmp
        
        if Fl == -1:
            line[0][1] = cutter[i]
        else:
            if i <= 1   :
                line[0][1] = m * (cutter[i] - line[0][0]) + line[0][1]
                line[0][0] = cutter[i]
                continue
            else:
                line[0][0] = (1 / m) * (cutter[i] - line[0][1]) + line[0][0]
                line[0][1] = cutter[i]

    window.scene.addLine(line[0][0], line[0][1], line[1][0], line[1][1], window.pen)


def get_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.line_color = color
        window.color_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.line_color.getRgb()))


def get_cut_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cut_line_color = color
        window.color_algo_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cut_line_color.getRgb()))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
