from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from database.request_user import UserRequest


class EmployeesUI(QWidget):
    def __init__(self, parent_tabs=None):
        super().__init__()
        self.parent_tabs = parent_tabs
        self.init_ui()
        self.load_employees()
    
    def init_ui(self):
        """UI elementlarini yaratish"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Yuqori panel
        top_panel = QHBoxLayout()
        top_panel.setContentsMargins(20, 15, 20, 15)
        top_panel.setSpacing(10)
        
        # Back tugmasi
        back_btn = QPushButton("← Orqaga")
        back_btn.setMaximumWidth(120)
        back_btn.setStyleSheet(self.get_back_button_stylesheet())
        back_btn.clicked.connect(self.on_back_clicked)
        top_panel.addWidget(back_btn)
        
        # Sarlavha
        title_label = QLabel("Xodimlar")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        top_panel.addWidget(title_label)
        
        top_panel.addStretch()
        
        # Refresh tugmasi
        self.refresh_btn = QPushButton("🔄 Yangilash")
        self.refresh_btn.setMaximumWidth(120)
        self.refresh_btn.setStyleSheet(self.get_refresh_button_stylesheet())
        self.refresh_btn.clicked.connect(self.on_refresh_clicked)
        top_panel.addWidget(self.refresh_btn)
        
        main_layout.addLayout(top_panel)
        
        # Separator line
        separator = QWidget()
        separator.setStyleSheet("background-color: #ddd; height: 2px;")
        separator.setMaximumHeight(2)
        main_layout.addWidget(separator)
        
        # Jadvali
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Login", "Parol", "Ro'yxatdan o'tgan", "Status", "Tanlash"])
        
        # Header font kattalashtirish
        header_font = QFont("Arial", 13)
        header_font.setBold(True)
        self.table.horizontalHeader().setFont(header_font)
        
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 120)
        
        self.table.setStyleSheet(self.get_table_stylesheet())
        self.table.verticalHeader().setDefaultSectionSize(60)
        
        main_layout.addWidget(self.table)
        
        # Tugmalar paneli
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 15, 20, 15)
        button_layout.setSpacing(10)
        
        delete_btn = QPushButton("🗑️ Tanlanganlarin o'chirish")
        delete_btn.setStyleSheet(self.get_delete_button_stylesheet())
        delete_btn.clicked.connect(self.on_delete_selected)
        delete_btn.setMinimumHeight(50)  
        delete_btn.setMinimumWidth(250)
        delete_btn.setFont(QFont("Arial", 15))
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        add_btn = QPushButton("➕ Xodim qo'shish")
        add_btn.setStyleSheet(self.get_add_button_stylesheet())
        add_btn.clicked.connect(self.on_add_employee)
        add_btn.setMinimumHeight(50)  
        add_btn.setMinimumWidth(250)
        add_btn.setFont(QFont("Arial", 15))
        button_layout.addWidget(add_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def load_employees(self):
        """Xodimlarni yuklash"""
        users = UserRequest.get_all_users()
        
        self.table.setRowCount(0)
        
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # ID
            id_item = QTableWidgetItem(str(user.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setFont(QFont("Arial", 14))
            self.table.setItem(row_position, 0, id_item)
            
            # Login
            login_item = QTableWidgetItem(user.login)
            login_item.setFlags(login_item.flags() & ~Qt.ItemIsEditable)
            login_item.setFont(QFont("Arial", 14))
            self.table.setItem(row_position, 1, login_item)
            
            # Parol
            password_item = QTableWidgetItem(user.password)
            password_item.setFlags(password_item.flags() & ~Qt.ItemIsEditable)
            password_item.setFont(QFont("Arial", 14))
            self.table.setItem(row_position, 2, password_item)
            
            # Qo'shildi
            joined_at = user.joined_at.strftime("%d.%m.%Y %H:%M:%S")
            joined_item = QTableWidgetItem(joined_at)
            joined_item.setFlags(joined_item.flags() & ~Qt.ItemIsEditable)
            joined_item.setFont(QFont("Arial", 14))
            self.table.setItem(row_position, 3, joined_item)
            
            # Status
            status_item = QTableWidgetItem(user.status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            status_item.setFont(QFont("Arial", 14))
            self.table.setItem(row_position, 4, status_item)
            
            # Checkbox (Tanlash)
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row_position, 5, checkbox_item)
    
    def on_refresh_clicked(self):
        """Yangilash tugmasi"""
        self.refresh_btn.setEnabled(False)
        self.load_employees()
        QTimer.singleShot(1000, lambda: self.refresh_btn.setEnabled(True))
        QMessageBox.information(self, "Muvaffaqiyat", "Ma'lumotlar yangilandi!")
    
    def on_back_clicked(self):
        """Orqaga tugmasi"""
        if self.parent_tabs:
            for i in range(self.parent_tabs.count()):
                if self.parent_tabs.tabText(i) == "Xodimlar":
                    self.parent_tabs.removeTab(i)
                    break
    
    def on_delete_selected(self):
        """Tanlangan xodimlarni o'chirish"""
        selected_rows = []
        
        for row in range(self.table.rowCount()):
            checkbox = self.table.item(row, 5)
            if checkbox.checkState() == Qt.Checked:
                user_id = int(self.table.item(row, 0).text())
                selected_rows.append(user_id)
        
        if not selected_rows:
            QMessageBox.warning(self, "Xato", "Hech qanday xodim tanlanmadi!")
            return
        
        reply = QMessageBox.question(
            self,
            "Tasdiqlash",
            f"{len(selected_rows)} ta xodim o'chirilishiga ishonchingiz komilmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for user_id in selected_rows:
                result = UserRequest.delete_user(user_id)
                if not result["success"]:
                    QMessageBox.warning(self, "Xato", result["message"])
                    return
            
            QMessageBox.information(self, "Muvaffaqiyat", "Xodimlar muvaffaqiyatli o'chirildi!")
            self.load_employees()
    
    def on_add_employee(self):
        """Xodim qo'shish"""
        dialog = AddEmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_employees()
    
    def get_back_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #616161; }
            QPushButton:pressed { background-color: #424242; }
        """
    
    def get_refresh_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """
    
    def get_delete_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 12px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover { background-color: #D32F2F; }
            QPushButton:pressed { background-color: #C62828; }
        """
    
    def get_add_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
        """
    
    def get_table_stylesheet(self):
        return """
            QTableWidget {
                gridline-color: #ddd;
                border: none;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
            }
        """


class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xodim qo'shish")
        self.setGeometry(100, 100, 450, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)
        
        login_label = QLabel("Login:")
        login_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(login_label)
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Xodim loginini kiriting")
        self.login_input.setStyleSheet(self.get_input_stylesheet())
        self.login_input.setMinimumHeight(35)
        layout.addWidget(self.login_input)
        
        password_label = QLabel("Parol:")
        password_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Xodim parolini kiriting")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_stylesheet())
        self.password_input.setMinimumHeight(35)
        layout.addWidget(self.password_input)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("✅ Saqlash")
        save_btn.setStyleSheet(self.get_save_button_stylesheet())
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.on_save)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("❌ Bekor qilish")
        cancel_btn.setStyleSheet(self.get_cancel_button_stylesheet())
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def on_save(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        
        if not login:
            QMessageBox.warning(self, "Xato", "Login kiritilmadi!")
            return
        
        if not password:
            QMessageBox.warning(self, "Xato", "Parol kiritilmadi!")
            return
        
        result = UserRequest.create_user(login, password)
        
        if result["success"]:
            QMessageBox.information(self, "Muvaffaqiyat", result["message"])
            self.accept()
        else:
            QMessageBox.warning(self, "Xato", result["message"])
    
    def get_input_stylesheet(self):
        return """
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus { border: 2px solid #2196F3; }
        """
    
    def get_save_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """
    
    def get_cancel_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #999;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #777; }
        """