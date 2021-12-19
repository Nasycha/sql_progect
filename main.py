from random import choice
import sys
from main_database import Database
from main_redact import Redact
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class MyWidget(QMainWindow):
    def __init__(self, db):
        super().__init__()
        uic.loadUi('progect_one.ui', self)
        self.main_flag = False
        self.db = db
        # self.count = 0

        # изображение
        self.pixmap = QPixmap("bloodthirsty_progect_one.jpeg.crdownload")
        self.image = QLabel(self)
        self.image.move(270, 350)
        self.image.resize(200, 200)

        # заполняем combo box значениями
        self.comboBox_time.addItem('15')
        self.comboBox_time.addItem('30')
        self.comboBox_time.addItem('45')
        self.comboBox_time.addItem('60')

        self.comboBox_language.addItem('English')
        self.comboBox_language.addItem('Русский')

        # вызов таймера по нажатию на кнопку
        self.pushButton_start.clicked.connect(self.make_flag)
        # запуск нового класса с виджетом БД списка слов
        self.pushButton_words.clicked.connect(self.open_redact)

    def recording_results(self):
        # self.count += 1
        f = open("results.txt", 'a', encoding="utf8")
        f.write('---------------')
        f.write(f'\n')
        # f.write(f'Результат №{self.count}')
        # f.write(f'\n')
        f.write(f'Время: {self.how_much_time}')
        f.write(f'\n')
        f.write(f'Аккуратность: {self.label_accuracy.text()}')
        f.write(f'\n')
        f.write(f'Количество слов: {self.label_score.text()}')
        f.write(f'\n')
        f.write(f'Язык: {self.language_name}')
        f.write(f'\n')
        f.close()

    def make_flag(self):
        #
        self.fl = False
        self.image.clear()
        self.language_name = self.comboBox_language.currentText()
        self.label_score.setText('0')
        self.textBrowser_show_word.setText('')
        self.label_accuracy.setText('100%')
        self.label_accuracy.setStyleSheet("color: black;")
        self.label_accuracy_text.setStyleSheet("color: black;")
        self.all_letters = 0
        self.all_clicks = 0
        self.timer_start()

    def timer_start(self):
        # считываем данные
        self.pushButton_start.setEnabled(False)
        self.how_much_time = int(self.comboBox_time.currentText())
        self.a = self.how_much_time
        self.five = 5
        # ставим время на виджетах
        self.label_time.setText(f'{self.how_much_time}')
        self.progressBar_time.setMaximum(self.how_much_time)
        self.progressBar_time.setValue(0)
        # таймер на 5 секунд для подготовки
        if not self.fl:
            self.label_7.setText('Отсчет начнется через:')
            self.label_8.setText('5')
            self.timer_ready()
        # когда флаг True (то есть счетчик в 5 сек прошел)
        # запускаем основной таймер
        else:
            self.main_flag = True
            self.timer_count()

    def timer_ready(self):
        # каждую секунду входим в функцию timer_ready_text
        QTimer.singleShot(1000, self.timer_ready_text)

    def timer_ready_text(self):
        # тут счетчик, выводящий информацию на виджет каждую секунду
        self.five -= 1
        self.label_8.setText(f'{self.five}')
        if self.five != 0:
            self.timer_ready()
        # когда 5 сек прошло, делаем флаг и заходим в timer_start
        else:
            self.fl = True
            self.words()
            self.label_7.setText('')
            self.label_8.setText('')
            self.timer_start()

    def timer_count(self):
        # каждую секунду заходим в функцию timer_finish
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_finish)
        self.timer.start(1000)

    def timer_finish(self):
        # тут отсчет времени и смена значения status bar
        self.a -= 1
        self.label_time.setText(f'{self.a}')
        self.progressBar_time.setValue(self.how_much_time - self.a)
        if self.a == 0:
            self.show_image()
            self.timer.stop()
            self.main_flag = False
            self.textBrowser_show_word.setText('')
            self.pushButton_start.setEnabled(True)
            self.recording_results()

    def show_image(self):
        self.image.setPixmap(self.pixmap)

    def words(self):
        self.l = 0
        self.textBrowser_show_word.setText(f'')
        language = self.comboBox_language.currentText()
        if language == 'English':
            language = 1
        else:
            language = 2
        res = self.db.word_where_language(language)
        a = choice(res)
        self.text = a[0]
        self.text = list(self.text)
        if ' ' in self.text[-1]:
            self.text.remove(' ')
        print(self.text)
        if self.all_clicks == 0:
            self.label_accuracy.setText(f'100%')
            self.label_accuracy.setStyleSheet("color: green;")
            self.label_accuracy_text.setStyleSheet("color: green;")
        else:
            self.acuraccy = round(self.all_letters / self.all_clicks * 100)
            self.label_accuracy.setText(f'{round(self.all_letters / self.all_clicks * 100)}%')
            if self.acuraccy >= 70:
                self.label_accuracy.setStyleSheet("color: green;")
                self.label_accuracy_text.setStyleSheet("color: green;")
            elif 70 > self.acuraccy >= 50:
                self.label_accuracy.setStyleSheet("color: orange;")
                self.label_accuracy_text.setStyleSheet("color: orange;")
            elif self.acuraccy < 50:
                self.label_accuracy.setStyleSheet("color: red;")
                self.label_accuracy_text.setStyleSheet("color: red;")
        self.all_letters += len(self.text)
        self.textBrowser_show_word.setText(f'{a[0]}')

    def keyPressEvent(self, event):
        if self.main_flag:
            self.all_clicks += 1
            key = event.text()
            if not key:
                key = " "
            if self.l <= len(self.text) - 1:
                if self.text[self.l] == key:
                    word = ''.join(self.text)
                    self.l += 1
                    ds = word[:self.l]
                    self.textBrowser_show_word.setHtml(
                        '<font color=gray>' + ds + '</font><font color=black>' + word[self.l:] + '</font>')
                    if self.l == len(self.text):
                        self.guessed = self.label_score.text()
                        self.label_score.setText(f'{int(self.guessed) + 1}')
                        self.words()
        else:
            print('no')

    def open_redact(self):
        # открытие нового окна с редактированием слов
        self.redactor = Redact(self, self.db)
        self.redactor.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook
if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database('first_project.db')
    ex = MyWidget(db)
    ex.show()
    code = app.exec()
    db.close()
    sys.exit(code)
