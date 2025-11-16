#Runs the app
import sys

#QApplication - needed to build application
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import init_database
from app import FinanceApp

def main():
    app = QApplication(sys.argv)

    if not init_database("expenses.db"):
        #popup error
        QMessageBox.critical(None, "Error", "Could not load your database...")
        sys.exit(1)

    window = FinanceApp()
    window.show()

    #Runs application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()