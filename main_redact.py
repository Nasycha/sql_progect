from PyQt5.QtWidgets import QTableWidgetItem, QWidget
from PyQt5 import uic


class Redact(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.db = db
        uic.loadUi('change_language_form_2.ui', self)
        self.label_message.clear()

        # заполнение виджетов
        self.comboBox_select_language.addItem('English')
        self.comboBox_select_language.addItem('Русский')
        self.comboBox_select_operation.addItem('Add')
        self.comboBox_select_operation.addItem('Remove')

        # заполнение таблицы элементами
        res = self.db.for_table()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        # меняет БД
        self.pushButton.clicked.connect(self.change)

    def change(self):
        self.label_message.setText('')
        # считываем все значения с виджетов
        language = self.comboBox_select_language.currentText()
        operation = self.comboBox_select_operation.currentText()
        word = self.lineEdit.text()
        # добавление элементов в БД
        if len(word) == 0:
            self.label_message.setText('Некорректный ввод')
        elif operation == 'Add':
            if language == 'English':
                number = 1
                self.db.insert_words(word, number)
            else:
                number = 2
                self.db.insert_words(word, number)
        # удаление элементов из БД
        elif operation == 'Remove':
            # проверяем есть ли слово в БД
            fl = False
            if language == 'English':
                num = 1
            else:
                num = 2
            res = self.db.word_where_language(num)
            for el in res:
                if word == el[0]:
                    fl = True
            # если есть, то удаляем его
            if fl:
                self.db.delete_words(word, num)
            else:
                self.label_message.setText('Ничего не найдено')

        # делаем таблицу со обновленными значениями из БД
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        res = self.db.for_table()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))