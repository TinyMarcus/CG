from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

import sys
from math import *
max_x = 600
max_y = 600

class win(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, max_x, max_y)
        self.canvas.setScene(self.scene)

        self.image = QImage(max_x, max_y, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.pen = QPen(Qt.black)

        self.add_point_bt.clicked.connect(lambda: add_dot_call(self))
        self.clear_bt.clicked.connect(lambda: clear(self))
        self.add_seed_pix_bt.clicked.connect(lambda: get_seed_pixel(self))
        self.fill_bt.clicked.connect(lambda: algorithm_seed(self))

        self.color_bg_bt.clicked.connect(lambda: get_bg_color(self))
        self.color_seed_bt.clicked.connect(lambda: get_seed_color(self))
        self.color_line_bt.clicked.connect(lambda: get_line_color(self))

        self.seed_pix_button_clicked = False
        self.now_figure = list()

        self.bg_color = QColor(Qt.white)
        self.line_color = QColor(Qt.black)
        self.paint_color = QColor(Qt.green)
        self.first_color_buttons()

        set_window_borders(self)

    def first_color_buttons(self):
        self.color_bg_bt.setStyleSheet("background-color:rgb" \
            + color_in_string(self.bg_color.getRgb()))
        self.color_seed_bt.setStyleSheet("background-color:rgb" \
            + color_in_string(self.paint_color.getRgb()))
        self.color_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_string(self.line_color.getRgb()))

class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            add_control_dot(event.scenePos())
        elif event.buttons() == Qt.LeftButton:
            add_dot(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            end_figure()
        else:
            algorithm_seed_call()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            add_control_dot(event.scenePos())
        elif event.buttons() == Qt.LeftButton:
            add_dot(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            end_figure()

def color_in_string(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

def get_seed_pixel(win):
    win.seed_pix_button_clicked = True

def algorithm_seed_call():
    global win
    algorithm_seed(win)

def add_dot(dot):
    global win

    if dot.x() < 0 or dot.y() < 0 or dot.x() > max_x - 1 or dot.y() > max_y - 1:
        return

    if win.seed_pix_button_clicked:
        win.x_input_seed.setText(str(dot.x()))
        win.y_input_seed.setText(str(dot.y()))
        win.seed_pix_button_clicked = False
        return

    rows = win.points_table.rowCount()
    win.points_table.insertRow(rows)
    index = rows - 1

    win.points_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(dot.x())))
    win.points_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(dot.y())))
    win.now_figure.append(dot)

    length = len(win.now_figure)

    if length > 1:
        bresenham(win, win.now_figure[length - 2].x(),
            win.now_figure[length - 2].y(),
            win.now_figure[length - 1].x(),
            win.now_figure[length - 1].y(),
            QPen(win.line_color).color().rgba())
        win.scene.clear()
        draw_image_from_pix(win)

def add_control_dot(dot):
    global win

    length = len(win.now_figure)

    if length == 0:
        add_dot(dot)

    else:
        last_dot = win.now_figure[length - 1]
        koef1 = fabs(dot.y() - last_dot.y())
        koef2 = fabs(last_dot.x() - dot.x())

        if koef2 == 0:
            add_dot(QPointF(dot.x(), last_dot.y()))
        elif fabs(degrees(atan(koef1 / koef2))) <= 45:
            add_dot(QPointF(dot.x(), last_dot.y()))
        else:
            add_dot(QPointF(last_dot.x(), dot.y()))

def add_dot_call(win):
    add_dot(QPointF(int(win.x_input.text()), int(win.y_input.text())))

def end_figure():
    global win

    length = len(win.now_figure)
    if length > 2:
        bresenham(win, win.now_figure[0].x(),
            win.now_figure[0].y(),
            win.now_figure[length - 1].x(),
            win.now_figure[length - 1].y(),
            QPen(win.line_color).color().rgba())

        draw_image_from_pix(win)
        win.now_figure = list()

def algorithm_seed(win):
    seed_point = QPointF(float(win.x_input_seed.text()), float(win.y_input_seed.text()))
    if not check_pixel(seed_point):
        QMessageBox.warning(win, "Ошибка", "Расположите затравочный пиксель в пределах экрана")

    line_color = win.line_color.rgb()
    paint_color = win.paint_color.rgb()

    stack_list = list()
    stack_list.append(seed_point)

    while stack_list:
        pixel = stack_list.pop()
        x = pixel.x()
        y = pixel.y()
        x_temp = x
        win.image.setPixel(x, y, paint_color)

        x = x + 1
        while win.image.pixel(x, y) != line_color:
            #if win.delay.isChecked():
            #    delay()                               
            #    win.scene.clear()
            #    draw_image_from_pix(win)
            win.image.setPixel(x, y, paint_color)
            x = x + 1

        x_r = x - 1
        x = x_temp
        
        x = x - 1
        while win.image.pixel(x, y) != line_color:
            #if win.delay.isChecked():
            #    delay()                               
            #    win.scene.clear()
            #    draw_image_from_pix(win)
            win.image.setPixel(x, y, paint_color)
            #print(len(stack_list))
            x = x - 1

        x_l = x + 1
           
        y = y + 1
        x = x_l

        while x <= x_r:
            f = False
            pixel_color = win.image.pixel(x, y)

            while (pixel_color != line_color and pixel_color != paint_color and x <= x_r):
                if f == False:
                    f = True
                x = x + 1
                pixel_color = win.image.pixel(x, y)

            if f:
                if (win.image.pixel(x, y) != line_color and win.image.pixel(x, y) != paint_color and x == x_r):
                    stack_list.append(QPointF(x, y))
                else:
                    stack_list.append(QPointF(x - 1, y))

            x_n = x
            while (win.image.pixel(x, y) == line_color or win.image.pixel(x, y) == paint_color) and x < x_r:
                x = x + 1

            if x == x_n:
                x = x + 1

        y = y - 2
        x = x_l

        while x <= x_r:
            f = False
            pixel_color = win.image.pixel(x, y)

            while pixel_color != paint_color and pixel_color != line_color and x <= x_r:
                if f == False:
                    f = True
                x = x + 1
                pixel_color = win.image.pixel(x, y)

            if f:
                if (win.image.pixel(x, y) != line_color and win.image.pixel(x, y) != paint_color and x == x_r):
                    stack_list.append(QPointF(x, y))
                else:
                    stack_list.append(QPointF(x - 1, y))

            x_n = x
            
            while (win.image.pixel(x, y) == line_color or win.image.pixel(x, y) == paint_color) and x < x_r:
                x = x + 1

            if x == x_n:
                x = x + 1

        if win.delay.isChecked():
                delay()                               
                win.scene.clear()
                draw_image_from_pix(win)
       
        print(stack_list)
            
    win.scene.clear()
    draw_image_from_pix(win)


def draw_image_from_pix(win):
    pixel = QPixmap(max_x, max_y)
    pixel.convertFromImage(win.image)
    win.scene.addPixmap(pixel)

def clear(win):
    rows = win.points_table.rowCount()
    for i in range(rows - 1, -1, -1):
        win.points_table.removeRow(i)
    win.points_table.insertRow(0)
    win.scene.clear()
    win.image.fill(Qt.white)
    win.now_figure = list()
    set_window_borders(win)

def sign(x):
    if (x > 0):
        return 1
    elif (x < 0):
        return -1
    else:
        return 0
        
def bresenham(win,x1,y1,x2,y2,color):
    dx = int(x2 - x1)
    dy = int(y2 - y1)
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)    

    swap = False
    if (dy <= dx):
        swap = False
    else:
        swap = True
        dx,dy = dy,dx
        
    
    e = int(2*dy-dx)
    x = int(x1)
    y = int(y1)
            
    for i in range(dx+1):
        win.image.setPixel(x,y,color)
        if (e>=0):
            if (swap):
                x += sx
            else:
                y +=sy
            e = e-2*dx
        if (e < 0): 
            if (swap):
                y +=sy
            else:
                x += sx
            e = e+2*dy

def delay():
    #QCoreApplication.processEvents(QEventLoop.AllEvents, 1)
    #QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)
    t = QTime.currentTime().addMSecs(1)
    while QTime.currentTime() < t:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 1)

#def delay():
#    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)

def check_pixel(dot):
    return not (dot.x() <= 0 or dot.y() <= 0 or dot.x() >= max_x or dot.y() >= max_y)

def get_bg_color(win):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        if color == win.line_color:
            QMessageBox.warning(win, "Ошибка", "У фона и у границы фигуры одинаковый цвет")
            return

        win.bg_color = color
        win.color_bg_bt.setStyleSheet("background-color:rgb" \
            + color_in_string(win.bg_color.getRgb()))
        fill_bg(win)

def get_seed_color(win):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        win.paint_color = color
        win.color_seed_bt.setStyleSheet("background-color:rgb" \
            + color_in_string(win.paint_color.getRgb()))

def get_line_color(win):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        if color == win.bg_color:
            QMessageBox.warning(win, "Ошибка", "У фона и у границы фигуры одинаковый цвет")
            return

        win.line_color = color
        win.color_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_string(win.line_color.getRgb()))
        set_window_borders(win)

def fill_bg(win):
    win.image.fill(win.bg_color)
    win.scene.clear()
    draw_image_from_pix(win)
    set_window_borders(win)

def set_window_borders(win):
    bresenham(win, 0, 0, max_x, 0, QPen(win.line_color).color().rgba())
    bresenham(win, 0, 0, 0, max_y - 1, QPen(win.line_color).color().rgba())
    bresenham(win, max_x - 1, 0, max_x - 1, max_y - 1, QPen(win.line_color).color().rgba())
    bresenham(win, 0, max_y - 1, max_x, max_y - 1, QPen(win.line_color).color().rgba())

    win.scene.clear()
    draw_image_from_pix(win)

def main():
    global win

    app = QtWidgets.QApplication(sys.argv)
    win = win()
    win.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

