from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, PRIMARY_COLOR


class MainWindow(QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle(f"{APP_NAME} - {current_user['login']}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(self.get_stylesheet())
        
        # Main oynasini yaratish
        self.init_ui()
    
    def init_ui(self):
        """UI elementlarini yaratish"""
        # Bosh widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Asosiy layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Yuqori paneli - Sarlavha va Chiqish
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(15, 10, 15, 10)
        
        # Foydalanuvchi ma'lumoti
        user_label = QLabel(f"Xush kelibsiz, {self.current_user['login']}!")
        user_font = QFont()
        user_font.setPointSize(12)
        user_font.setBold(True)
        user_label.setFont(user_font)
        user_label.setStyleSheet("color: #333;")
        top_layout.addWidget(user_label)
        
        top_layout.addStretch()
        
        # Chiqish tugmasi
        logout_btn = QPushButton("Chiqish")
        logout_btn.setStyleSheet(self.get_logout_button_stylesheet())
        logout_btn.setMaximumWidth(100)
        logout_btn.clicked.connect(self.on_logout_clicked)
        top_layout.addWidget(logout_btn)
        
        main_layout.addLayout(top_layout)
        
        # Separator line
        separator = QWidget()
        separator.setStyleSheet("background-color: #ddd; height: 1px;")
        separator.setMaximumHeight(1)
        main_layout.addWidget(separator)
        
        # Tugmalar paneli
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(10)
        
        # Savdo tugmasi
        btn_sales = QPushButton("Savdo")
        btn_sales.setStyleSheet(self.get_button_stylesheet())
        btn_sales.setMinimumHeight(100)
        btn_sales.clicked.connect(self.on_sales_clicked)
        button_layout.addWidget(btn_sales)
        
        # Savdo tarixi tugmasi
        btn_history = QPushButton("Savdo tarixi")
        btn_history.setStyleSheet(self.get_button_stylesheet())
        btn_history.setMinimumHeight(100)
        btn_history.clicked.connect(self.on_history_clicked)
        button_layout.addWidget(btn_history)
        
        # Mahsulotlar tugmasi
        btn_products = QPushButton("Mahsulotlar")
        btn_products.setStyleSheet(self.get_button_stylesheet())
        btn_products.setMinimumHeight(100)
        btn_products.clicked.connect(self.on_products_clicked)
        button_layout.addWidget(btn_products)
        
        # Xodimlar tugmasi
        btn_employees = QPushButton("Xodimlar")
        btn_employees.setStyleSheet(self.get_button_stylesheet())
        btn_employees.setMinimumHeight(100)
        btn_employees.clicked.connect(self.on_employees_clicked)
        button_layout.addWidget(btn_employees)
        
        # Kunlik Hisobot tugmasi
        btn_report = QPushButton("Kunlik Hisobot")
        btn_report.setStyleSheet(self.get_button_stylesheet())
        btn_report.setMinimumHeight(100)
        btn_report.clicked.connect(self.on_report_clicked)
        button_layout.addWidget(btn_report)

        main_layout.addLayout(button_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(self.get_tab_stylesheet())
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def on_sales_clicked(self):
        """Savdo tugmasi bosilganda"""
        print("Savdo oynasi ochildi")
        # Keyingi qismda sales_ui ni qo'shamiz
    
    def on_history_clicked(self):
        """Savdo tarixi tugmasi bosilganda"""
        print("Savdo tarixi oynasi ochildi")
        # Keyingi qismda sales_history_ui ni qo'shamiz
    
    def on_products_clicked(self):
        """Mahsulotlar tugmasi bosilganda"""
        from .product_ui import ProductsUI
        
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "Mahsulotlar":
                self.tabs.setCurrentIndex(i)
                return
        
        products_widget = ProductsUI(parent_tabs=self.tabs)
        tab_index = self.tabs.addTab(products_widget, "Mahsulotlar")
        self.tabs.setCurrentIndex(tab_index)
    
    def on_employees_clicked(self):
        """Xodimlar tugmasi bosilganda"""
        from .employee_ui import EmployeesUI
    
        # Tab ichida allaqachon mavjudligini tekshirish
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "Xodimlar":
                self.tabs.setCurrentIndex(i)
                return
        
        # Yangi tab qo'shish
        employees_widget = EmployeesUI(parent_tabs=self.tabs)
        tab_index = self.tabs.addTab(employees_widget, "Xodimlar")
        self.tabs.setCurrentIndex(tab_index)
        
        # Tab style - tugmalarni yo'qolsin va full width bo'lsin
        self.tabs.tabBar().hide()
    
    def on_report_clicked(self):
        """Kunlik Hisobot tugmasi bosilganda"""
        print("Kunlik Hisobot oynasi ochildi")
        # Keyingi qismda daily_report_ui ni qo'shamiz
    
    def on_logout_clicked(self):
        """Chiqish tugmasi bosilganda"""
        self.close()
        # Keyingi qismda auth_ui ni qayta ochishimiz kerak
    
    def get_stylesheet(self):
        """Asosiy stil"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
        """
    
    def get_button_stylesheet(self):
        """Tugma stil"""
        return f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                padding: 18px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 17px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #1565C0;
            }}
        """
    
    def get_logout_button_stylesheet(self):
        """Chiqish tugma stil"""
        return """
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #C62828;
            }
        """
    
    def get_tab_stylesheet(self):
        """Tab stil"""
        return """
            QTabWidget {
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333;
                padding: 8px 20px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: """ + PRIMARY_COLOR + """;
                color: white;
            }
        """