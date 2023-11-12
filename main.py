import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from db_Illustrator_master import db_session_master
from db_Illustrator_master.creating_tag_master import add_main_master
from db_Illustrator_master.main_db import Main_master

from PIL import Image


# главное окно
class Illustrator_master(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initIO()

    def initIO(self):
        self.setWindowIcon(QIcon('img_PyQt/wnd_paint.png'))
        self.setGeometry(0, 0, 1920, 1080)

        # подключаем дизайн
        uic.loadUi('UI_MASTER/main_wnd.html', self)

        # загрузка шрифта
        QFontDatabase.addApplicationFont('Font/Ravie.ttf')
        QFontDatabase.addApplicationFont('Font/Pristina.ttf')

        # загружаем фото на главное окно
        self.pixmap = QPixmap('img_PyQt/palitra.png')
        self.foto_paint.setPixmap(self.pixmap)

        # подключаем кнопки
        self.create_btn.clicked.connect(self.draw_wnd)
        self.bd_btn.clicked.connect(self.db_btn_window)

    def draw_wnd(self):
        main_window_app.hide()
        self.draw_w = Drawing_window()
        self.draw_w.show()

    def db_btn_window(self):
        main_window_app.hide()
        self.db_window = db_Window()
        self.db_window.show()


class Circle:
    def __init__(self, x0, y0, x1, y1, fill_color=Qt.white, outline_color=Qt.black):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.fill_color = fill_color
        self.outline_color = outline_color

    def draw(self, paint):
        paint.setBrush(QBrush(self.fill_color))
        paint.setPen(QPen(self.outline_color, 4))
        radius = int(((self.x0 - self.x1) ** 2 + (self.y0 - self.y1) ** 2) ** 0.5)
        paint.drawEllipse(self.x0 - radius, self.y0 - radius, radius * 2, radius * 2)


class Line:
    def __init__(self, x0, y0, x1, y1, color=Qt.black):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color

    def draw(self, paint):
        paint.setPen(QPen(self.color, 3))
        paint.drawLine(self.x0, self.y0, self.x1, self.y1)


class Rectangle:
    def __init__(self, x0, y0, x1, y1, fill_color=Qt.white, outline_color=Qt.black):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.fill_color = fill_color
        self.outline_color = outline_color

    def draw(self, paint):
        paint.setPen(QPen(self.outline_color, 4))
        paint.setBrush(QBrush(self.fill_color))
        paint.drawRect(self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)


# режим рисования
class Drawing_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initIO()

    def initIO(self):
        self.setGeometry(0, 0, 1920, 1080)
        # загружаем дизайн
        uic.loadUi('UI_MASTER/draw_wnd.html', self)
        self.setWindowIcon(QIcon('img_PyQt/wnd_paint.png'))

        self.fon = QImage(self.size(), QImage.Format_RGB32)
        self.fon.fill(Qt.white)

        self.color = Qt.black
        self.color_figure = Qt.white
        self.size_pen = 2
        self.last_pos = QPoint()
        self.instrument = ''
        self.figure = []
        self.pen_px = 2
        self.eraser_px = 10
        self.saved = False

        self.txt = QLabel(self)
        self.txt.resize(1800, 780)
        self.txt.move(5, 100)

        # menuBar
        # ========================================================================================
        # загружаем верхние и нижние кнопки
        self.menu_bar = self.menuBar()

        self.file_btn = self.menu_bar.addMenu("File")

        # при нажатии на кнопку 'File' открываются следующие кнопки
        self.save_btn = QAction(QIcon('img_PyQt/btn_save.png'), 'Save', self)
        self.crete_new_btn = QAction(QIcon('img_PyQt/btn_new_file.png'), 'New file', self)
        self.open_btn = QAction(QIcon('img_PyQt/btn_open.png'), 'Open', self)
        self.clear_btn = QAction(QIcon('img_PyQt/btn_clear.png'), 'Clear', self)

        # добавление кнопок к 'File'
        self.file_btn.addAction(self.save_btn)
        self.file_btn.addAction(self.crete_new_btn)
        self.file_btn.addAction(self.open_btn)
        self.file_btn.addAction(self.clear_btn)

        # события нажатия на кнопки
        self.save_btn.triggered.connect(self.save)
        self.open_btn.triggered.connect(self.open)
        self.clear_btn.triggered.connect(self.clear)
        self.crete_new_btn.triggered.connect(self.new_file)

        # выход в меню
        self.menu_btn = self.menu_bar.addMenu("Menu")
        self.menu_btn.setFixedHeight(40)

        self.exit_menu = QAction(QIcon('img_PyQt/menu_img.png'), 'Menu', self)
        self.exit_menu.triggered.connect(self.menu_clicked_button)
        self.menu_btn.addAction(self.exit_menu)

        # размеры и цвета
        self.view_btn = self.menu_bar.addMenu("View")

        # размер пера ручки
        self.icon_pen_size = self.view_btn.addMenu(QIcon('img_PyQt/icon_pen_size.png'), "Pen size")

        self.px_2 = QAction('2 px', self)  # создаем кнопки
        self.px_4 = QAction('4 px', self)
        self.px_6 = QAction('6 px', self)
        self.px_10 = QAction('10 px', self)

        self.icon_pen_size.addAction(self.px_2)  # довавляем кнопки
        self.icon_pen_size.addAction(self.px_4)
        self.icon_pen_size.addAction(self.px_6)
        self.icon_pen_size.addAction(self.px_10)

        self.px_2.triggered.connect(self.px_2_size)  # подключаем кнопки
        self.px_4.triggered.connect(self.px_4_size)
        self.px_6.triggered.connect(self.px_6_size)
        self.px_10.triggered.connect(self.px_10_size)

        # размер ластика
        self.icon_eraser_size = self.view_btn.addMenu(QIcon('img_PyQt/icon_eraser_size.png'), "Eraser size")

        self.px_10_eraser = QAction('10 px', self)  # создаем кнопки
        self.px_15_eraser = QAction('15 px', self)
        self.px_20_eraser = QAction('20 px', self)
        self.px_40_eraser = QAction('40 px', self)

        self.icon_eraser_size.addAction(self.px_10_eraser)  # довавляем кнопки
        self.icon_eraser_size.addAction(self.px_15_eraser)
        self.icon_eraser_size.addAction(self.px_20_eraser)
        self.icon_eraser_size.addAction(self.px_40_eraser)

        self.px_10_eraser.triggered.connect(self.px_10_eraser_size)  # подключаем кнопки
        self.px_15_eraser.triggered.connect(self.px_15_eraser_size)
        self.px_20_eraser.triggered.connect(self.px_20_eraser_size)
        self.px_40_eraser.triggered.connect(self.px_40_eraser_size)

        # ===============================================================================
        # панель инструментов
        self.toolbar = QToolBar('Main ToolBar')
        self.addToolBar(self.toolbar)
        self.toolbar.setFixedHeight(55)

        # размер кнопки
        self.toolbar.setStyleSheet("QToolButton{padding: 18px;}")
        self.toolbar.addSeparator()
        self.toolbar.setIconSize(QSize(45, 45))

        # кнопка назад
        self.icon_back = QAction(QIcon('img_PyQt/icon_back.png'), '&back', self)
        self.icon_back.triggered.connect(self.back)
        self.toolbar.addAction(self.icon_back)
        self.toolbar.addSeparator()

        # ручка
        self.icon_pen = QAction(QIcon('img_PyQt/imf_pen.png'), '&pen', self)
        self.icon_pen.triggered.connect(self.pen)
        self.toolbar.addAction(self.icon_pen)
        self.toolbar.addSeparator()

        # выбор цвета ручки
        self.icon_outline_color = QAction(QIcon('img_PyQt/outline_color.png'), '&pen color', self)
        self.icon_outline_color.triggered.connect(self.outline_color)
        self.toolbar.addAction(self.icon_outline_color)
        self.toolbar.addSeparator()

        # ластик
        self.icon_eraser = QAction(QIcon('img_PyQt/icon_eraser.png'), '&eraser', self)
        self.icon_eraser.triggered.connect(self.eraser)
        self.toolbar.addAction(self.icon_eraser)
        self.toolbar.addSeparator()

        # круг
        self.icon_circle = QAction(QIcon('img_PyQt/icon_circle.png'), '&circle', self)
        self.icon_circle.triggered.connect(self.circle_figure)
        self.toolbar.addAction(self.icon_circle)
        self.toolbar.addSeparator()

        # прямоугольник
        self.icon_rectangle = QAction(QIcon('img_PyQt/icon_rectangle.png'), '&rectangle', self)
        self.icon_rectangle.triggered.connect(self.rectangle_figure)
        self.toolbar.addAction(self.icon_rectangle)
        self.toolbar.addSeparator()

        # линия
        self.icon_line = QAction(QIcon('img_PyQt/icon_line.png'), '&line', self)
        self.icon_line.triggered.connect(self.line_figure)
        self.toolbar.addAction(self.icon_line)
        self.toolbar.addSeparator()

        # выбор цвета заливки
        self.icon_full_color = QAction(QIcon('img_PyQt/icon_color.png'), '&full color', self)
        self.icon_full_color.triggered.connect(self.fill_color)
        self.toolbar.addAction(self.icon_full_color)
        self.toolbar.addSeparator()

    # =========================================================================================

    # выходим в меню при нажатии на кнопку "Menu"
    def menu_clicked_button(self):
        main_window_app.show()
        self.close()

    # сохранение файла
    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save image', '', '*.PNG')

        # добавляем в базу данных путь файла
        add_main_master(file_path)

        pix = QPixmap(self.size())
        pix_copy = pix.copy(0, 0, 1946, 947)
        self.render(pix_copy)
        if not file_path:
            return
        pix_copy.save(file_path)
        self.saved = True

    # открыть файл
    def open(self, event):
        file_name = QFileDialog.getOpenFileName(self, 'Открыть файл', '', "Image (*.png *.jpg);; Text (*.txt)")[0]
        file_painter = QPainter(self.fon)
        file_painter.setPen(QPen(Qt.NoPen))

        if not file_name:
            return

        # открываем файл txt
        if file_name.split('.')[-1] == 'txt':
            with open(file_name, 'r', encoding='utf-8') as file_txt:
                self.text = file_txt.read()
            self.txt.setText(self.text)
        # открываем фото
        else:
            image = QImage(file_name)
            img_copy = image.copy(0, 90, image.width(), image.height())

            if img_copy.height() >= 880:
                file_painter.drawImage(QRect(0, 90, img_copy.width(), img_copy.height() + 90), img_copy)
            if image.height() < 880:
                file_painter.drawImage(QRect(0, 100, image.width(), image.height()), image)

    # очистка холста
    def clear(self):
        self.figure.clear()
        self.fon.fill(Qt.white)
        self.txt.setText('')
        self.update()

    def closeEvent(self, event):
        if not self.saved:
            # диалог закрытия окна
            message_text = '''Are you sure you want to get out?\nExiting may result in data loss!'''
            messege_close = QMessageBox.question(self, 'Notice!', message_text,
                                                 QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Close)
            if messege_close == QMessageBox.Save:
                self.save()

            elif messege_close == QMessageBox.Close:
                self.close()

            elif messege_close == QMessageBox.Cancel:
                event.ignore()
            else:
                pass
        else:
            pass

    # создание нового файла
    def new_file(self):
        self.draw_w = Drawing_window()
        self.draw_w.show()

    # ==================================================== меняем размера пера ручки
    def px_2_size(self):
        self.size_pen = 2
        self.pen_px = 2

    def px_4_size(self):
        self.size_pen = 4
        self.pen_px = 4

    def px_6_size(self):
        self.size_pen = 6
        self.pen_px = 6

    def px_10_size(self):
        self.size_pen = 10
        self.pen_px = 10

    # ====================================================== меняем размер ластика
    def px_10_eraser_size(self):
        self.size_pen = 10
        self.eraser_px = 10

    def px_15_eraser_size(self):
        self.size_pen = 15
        self.eraser_px = 15

    def px_20_eraser_size(self):
        self.size_pen = 20
        self.eraser_px = 20

    def px_40_eraser_size(self):
        self.size_pen = 40
        self.eraser_px = 40

    # рисуем ручкой
    def pen(self):
        self.instrument = 'pen'
        self.color = Qt.black
        self.size_pen = self.pen_px

    # ластик
    def eraser(self):
        self.instrument = 'pen'
        self.color = Qt.white
        self.size_pen = self.eraser_px

    # =============================================================== фигуры
    # круг
    def circle_figure(self):
        self.instrument = 'circle'

    # линия
    def line_figure(self):
        self.instrument = 'line'

    # прямогольник
    def rectangle_figure(self):
        self.instrument = 'rect'

    # ============================================================= цвет
    def fill_color(self):
        self.color_figure = QColorDialog.getColor()

    def outline_color(self):
        self.color = QColorDialog.getColor()

    # ================================================================
    # убираем фигуры
    def back(self):
        if self.figure:
            self.figure.pop(-1)
        else:
            return
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)

        painter.drawImage(self.rect(), self.fon, self.fon.rect())
        # отображаем все фигуры нашего списка
        for figur in self.figure:
            figur.draw(painter)
        painter.end()

    # клавиша зажата
    def mousePressEvent(self, event):
        # процесс рисования ручкой
        if event.button() == Qt.LeftButton and event.y() > 97 and self.instrument == 'pen':
            self.last_pos = event.pos()

        # рисуем круг и добавляем его в список
        if self.instrument == 'circle':
            self.figure.append(Circle(event.x(), event.y(), event.x(), event.y(), self.color_figure))
            self.update()

        # риуем линию и добавляем её в список
        if self.instrument == 'line':
            self.figure.append(Line(event.x(), event.y(), event.x(), event.y(), self.color))
            self.update()

        if self.instrument == 'rect':
            self.figure.append(Rectangle(event.x(), event.y(), event.x(), event.y(), self.color_figure))
            self.update()

    def mouseMoveEvent(self, event):
        # отображение координат в процессе рисования
        self.label_mouse_pos.setText(f'{event.x()}, {event.y()}')

        # процесс рисования ручкой
        if event.buttons() == Qt.LeftButton and self.instrument == 'pen' and event.y() > 97:
            painter = QPainter(self.fon)
            painter.setPen(QPen(self.color, self.size_pen))
            painter.drawLine(self.last_pos, event.pos())
            self.last_pos = event.pos()
            self.update()

        # изменяем последние координаты при передвижении мышки
        if self.instrument == 'circle' or self.instrument == 'line' or self.instrument == 'rect':
            self.figure[-1].x1 = event.x()
            self.figure[-1].y1 = event.y()
            self.update()


# окно с отображением последних рисунков(подключение к базе данных)
class db_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initIO()

    def initIO(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QIcon('img_PyQt/wnd_paint.png'))
        self.setWindowTitle('Recent drawings')

        # меню
        self.menu_bar = self.menuBar()
        self.menu_btn = self.menu_bar.addMenu("Menu")
        self.menu_btn.setFixedHeight(40)

        self.exit_menu = QAction(QIcon('img_PyQt/menu_img.png'), 'Menu', self)
        self.exit_menu.triggered.connect(self.menu_clicked_button)
        self.menu_btn.addAction(self.exit_menu)

        self.open_btn = QPushButton('Open', self)
        self.open_btn.move(1420, 50)
        self.open_btn.resize(100, 50)
        self.open_btn.clicked.connect(self.open_run)

        # база данных
        self.list_db = []
        self.db_sess = db_session_master.create_session()
        app_master = self.db_sess.query(Main_master).all()
        self.list_db.extend(app_master)
        list_db_2 = sorted(self.list_db, key=lambda x: x.time, reverse=True)

        self.sp = []

        for elem in list_db_2:
            self.sp.extend([(elem.id, elem.time, elem.drawing)])
        print(self.sp)

        self.table_widget = QTableWidget(self)
        self.table_widget.move(500, 50)
        self.table_widget.resize(800, 900)

        self.row = 0
        self.col = 0
        self.cols = 3
        self.table_widget.setRowCount(self.row)
        self.table_widget.setColumnCount(self.cols)
        self.table_widget.setHorizontalHeaderLabels(['id', 'time', 'drawing'])
        self.table_widget.cellClicked.connect(self.cellClick)
        self.name_file = ''
        self.flag_item = False
        self.window_db()

    # выходим в меню при нажатии на кнопку "Menu"
    def menu_clicked_button(self):
        main_window_app.show()
        self.close()

    def closeEvent(self, event):
        main_window_app.show()
        # При закрытии формы закроем и наше соединение с базой данных
        self.db_sess.close()

    def window_db(self):
        for row, form in enumerate(self.sp):
            self.table_widget.insertRow(self.table_widget.rowCount())
            for column, item in enumerate(form):
                self.table_widget.setVerticalHeaderLabels([''] * (row + 1))
                # добавляем данные в таблицу
                self.flag_item = True
                self.table_widget.setItem(row, column, QTableWidgetItem(str(item)))
        # размеры столбцов
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 300)
        self.table_widget.setColumnWidth(2, 400)

    def cellClick(self, row, col):
        self.row = row
        self.col = col

    def open_run(self):
        if self.flag_item:
            self.cell = []
            self.cell.append(self.table_widget.item(self.row, self.col).text())
            self.name_file = self.cell[-1]
            print(self.name_file)

            # открываем изображение
            img = Image.open(self.name_file)
            new_img = img.crop((0, 90, 1920, 900))
            new_img.show()
        return


if __name__ == '__main__':
    db_session_master.global_init("db_Illustrator/main_db_Illustrator_master.db")
    app = QApplication(sys.argv)
    main_window_app = Illustrator_master()
    main_window_app.show()
    sys.exit(app.exec())
