import sys
from logic.logic import *
from logic.loading_polygon import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ctypes


class main_application(QWidget):
    def __init__(self):
        super().__init__()
        self.hight = 1080
        self.width = 1920
        self.resize(self.width, self.hight)
        self.setMinimumSize(self.width, self.hight)

        self.setWindowIcon(QIcon("icon.png"))
        my_app_id = 'by_Müller_Willi.3D_Engine.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

        self.setWindowTitle('3D_Engine')

        self.rotate_up = False
        self.rotate_left = False
        self.rotate_right = False
        self.rotate_down = False
        self.turn_left = False
        self.turn_right = False

        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False

        self.view_x = 0
        self.view_y = 0

        self.width_h = self.width // 2
        self.hight_h = self.hight // 2

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(0)
        
        # Select the PLY Data 
        self.polygone = load_poly('ply_data/bunny/bun_zipper_res4.ply')

        self.polygone.zoom_image(2000)
        x, y, z = mid_point(self.polygone.poly)
        self.polygone.verschieben(self.width_h + -x, self.hight_h + -y,
                          math.sqrt(pow(self.width_h, 2) + pow(self.hight_h, 2)))

    def animation(self):

        self.polygone.verschieben(-self.width_h - 10 * self.view_x, -self.hight_h - 10 * self.view_y,
                          -math.sqrt(pow(self.width_h, 2) + pow(self.hight_h, 2)))

        if self.rotate_right:
            self.polygone.rotate_x_y(-1, 0, 0)

        if self.rotate_left:
            self.polygone.rotate_x_y(1, 0, 0)

        if self.rotate_down:
            self.polygone.rotate_y_z(1, 0, 0)

        if self.rotate_up:
            self.polygone.rotate_y_z(-1, 0, 0)

        if self.turn_right:
            self.polygone.rotate_x_z(1, 0, 0)

        if self.turn_left:
            self.polygone.rotate_x_z(-1, 0, 0)

        if self.move_left:
            self.view_x -= 1

        if self.move_up:
            self.view_y -= 1

        if self.move_down:
            self.view_y += 1

        if self.move_right:
            self.view_x += 1

        self.polygone.mergeSort(self.polygone.poly)
        self.polygone.verschieben(self.width_h + 10 * self.view_x, self.hight_h + 10 * self.view_y,
                          math.sqrt(pow(self.width_h, 2) + pow(self.hight_h, 2)))

        self.update()

    def paintEvent(self, event):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor("black"))
        painter = QPainter(self)
        painter.setPen(pen)
        painter.fillRect(QRect(0, 0, self.width, self.hight), QColor("white"))

        # Malt alle Polygone
        for i in range(len(self.polygone.poly)):
            pen.setColor(QColor("black"))
            painter.setPen(pen)

            point1x = int(self.polygone.poly[i][0][0])
            point1y = int(self.polygone.poly[i][0][1])

            point2x = int(self.polygone.poly[i][1][0])
            point2y = int(self.polygone.poly[i][1][1])

            point3x = int(self.polygone.poly[i][2][0])
            point3y = int(self.polygone.poly[i][2][1])

            pointsF = QPolygonF([
                QPoint(point1x, point1y),
                QPoint(point2x, point2y),
                QPoint(point3x, point3y)
            ])

            fill_brush = QBrush()
            fill_brush.setColor(self.polygone.poly[i][3])
            fill_brush.setStyle(Qt.SolidPattern)

            path = QPainterPath()
            path.addPolygon(pointsF)

            painter.fillPath(path, fill_brush)
            painter.drawPolygon(pointsF)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_A:
            self.rotate_left = True
        if key == Qt.Key_W:
            self.rotate_up = True
        if key == Qt.Key_S:
            self.rotate_down = True
        if key == Qt.Key_D:
            self.rotate_right = True
        if key == Qt.Key_Q:
            self.turn_left = True
        if key == Qt.Key_E:
            self.turn_right = True

        if key == Qt.Key_Up:
            self.move_up = True

        if key == Qt.Key_Down:
            self.move_down = True

        if key == Qt.Key_Left:
            self.move_left = True

        if key == Qt.Key_Right:
            self.move_right = True

        if key == Qt.Key_Up:
            self.view_y -= 1
            self.polygone.verschieben(0, -10, 0)

        if key == Qt.Key_Down:
            self.view_y += 1
            self.polygone.verschieben(0, 10, 0)

        if key == Qt.Key_Left:
            self.view_x -= 1
            self.polygone.verschieben(-10, 0, 0)

        if key == Qt.Key_Right:
            self.view_x += 1
            self.polygone.verschieben(10, 0, 0)

        if key == Qt.Key_Minus:
            self.polygone.un_zoom_image(2)
            self.polygone.verschieben(self.width_h // 2, self.hight_h // 2, 0)

        if key == Qt.Key_Escape:
            sys.exit()

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key_A:
            self.rotate_left = False
        if key == Qt.Key_W:
            self.rotate_up = False
        if key == Qt.Key_S:
            self.rotate_down = False
        if key == Qt.Key_D:
            self.rotate_right = False
        if key == Qt.Key_Q:
            self.turn_left = False
        if key == Qt.Key_E:
            self.turn_right = False

        if key == Qt.Key_Up:
            self.move_up = False

        if key == Qt.Key_Down:
            self.move_down = False

        if key == Qt.Key_Left:
            self.move_left = False

        if key == Qt.Key_Right:
            self.move_right = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = main_application()
    application.show()
    sys.exit(app.exec_())



