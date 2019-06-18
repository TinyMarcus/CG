from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt
from math import sin, cos, exp, sqrt, pi
#from horizon import float_horizon

red = Qt.red
blue = Qt.blue
black = Qt.black
white = Qt.white
magenta = Qt.magenta

first_angle = 0
second_angle = 0
third_angle = 0

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QGraphicsScene(0, 0, 711, 601)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(710, 600, QImage.Format_Alpha8)
        self.image.fill(magenta)
        self.pen = QPen(QColor("pink"))
        self.draw.clicked.connect(lambda: draw(self))
        self.slider_x.valueChanged.connect(lambda: draw(self))
        self.slider_y.valueChanged.connect(lambda: draw(self))
        self.slider_z.valueChanged.connect(lambda: draw(self))
        self.funcs.addItem("(sin(z))^2 - (cos(x))^2")
        self.funcs.addItem("cos(x) * sin(z)")
        self.funcs.addItem("(x^2 + z^2)^0.5")

    def keyPressEvent(self, ev):
        global second_angle, first_angle, third_angle

        if ev.key() == 81: #Q
            first_angle += 5
        elif ev.key() == 65: #A
            first_angle -= 5
        elif ev.key() == 87: #W
            second_angle += 5
        elif ev.key() == 83: #S
            second_angle -= 5
        elif ev.key() == 69: #E
            third_angle += 5
        elif ev.key() == 68: #D
            third_angle -= 5

        draw(self)


def func_1(x, z):
    return (sin(z))**2 - (cos(x))**2

def func_2(x, z):
    return cos(x) * sin(z)

def func_3(x, z):
    return (x**2 + z**2)**0.5

def sign(num):
    if (num < 0):
        return -1
    elif (num > 0):
        return 1
    else:
        return 0

def find_intersection(x1, y1, x2, y2, array):
    if (x2 < 0 or x2 >= len(array) or x1 < 0 or x1 >= len(array)):
        return x1, y1

    xi = x1
    yi = y1

    delta_x = x2 - x1
    delta_y = y2 - y1
    delta = array[x2] - array[x1]   

    if (delta_x == 0):
        xi = x2
        yi = array[x2]
    elif (y1 == array[x1] and y2 == array[x2]):
        xi = x1
        yi = y1
    elif (delta_y == delta):
        return x1, y1
    else:
        k = delta_y / delta_x
        xi = x1 - round(delta_x * (y1 - array[x1]) / (delta_y - delta))
        yi = round((xi - x1) * k + y1)

    return xi, yi

def horizon(x1, y1, x2, y2, top, bottom, win):
    if (x2 < 0 or x2 >= len(top) or x1 < 0 or x1 >= len(top)):
        return top, bottom

    if (x2 < x1):
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    if (x2 - x1 == 0):
        top[x2] = max(top[x2], y2)
        bottom[x2] = min(bottom[x2], y2)

        if (x2 >= 0 and x2 <= win.scene.width()):
            win.scene.addLine(x1, y1, x2, y2, win.pen)
    else:
        x_prev = int(x1)
        y_prev = int(y1)
        k = (y2 - y1) / (x2 -x1)
        x = x1

        while (x <= x2):
            y = round(k * (x - x1) + y1)
            top[x] = max(top[x], y)
            bottom[x] = min(bottom[x], y)

            if (x >= 0 and x <= win.scene.width()):
                win.scene.addLine(x_prev, y_prev, x, y, win.pen)
            
            x += 1
    
    return top, bottom

def check_edge(x, y, x_edge, y_edge, top, bottom, win):
    if (x_edge == -1):
        x_edge = x
        y_edge = y
    else:
        top, bottom = horizon(x_edge, y_edge, x, y, top, bottom, win)
        x_edge = x
        y_edge = y
    
    return x_edge, y_edge, top, bottom

def visible(x, y, top, bottom):
    t_flag = 0

    if x < 0 or x >= len(bottom):
        return t_flag

    if (y < top[x] and y > bottom[x]):
        t_flag = 0
    if (y >= top[x]):
        t_flag = 1
    if (y <= bottom[x]):
        t_flag = -1

    return t_flag

def draw(win):
    global first_angle, second_angle, third_angle
    print(win.slider_x.value())
    #angle_x = int(win.ox_angle.text())
    #angle_y = int(win.oy_angle.text())
    #angle_z = int(win.oz_angle.text())

    #first_angle = int(win.slider_x.value())
    #second_angle = int(win.slider_y.value())
    #third_angle = int(win.slider_z.value())

    #print(first_angle, second_angle, third_angle)

    #draw_call(win, win.slider_x.value(), win.slider_y.value(), win.slider_z.value())
    draw_call(win, first_angle, second_angle, third_angle)
    #draw_call(win, angle_x, angle_y, angle_z)

    return

def draw_call(win, theta_x, theta_y, theta_z):
    win.scene.clear()

    print(theta_x, theta_y, theta_z)

    if win.funcs.currentIndex() == 0:
        algo(func_1, theta_x, theta_y, theta_z, win)
    elif win.funcs.currentIndex() == 1:
        algo(func_2, theta_x, theta_y, theta_z, win)
    elif win.funcs.currentIndex() == 2:
       algo(func_3, theta_x, theta_y, theta_z, win)

def rotate_x(y, z, theta_x):
    theta_x = theta_x * pi / 180
    tmp = y
    y = cos(theta_x) * y - sin(theta_x) * z
    z = cos(theta_x) * z + sin(theta_x) * tmp

    return y, z

def rotate_y(x, z, theta_y):
    theta_y = theta_y * pi / 180
    tmp = x
    x = cos(theta_y) * x - sin(theta_y) * z
    z = cos(theta_y) * z + sin(theta_y) * tmp

    return x, z

def rotate_z(x, y, theta_z):
    theta_z = theta_z * pi / 180
    tmp = x
    x = cos(theta_z) * x - sin(theta_z) * y
    y = cos(theta_z) * y + sin(theta_z) * tmp

    return x, y

def transform(x, y, z, theta_x, theta_y, theta_z, win):
    x_center = win.scene.width() / 2
    y_center = win.scene.height() / 2
    
    x_tmp = x
    y_tmp = y
    z_tmp = z

    y_tmp, z_tmp = rotate_x(y_tmp, z_tmp, theta_x)
    x_tmp, z_tmp = rotate_x(x_tmp, z_tmp, theta_y)
    x_tmp, y_tmp = rotate_x(x_tmp, y_tmp, theta_z)

    res_x = round(x_tmp * 60 + x_center)
    res_y = round(y_tmp * 60 + y_center)

    return res_x, res_y

def algo(func, theta_x, theta_y, theta_z, win):
    '''print(win.x_min.value(), win.x_max.value(), win.dx.value())
    print(win.z_min.value(), win.z_max.value(), win.dz.value())
    print(win.scene.width(), win.scene.height())
    '''
    top = [0 for i in range(int(win.scene.width()))]
    bottom = [int(win.scene.height()) for i in range(int(win.scene.width()))]

    x_left = -1
    y_left = -1
    x_right = -1
    y_right = -1
    
    z = win.z_max.value()
    i = 0

    while (z >= win.z_min.value()):
        #print(z)
        #x_prev_tmp = win.x_min.value()
        y_prev_tmp = func(win.x_min.value(), z)
        x_prev, y_prev = transform(win.x_min.value(), y_prev_tmp, z, theta_x, theta_y, theta_z, win)
        x_left, y_left, top, bottom = check_edge(x_prev, y_prev, x_left, y_left, top, bottom, win)
        p_flag = visible(x_prev, y_prev, top, bottom)
        x = win.x_min.value()
        #print(i)
        #i += 1

        while (x <= win.x_max.value()):
            #print(i)
            #i += 1
            x_curr = 0
            y_curr = 0

            y_prev_tmp = func(x, z)
            x_curr, y_curr = transform(x, y_prev_tmp, z, theta_x, theta_y, theta_z, win)

            t_flag = visible(x_curr, y_curr, top, bottom)

            if (t_flag == p_flag):
                if (p_flag):
                    top, bottom = horizon(x_prev, y_prev, x_curr, y_curr, top, bottom, win)
            elif (t_flag == 0):
                if (p_flag == 1):
                    xi, yi = find_intersection(x_prev, y_prev, x_curr, y_curr, top)
                else:
                    xi, yi = find_intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom, win)
            elif (t_flag == 1):
                if (p_flag == 0):
                    xi, yi = find_intersection(x_prev, y_prev, x_curr, y_curr, top)
                    top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom, win)
                else:
                    xi, yi = find_intersection(x_prev, y_prev, x_curr, y_curr, top)
                    top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom, win)
                    xi, yi = find_intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                    top, bottom = horizon(xi, yi, x_curr, y_curr, top, bottom, win)
            else:
                if (p_flag == 0):
                    xi, yi = find_intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                    top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom, win)
                else:
                    xi, yi, = find_intersection(x_prev, y_prev, x_curr, y_curr, top)
                    top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom, win)
                    xi, yi, = find_intersection(x_prev, y_prev, x_curr, y_curr, bottom)
                    top, bottom = horizon(xi, yi, x_curr, y_curr, top, bottom, win)
            p_flag = t_flag
            x_prev = x_curr
            y_prev = y_curr
            x += win.dx.value()
        x_right, y_right, top, bottom = check_edge(x_prev, y_prev, x_right, y_right, top, bottom, win)
        z -= win.dz.value()
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
