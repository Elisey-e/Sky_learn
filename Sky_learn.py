from sys import argv, exit
from os import listdir, curdir, walk, remove, mkdir, rename
from os.path import abspath, exists, dirname
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QInputDialog,\
    QMessageBox, QFileDialog, QKeySequenceEdit, QAction, qApp, QMainWindow, QDialog, QScrollArea
from os import listdir, remove, mkdir, rename
from os.path import abspath, dirname
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QInputDialog,\
    QMessageBox, QAction, qApp, QMainWindow, QDialog,\
    QGridLayout, QComboBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QLinearGradient, QImage, QPalette, QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import QObject, pyqtSignal, QSize, Qt, QUrl, QRect
from time import localtime, timezone, sleep
import webbrowser
from PyQt5.QtGui import QPainter, QPen, QBrush, QLinearGradient, QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QRect
from time import sleep
from shutil import copy
from time import time
from PIL import Image
from math import acos, degrees, radians, sin
from math import acos, sin

import tkinter as tk

root = tk.Tk()
from ctypes import *


new = ''
UT = ''
alph = 'αβγδεζηθικλμνξοπρστυφχψω'
dial = ''
opened = ''
s = ''
uuu = ''
rosticin = ''
kode = 0
true = ''
qq = []
searcher_global = False
screen_increase = 1.25
point_type = ''


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.pixmap = QPixmap("Skycharts\\ground.png")
        im = Image.open("Skycharts\\ground.png")
        self.x, self.y = im.size
        self.setGeometry(200, 100, *(self.x, self.y))
        self.setWindowTitle('Sky Learn')
        self.setWindowIcon(QIcon('title.jpg'))
        self.abs_h = 0
        self.k = 0
        self.on = False
        self.draw_buttons = False
        self.abs_h_2 = 0

        exitAction = QAction(QIcon('exit.png'), '&Закрыть', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть всё')
        exitAction.triggered.connect(qApp.quit)

        sys_size = QAction('&Подстроить масштаб', self)
        sys_size.setShortcut('Ctrl+S')
        sys_size.setStatusTip('Подстроить масштаб элементов')
        sys_size.triggered.connect(self.change_size)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Общие')
        fileMenu1.addAction(exitAction)
        fileMenu1.addAction(sys_size)

        self.button_cons_lines = QPushButton("Линии созвездий", self)
        self.button_cons_lines.setFont(QFont('SansSerif', 20))
        self.button_cons_lines.resize(400, 50)
        self.button_cons_lines.move(450, self.y + 10)

        self.button_cons_names = QPushButton("Названия созвездий", self)
        self.button_cons_names.setFont(QFont('SansSerif', 20))
        self.button_cons_names.resize(400, 50)
        self.button_cons_names.move(450, self.y + 10)

        self.button_stars_names = QPushButton("Названия звезд", self)
        self.button_stars_names.setFont(QFont('SansSerif', 20))
        self.button_stars_names.resize(400, 50)
        self.button_stars_names.move(450, self.y + 10)

        self.button_dss_messier = QPushButton("Объекты Мессье", self)
        self.button_dss_messier.setFont(QFont('SansSerif', 20))
        self.button_dss_messier.resize(400, 50)
        self.button_dss_messier.move(450, self.y + 10)

        self.button_dss_caldwell = QPushButton("Объекты Колдуэлла", self)
        self.button_dss_caldwell.setFont(QFont('SansSerif', 20))
        self.button_dss_caldwell.resize(400, 50)
        self.button_dss_caldwell.move(450, self.y + 10)

        self.button_solar_bodies = QPushButton("Объекты СС", self)
        self.button_solar_bodies.setFont(QFont('SansSerif', 20))
        self.button_solar_bodies.resize(400, 50)
        self.button_solar_bodies.move(450, self.y + 10)

        self.button_meteor_showers = QPushButton("Метеорные потоки", self)
        self.button_meteor_showers.setFont(QFont('SansSerif', 20))
        self.button_meteor_showers.resize(400, 50)
        self.button_meteor_showers.move(450, self.y + 10)

        self.button_sphere_notes = QPushButton("Обозначения небесной сферы", self)
        self.button_sphere_notes.setFont(QFont('SansSerif', 20))
        self.button_sphere_notes.resize(400, 50)
        self.button_sphere_notes.move(450, self.y + 10)

        self.button_dss_messier.clicked.connect(self.open_messier)
        self.button_cons_lines.clicked.connect(self.open_constellations)
        self.button_cons_names.clicked.connect(self.ans)


        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def wheelEvent(self, e):
        a = str(e.angleDelta())
        b = a[a.find('(') + 1: a.find(')')]
        q = b.split(', ')
        if abs(int(q[1])) > 150:
            q[1] = '0'
        if self.abs_h_2 < 0:
            self.draw_buttons = False
            self.abs_h -= 1
        if not self.draw_buttons:
            self.abs_h += -int(q[1])
        if self.abs_h > 1000:
            self.abs_h = 1000
            self.draw_buttons = True
        if self.abs_h < 0:
            self.abs_h = 0
        k_old = self.k
        self.k = (self.abs_h // 100) * 100
        if k_old != self.k:
            self.pixmap = QPixmap("Skycharts\\grounds\\ground" + str(self.k // 5) + ".jpg")
            self.update()
        if self.draw_buttons:
            self.abs_h_2 -= int(q[1])
            if self.abs_h_2 > 1000:
                self.abs_h_2 = 1000
            self.do_buttons()

    def do_buttons(self):
        self.cons_lines_pixmap = QPixmap("Skycharts\\main_sections\\constallations.png")
        self.cons_names_pixmap = QPixmap("Skycharts\\main_sections\\cons_names.png")
        self.stars_names_pixmap = QPixmap("Skycharts\\main_sections\\stars_names.png")
        self.messier_pixmap = QPixmap("Skycharts\\main_sections\\messier.png")
        self.caldwell_pixmap = QPixmap("Skycharts\\main_sections\\caldwell.png")
        *ok, self.cons_x, self.cons_y = self.cons_lines_pixmap.rect().getCoords()
        self.button_cons_lines.move(70, self.y + 50 - self.abs_h_2)
        self.button_cons_names.move(570, self.y + 50 - self.abs_h_2)
        self.button_stars_names.move(1070, self.y + 50 - self.abs_h_2)
        self.button_dss_messier.move(310, self.y + 450 - self.abs_h_2)
        self.button_dss_caldwell.move(830, self.y + 450 - self.abs_h_2)
        self.update()

    def drawLines(self, qp):
        qp.drawPixmap(QRect(*(0, 0), *(self.x, self.y)), self.pixmap)
        if self.draw_buttons:
            qp.drawPixmap(QRect(*(70, self.y + 100 - self.abs_h_2), *(400, int(self.cons_y * 400 / self.cons_x))), self.cons_lines_pixmap)
            qp.drawPixmap(QRect(*(570, self.y + 100 - self.abs_h_2), *(400, int(self.cons_y * 400 / self.cons_x))), self.cons_names_pixmap)
            qp.drawPixmap(QRect(*(1070, self.y + 100 - self.abs_h_2), *(400, int(self.cons_y * 400 / self.cons_x))), self.stars_names_pixmap)
            qp.drawPixmap(QRect(*(310, self.y + 500 - self.abs_h_2), *(400, int(self.cons_y * 400 / self.cons_x))), self.messier_pixmap)
            qp.drawPixmap(QRect(*(830, self.y + 500 - self.abs_h_2), *(400, int(self.cons_y * 400 / self.cons_x))), self.caldwell_pixmap)

    def prosess_ground(self):
        im = Image.open("Skycharts\\ground.png")
        im_di = Image.open("Skycharts\\ground_misted.jpg")
        pix_1 = im.load()
        pix_2 = im_di.load()
        for j in range(self.y - 1):
            for i in range(self.x - 1):
                pix_1[i, j] = (int(pix_1[i, j][0] * self.k / 200) + int(pix_2[i, j][0] * (-self.k + 200) / 200),
                         int(pix_1[i, j][1] * self.k / 200) + int(pix_2[i, j][1] * (-self.k + 200) / 200),
                         int(pix_1[i, j][2] * self.k / 200) + int(pix_2[i, j][2] * (-self.k + 200) / 200))
        im.save("Skycharts\\build\\ground.png")
        self.pixmap = QPixmap("Skycharts\\build\\ground.png")
        remove(abspath(curdir) + '\\Skycharts\\build\\ground.png')
        print(self.k)
        self.update()

    def change_size(self):
        global screen_increase
        i, okBtnPressed = QInputDialog.getInt(self, "Масштаб",
                                              "Введите масштаб, %",
                                              150, 100, 175, 25)
        if okBtnPressed:
            screen_increase = i / 100

    def keyPressEvent(self, e):
        if e.key() == 16777220 or e.key() == Qt.Key_Enter:
            self.add()
        if e.key() == Qt.Key_F1:
            dialog = Information_Dialog(self)

    def open_messier(self):
        self.dia('messier')

    def open_constellations(self):
        self.dia('constellations')

    def dia(self, type):
        global qq, searcher_global
        q = sorted(listdir(path=abspath(curdir) + '\\Skycharts\\constellations'))
        qq = q
        s = searcher(self)
        s.exec_()
        self.TwoWindow = None
        if searcher_global:
            searcher_global = False
            if type == 'messier':
                self.set_clock_window('open messier')
            elif type == 'constellations':
                self.set_clock_window('open chart')

    def add(self):
        global new
        i, okBtnPressed = QInputDialog.getItem(self, "Выбрать редактор",
                                               "Выберите редактор\n",
                                               ('Созвездия', 'Точечные объекты'),
                                               0, False)
        if okBtnPressed:
            if i == 'Созвездия':
                self.set_clock_window('new chart')
            elif i == 'Точечные объекты':
                self.set_clock_window('new point')
            new = i

    def set_clock_window(self, i):
        global dial, point_type
        if i == 'new chart':
            dialog = ConstellationEditor(self)
            dial = dialog
        elif i == 'open chart':
            dialog = ConstellationDialog(self)
            dial = dialog
        elif i == 'open messier':
            point_type = 'messier'
            dialog = MessierDialog(self)
            dial = dialog
        if i == 'new point':
            dialog = PointsEditor(self)
            dial = dialog

    def ans(self):
        global opened, s
        f = open("Skycharts\\Cons_bayer.txt")
        q = f.readlines()
        f.close()
        q = list(map(lambda x: [x[:x.rfind(' ')], x[-4:-1]], q))
        se = {}
        for i in q:
            se[i[0]] = i[1]
        s = se
        opened = Guess_Cons(self)


class MessierDialog(QMainWindow):
    def __init__(self, parent=None):
        super(MessierDialog, self).__init__(parent)

        reverse_color = QAction('&Цвет', self)
        reverse_color.setShortcut('Ctrl+R')
        reverse_color.setStatusTip('Изменить стиль картинки')
        reverse_color.triggered.connect(self.reverse_im)

        size = QAction('&Размер', self)
        size.setShortcut('Ctrl+K')
        size.setStatusTip('Изменить размер картинки')
        size.triggered.connect(self.ch_size)

        strictness = QAction('&Точность', self)
        strictness.setShortcut('Ctrl+S')
        strictness.setStatusTip('Изменить точность проведения линии')
        strictness.triggered.connect(self.change_strictness)

        FPS = QAction('&FPS', self)
        FPS.setShortcut('Ctrl+F')
        FPS.setStatusTip('Изменить частоту обновления картинки')
        FPS.triggered.connect(self.change_fps)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Общие')
        fileMenu1.addAction(FPS)
        fileMenu2 = menubar.addMenu('&Изображение')
        fileMenu2.addAction(reverse_color)
        fileMenu2.addAction(size)
        fileMenu3 = menubar.addMenu('&Выделение и проверка')
        fileMenu3.addAction(strictness)

        self.setWindowTitle(UT)
        self.im_pos = 400, 50
        self.win_x, self.win_y = root.winfo_screenwidth(), root.winfo_screenheight()
        self.setGeometry(0, 0, int(self.win_x * screen_increase) - 10, int(self.win_y * screen_increase) - 75 * screen_increase)
        self.dir = dirname(abspath(__file__))
        self.rasm = False
        self.pixmap = QPixmap('Skycharts\\constellations\\' + UT + '\\photo.png')
        im = Image.open('Skycharts\\constellations\\' + UT + '\\photo.png')
        self.real_size = im.size
        ma = max(self.real_size)
        self.im_size = tuple(map(lambda x: int(x / ma * self.win_x * screen_increase / 2), self.real_size))
        del im
        self.time = False
        self.user_data = []
        self.reversed = False
        self.deleted = []
        self.curr_pos = None
        self.k = 1
        self.fps = 25
        self.to_edit = False
        self.change_name = False

        self.wait = QLabel("", self)
        self.wait.resize(200, 30)
        self.wait.move(10, 60)

        self.st = QPushButton("Начать выделение", self)
        self.st.resize(200, 50)
        self.st.move(10, 50)
        self.st.clicked.connect(self.start)

        self.check = QPushButton("Проверить!", self)
        self.check.resize(200, 50)
        self.check.move(10, 110)
        self.check.clicked.connect(self.checker)

        self.to_show = False

        self.ans = QPushButton("Показать ответ", self)
        self.ans.resize(200, 50)
        self.ans.move(10, 170)
        self.ans.clicked.connect(self.show_ans)

        self.timer = QLabel("00:00:00.00", self)
        self.timer.setFont(QFont('SansSerif', 20))
        self.timer.resize(300, 50)
        self.timer.move(20, int(self.win_y * screen_increase) - 125 * screen_increase)
        self.stric = 20
        self.i = 0
        self.loader()
        self.show()

    def change_strictness(self):
        i, okBtnPressed = QInputDialog.getInt(self, "Точность",
                                              "Введите точность",
                                              5, 1, 50, 1)
        if okBtnPressed:
            self.stric = i

    def change_fps(self):
        i, okBtnPressed = QInputDialog.getInt(self, "FPS",
                                              "Введите fps",
                                              25, 1, 50, 1)
        if okBtnPressed:
            self.fps = i

    def reverse_im(self):
        if not self.reversed:
            im = Image.open('Skycharts\\constellations\\' + UT + '\\photo.png')
            pixels = im.load()
            x, y = im.size
            for i in range(x):
                for j in range(y):
                    c = 256 - sum(pixels[i, j]) // 3
                    pixels[i, j] = tuple([c for i in range(3)])
            rod = 0
            im.save(dirname(abspath(__file__)) + '/Skycharts/build/photo.png')
            self.pixmap = QPixmap(dirname(abspath(__file__)) + '/Skycharts/build/photo.png')
            remove(dirname(abspath(__file__)) + '/Skycharts/build/photo.png')
            self.reversed = not self.reversed
            self.update()
        else:
            self.pixmap = QPixmap('Skycharts\\constellations\\' + UT + '\\photo.png')
            self.reversed = not self.reversed
            self.update()

    def ch_size(self):
        i, okBtnPressed = QInputDialog.getInt(self, "Размер",
                                              "Введите размер в процентах от стандартного",
                                              100, 10, 200, 5)
        if okBtnPressed:
            k = i / 100
            self.im_size = tuple(map(lambda x: x * k / self.k, self.im_size))
            for j in range(len(self.true_data)):
                x, y = self.true_data[j][1][0], self.true_data[j][1][1]
                x = (x - self.im_pos[0]) * k / self.k + self.im_pos[0]
                y = (y - self.im_pos[1]) * k / self.k + self.im_pos[1]
                self.true_data[j] = [self.true_data[j][0], (x, y)]
            for j in range(len(self.user_data)):
                x, y = self.user_data[j][1][0], self.user_data[j][1][1]
                x = (x - self.im_pos[0]) * k / self.k + self.im_pos[0]
                y = (y - self.im_pos[1]) * k / self.k + self.im_pos[1]
                self.user_data[j] = [self.user_data[j][0], (x, y), self.user_data[j][2]]
            self.update()
            self.k = k

    def mousePressEvent(self, e):
        point = e.pos().x(), e.pos().y()
        if self.rasm:
            if self.to_edit:
                if self.im_pos[0] <= point[0] <= self.im_size[0] + self.im_pos[0] \
                        and self.im_pos[1] <= point[1] <= self.im_size[1] + self.im_pos[1]:
                    f = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5
                    found = 1
                    min = 1000
                    self.user_data[self.i][2] = QPen(Qt.yellow, 2)
                    for j in range(len(self.user_data)):
                        if f(self.user_data[j][1], point) < min:
                            found = self.user_data[j][0]
                            min = f(self.user_data[j][1], point)
                            self.i = j
                    self.user_data[self.i][2] = QPen(Qt.white, 2)
                    self.messier_pixmap = QPixmap('Skycharts\\messier\\m ' + str(found) + '.jpg')
                    self.change_name = True
            else:
                if self.im_pos[0] <= point[0] <= self.im_size[0] + self.im_pos[0] \
                        and self.im_pos[1] <= point[1] <= self.im_size[1] + self.im_pos[1]:
                    if point_type == 'messier' or point_type == 'caldwell':
                        i, okBtnPressed = QInputDialog.getInt(self, "Номер",
                                                              "Введите номер объекта",
                                                              1, 1, 110, 1)
                        if okBtnPressed:
                            self.user_data.append([i, point, QPen(Qt.yellow, 2)])
                    elif point_type == 'stars_bayer':
                        i, okBtnPressed = QInputDialog.getItem(self, "Буква",
                                                               "Выберите букву\n",
                                                               tuple(alph),
                                                               len(self.type_data), False)
                        if okBtnPressed:
                            i = alph.find(i) + 1
                            self.user_data.append([i, point, QPen(Qt.yellow, 2)])
                    self.update()

    def paintEvent(self, e):
        sleep(1 / self.fps)
        painter = QPainter(self)
        painter.drawPixmap(QRect(*self.im_pos, *self.im_size), self.pixmap)
        if self.change_name:
            painter.drawPixmap(QRect(*(50, 500), *(200, 200)), self.messier_pixmap)
        if self.rasm:
            st = time() - self.bal
            h = str(int((st // 3600) % 24)).rjust(2, '0')
            m = str(int((st // 60) % 60)).rjust(2, '0')
            s = str(st % 60)
            self.timer.setText(h + ':' + m + ':' + s[:s.find('.') + 3].rjust(5, '0'))
            self.update()
        for i in self.user_data:
            painter.setPen(i[2])
            painter.drawEllipse(i[1][0] - 5, i[1][1] - 5, 10, 10)
        if self.to_show:
            for i in self.true_data:
                painter.setPen(QPen(Qt.green, 2))
                painter.drawEllipse(i[1][0] - 5, i[1][1] - 5, 10, 10)
                self.update()

    def start(self):
        self.rasm = True
        self.bal = time()

    def checker(self):
        f = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5 <= self.stric
        k = 0
        res = False
        for i in self.user_data:
            found = False
            for j in self.true_data:
                if f(j[1], i[1]) is True and i[0] == j[0]:
                    found = True
                    k += 1
                    break
            if not found:
                i[2] = QPen(Qt.red, 2)
                res = True
        if k != len(self.true_data) or res is True:
            QMessageBox.information(None, "Результат", "Неверно", defaultButton=QMessageBox.Close)
        else:
            QMessageBox.information(None, "Результат", "Верно", defaultButton=QMessageBox.Close)

    def loader(self):
        path = 'Skycharts\\constellations\\' + UT + '\\' + point_type + '_data.txt'
        f1 = open(path, 'r')
        sp = f1.read().split('\n')
        self.true_data = []
        for i in sp:
            if i == '!':
                break
            name, x, y = map(float, i.split())
            name = int(name)
            k = self.im_size[0] / self.real_size[0]
            self.true_data.append([name, (x * k + self.im_pos[0], y * k + self.im_pos[1])])
        f1.close()

    def show_ans(self):
        if self.to_show == False:
            self.to_show = True
        else:
            self.to_show = False

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Z) and (e.modifiers() == Qt.ControlModifier):
            if len(self.user_data) != 0:
                self.user_data.pop(-1)
                self.update()
        if (e.key() == Qt.Key_E) and (e.modifiers() == Qt.ControlModifier):
            if self.to_edit:
                self.to_edit = False
            else:
                self.to_edit = True
        if (e.key() == Qt.Key_E) and self.to_edit:
            pass


class ConstellationDialog(QMainWindow):
    def __init__(self, parent=None):
        super(ConstellationDialog, self).__init__(parent)
        exitAction = QAction(QIcon('exit.png'), '&Закрыть', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть всё')
        exitAction.triggered.connect(qApp.quit)

        reverse_color = QAction('&Цвет', self)
        reverse_color.setShortcut('Ctrl+R')
        reverse_color.setStatusTip('Изменить стиль картинки')
        reverse_color.triggered.connect(self.reverse_im)

        size = QAction('&Размер', self)
        size.setShortcut('Ctrl+K')
        size.setStatusTip('Изменить размер картинки')
        size.triggered.connect(self.ch_size)

        strictness = QAction('&Точность', self)
        strictness.setShortcut('Ctrl+S')
        strictness.setStatusTip('Изменить точность проведения линии')
        strictness.triggered.connect(self.change_strictness)

        FPS = QAction('&FPS', self)
        FPS.setShortcut('Ctrl+F')
        FPS.setStatusTip('Изменить частоту обновления картинки')
        FPS.triggered.connect(self.change_fps)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Общие')
        fileMenu1.addAction(exitAction)
        fileMenu1.addAction(FPS)
        fileMenu2 = menubar.addMenu('&Изображение')
        fileMenu2.addAction(reverse_color)
        fileMenu2.addAction(size)
        fileMenu3 = menubar.addMenu('&Выделение и проверка')
        fileMenu3.addAction(strictness)
        self.setWindowTitle(UT)
        self.im_pos = 300, 50
        self.win_x, self.win_y = root.winfo_screenwidth(), root.winfo_screenheight()
        self.setGeometry(0, 0, int(self.win_x*screen_increase) - 10, int(self.win_y*screen_increase) - 75 * screen_increase)
        self.dir = dirname(abspath(__file__))
        self.rasm = False
        self.pixmap = QPixmap('Skycharts\\constellations\\' + UT + '\\photo.png')
        im = Image.open('Skycharts\\constellations\\' + UT + '\\photo.png')
        self.real_size = im.size
        ma = max(self.real_size)
        self.im_size = tuple(map(lambda x: int(x / ma * self.win_x * screen_increase / 2), self.real_size))
        self.im_size_um = self.im_size
        del im
        self.paint = False
        self.time = False
        self.lines = []
        self.reversed = False
        self.deleted = []
        self.curr_pos = None
        self.k = 1
        self.fps = 40

        self.wait = QLabel("", self)
        self.wait.resize(200, 30)
        self.wait.move(10, 60)

        self.st = QPushButton("Начать выделение", self)
        self.st.resize(200, 50)
        self.st.move(10, 50)
        self.st.clicked.connect(self.start)

        self.check = QPushButton("Проверить!", self)
        self.check.resize(200, 50)
        self.check.move(10, 110)
        self.check.clicked.connect(self.checker)

        self.to_show = False

        self.ans = QPushButton("Показать ответ", self)
        self.ans.resize(200, 50)
        self.ans.move(10, 170)
        self.ans.clicked.connect(self.show_ans)

        self.timer = QLabel("00:00:00.00", self)
        self.timer.setFont(QFont('SansSerif', 20))
        self.timer.resize(300, 50)
        self.timer.move(20, int(self.win_y * screen_increase) - 125 * screen_increase)
        self.ros = False
        self.rost = False
        self.stric = 5
        self.loader()
        self.show()

    def ch_size(self):
        i, okBtnPressed = QInputDialog.getInt(self, "Размер",
                                              "Введите размер в процентах от стандартного",
                                              100, 10, 200, 5)
        if okBtnPressed:
            k = i / 100
            self.im_size = tuple(map(lambda x: x * k, self.im_size_um))
            for j in range(len(self.true_lines)):
                x1, y1, x2, y2 = *self.true_lines[j][0], *self.true_lines[j][1]
                x1 -= self.im_pos[0]
                x2 -= self.im_pos[0]
                y1 -= self.im_pos[1]
                y2 -= self.im_pos[1]
                self.true_lines[j] = ((x1 * k / self.k + self.im_pos[0], y1 * k / self.k + self.im_pos[1]),
                                      (x2 * k / self.k + self.im_pos[0], y2 * k / self.k + self.im_pos[1]))
            for j in range(len(self.lines)):
                x1, y1, x2, y2 = *self.lines[j][0], *self.lines[j][1]
                x1 -= self.im_pos[0]
                x2 -= self.im_pos[0]
                y1 -= self.im_pos[1]
                y2 -= self.im_pos[1]
                self.lines[j] = ((x1 * k / self.k + self.im_pos[0], y1 * k / self.k + self.im_pos[1]),
                                (x2 * k / self.k + self.im_pos[0], y2 * k / self.k + self.im_pos[1]))
            self.update()
            self.k = k

    def change_strictness(self):
        i, okBtnPressed = QInputDialog.getInt(self, "Точность",
                                              "Введите точность",
                                              5, 1, 50, 1)
        if okBtnPressed:
            self.stric = i

    def change_fps(self):
        i, okBtnPressed = QInputDialog.getInt(self, "FPS",
                                              "Введите fps",
                                              25, 1, 50, 1)
        if okBtnPressed:
            self.fps = i

    def reverse_im(self):
        if not self.reversed:
            im = Image.open(dirname(abspath(__file__)) + '/Skycharts/constellations/' + UT + '/photo.png')
            pixels = im.load()
            x, y = im.size
            for i in range(x):
                for j in range(y):
                    c = 256 - sum(pixels[i, j]) // 3
                    pixels[i, j] = tuple([c for i in range(3)])
            rod = 0
            im.save('Skycharts\\build\\photo.png')
            self.pixmap = QPixmap('Skycharts\\build\\photo.png')
            remove(abspath(curdir) + '\\Skycharts\\build\\photo.png')
            self.reversed = not self.reversed
            self.update()
        else:
            self.pixmap = QPixmap(dirname(abspath(__file__)) + '/Skycharts/constellations/' + UT + '/photo.png')
            self.reversed = not self.reversed
            self.update()

    def mouseReleaseEvent(self, e):
        if self.point != self.curr_pos and self.curr_pos is not None and self.ros and self.rost and self.rasm:
            if self.im_pos[0] <= self.curr_pos[0] <= self.im_size[0] + self.im_pos[0] \
                    and self.im_pos[1] <= self.curr_pos[1] <= self.im_size[1] + self.im_pos[1]:
                self.lines.append((self.point, self.curr_pos))
                self.deleted.clear()
                self.rost = False
                self.ros = False
                self.point = (0, 0)
                self.curr_pos = None
            else:
                self.ros = False
                self.rost = False

    def mouseDoubleClickEvent(self, e):
        if self.rasm:
            coord = e.pos().x(), e.pos().y()
            f = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5
            mi = 1000
            v = 0
            for i in self.lines:
                d1 = f(i[0], coord) + 1
                d2 = f(i[1], coord) + 1
                d3 = f(i[0], i[1]) + 1
                angel = acos((d1 ** 2 + d3 ** 2 - d2 ** 2) / (2 * d1 * d3))
                h = d1 * sin(angel)
                if h < mi:
                    v = i
                    mi = h
            if self.lines:
                self.lines.remove(v)

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Z) and (e.modifiers() == Qt.ControlModifier):
            if len(self.lines) != 0:
                self.deleted.append(self.lines.pop(-1))
                self.update()
        if (e.key() == Qt.Key_Z) and (e.modifiers() == Qt.ShiftModifier):
            if len(self.deleted) != 0:
                self.lines.append(self.deleted.pop(-1))
                self.update()

    def mousePressEvent(self, e):
        point = e.pos().x(), e.pos().y()
        self.point = point
        if self.rasm:
            if self.im_pos[0] <= point[0] <= self.im_size[0] + self.im_pos[0]\
                    and self.im_pos[1] <= point[1] <= self.im_size[1] + self.im_pos[1]:
                self.ros = True
                self.paint = True
                self.update()

    def mouseMoveEvent(self, e):
        if self.rasm:
            self.curr_pos = e.pos().x(), e.pos().y()
            self.rost = True

    def paintEvent(self, e):
        sleep(1 / self.fps)
        painter = QPainter(self)
        painter.drawPixmap(QRect(*self.im_pos, *self.im_size), self.pixmap)
        if self.rasm:
            st = time() - self.bal
            h = str(int((st // 3600) % 24)).rjust(2, '0')
            m = str(int((st // 60) % 60)).rjust(2, '0')
            s = str(st % 60)
            self.timer.setText(h + ':' + m + ':' + s[:s.find('.') + 3].rjust(5, '0'))
            self.update()
        if self.ros and self.rost:
            painter.setPen(Qt.red)
            painter.drawLine(*self.point, *self.curr_pos)
            self.update()
        for i in self.lines:
            painter.setPen(Qt.red)
            painter.drawLine(round(i[0][0]), round(i[0][1]), round(i[1][0]), round(i[1][1]))
        if self.to_show:
            for i in self.true_lines:
                painter.setPen(Qt.blue)
                painter.drawLine(round(i[0][0]), round(i[0][1]), round(i[1][0]), round(i[1][1]))
                self.update()

    def start(self):
        self.rasm = True
        self.bal = time()

    def checker(self):
        f = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5 <= self.stric
        k = 0
        for i in self.lines:
            found = []
            for j in self.true_lines:
                if f(j[0], i[0]) == f(j[1], i[1]) == True:
                    found = True
                    k += 1
                    break
                elif f(j[1], i[0]) == f(j[0], i[1]) == True:
                    found = True
                    k += 1
                    break
            if not found:
                QMessageBox.information(None, "Результат", "Неверно", defaultButton=QMessageBox.Close)
                return
        if k != len(self.true_lines):
            QMessageBox.information(None, "Результат", "Неверно", defaultButton=QMessageBox.Close)
        else:
            QMessageBox.information(None, "Результат", "Верно", defaultButton=QMessageBox.Close)

    def loader(self):
        path = dirname(abspath(__file__)) + '/Skycharts/constellations/' + UT + '/star_data.txt'
        f1 = open(path, 'r')
        sp = f1.read().split('\n')
        self.true_lines = []
        for i in sp:
            if i == '!':
                break
            x1, y1, x2, y2 = map(float, i.split())
            k = self.im_size[0] / self.real_size[0]
            self.true_lines.append(((x1 * k + self.im_pos[0], y1 * k + self.im_pos[1]),
                                    (x2 * k + self.im_pos[0], y2 * k + self.im_pos[1])))
        f1.close()

    def show_ans(self):
        if self.to_show == False:
            self.to_show = True
        else:
            self.to_show = False


class Information_Dialog(QMainWindow):
    def __init__(self, parent=None):
        super(Information_Dialog, self).__init__(parent)
        self.setGeometry(300, 100, 400, 400)
        self.setWindowTitle("Справка")
        self.setWindowIcon(QIcon('Ask.jpg'))

        self.abs_h = -3500

        self.title = QLabel('Справка', self)
        self.title.setFont(QFont('SansSerif', 20 / screen_increase))
        self.title.resize(200, 35)
        self.title.setStyleSheet("color: rgb(255, 0, 0);")

        self.t1 = QLabel('Разделы:', self)
        self.t1.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t1.resize(200, 25)
        self.t1.setStyleSheet("color: rgb(0, 0, 255);")

        self.dest_1 = QLabel('-Вступление', self)
        self.dest_1.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_1.resize(300, 25)
        self.dest_1.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_2 = QLabel('-Параметры справки', self)
        self.dest_2.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_2.resize(300, 25)
        self.dest_2.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_3 = QLabel('-Настройки под вашу ОС', self)
        self.dest_3.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_3.resize(300, 25)
        self.dest_3.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_4 = QLabel('-Непредвиденные обстоятельства', self)
        self.dest_4.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_4.resize(300, 25)
        self.dest_4.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_5 = QLabel('-Параметры главного окна', self)
        self.dest_5.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_5.resize(300, 25)
        self.dest_5.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_6 = QLabel('-Параметры боталки созвездий', self)
        self.dest_6.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_6.resize(300, 25)
        self.dest_6.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_7 = QLabel('-Параметры боталки названий созвездий', self)
        self.dest_7.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_7.resize(300, 25)
        self.dest_7.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_8 = QLabel('-Параметры боталки мессье', self)
        self.dest_8.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_8.resize(300, 25)
        self.dest_8.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_9 = QLabel('-Параметры боталки колдуэлла', self)
        self.dest_9.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_9.resize(300, 25)
        self.dest_9.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_10 = QLabel('-Параметры боталки звезд', self)
        self.dest_10.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_10.resize(300, 25)
        self.dest_10.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_11 = QLabel('-Параметры боталки объектов СС', self)
        self.dest_11.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_11.resize(300, 25)
        self.dest_11.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_12 = QLabel('-Параметры боталки метеорных потоков', self)
        self.dest_12.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_12.resize(300, 25)
        self.dest_12.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_13 = QLabel('-Параметры боталки небесных кругов', self)
        self.dest_13.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_13.resize(300, 25)
        self.dest_13.setStyleSheet("color: rgb(0, 100, 255);")

        self.dest_14 = QLabel('-Параметры редактора', self)
        self.dest_14.setFont(QFont('SansSerif', 12 / screen_increase))
        self.dest_14.resize(300, 25)
        self.dest_14.setStyleSheet("color: rgb(0, 100, 255);")

        self.t2 = QLabel('Вступление', self)
        self.t2.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t2.resize(400, 25)
        self.t2.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Приложение SkyLearn создано для удобной',
                  'подготовки к наблюдательной части олимпиад',
                  'по астрономии. Оно включает в себя',
                  'интерактивные задания на темы, приведенные',
                  'выше. В программе также реализован редактор',
                  'для добавления пользовательских заданий.',
                  'Кроссплатформенность приложения будет',
                  'достигнута на таких платформах как MacOs,',
                  'Windows 10, 7. К этим системам сейчас',
                  'имеется непосредственный доступ для проведения',
                  'редактирования у авторов. На остальных системах',
                  'работоспособность "из коробки" не гарантируется,',
                  'но у пользователя, обладающего примитивными',
                  'навыками программирования, будет иметься',
                  'возможность отредактировать программу под свой',
                  'аппарат. Автор советует полностью прочитать',
                  'справочные данные по приложению, потому что',
                  'оно имеет весьма нетривиальные фичи.']

        self.tx1 = QLabel('\n'.join(self.q), self)
        self.tx1.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx1.resize(1000, 1000)

        self.t3 = QLabel('Параметры справки', self)
        self.t3.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t3.resize(400, 25)
        self.t3.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Окно, в которое вы сейчас попали, называется',
                  'справочным. В него можно попасть, используя',
                  'клавишу F1 и характерные для вашей системы',
                  'клавиши – модификаторы(Fn, реже остальные).',
                  'Ниже они не будут вписываться в сочетания клавиш.',
                  '',
                  'Окно обладает возможностью медленной прокрутки',
                  'клавишами Up - Down, а также быстрой при помощи',
                  'PgUp – PgDown. ',
                  '',
                  'Содержательная часть включает оглавление с',
                  'доступом к подразделам по ссылкам. Достаточно',
                  'кликнуть правой кнопкой мыши на подраздел, и вас',
                  'телепортирует в тыкнутое место.',
                  '',
                  'Справка в том числе обладает гиперссылками,',
                  'ведущими в браузер. Они синие с подчеркиванием',
                  'снизу.']

        self.tx2 = QLabel('\n'.join(self.q), self)
        self.tx2.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx2.resize(1000, 1000)

        self.t4 = QLabel('Настройки под вашу ОС', self)
        self.t4.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t4.resize(400, 25)
        self.t4.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Как было описано, неразумно надеяться, что при',
                  'первом запуске программа начнет(если вдруг),',
                  'работать корректно у вас на компьютере.',
                  'Программа разрабатывалась на windows',
                  '– операционных системах, поэтому именно на них',
                  'вероятность получить что-то нерабочее, меньше,',
                  'чем для остальных. Тем не менее, отличные',
                  'настройки вашей системы могут негативно влиять',
                  'на работу приложения. Существуют как встроенные',
                  'в программу инструменты коррекции искажений, так',
                  'и ваши знания по программированию и',
                  'возможность менять сам код программы.',
                  '',
                  'Самая вероятная причина проблемы – разные',
                  'правила определения масштаба элементов у разных',
                  'ОС. Это влияет на многое – от размера окна до',
                  'расположения и размера текста. Поэтому мне',
                  'пришлось сделать пересчет координат всех объектов',
                  'через определенный системный коэффициент.',
                  'В Windows 10 он есть в настройках, далее я напишу,',
                  'как его найти. В остальных системах он тоже',
                  'присутствует в том или ином виде, просьба',
                  'погуглить самим). ',
                  '',
                  'Чтобы изменить коэффициент, зайдите в главном',
                  'окне в пункт Общие – Подстроить масштаб, либо',
                  'тыкните Ctrl+S. В диалоговом окне',
                  'поэкспериментируйте с коэффициентом, сделав',
                  'спорные элементы максимально эстетическими с',
                  'вашей точки зрения.',
                  '',
                  'Для Windows 10 в строке поиска вбейте параметр',
                  '“Изменение разрешения дисплея”, либо “Изменение',
                  'размера текста, приложений и других элементов”.',
                  'Далее найдите подраздел “Масштаб и разметка”.',
                  'Используемый там масштаб просто вставьте в',
                  'описанную сверху настройку.',
                  '',
                  'Важно понимать, что далеко не на все элементы',
                  'влияет коррекция масштаба, так что даже кривые',
                  'элементы могут не быть изменены. Ваша система',
                  'может просто не позволить скорректировать все',
                  'изменяемые элементы верно. Это должно быть',
                  'поводом для вас подобрать коэффициент,',
                  'доводящим ваше удовлетворение до локального',
                  'эстетического экстремума, если вас устраивает',
                  'такое расположение дел. Если проблем осталось',
                  'слишком много, можно как писать разработчикам,',
                  'так и использовать навыки программирования. Архив',
                  'питоновского проекта лежит на странице проекта,',
                  'главный файл запустится даже из консоли питона.',
                  'Если что, даже если проблему удалось устранить',
                  'программно, напишите плиз). Это помогает в',
                  'дальнейшем дебаггинге приложения.']

        self.tx3 = QLabel('\n'.join(self.q), self)
        self.tx3.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx3.resize(1000, 1500)

        self.t5 = QLabel('Непредвиденные обстоятельства', self)
        self.t5.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t5.resize(400, 25)
        self.t5.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Этот раздел отличается от предыдущего тем, что',
                  'здесь я опишу проблемы, склонные к возникновению',
                  'со временем при работе приложения.',
                  '',
                  'Сразу замечу, что в приложении нет чувствительных',
                  'к непредвиденному завершению работы компонент,',
                  'как и автосохранения. Так что при внезапном',
                  'завершении сеанса вы потеряете несохраненные',
                  'данные, но при этом маловероятен выход программы',
                  'из строя. Разные действия пользователя с системой',
                  'во время работы программы(например изменение',
                  'системного размера шрифта, см. предыдущий',
                  'раздел) могут повлечь как изменение элементов',
                  'программы, так и внезапную остановку её работы.'
                  '',
                  'Тем не менее, возможен самостоятельный выход',
                  'программы из строя, обычно сопровождающийся',
                  'банальным несохранением сеанса, но остается',
                  'вероятным и повреждение файлов программы. В',
                  'обоих случаях рекомендуется найти',
                  'дестабилизирующее действие, и написать',
                  'разработчикам. Во втором случае может помочь',
                  'переустановка программы, при этом наименее',
                  'вероятна потеря ваших настроек программы.',
                  '',
                  'Приложение чувствительно к языку раскладки',
                  'в контексте клавиатурных сокращений, так что',
                  'желательно работать в программе с английской',
                  'раскладкой']

        self.tx4 = QLabel('\n'.join(self.q), self)
        self.tx4.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx4.resize(1000, 1500)

        self.t6 = QLabel('Параметры главного окна', self)
        self.t6.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t6.resize(400, 25)
        self.t6.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Главное окно – среда для выбора режима подготовки.',
                  'В текущий момент оно включает 4 кнопки, на',
                  'которые можно нажимать. Делая это можно попасть либо',
                  'напрямую в режим для подготовки, либо в',
                  'предварительное окно режима для выбора его',
                  'параметров.',
                  '',
                  'Шапка окна включает описанную в разделе',
                  '“Настройки под вашу ОС” функцию изменения',
                  'масштаба текста.']

        self.tx5 = QLabel('\n'.join(self.q), self)
        self.tx5.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx5.resize(1000, 1500)

        self.t7 = QLabel('Параметры боталки созвездий', self)
        self.t7.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t7.resize(400, 25)
        self.t7.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Раздел призван дать вам возможность выучить',
                  'стандартный образ линий созвездий для олимпиад.',
                  'Культура созвездий Западная стеллариумовская.',
                  'Сведения раздела взяты из программы stellarium.',
                  '',
                  'В раздел можно попасть, нажав на кнопку',
                  '“Ботать созвездия” на главном окне. Сначала вы',
                  'перейдете в диалоговое окно выбора созвездия.',
                  'Там вы можете выбрать созвездие, которое вы',
                  'хотите выучить. Просто вбейте название созвездия',
                  'в поисковую строку или выберите название созвездия',
                  'из вападаемого списка. Регистр не имеет значения.',
                  'Как только искомое вами созвездие отобразится',
                  'выбранным вверху списка, можно нажимать ок.',
                  'Диалог сменится основным окном приложения.',
                  'Перейду к описанию настроек окна.',
                  '',
                  'В разделе “общие” есть настройка fps. Окно активно',
                  'использует ресурсы процессора при работе в нем,',
                  'поэтому может поглощать половину процессора. При',
                  'этом это не дота, поэтому бесполезно перегружать',
                  'процессор. Для снижения его нагрузки установите',
                  'удобное вам значение частоты отрисовки ваших',
                  'изменений на картинке. По умолчанию стоит 25',
                  'кадров в секунду. Если у вас майнинг ферма, можете',
                  'ставить мегагерц или больше, верхний предел',
                  'зависит только от вашего железа.',
                  '',
                  'В разделе “изображение” есть настройка цвета. Все',
                  'зависит от вашего вкуса – ботать небо по',
                  'стеллариуму или на распечатанных скайчартах.',
                  'Вторая настройка размера. Она позволит отдельно',
                  'подстроить вне зависимости от шрифта размер',
                  'изображения.',
                  '',
                  'Раздел “Выделение и проверка” включает настройку',
                  'точности.Когда вы запускаете проверку ваших линий',
                  'созвездия, программа должна решить, правильно ли',
                  'вы отрисовали некоторые спорные линии, или нет.',
                  'Точность – это максимальное расстояние в пикселях',
                  'конца вашего отрезка от конца верного, на котором',
                  'ваш будет зачтен. Увеличение точности расширяет',
                  'ваше право на ошибку, но при этом аналогичное',
                  'происходит и у программы. То есть криво',
                  'нарисованная вами верная линия может быть',
                  'зачтена, но при этом случайно оказавшаяся вблизи',
                  'неверная линия тоже может быть засчитана.',
                  'Значение по умолчанию рассчитано исходя из',
                  'усредненного размера звезды. Я не считаю, что',
                  'его стоит менять, просто старайтесь концом',
                  'линии попадать в звезду.',
                  '',
                  'Теперь перейду к описанию процесса бота. Кнопка',
                  '“Показать ответ” отображает верный контур',
                  'созвездия и только его. Её можно использовать как',
                  'для поиска ошибок у себя, так и для запоминания',
                  'фигуры созвездия. Кнопка “Начать выделение”',
                  'запускает таймер и одновременно дает вам доступ',
                  'к рисовалке на изображении. После того, как вы',
                  'закончили, нажмите на кнопку проверки; в',
                  'диалоговом окне отобразится ваш результат. При',
                  'закрытии этого окна ничего не изменится, и вы',
                  'сможете продолжить редактирование в скайчарте.',
                  '',
                  'Наконец, расскажу о методах взаимодействия с',
                  'изображением. Чтобы соединить 2 звезды линией,',
                  'наведите курсор на одну из них, нажмите ЛКМ,',
                  'затем переместите курсор ко второй звезде и',
                  'отпустите кнопку. Линия будет сохранена в',
                  'текущем сеансе. Направление выделения не важно.',
                  'Любые ваши взаимодействия выделением вне',
                  'изображения игнорируются. Чтобы удалить',
                  'последнюю линию, нажмите Ctrl+Z. Для удаления',
                  'произвольной линии совершите двойной клик ЛКМ',
                  'по месту на изображении. Будет удалена линия',
                  'на ближайшем расстоянии вдоль перпендикуляра к',
                  'прямой, содержащей эту линию. Важно!',
                  'Разработчику было лень модифицировать этот',
                  'алгоритм(в нем есть очев проблемы), ждите',
                  'нового релиза. Также вы можете отменить удаление,',
                  'нажав Shift+Z. Разумеется, после того, как вы',
                  'нарисуете новую линию, вернуть удаленные уже',
                  'будет нельзя(можно оспорить удобство, если',
                  'удобно не очищать список удаленных линий, и',
                  'восстанавливать в любой момент удаленную ранее',
                  'линию, как из стека, пишите, отредачу).']

        self.tx6 = QLabel('\n'.join(self.q), self)
        self.tx6.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx6.resize(1000, 2000)

        self.t8 = QLabel('Параметры редактора', self)
        self.t8.setFont(QFont('SansSerif', 18 / screen_increase))
        self.t8.resize(400, 25)
        self.t8.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Важно понимать, что редактор как таковой боооольшой костыль. Окда. Пизда.']

        self.tx7 = QLabel('\n'.join(self.q), self)
        self.tx7.setFont(QFont('SansSerif', 12 / screen_increase))
        self.tx7.resize(1000, 1500)

        #self.tx101 = QLabel('<a href="https://stellarium.org/ru/">Stellarium</a>', self)
        #self.tx101.setOpenExternalLinks(True)
        #self.tx101.resize(500, 100)
        #self.tx101.setStyleSheet("color: rgb(0, 0, 255);")

        self.generate()
        self.show()

    def generate(self):
        self.title.move(150, self.abs_h)
        self.t1.move(10, self.abs_h + 40)
        self.t2.move(10, self.abs_h + 360)
        self.t3.move(10, self.abs_h + 725)
        self.t4.move(10, self.abs_h + 1090)
        self.t5.move(10, self.abs_h + 2105)
        self.t6.move(10, self.abs_h + 2655)
        self.t7.move(10, self.abs_h + 2880)
        self.t8.move(10, self.abs_h + 4480)
        self.tx1.move(20, self.abs_h + 55)
        self.tx2.move(20, self.abs_h + 420)
        self.tx3.move(20, self.abs_h + 860)
        self.tx4.move(20, self.abs_h + 1645)
        self.tx5.move(20, self.abs_h + 2030)
        self.tx6.move(20, self.abs_h + 2695)
        self.tx7.move(20, self.abs_h + 4000)
        self.dest_1.move(30, self.abs_h + 70)
        self.dest_2.move(30, self.abs_h + 90)
        self.dest_3.move(30, self.abs_h + 110)
        self.dest_4.move(30, self.abs_h + 130)
        self.dest_5.move(30, self.abs_h + 150)
        self.dest_6.move(30, self.abs_h + 170)
        self.dest_7.move(30, self.abs_h + 190)
        self.dest_8.move(30, self.abs_h + 210)
        self.dest_9.move(30, self.abs_h + 230)
        self.dest_10.move(30, self.abs_h + 250)
        self.dest_11.move(30, self.abs_h + 270)
        self.dest_12.move(30, self.abs_h + 290)
        self.dest_13.move(30, self.abs_h + 310)
        self.dest_14.move(30, self.abs_h + 330)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Down:
            self.abs_h -= 10
            self.generate()
        if e.key() == Qt.Key_Up and self.abs_h < 0:
            self.abs_h += 10
            self.generate()
        if e.key() == Qt.Key_PageDown:
            self.abs_h -= 200
            self.generate()
        if e.key() == Qt.Key_PageUp:
            self.abs_h += 200
            if self.abs_h >= 0:
                self.abs_h = 0
            self.generate()
        if e.key() == Qt.Key_Home:
            self.abs_h = 0
            self.generate()
        if e.key() == Qt.Key_End:
            self.abs_h = -5000
            self.generate()


class PointsEditor(QMainWindow):
    def __init__(self, parent=None):
        super(PointsEditor, self).__init__(parent)
        exitAction = QAction(QIcon('exit.png'), '&Закрыть', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть всё')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Файл')
        fileMenu1.addAction(exitAction)

        self.win_x, self.win_y = root.winfo_screenwidth(), root.winfo_screenheight()
        self.setGeometry(0, 0, self.win_x, self.win_y)
        self.setWindowIcon(QIcon('title.jpg'))
        self.setWindowTitle('Редактор точечных объектов')
        self.mode = 'messier'
        self.pic = False
        self.paint = False
        self.draw = False
        self.rasm = False
        self.show_made = False
        self.delta = (400, 50)
        self.type_data = []

        self.photo = QPushButton('Выбрать режим', self)
        self.photo.resize(200, 50)
        self.photo.move(10, 70)
        self.photo.clicked.connect(self.set_mode)

        self.photo = QPushButton('Выбрать фото', self)
        self.photo.resize(200, 50)
        self.photo.move(10, 130)
        self.photo.clicked.connect(self.choose_photo)

        self.image = QLabel(self)
        self.image.move(400, 50)
        self.image.resize(911, 513)

        self.btn_cr = QPushButton('Определить директорию', self)
        self.btn_cr.resize(200, 50)
        self.btn_cr.move(10, 190)
        self.btn_cr.clicked.connect(self.create_folder)

        self.btn_st = QPushButton('Начать разметку', self)
        self.btn_st.resize(200, 50)
        self.btn_st.move(10, 250)
        self.btn_st.clicked.connect(self.redaction_permittion)

        self.btn_rev = QPushButton('Сохранить объект', self)
        self.btn_rev.resize(200, 50)
        self.btn_rev.move(10, 310)
        self.btn_rev.clicked.connect(self.save_object)

        self.btn_save = QPushButton('Сохранить и завершить', self)
        self.btn_save.resize(200, 50)
        self.btn_save.move(10, 370)
        self.btn_save.clicked.connect(self.saver)

        self.btn_save = QPushButton('Показать сделанное', self)
        self.btn_save.resize(200, 50)
        self.btn_save.move(10, 430)
        self.btn_save.clicked.connect(self.to_show_made)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_S:
            self.point = tuple([self.point[0], self.point[1] + 1])
            self.update()
        if e.key() == Qt.Key_W:
            self.point = tuple([self.point[0], self.point[1] - 1])
            self.update()
        if e.key() == Qt.Key_A:
            self.point = tuple([self.point[0] - 1, self.point[1]])
            self.update()
        if e.key() == Qt.Key_D:
            self.point = tuple([self.point[0] + 1, self.point[1]])
            self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        if self.pic:
            painter.drawPixmap(QRect(*self.delta, *self.im_size), self.pixmap)
        if self.paint:
            painter.setPen(QPen(Qt.red, 1))
            painter.drawEllipse(self.point[0] - 5, self.point[1] - 5, 10, 10)
            painter.drawLine(self.point[0] - 5, self.point[1], self.point[0] + 5, self.point[1])
            painter.drawLine(self.point[0], self.point[1] - 5, self.point[0], self.point[1] + 5)
        if self.show_made:
            for i in self.type_data:
                painter.setPen(QPen(Qt.red, 2))
                painter.drawEllipse(i[1][0] - 5, i[1][1] - 5, 10, 10)
                self.update()

    def mousePressEvent(self, e):
        point = e.pos().x(), e.pos().y()
        self.point = point
        if self.rasm:
            if self.delta[0] <= point[0] <= self.im_size[0] + self.delta[0] and self.delta[1] <= point[1] <= self.im_size[1] + self.delta[1]:
                self.paint = True
                self.update()
            else:
                self.paint = False

    def to_show_made(self):
        if self.show_made:
            self.show_made = False
        else:
            self.show_made = True

    def set_mode(self):
        i, okBtnPressed = QInputDialog.getItem(self, "Выбрать тип",
                                               "Выберите тип объектов\n",
                                               ('Мессье', 'Колдуэлл', 'Звезды по Байеру'),
                                               0, False)
        if okBtnPressed:
            if i == 'Meccье':
                self.mode = 'messier'
            elif i == 'Колдуэлл':
                self.mode = 'caldwell'
            elif i == 'Звезды по Байеру':
                self.mode = 'stars_bayer'

    def create_folder(self):
        dir = dirname(abspath(__file__))
        i, ok = QInputDialog.getText(self, '', 'Введите название скайчарта')
        if ok:
            dir += '/Skycharts/constellations/' + i
            try: mkdir(dir)
            except: QMessageBox.information(None, "Внимание", "Вы выбрали сохранение\n"
                                                                              "в имеющуюся директорию.\n"
                                                                              "Убедитесь, что вы этого желали", defaultButton=QMessageBox.Close)
            self.dir = dir
            try: copy(self.photo_path, dir)
            except: QMessageBox.information(None, "Внимание", "Вы выбрали имеющуюся\n"
                                                                              "в директории фотографию.\n"
                                                                              "Убедитесь, что вы этого желали", defaultButton=QMessageBox.Close)
            rename(dir + self.photo_path[self.photo_path.rfind('/'):], dir + '/photo.png')
            f1 = open(dir + '/' + self.mode + '_data.txt', 'w')
            f1.close()
            self.btn_cr.setEnabled(False)

    def choose_photo(self):
        if exists('C:\\Users\\Asus\\Pictures\\Stellarium'):
            fname, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                    'C:\\Users\\Asus\\Pictures\\Stellarium', "Картинка(*.png)")
        else:
            fname, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                    'C:\\Users\\Asus\\Pictures\\Stellarium', "Картинка(*.png)")
        if ok:
            self.photo_path = fname
            self.load_image()

    def load_image(self):
        self.pixmap = QPixmap(self.photo_path)
        im = Image.open(self.photo_path)
        self.real_size = im.size
        ma = max(self.real_size)
        self.im_size = tuple(map(lambda x: int(x / ma * self.win_x * screen_increase / 2), self.real_size))
        self.pic = True

    def saver(self):
        f1 = open(self.dir + '/' + self.mode + '_data.txt', 'w')
        for i in self.type_data:
            name, x, y = i[0], i[1][0], i[1][1]
            x -= self.delta[0]
            y -= self.delta[1]
            x = round(x * (self.real_size[0] / self.im_size[0]), 1)
            y = round(y * (self.real_size[0] / self.im_size[0]), 1)
            f1.write(' '.join([str(name), str(x), str(y)]) + '\n')
        f1.write('!')
        f1.close()
        self.close()

    def redaction_permittion(self):
        if self.rasm:
            self.rasm = False
            self.paint = False
            self.btn_st.setEnabled(False)
        else:
            self.rasm = True
            self.btn_st.setText('Закончить разметку')

    def save_object(self):
        if self.mode == 'messier' or self.mode == 'caldwell':
            fname, ok = QInputDialog.getInt(self, 'Номер', 'Введите номер объекта',
                                                    0, 1, 100000, 1)
        elif self.mode == 'stars_bayer':
            fname, ok = QInputDialog.getItem(self, "Буква",
                                               "Выберите букву\n",
                                               tuple(alph),
                                               len(self.type_data), False)
        if ok:
            if self.mode == 'messier' or self.mode == 'caldwell':
                self.type_data.append([fname, (self.point[0], self.point[1])])
            elif self.mode == 'stars_bayer':
                self.type_data.append([alph.find(fname) + 1, (self.point[0], self.point[1])])


class ConstellationEditor(QMainWindow):
    def __init__(self, parent=None):
        super(ConstellationEditor, self).__init__(parent)
        exitAction = QAction(QIcon('exit.png'), '&Закрыть', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть всё')
        exitAction.triggered.connect(qApp.quit)

        reverse_color = QAction('&Цвет', self)
        reverse_color.setShortcut('Ctrl+R')
        reverse_color.setStatusTip('Изменить цвет картинки')
        reverse_color.triggered.connect(self.reverse_im)

        size = QAction('&Размер', self)
        size.setShortcut('Ctrl+K')
        size.setStatusTip('Изменить размер картинки')
        size.triggered.connect(self.ch_size)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Файл')
        fileMenu1.addAction(exitAction)
        fileMenu2 = menubar.addMenu('&Изображение')
        fileMenu2.addAction(reverse_color)
        fileMenu2.addAction(size)
        self.win_x, self.win_y = root.winfo_screenwidth(), root.winfo_screenheight()
        self.setGeometry(0, 0, self.win_x, self.win_y)
        self.setWindowIcon(QIcon('title.jpg'))
        self.setWindowTitle('Редактор созвездий')
        self.rasm = False
        self.star_data = []
        self.graph_data = []
        self.p_n = 1
        self.paint = False
        self.pic = False
        self.star1 = False
        self.star2 = False
        self.k = 1
        self.delta = (400, 50)

        self.photo = QPushButton('Выбрать фото', self)
        self.photo.resize(200, 50)
        self.photo.move(10, 30)
        self.photo.clicked.connect(self.dial)

        self.image = QLabel(self)
        self.image.move(400, 50)
        self.image.resize(911, 513)

        self.btn_cr = QPushButton('Создать директорию', self)
        self.btn_cr.resize(200, 50)
        self.btn_cr.move(10, 90)
        self.btn_cr.clicked.connect(self.create_folder)

        self.btn_st = QPushButton('Начать разметку', self)
        self.btn_st.resize(200, 50)
        self.btn_st.move(10, 150)
        self.btn_st.clicked.connect(self.red)

        self.btn_1 = QPushButton('Подтвердить выбор\nпервой звезды', self)
        self.btn_2 = QPushButton('Подтвердить выбор\nвторой звезды', self)
        self.btn_1.resize(115, 50)
        self.btn_1.move(10, 210)
        self.btn_2.resize(115, 50)
        self.btn_2.move(130, 210)
        self.btn_2.clicked.connect(self.choice)
        self.btn_1.clicked.connect(self.choice)

        self.btn_rev = QPushButton('Сохранить пару', self)
        self.btn_rev.resize(200, 50)
        self.btn_rev.move(10, 270)
        self.btn_rev.clicked.connect(self.rev_buttons)

        self.btn_save = QPushButton('Сохранить и завершить', self)
        self.btn_save.resize(200, 50)
        self.btn_save.move(10, 330)
        self.btn_save.clicked.connect(self.saver)

        self.btn_save = QPushButton('Показать сделанное', self)
        self.btn_save.resize(200, 50)
        self.btn_save.move(10, 390)
        self.btn_save.clicked.connect(self.ch)

        self.draw = False

        self.show()

    def reverse_im(self):
        pass

    def ch_size(self):
        i, okBtnPressed = QInputDialog.getInt(self, "Размер",
                                              "Введите размер в процентах от стандартного",
                                              100, 10, 200, 5)
        if okBtnPressed:
            k = i / 100
            self.im_size = tuple(map(lambda x: int(x * k / self.k), self.im_size))
            for j in range(len(self.star_data)):
                x1, y1, x2, y2 = *self.star_data[j][0], *self.star_data[j][1]
                x1 -= self.delta[0]
                x2 -= self.delta[0]
                y1 -= self.delta[1]
                y2 -= self.delta[1]
                self.star_data[j] = ((x1 * k / self.k + self.delta[0], y1 * k / self.k + self.delta[1]),
                                      (x2 * k / self.k + self.delta[0], y2 * k / self.k + self.delta[1]))
            self.update()
            self.k = k

    def mouseDoubleClickEvent(self, e):
        if self.rasm:
            coord = e.pos().x(), e.pos().y()
            f = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5
            mi = 1000
            v = 0
            for i in self.star_data:
                d1 = f(i[0], coord) + 1
                d2 = f(i[1], coord) + 1
                d3 = f(i[0], i[1]) + 1
                angel = acos((d1 ** 2 + d3 ** 2 - d2 ** 2) / (2 * d1 * d3))
                h = d1 * sin(angel)
                if h < mi:
                    v = i
                    mi = h
            if self.star_data:
                self.star_data.remove(v)

    def mousePressEvent(self, e):
        point = e.pos().x(), e.pos().y()
        self.point = point
        if self.rasm:
            if self.delta[0] <= point[0] <= self.im_size[0] + self.delta[0] and self.delta[1] <= point[1] <= self.im_size[1] + self.delta[1]:
                self.paint = True
                self.update()
            else:
                self.paint = False

    def paintEvent(self, e):
        painter = QPainter(self)
        if self.pic:
            painter.drawPixmap(QRect(*self.delta, *self.im_size), self.pixmap)
        if self.paint:
            painter.setPen(QPen(Qt.red, 1))
            painter.drawEllipse(self.point[0] - 5, self.point[1] - 5, 10, 10)
            painter.drawLine(self.point[0] - 5, self.point[1], self.point[0] + 5, self.point[1])
            painter.drawLine(self.point[0], self.point[1] - 5, self.point[0], self.point[1] + 5)
        if self.draw:
            for i in self.star_data:
                painter.setPen(Qt.red)
                painter.drawLine(*i[0], *i[1])
                self.update()

    def dial(self):
        if exists('C:\\Users\\Asus\\Pictures\\Stellarium'):
            fname, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                'C:\\Users\\Asus\\Pictures\\Stellarium', "Картинка(*.png)")
        else:
            fname, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                    'C:\\Users\\Asus\\Pictures\\Stellarium', "Картинка(*.png)")
        if ok:
            self.photo_path = fname
            self.load_image()

    def ch(self):
        if self.draw == False:
            self.draw = True
        else:
            self.draw = False

    def load_image(self):
        self.pixmap = QPixmap(self.photo_path)
        im = Image.open(self.photo_path)
        self.real_size = im.size
        ma = max(self.real_size)
        self.im_size = tuple(map(lambda x: int(x / ma * self.win_x * screen_increase / 2), self.real_size))
        self.pic = True

    def create_folder(self):
        dir = dirname(abspath(__file__))
        i, ok = QInputDialog.getText(self, '', 'Введите название скайчарта')
        if ok:
            dir += '/Skycharts/constellations/' + i
            mkdir(dir)
            self.dir = dir
            copy(self.photo_path, dir)
            rename(dir + self.photo_path[self.photo_path.rfind('/'):], dir + '/photo.png')
            f1 = open(dir + '/star_data.txt', 'w')
            f1.close()
            f2 = open(dir + '/coords.txt', 'w')
            f2.close()
            self.btn_cr.setEnabled(False)

    def red(self):
        if self.rasm:
            self.rasm = False
            self.paint = False
            self.btn_st.setEnabled(False)
        else:
            self.rasm = True
            self.btn_st.setText('Закончить разметку')

    def choice(self):
        if self.star1 == False:
            self.star1 = self.point
            self.btn_1.setEnabled(False)
        else:
            self.star2 = self.point
            self.star_data.append((self.star1, self.star2))
            self.star1 = False
            self.star2 = False
            self.btn_2.setEnabled(False)

    def rev_buttons(self):
        self.btn_1.setEnabled(True)
        self.btn_2.setEnabled(True)

    def saver(self):
        f1 = open(self.dir + '/star_data.txt', 'w')
        for i in self.star_data:
            x1, x2, x3, x4 = i[0][0], i[0][1], i[1][0], i[1][1]
            x1 -= self.delta[0]
            x3 -= self.delta[0]
            x2 -= self.delta[1]
            x4 -= self.delta[1]
            x1 = round(x1 * (self.real_size[0] / self.im_size[0]), 1)
            x2 = round(x2 * (self.real_size[0] / self.im_size[0]), 1)
            x3 = round(x3 * (self.real_size[0] / self.im_size[0]), 1)
            x4 = round(x4 * (self.real_size[0] / self.im_size[0]), 1)
            f1.write(' '.join([str(x1), str(x2), str(x3), str(x4)]) + '\n')
        f1.write('!')
        f1.close()
        self.close()

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Z) and (e.modifiers() == Qt.ControlModifier):
            if len(self.star_data) != 0:
                self.star_data.pop(-1)
        if (e.key() == Qt.Key_Z) and (e.modifiers() == Qt.ShiftModifier):
            pass
        if e.key() == Qt.Key_S:
            self.point = tuple([self.point[0], self.point[1] + 1])
            self.update()
        if e.key() == Qt.Key_W:
            self.point = tuple([self.point[0], self.point[1] - 1])
            self.update()
        if e.key() == Qt.Key_A:
            self.point = tuple([self.point[0] - 1, self.point[1]])
            self.update()
        if e.key() == Qt.Key_D:
            self.point = tuple([self.point[0] + 1, self.point[1]])
            self.update()


class Guess_Cons(QMainWindow):
    def __init__(self, parent=None):
        super(Guess_Cons, self).__init__(parent)
        global uuu, rosticin
        self.win_x, self.win_y = root.winfo_screenwidth(), root.winfo_screenheight()
        self.setGeometry(230, 30, self.win_x - 240, self.win_y)
        self.setWindowTitle("Назови Созвездие")
        self.setWindowIcon(QIcon('title.jpg'))

        q = sorted(listdir(path=dirname(abspath(__file__)) + '/Skycharts/constellations'))
        from random import choice
        self.uuu = choice(q)
        uuu = self.uuu
        self.pix = QPixmap(dirname(abspath(__file__)) + '/Skycharts/constellations/'+ self.uuu + '/photo.png')
        self.lbl_pix = QLabel(self)
        self.lbl_pix.move(100, 100)
        self.lbl_pix.setPixmap(self.pix)
        rosticin = ans_dia(self)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(QRect(1, 1, self.win_x - 242, self.win_y - 35), self.pix)

    def closer(self):
        self.close()


class ans_dia(QMainWindow):
    def __init__(self, parent=None):
        super(ans_dia, self).__init__(parent)
        self.uuu = uuu
        self.win_x, self.win_y = root.winfo_screenwidth(), root.winfo_screenheight()
        self.setGeometry(0, 0, 250, 200)
        self.setWindowIcon(QIcon('title.jpg'))
        self.setWindowTitle('Ответ')

        self.lbl = QLabel('Введите данные о созвездие ниже:', self)
        self.lbl.resize(220, 50)
        self.lbl.move(10, -10)

        self.bayer = QLineEdit(self)
        self.bayer.move(100, 30)
        self.bayer.resize(90, 30)
        self.lbl_bayer = QLabel('- Название по\n  Байеру', self)
        self.lbl_bayer.resize(100, 30)
        self.lbl_bayer.move(10, 30)

        self.name = QLineEdit(self)
        self.name.move(100, 70)
        self.name.resize(90, 30)

        self.lbl_name = QLabel('- Обычное\n название', self)
        self.lbl_name.resize(100, 30)
        self.lbl_name.move(10, 70)

        self.to_ans = QPushButton('Ответить', self)
        self.to_ans.resize(100, 30)
        self.to_ans.move(50, 120)
        self.to_ans.clicked.connect(self.res)
        self.show()

    def res(self):
        global kode, true
        bay, name = self.bayer.text(), self.name.text()
        real_name, real_bay = self.uuu, s[self.uuu]
        true = real_name, real_bay
        if real_name.lower() == name.lower() and real_bay.lower() == bay.lower():
            kode = 1
        elif real_name.lower() == name.lower():
            kode = 2
        elif real_bay.lower() == bay.lower():
            kode = 3
        else:
            kode = 4
        guess_res(self)

    def closer(self):
        self.close()


class guess_res(QMainWindow):
    def __init__(self, parent=None):
        super(guess_res, self).__init__(parent)
        self.setGeometry(100, 100, 175, 100)
        self.setWindowTitle(' ')
        self.btn = QPushButton('Завершить', self)
        self.btn.resize(80, 20)
        self.btn.move(5, 75)
        self.btn.clicked.connect(self.closer)

        self.btn = QPushButton('Ещё', self)
        self.btn.resize(80, 20)
        self.btn.move(90, 75)
        self.btn.clicked.connect(self.new)

        self.lbl = QLabel('', self)
        self.lbl.resize(200, 60)
        self.lbl.move(10, 10)
        if kode == 0:
            self.lbl.setText('System Error')
        elif kode == 1:
            self.lbl.setText('Всё верно')
        elif kode == 2:
            self.lbl.setText('Ошибка в названии\nпо каталогу Байера\nПравильный ответ:\n' + true[1])
        elif kode == 3:
            self.lbl.setText('Ошибка в названии\nПравильный ответ:\n' + true[0])
        else:
            self.lbl.setText('Ошибка в обоих вопросах\nПравильный ответ:\n' + true[0] + '; ' + true[1])
        self.show()

    def closer(self):
        global opened, rosticin
        opened.closer()
        rosticin.closer()
        self.close()

    def new(self):
        global opened, rosticin
        opened.closer()
        rosticin.closer()
        self.close()
        opened = Guess_Cons(self)


class searcher(QDialog):
    def __init__(self, parent=None):
        super(searcher, self).__init__(parent)
        self.q = qq
        self.resize(200, 100)
        self.box = QComboBox()
        self.line = QLineEdit()
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.line)
        self.grid.addWidget(self.box)
        self.box.addItems(qq)
        self.line.textEdited.connect(self.go)

        self.btn = QPushButton('OK', self)
        self.btn.clicked.connect(self.ex)
        self.grid.addWidget(self.btn)
        self.show()

    def go(self):
        txt = self.line.text().lower()
        p = []
        self.box.clear()
        self.box.addItems(self.q)
        for i in range(len(self.box)):
            el = self.box.itemText(i).lower()
            if el.startswith(txt):
                p.append(' '.join(list(map(lambda x: x[0].upper() + x[1:], el.split()))))
        self.box.clear()
        self.box.addItems(p)

    def ex(self):
        global UT, searcher_global
        UT = ' '.join(list(map(lambda x: x[0].upper() + x[1:], self.box.currentText().split())))
        searcher_global = True
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    ex = Example()
    exit(app.exec_())
