from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QWidget, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import APP_NAME, PRIMARY_COLOR
from database.request_user import UserRequest


class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} - Login")

        # Full screen ochish
        self.showMaximized()

        self.setStyleSheet(self.get_stylesheet())
        self.current_user = None

        self.init_ui()

    def init_ui(self):
        # ===== ROOT WIDGET =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignCenter)

        # ===== LOGIN CARD =====
        card = QFrame()
        card.setFixedWidth(500)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
            }}
        """)

        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)

        # ===== TITLE =====
        title_label = QLabel(APP_NAME)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # ===== LOGIN =====
        login_block = QVBoxLayout()
        login_block.setSpacing(10)

        login_label = QLabel("Login")
        login_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        card_layout.addWidget(login_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Foydalanuvchi nomini kiriting")
        self.login_input.setMinimumHeight(45)
        self.login_input.setStyleSheet(self.get_input_stylesheet())
        card_layout.addWidget(self.login_input)

        # ===== PASSWORD =====
        password_block = QVBoxLayout()
        password_block.setSpacing(10)

        password_label = QLabel("Parol")
        password_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        card_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Parolni kiriting")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet(self.get_input_stylesheet())
        card_layout.addWidget(self.password_input)

        # ===== BUTTONS =====
        button_layout = QHBoxLayout()

        login_btn = QPushButton("Kirish")
        login_btn.setMinimumHeight(45)
        login_btn.setStyleSheet(self.get_button_stylesheet())
        login_btn.clicked.connect(self.on_login_clicked)
        button_layout.addWidget(login_btn)

        exit_btn = QPushButton("Chiqish")
        exit_btn.setMinimumHeight(45)
        exit_btn.setStyleSheet(self.get_button_secondary_stylesheet())
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)

        card_layout.addLayout(button_layout)

        card.setLayout(card_layout)

        root_layout.addWidget(card)
        central_widget.setLayout(root_layout)

    # ================= LOGIC =================

    def on_login_clicked(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login:
            QMessageBox.warning(self, "Xato", "Login kiritilmadi!")
            return

        if not password:
            QMessageBox.warning(self, "Xato", "Parol kiritilmadi!")
            return

        result = UserRequest.login_user(login, password)

        if result["success"]:
            self.current_user = result["user"]
            QMessageBox.information(self, "Muvaffaqiyat", f"Xush kelibsiz, {login}!")
            self.login_success()
        else:
            QMessageBox.warning(self, "Xato", result["message"])

    def login_success(self):
        from ui.main_ui import MainWindow
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
        self.close()

    # ================= STYLES =================

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f0f2f5;
            }
        """

    def get_input_stylesheet(self):
        return f"""
            QLineEdit {{
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY_COLOR};
            }}
        """

    def get_button_stylesheet(self):
        return f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #1565C0;
            }}
        """

    def get_button_secondary_stylesheet(self):
        return """
            QPushButton {
                background-color: #888;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #444;
            }
        """