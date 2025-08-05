from logic.logic import *

def read_file(file):
    with open(file) as b:
        lines = b.readlines()
    return lines

def find(lines):
    number = 0
    temp = 0
    for i in range(len(lines)):
        if "element vertex" in lines[i]:
            number = lines[i].split(" ")[2]
        if "end_header" in lines[i]:
            temp = i + 1
            break
    return number, temp

def load_poly(file: str) -> Polygonen:
    poly = Polygonen()
    k = read_file(file)
    num, start = find(k)

    for i in range(int(start), int(num) + int(start)):
        poly.add_point(float(k[i].split(" ")[0]), float(k[i].split(" ")[1]), float(k[i].split(" ")[2]))
    for i in range(int(start) + int(num), len(k)):
        poly.add_list(int(k[i].split(" ")[1]), int(k[i].split(" ")[2]), int(k[i].split(" ")[3]))
    for i in range(len(poly.list)):
            poly.add_poly(-poly.point[poly.list[i][0]][0], -poly.point[poly.list[i][0]][1],
                        -poly.point[poly.list[i][0]][2],
                        -poly.point[poly.list[i][1]][0], -poly.point[poly.list[i][1]][1],
                        -poly.point[poly.list[i][1]][2],
                        -poly.point[poly.list[i][2]][0], -poly.point[poly.list[i][2]][1],
                        -poly.point[poly.list[i][2]][2],
                        QColor("blue"))
            
    return poly



