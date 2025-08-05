from PyQt5.QtGui import *
import math
import random


def mid_point_z(obj):
    z = 0
    for i in range(len(obj) - 2):
        z = z + obj[i][2]
    z = z / len(obj)
    return z


def mid_point(obj):
    x = y = z = 0
    for i in range(len(obj)):
        x = x + obj[i][0][0] + obj[i][1][0] + obj[i][2][0]
        y = y + obj[i][0][1] + obj[i][1][1] + obj[i][2][1]
        z = z + obj[i][0][2] + obj[i][1][2] + obj[i][2][2]
    x = x / (len(obj) * 3)
    y = y / (len(obj) * 3)
    z = z / (len(obj) * 3)
    return x, y, z


class Polygonen:
    def __init__(self):
        self.poly = []
        self.point = []
        self.rand_color = 0
        self.list = []

    def add_point(self, x, y, z):
        self.point.append([x, y, z])

    def add_list(self, first, second, third):
        self.list.append([first, second, third])

    def add_poly(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, rgb):
        max_z = (z1 + z2 + z3) / 3
        self.poly.append([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3], rgb, max_z])
        self.poly_sort()

    def del_poly(self, n):
        self.poly.pop(n)

    def poly_sort(self):
        if len(self.poly) >= 2:
            i = len(self.poly) - 1
            while i > 0:
                if self.poly[i][4] < self.poly[i - 1][4]:
                    temp = self.poly[i - 1]
                    self.poly[i - 1] = self.poly[i]
                    self.poly[i] = temp
                    i -= 1
                else:
                    i = 0

    def random_colour(self):
        return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

    def zoom_image(self, n):
        for i in range(len(self.poly)):
            self.poly[i][0][0] *= n
            self.poly[i][0][1] *= n
            self.poly[i][0][2] *= n
            self.poly[i][1][0] *= n
            self.poly[i][1][1] *= n
            self.poly[i][1][2] *= n
            self.poly[i][2][0] *= n
            self.poly[i][2][1] *= n
            self.poly[i][2][2] *= n

    def un_zoom_image(self, n):
        for i in range(len(self.poly)):
            self.poly[i][0][0] //= n
            self.poly[i][0][1] //= n
            self.poly[i][0][2] //= n
            self.poly[i][1][0] //= n
            self.poly[i][1][1] //= n
            self.poly[i][1][2] //= n
            self.poly[i][2][0] //= n
            self.poly[i][2][1] //= n
            self.poly[i][2][2] //= n

    def verschieben(self, x, y, z):
        for i in range(len(self.poly)):
            self.poly[i][0][0] += x
            self.poly[i][0][1] += y
            self.poly[i][0][2] += z
            self.poly[i][1][0] += x
            self.poly[i][1][1] += y
            self.poly[i][1][2] += z
            self.poly[i][2][0] += x
            self.poly[i][2][1] += y
            self.poly[i][2][2] += z

    def rotate_x_y(self, grad, cx, cy):
        theta = math.radians(grad)
        cosang, sinang = math.cos(theta), math.sin(theta)

        for i in range(len(self.poly)):
            for k in range(len(self.poly[i]) - 2):
                x, y = self.poly[i][k][0], self.poly[i][k][1]
                tx, ty = x - cx, y - cy
                new_x = (tx * cosang + ty * sinang) + cx
                new_y = (-tx * sinang + ty * cosang) + cy
                self.poly[i][k][0] = new_x
                self.poly[i][k][1] = new_y

    def rotate_y_z(self, grad, cy, cz):
        theta = math.radians(grad)
        cosang, sinang = math.cos(theta), math.sin(theta)
        for i in range(len(self.poly)):
            for k in range(len(self.poly[i]) - 2):
                y, z = self.poly[i][k][1], self.poly[i][k][2]
                ty, tz = y - cy, z - cz
                new_y = (ty * cosang + tz * sinang) + cy
                new_z = (-ty * sinang + tz * cosang) + cz
                self.poly[i][k][1] = new_y
                self.poly[i][k][2] = new_z

    def rotate_x_z(self, grad, cx, cz):
        theta = math.radians(grad)
        cosang, sinang = math.cos(theta), math.sin(theta)
        for i in range(len(self.poly)):
            for k in range(len(self.poly[i]) - 2):
                x, z = self.poly[i][k][0], self.poly[i][k][2]
                tx, tz = x - cx, z - cz
                new_x = (tx * cosang + tz * sinang) + cx
                new_z = (-tx * sinang + tz * cosang) + cz
                self.poly[i][k][0] = new_x
                self.poly[i][k][2] = new_z

    def mergeSort(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]
            self.mergeSort(L)
            self.mergeSort(R)
            i = j = k = 0
            while i < len(L) and j < len(R):
                z1 = mid_point_z(L[i])
                z2 = mid_point_z(R[j])
                if z1 < z2:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
