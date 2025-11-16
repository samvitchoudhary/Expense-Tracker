# App Design

#QWidget - Window that user sees
#QLabel - All the text we want to see
#QPushButton - All the buttons
#QLineEdit - User input box
#QComboBox - Drop down selection
#QDateEdit - Date selection
#QTableWidget - Spreadsheet/Table in the app
#QVBoxLayout - Vertical layout (Column)
#QHBoxLayout - Horizontal layout (Row)
#QMessageBox - Popup
#QTableWidgetItem - Widgets
#QHeaderView - Styling
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView

#QDate - Works with the date
#Qt - Alignment
from PyQt6.QtCore import QDate, Qt

#need these to call when a button is clicked
from database import get_expenses, add_expenses, remove_expenses

#Everything is built on the window (QWidget)
class FinanceApp(QWidget):
    #Constructor
    def __init__(self):
        #Activates inheritance
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table() 

    #Housing initial settings
    def settings(self):
        #Where window appears on screen
        self.setGeometry(750, 300, 550, 500)
        self.setWindowTitle("Expense Tracker App")

    #Design
    def initUI(self):
        #Creating all objects
        self.date_box = QDateEdit()
        #current day
        self.date_box.setDate(QDate.currentDate())
        #Dropdown for what the expense is for
        self.dropdown = QComboBox()
        #Enter amount spent
        self.amount = QLineEdit()
        #Description for what it was spent on
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        #id that can be accessed by CSS specifically for each button
        self.btn_add.setObjectName("btn_add")
        self.btn_delete = QPushButton("Delete Expense")
        self.btn_delete.setObjectName("btn_delete")

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        
        #edit table width
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        #dropdown menu for selecting what type of expense
        self.dropdown_options()

        #connects buttons to functions
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.remove_expense)

        self.apply_style()
        #Add widgets to a layout (either row or column)
        self.setup_layout()

    #final layout - vertical
    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        #Row 1
        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        #Row 2
        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)

    def apply_style(self):
        self.setStyleSheet("""
        /* Base styling */
        QWidget {
            background-color: #e3e9f2;
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
        }

        /* Headings for labels */
        QLabel {
            font-size: 16px;
            color: #2c3e50;
            font-weight: bold;
            padding: 5px;
        }

        /* Styling for input fields */
        QLineEdit, QComboBox, QDateEdit {
            background-color: #ffffff;
            font-size: 14px;
            color: #333;
            border: 1px solid #b0bfc6;
            border-radius: 5px;
            padding: 5px;
        }
        QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
            border: 1px solid #2c3e50;
        }
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 1px solid #2a9d8f;
            background-color: #f5f9fc;
        }

        /* Table styling */
        QTableWidget {
            background-color: #ffffff;
            alternate-background-color: #f2f7fb;
            gridline-color: #c0c9d0;
            selection-background-color: #4caf50;
            selection-color: white;
            font-size: 14px;
            border: 1px solid #cfd9e1;
        }
        QHeaderView::section {
            background-color: #2c3e50;
            color: white;
            font-weight: bold;
            padding: 4px;
            border: 1px solid #cfd9e1;
        }

        /* Scroll bar styling */
        QScrollBar:vertical {
            width: 12px;
            background-color: #f0f0f0;
            border: none;
        }
        QScrollBar::handle:vertical {
            background-color: #2c3e50;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }

        /* Buttons */
        #btn_add {
            background-color: #4caf50;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        #btn_add:hover {
            background-color: #45a049;
        }
        #btn_add:pressed {
            background-color: #3d8b40;
        }
        
        #btn_delete {
            background-color: #ff102e;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        #btn_delete:hover {
            background-color: #db0d29;
        }
        #btn_delete:pressed {
            background-color: #ff102e;
        }                

        QPushButton:disabled {
            background-color: #c8c8c8;
            color: #6e6e6e;
        }

        /* Tooltip styling */
        QToolTip {
            background-color: #2c3e50;
            color: #ffffff;
            border: 1px solid #333;
            font-size: 12px;
            padding: 5px;
            border-radius: 4px;
        }
        """)

    #expense categories
    def dropdown_options(self):
        #List of options
        categories = ["Select", "Food", "Rent", "Bills", "Going Out", "Shopping", "Misc."]
        self.dropdown.addItems(categories)

    def load_table(self):
        expenses = get_expenses()
        self.table.setRowCount(0)
        
        for row, expense in enumerate(expenses):
            self.table.insertRow(row)
            for column, data in enumerate(expense):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText() #QComboBox
        amount = self.amount.text() #QLineEdit
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description cannot be empty")
            return
        
        #everytime we add an expense we should call the load table to refresh the table
        if add_expenses(date, category, amount, description):
            self.load_table()
            # Clear inputs
            self.clear_inputs()
        else: 
            QMessageBox.critical(self, "Error", "Failed to add expense")

    def remove_expense(self):
        selected_row = self.table.currentRow()
        
        if selected_row == -1: 
            QMessageBox.warning(self, "Uh oh", "You need to choose a row to delete")
            return
        
        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this expense?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes and remove_expenses(expense_id):
            #_data??
            self.load_table()
