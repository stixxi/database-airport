from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt5 import QtWidgets
import sys
import sqlite3
from main import Ui_MainWindow, Ui_EmployeesForm, Ui_FlightsForm, Ui_PassengersForm, Ui_AirplanesForm, Ui_DelForm

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = sqlite3.connect('airport.db')
        self.cursor = self.conn.cursor()
        self.tables = ["passengers", "flights", "airplanes", "employees"]
        self.current_table_index = 0
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Номер Паспорта'])
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.resizeColumnsToContents()
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.load_data()
        self.ui.pushButton.clicked.connect(self.switch_table)
        self.ui.pushButton_2.clicked.connect(self.open_window_add)
        self.ui.pushButton_3.clicked.connect(self.open_window_del)
    def open_window_del(self):
        current_table = self.tables[self.current_table_index]
        if current_table == 'employees':
            self.WindowDel = WindowDelete_Employees(self)
            self.WindowDel.exec_()
        elif current_table == 'flights':
            self.WindowDel = WindowDelete_Flights(self)
            self.WindowDel.exec_()
        elif current_table == 'passengers':
            self.WindowDel = WindowDelete_Passengers(self)
            self.WindowDel.exec_()
        elif current_table == 'airplanes':
            self.WindowDel = WindowDelete_AirPlanes(self)
            self.WindowDel.exec_()
    def open_window_add(self):
        current_table = self.tables[self.current_table_index]
        if current_table == 'passengers':
            self.WindowAdd = WindowAdd_Passengers(self)
            self.WindowAdd.exec_()
        elif current_table == 'flights':
            self.WindowAdd = WindowAdd_Flights(self)
            self.WindowAdd.exec_()
        elif current_table == 'airplanes':
            self.WindowAdd = WindowAdd_Airplanes(self)
            self.WindowAdd.exec_()
        elif current_table == 'employees':
            self.WindowAdd = WindowAdd_Employees(self)
            self.WindowAdd.exec_()

    def load_data(self):
        self.ui.tableWidget.setRowCount(0)
        current_table = self.tables[self.current_table_index]
        if current_table == "passengers":
            self.cursor.execute("SELECT * FROM passengers ORDER BY id DESC")
            data = self.cursor.fetchall()
            self.ui.tableWidget.setColumnCount(4)
            self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Номер Паспорта'])
        elif current_table == "flights":
            self.cursor.execute("SELECT * FROM flights ORDER BY id DESC")
            data = self.cursor.fetchall()
            self.ui.tableWidget.setColumnCount(6)
            self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Номер рейса', 'Аэропорт вылета', 'Аэропорт прилета', 'Время вылета', 'Время прибытия'])
        elif current_table == "airplanes":
            self.cursor.execute("SELECT * FROM airplanes ORDER BY id DESC")
            data = self.cursor.fetchall()
            self.ui.tableWidget.setColumnCount(3)
            self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Модель', 'Вместимость'])
        elif current_table == "employees":
            self.cursor.execute("SELECT * FROM employees ORDER BY id DESC")
            data = self.cursor.fetchall()
            self.ui.tableWidget.setColumnCount(4)
            self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Должность'])
        for row_number, row_data in enumerate(data):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

    def switch_table(self):
        self.current_table_index = (self.current_table_index + 1) % len(self.tables)
        self.load_data()


class WindowAdd_Passengers(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PassengersForm()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.add)

    def add(self):
        if not self.ui.lineEdit.text() or not self.ui.lineEdit_2.text() or not self.ui.lineEdit_3.text():
            QMessageBox.warning(self, "Ошибка", "Ошибка! Какая-то из строк пустая!")
        else:
            con = sqlite3.connect('airport.db')
            cursor = con.cursor()
            passport_number = self.ui.lineEdit.text()
            surname = self.ui.lineEdit_2.text()
            name = self.ui.lineEdit_3.text()
            cursor.execute('INSERT INTO passengers (first_name, last_name, passport_number) VALUES (?, ?, ?)', 
                           (name, surname, passport_number))
            con.commit()
            con.close()

            if self.parent():
                self.parent().load_data()

            self.close()

class WindowAdd_Flights(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_FlightsForm()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.add)

    def add(self):
        if not self.ui.lineEdit.text() or not self.ui.lineEdit_2.text() or not self.ui.lineEdit_3.text() or not self.ui.lineEdit_4.text() or not self.ui.lineEdit_5.text():
            QMessageBox.warning(self, "Ошибка", "Ошибка! Какая-то из строк пустая!")
        else:
            con = sqlite3.connect('airport.db')
            cursor = con.cursor()
            flight_number = self.ui.lineEdit_3.text()
            departure_airport = self.ui.lineEdit_2.text()
            arrival_airport = self.ui.lineEdit.text()
            departure_time = self.ui.lineEdit_4.text()
            arrival_time = self.ui.lineEdit_5.text()
            cursor.execute('INSERT INTO flights (flight_number, departure_airport, arrival_airport, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)', 
                           (flight_number, departure_airport, arrival_airport, departure_time, arrival_time))
            con.commit()
            con.close()
            if self.parent():
                self.parent().load_data()
            self.close()



class WindowAdd_Airplanes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AirplanesForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add)

    def add(self):
        if not self.ui.lineEdit_3.text() or not self.ui.lineEdit_2.text():
            QMessageBox.warning(self, "Ошибка", "Ошибка! Какая-то из строк пустая!")
        else:
            con = sqlite3.connect('airport.db')
            cursor = con.cursor()
            model = self.ui.lineEdit_3.text()
            capacity = self.ui.lineEdit_2.text()
            cursor.execute('INSERT INTO airplanes (model, capacity) VALUES (?, ?)', 
                           (model, capacity))
            con.commit()
            con.close()
            if self.parent():
                self.parent().load_data()
            self.close()



class WindowAdd_Employees(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_EmployeesForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add)

    def add(self):
        if not self.ui.lineEdit.text() or not self.ui.lineEdit_2.text() or not self.ui.lineEdit_3.text():
            QMessageBox.warning(self, "Ошибка", "Ошибка! Какая-то из строк пустая!")
        else:
            con = sqlite3.connect('airport.db')
            cursor = con.cursor()
            first_name = self.ui.lineEdit_3.text()
            last_name = self.ui.lineEdit_2.text()
            position = self.ui.lineEdit.text()
            cursor.execute('INSERT INTO employees (first_name, last_name, position) VALUES (?, ?, ?)', 
                           (first_name, last_name, position))
            con.commit()
            con.close()
            if self.parent():
                self.parent().load_data()
            self.close()
class WindowDelete_Employees(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DelForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.delete)

    def delete(self):
        if not self.ui.lineEdit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните пустое поле!")
        else:
            try:
                con = sqlite3.connect('airport.db')
                cursor = con.cursor()
                cursor.execute("SELECT id FROM employees WHERE id = ?", (int(self.ui.lineEdit.text()),))
                result = cursor.fetchone()
                
                if result is None:
                    QMessageBox.warning(self, 'Ошибка', f'ID не найден!')
                else:
                    cursor.execute("DELETE FROM employees WHERE id = ?", (int(self.ui.lineEdit.text()),))
                    con.commit()
                    QMessageBox.information(self, 'Успех', 'Данные успешно удалены!')
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit.setFocus()

                    if self.parent():
                        self.parent().load_data()

            except:
                QMessageBox.warning(self, 'Ошибка', 'Введено не числовое значение для ID!')

class WindowDelete_AirPlanes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DelForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.delete)

    def delete(self):
        if not self.ui.lineEdit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните пустое поле!")
        else:
            try:
                con = sqlite3.connect('airport.db')
                cursor = con.cursor()
                cursor.execute("SELECT id FROM airplanes WHERE id = ?", (int(self.ui.lineEdit.text()),))
                result = cursor.fetchone()
                
                if result is None:
                    QMessageBox.warning(self, 'Ошибка', f'ID не найден!')
                else:
                    cursor.execute("DELETE FROM airplanes WHERE id = ?", (int(self.ui.lineEdit.text()),))
                    con.commit()
                    QMessageBox.information(self, 'Успех', 'Данные успешно удалены!')
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit.setFocus()

                    if self.parent():
                        self.parent().load_data()

            except:
                QMessageBox.warning(self, 'Ошибка', 'Введено не числовое значение для ID!')

class WindowDelete_Flights(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DelForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.delete)

    def delete(self):
        if not self.ui.lineEdit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните пустое поле!")
        else:
            try:
                con = sqlite3.connect('airport.db')
                cursor = con.cursor()
                cursor.execute("SELECT id FROM flights WHERE id = ?", (int(self.ui.lineEdit.text()),))
                result = cursor.fetchone()
                
                if result is None:
                    QMessageBox.warning(self, 'Ошибка', f'ID не найден!')
                else:
                    cursor.execute("DELETE FROM flights WHERE id = ?", (int(self.ui.lineEdit.text()),))
                    con.commit()
                    QMessageBox.information(self, 'Успех', 'Данные успешно удалены!')
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit.setFocus()

                    if self.parent():
                        self.parent().load_data()

            except:
                QMessageBox.warning(self, 'Ошибка', 'Введено не числовое значение для ID!')

class WindowDelete_Passengers(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DelForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.delete)

    def delete(self):
        if not self.ui.lineEdit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните пустое поле!")
        else:
            try:
                con = sqlite3.connect('airport.db')
                cursor = con.cursor()
                cursor.execute("SELECT id FROM passengers WHERE id = ?", (int(self.ui.lineEdit.text()),))
                result = cursor.fetchone()
                
                if result is None:
                    QMessageBox.warning(self, 'Ошибка', f'ID не найден!')
                else:
                    cursor.execute("DELETE FROM passengers WHERE id = ?", (int(self.ui.lineEdit.text()),))
                    con.commit()
                    QMessageBox.information(self, 'Успех', 'Данные успешно удалены!')
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit.setFocus()

                    if self.parent():
                        self.parent().load_data()

            except:
                QMessageBox.warning(self, 'Ошибка', 'Введено не числовое значение для ID!')
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
