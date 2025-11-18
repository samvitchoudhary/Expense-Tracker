#Runs the app
import sys

#QApplication - needed to build application
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import init_database
from app import FinanceApp
from login_window import LoginWindow

def main():
    app = QApplication(sys.argv)

    if not init_database("expenses.db"):
        #popup error
        QMessageBox.critical(None, "Error", "Could not load your database...")
        sys.exit(1)

    #shows login window first
    login_window = LoginWindow()
    login_window.show()

    #waits for user to authenticate
    app.exec()

    #checks if authentication was succesful
    if login_window.user_id:
        #closes login window
        login_window.close()
        
        #opens main app
        window = FinanceApp(login_window.user_id)
        window.show()
        
        #runs app
        sys.exit(app.exec())
    else: 
        sys.exit(0)
    


if __name__ == "__main__":
    main()