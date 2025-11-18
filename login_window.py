from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QStackedWidget
from PyQt6.QtCore import Qt
from database import authenticate_user, create_user, user_exists

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.settings()
        self.initUI()
        self.apply_style()

    def settings(self):
        self.setGeometry(800, 400, 400, 300)
        self.setWindowTitle("Expense Tracker - Login")

    def initUI(self):
        # Stacked widget to switch between login and signup
        self.stack = QStackedWidget()
        
        # Login page
        self.login_widget = QWidget()
        login_layout = QVBoxLayout()
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        
        self.signup_link_btn = QPushButton("Don't have an account? Sign up")
        self.signup_link_btn.setFlat(True)
        self.signup_link_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        login_layout.addWidget(QLabel("Login"))
        login_layout.addWidget(self.login_username)
        login_layout.addWidget(self.login_password)
        login_layout.addWidget(self.login_btn)
        login_layout.addWidget(self.signup_link_btn)
        login_layout.addStretch()
        
        self.login_widget.setLayout(login_layout)
        
        # Signup page
        self.signup_widget = QWidget()
        signup_layout = QVBoxLayout()
        
        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText("Username")
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_confirm_password = QLineEdit()
        self.signup_confirm_password.setPlaceholderText("Confirm Password")
        self.signup_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.handle_signup)
        
        self.login_link_btn = QPushButton("Already have an account? Login")
        self.login_link_btn.setFlat(True)
        self.login_link_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        signup_layout.addWidget(QLabel("Sign Up"))
        signup_layout.addWidget(self.signup_username)
        signup_layout.addWidget(self.signup_password)
        signup_layout.addWidget(self.signup_confirm_password)
        signup_layout.addWidget(self.signup_btn)
        signup_layout.addWidget(self.login_link_btn)
        signup_layout.addStretch()
        
        self.signup_widget.setLayout(signup_layout)
        
        # Add widgets to stack
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.signup_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        user_id = authenticate_user(username, password)
        
        if user_id:
            self.user_id = user_id
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def handle_signup(self):
        username = self.signup_username.text().strip()
        password = self.signup_password.text()
        confirm_password = self.signup_confirm_password.text()
        
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(password) < 4:
            QMessageBox.warning(self, "Error", "Password must be at least 4 characters")
            return
        
        if user_exists(username):
            QMessageBox.warning(self, "Error", "Username already exists")
            return
        
        if create_user(username, password):
            QMessageBox.information(self, "Success", "Account created successfully! Please login.")
            self.stack.setCurrentIndex(0)
            self.signup_username.clear()
            self.signup_password.clear()
            self.signup_confirm_password.clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to create account")

    def apply_style(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #e3e9f2;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        QLabel {
            font-size: 18px;
            color: #2c3e50;
            font-weight: bold;
            padding: 10px;
        }
        QLineEdit {
            background-color: #ffffff;
            font-size: 14px;
            color: #333;
            border: 1px solid #b0bfc6;
            border-radius: 5px;
            padding: 8px;
            margin: 5px;
        }
        QLineEdit:focus {
            border: 1px solid #2a9d8f;
            background-color: #f5f9fc;
        }
        QPushButton {
            background-color: #4caf50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:flat {
            background-color: transparent;
            color: #2c3e50;
            text-decoration: underline;
        }
        QPushButton:flat:hover {
            color: #2a9d8f;
        }
        """)