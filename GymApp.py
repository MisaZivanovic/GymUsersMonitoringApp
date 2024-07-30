import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QInputDialog, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate

class ExpiryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.load_data()

    def initUI(self):
        self.setWindowTitle('Kasper')
        self.setGeometry(100, 100, 1024, 768)  # rezolucija prozora

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Ime', 'Datum isteka', 'Istekla Članarina'])
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setColumnWidth(0, 312)  # Sirina za ime
        self.table.setColumnWidth(1, 312)  # Sirina za datum isteka
        self.table.setColumnWidth(2, 312)  # Sirina za istekla clanarina

        self.button_add = QPushButton('Dodaj')
        self.button_extend = QPushButton('Produži')
        self.button_delete = QPushButton('Obriši')

        self.button_add.clicked.connect(self.add_user)
        self.button_extend.clicked.connect(self.extend_date)
        self.button_delete.clicked.connect(self.delete_user)

        layout.addWidget(self.table)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_extend)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

    def load_data(self):
        try:
            with open('data.json', 'r') as file:
                self.items = json.load(file)
        except FileNotFoundError:
            self.items = []
        self.populate_table()

    def save_data(self):
        with open('data.json', 'w') as file:
            json.dump(self.items, file)

    def populate_table(self):
        self.table.setRowCount(len(self.items))
        today = QDate.currentDate()

        for row, item in enumerate(self.items):
            name, expiry_date = item['name'], item['expiry_date']
            expired = 'Istekla' if QDate.fromString(expiry_date, 'yyyy-MM-dd') < today else 'Nije istekla'

            self.table.setItem(row, 0, QTableWidgetItem(name))
            expiry_date_item = QTableWidgetItem(expiry_date)
            expired_item = QTableWidgetItem(expired)

            if expired == 'Istekla':
                expiry_date_item.setBackground(QColor('red'))
                expired_item.setBackground(QColor('red'))

            self.table.setItem(row, 1, expiry_date_item)
            self.table.setItem(row, 2, expired_item)

    def add_user(self):
        name, ok_name = QInputDialog.getText(self, 'Dodaj korisnika', 'Ime:')
        if ok_name and name:
            expiry_date, ok_date = QInputDialog.getText(self, 'Dodaj korisnika', 'Unesi datum isteka (YYYY-MM-DD):')
            if ok_date and expiry_date:
                self.items.append({'name': name, 'expiry_date': expiry_date})
                self.save_data()
                self.populate_table()

    def extend_date(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            expiry_date = QDate.fromString(self.items[selected_row]['expiry_date'], 'yyyy-MM-dd')
            new_expiry_date = expiry_date.addDays(30).toString('yyyy-MM-dd')
            self.items[selected_row]['expiry_date'] = new_expiry_date
            self.save_data()
            self.populate_table()
        else:
            QMessageBox.warning(self, 'Upozorenje', 'Molim vas izaberite korsnika za produženje članarine.')

    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.items.pop(selected_row)
            self.save_data()
            self.populate_table()
        else:
            QMessageBox.warning(self, 'Upozorenje', 'Molim vas izaberite korsnika za brisanje.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExpiryApp()
    ex.show()
    sys.exit(app.exec_())
