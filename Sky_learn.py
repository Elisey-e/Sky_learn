from sys import argv, exit
from os import listdir, curdir, walk, remove, mkdir, rename
from os.path import abspath, exists
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QInputDialog,\
    QMessageBox, QFileDialog, QKeySequenceEdit, QAction, qApp, QMainWindow, QMessageBox, QDialog, QScrollArea,\
    QGridLayout, QComboBox, QDesktopWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QLinearGradient, QImage, QPalette, QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import QObject, pyqtSignal, QSize, Qt, QUrl, QRect
from time import localtime, timezone
import webbrowser
from shutil import copy
from time import time
from PIL import Image
from math import acos, degrees, radians, sin

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
SystemWidth = 0
SystemHeight = 0


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 810, 400)
        self.setWindowTitle('Sky Learn')
        self.setWindowIcon(QIcon('title.jpg'))

        self.btn = QPushButton('Ботать\nсозвездия!', self)
        self.btn.setFont(QFont('SansSerif', 13))
        self.btn.resize(190, 100)
        self.btn.move(10, 10)
        self.btn.clicked.connect(self.dia)

        self.btn2 = QPushButton('Ботать\nМессье!', self)
        self.btn2.setFont(QFont('SansSerif', 13))
        self.btn2.resize(190, 100)
        self.btn2.move(210, 10)

        self.btnn = QPushButton('Добавить\nСкайчарт!', self)
        self.btnn.setFont(QFont('SansSerif', 13))
        self.btnn.resize(190, 100)
        self.btnn.move(410, 10)
        self.btnn.clicked.connect(self.add)

        self.btnr = QPushButton('Назови\nСозвездие!', self)
        self.btnr.setFont(QFont('SansSerif', 13))
        self.btnr.resize(190, 100)
        self.btnr.move(610, 10)
        self.btnr.clicked.connect(self.ans)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        # Рисуем фон
        g = QLinearGradient(0, 0, 0, 400)
        g.setColorAt(0, Qt.blue)
        g.setColorAt(1, Qt.yellow)
        y = 400 - 1 * 400 / 4095.0
        qp.fillRect(0, 0, 810, 400, g)
        qp.setPen(Qt.black)
        qp.drawLine(0, y, 810, y)
        #
        brush = QBrush(QColor(200, 200, 150))
        brush.setStyle(Qt.Dense4Pattern)
        qp.setBrush(brush)
        qp.drawRect(-1, -1, 811, 401)
        #

    def keyPressEvent(self, e):
        if e.key() == 16777220 or e.key() == Qt.Key_Enter:
            self.dia()
        if e.key() == Qt.Key_F1:
            dialog = Information_Dialog(self)

    def dia(self):
        global qq
        q = sorted(listdir(path=abspath(curdir) + '/Skycharts/constellations'))
        qq = q
        s = searcher(self)
        s.exec_()
        self.TwoWindow = None
        self.set_clock_window('open chart')

    def add(self):
        global new
        i, okBtnPressed = QInputDialog.getItem(self, "Выбрать редактор",
                                               "Выберите редактор\n",
                                               ('Созвездия', 'Мессье'),
                                               0, False)
        if okBtnPressed:
            new = i
            self.TwoWindow = None
            self.set_clock_window('new chart')

    def set_clock_window(self, i):
        global dial
        if i == 'new chart':
            dialog = Editor(self)
        elif i == 'open chart':
            dialog = ConstellationDialog(self)
            dial = dialog

    def ans(self):
        global opened, s
        f = open("Skycharts/Cons_bayer.txt")
        q = f.readlines()
        f.close()
        q = list(map(lambda x: [x[:x.rfind(' ')], x[-4:-1]], q))
        se = {}
        for i in q:
            se[i[0]] = i[1]
        s = se
        opened = Guess_Cons(self)


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

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Файл')
        fileMenu1.addAction(exitAction)
        fileMenu2 = menubar.addMenu('&Изображение')
        fileMenu2.addAction(reverse_color)
        fileMenu2.addAction(size)
        fileMenu3 = menubar.addMenu('&Выделение и проверка')
        fileMenu3.addAction(strictness)
        self.setWindowTitle(UT)
        self.im_pos = 400, 50
        self.im_size = 911, 513
        self.im_size_um = 911, 513
        self.win_x, self.win_y = SystemWidth, SystemHeight
        self.setGeometry(0, 0, self.win_x, self.win_y)
        self.dir = abspath(curdir)
        self.rasm = False
        self.pixmap = QPixmap('Skycharts/constellations/' + UT + '/photo.png')
        im = Image.open('Skycharts/constellations/' + UT + '/photo.png')
        self.real_size = im.size
        del im
        self.paint = False
        self.time = False
        self.lines = []
        self.reverseded = False
        self.deleted = []
        self.curr_pos = None
        self.k = 1

        self.wait = QLabel("", self)
        self.wait.resize(200, 30)
        self.wait.move(10, self.win_y - 60)

        self.st = QPushButton("Начать выделение", self)
        self.st.resize(200, 50)
        self.st.move(10, 30)
        self.st.clicked.connect(self.start)

        self.check = QPushButton("Проверить!", self)
        self.check.resize(200, 50)
        self.check.move(10, 90)
        self.check.clicked.connect(self.checker)

        self.to_show = False

        self.ans = QPushButton("Показать ответ", self)
        self.ans.resize(200, 50)
        self.ans.move(10, 150)
        self.ans.clicked.connect(self.show_ans)

        self.timer = QLabel("00:00:00.00", self)
        self.timer.setFont(QFont('SansSerif', 20))
        self.timer.resize(150, 50)
        self.timer.move(self.win_x - 200, self.win_y - 100)
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
            self.im_size = tuple(map(lambda x: int(x * k), self.im_size_um))
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

    def reverse_im(self):
        if not self.reverseded:
            im = Image.open('Skycharts/constellations/' + UT + '/photo.png')
            pixels = im.load()
            x, y = im.size
            for i in range(x):
                for j in range(y):
                    c = 256 - sum(pixels[i, j]) // 3
                    pixels[i, j] = tuple([c for i in range(3)])
            rod = 0
            im.save('Skycharts/build/photo.png')
            self.pixmap = QPixmap('Skycharts/build/photo.png')
            remove(abspath(curdir) + '/Skycharts/build/photo.png')
            self.reverseded = not self.reverseded
            self.update()
        else:
            self.pixmap = QPixmap('Skycharts/constellations/' + UT + '/photo.png')
            self.reverseded = not self.reverseded
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
        path = 'Skycharts/constellations/' + UT + '/star_data.txt'
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

        self.abs_h = 0

        self.title = QLabel('Приложение Sky Learn', self)
        self.title.setFont(QFont('SansSerif', 15))
        self.title.resize(220, 35)
        self.title.setStyleSheet("color: rgb(255, 0, 0);")

        self.t1 = QLabel('Общая информация', self)
        self.t1.setFont(QFont('SansSerif', 10))
        self.t1.resize(200, 25)
        self.t1.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Приложение Sky Learn реализовано на основе программы                 , то есть',
                  'за графические материалы я искренне благодарен её создателям. Но моя',
                  'программа нацелена на изучение некоторых небесных объектов(в',
                  'частности - созвездий). То есть я реализовал приложение, с помощью',
                  'которого можно с большими удобствами подготовиться к заданиям на',
                  'темы:',
                  ' -Созвездия - знание фигуры(линий)',
                  ' -Созвездия - знание звезд(каталог Байера)',
                  ' -Каталог Мессье',
                  ' -Каталог Колдуэлла',
                  ' -Планеты',
                  'В программе также реализован редактор для добавления',
                  'пользовательских объектов. Теперь приступлю к описанию возможностей',
                  'программы.']
        self.tx1 = QLabel('\n'.join(self.q), self)
        self.tx1.resize(500, 1000)

        self.tx2 = QLabel('<a href="https://stellarium.org/ru/">Stellarium</a>', self)
        self.tx2.setOpenExternalLinks(True)
        self.tx2.resize(500, 100)
        self.tx2.setStyleSheet("color: rgb(0, 0, 255);")

        self.q = ['Главное меню']
        self.tx3 = QLabel('\n'.join(self.q), self)
        self.tx3.setStyleSheet("color: rgb(0, 0, 255);")
        self.tx3.setFont(QFont('SansSerif', 10))

        self.q = ['']
        self.tx4 = QLabel('\n'.join(self.q))
        self.tx4.resize(500, 500)

        self.generate()
        self.show()

    def generate(self):
        self.title.move(90, self.abs_h)
        self.t1.move(10, self.abs_h + 70)
        self.tx1.move(10, self.abs_h - 315)
        self.tx2.move(305, self.abs_h + 51)
        self.tx3.move(10, self.abs_h + 310)

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


class Editor(QMainWindow):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        exitAction = QAction(QIcon('exit.png'), '&Закрыть', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Закрыть всё')
        exitAction.triggered.connect(qApp.quit)

        reverse_color = QAction('&Цвет', self)
        reverse_color.setShortcut('Ctrl+R')
        reverse_color.setStatusTip('Изменить цвет картинки')
        reverse_color.triggered.connect(self.reverse_im)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu1 = menubar.addMenu('&Файл')
        fileMenu1.addAction(exitAction)
        fileMenu2 = menubar.addMenu('&Изображение')
        fileMenu2.addAction(reverse_color)
        self.win_x, self.win_y = SystemWidth, SystemHeight
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

        self.im_size = (911, 513)
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
            if 400 <= point[0] <= 911 + 400 and 50 <= point[1] <= 563:
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
        if exists('C:/Users/Asus/Pictures/Stellarium'):
            fname, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                'C:/Users/Asus/Pictures/Stellarium', "Картинка(*.png)")
        else:
            fname, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                    'C:/Users/Asus/Pictures/Stellarium', "Картинка(*.png)")
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
        self.pic = True

    def create_folder(self):
        dir = abspath(curdir)
        i, ok = QInputDialog.getText(self, '', 'Введите название скайчарта')
        if ok:
            if '/' in dir:
                dir = dir.replace('/', '/')
            dir += '/Skycharts/constellations/' + i
            mkdir(dir)
            self.dir = dir
            copy(self.photo_path, dir)
            rename(dir + self.photo_path[self.photo_path.rfind('/'):], dir + '/photo.png')
            f1 = open(dir + '/star_data.txt', 'w')
            f1.close()
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
        self.win_x, self.win_y = SystemWidth, SystemHeight
        self.setGeometry(230, 30, self.win_x - 240, self.win_y)
        self.setWindowTitle("Назови Созвездие")
        self.setWindowIcon(QIcon('title.jpg'))

        q = sorted(listdir(path=abspath(curdir) + '/Skycharts/constellations'))
        from random import choice
        self.uuu = choice(q)
        uuu = self.uuu
        self.pix = QPixmap('Skycharts/constellations/'+ self.uuu + '/photo.png')
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
        self.win_x, self.win_y = SystemWidth, SystemHeight
        self.setGeometry(0, 0, 200, 200)
        self.setWindowIcon(QIcon('title.jpg'))
        self.setWindowTitle('Ответ')

        self.lbl = QLabel('Введите данные о созвездие ниже:', self)
        self.lbl.resize(200, 50)
        self.lbl.move(10, -10)

        self.bayer = QLineEdit(self)
        self.bayer.move(90, 30)
        self.bayer.resize(90, 30)
        self.lbl_bayer = QLabel('- Название по\n  Байеру', self)
        self.lbl_bayer.resize(100, 30)
        self.lbl_bayer.move(10, 30)

        self.name = QLineEdit(self)
        self.name.move(90, 70)
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
        self.setGeometry(100, 100, 150, 100)
        self.setWindowTitle(' ')
        self.btn = QPushButton('Завершить', self)
        self.btn.resize(65, 20)
        self.btn.move(5, 75)
        self.btn.clicked.connect(self.closer)

        self.btn = QPushButton('Ещё', self)
        self.btn.resize(65, 20)
        self.btn.move(80, 75)
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
        global UT
        UT = ' '.join(list(map(lambda x: x[0].upper() + x[1:], self.box.currentText().split())))
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    SystemWidth = QDesktopWidget().availableGeometry().width()
    SystemHeight = QDesktopWidget().availableGeometry().height()
    ex = Example()
    exit(app.exec_())
