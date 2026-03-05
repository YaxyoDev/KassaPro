from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from database.request_product import ProductRequest


class ProductsUI(QWidget):
    def __init__(self, parent_tabs=None):
        super().__init__()
        self.parent_tabs = parent_tabs
        self.init_ui()
        self.load_products()
    
    def get_combo_stylesheet(self):
        return """
            QComboBox {
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
            }
        """

    def get_spinbox_stylesheet(self):
        return """
            QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QSpinBox:focus { border: 2px solid #2196F3; }
        """
    
    def get_save_button_stylesheet(self):
        return """
            QPushButton {
                background: #4CAF50;
                color: white;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover { background: #45a049; }
        """

    def get_cancel_button_stylesheet(self):
        return """
        QPushButton {
            background: #f44336;
            color: white;
            border-radius: 6px;
            padding: 10px;
            font-size: 12px;
        }
        QPushButton:hover { background: #e53935; }
    """

    def clear_form(self):
        self.name_input.clear()
        self.price_input.clear()
        self.quantity_input.setValue(0)
        self.status_combo.setCurrentIndex(0)
        self.generate_barcode()

    def init_ui(self):
        """ASOSIY UI - TO'LIQLIKDA QAYTA YOZILGAN"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # ========== YUQORI PANEL: QIDIRISH VA TUGMALAR ==========
        top_layout = QHBoxLayout()
        
        # Qidirish
        search_label = QLabel("Qidirish:")
        search_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        top_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Mahsulot nomini izlang...")
        self.search_input.setStyleSheet(self.get_input_stylesheet())
        self.search_input.setMaximumWidth(250)
        self.search_input.textChanged.connect(self.on_search)
        top_layout.addWidget(self.search_input)
        
        top_layout.addStretch()
        
        # Tugmalar
        add_btn = QPushButton("➕ Qo'shish")
        add_btn.setStyleSheet(self.get_add_button_stylesheet())
        add_btn.setMaximumWidth(120)
        add_btn.clicked.connect(self.on_add_product)
        top_layout.addWidget(add_btn)
        
        update_btn = QPushButton("✏️ Yangilash")
        update_btn.setStyleSheet(self.get_update_button_stylesheet())
        update_btn.setMaximumWidth(120)
        update_btn.clicked.connect(self.on_update_product)
        top_layout.addWidget(update_btn)
        
        delete_btn = QPushButton("🗑️ O'chirish")
        delete_btn.setStyleSheet(self.get_delete_button_stylesheet())
        delete_btn.setMaximumWidth(120)
        delete_btn.clicked.connect(self.on_delete_selected)
        top_layout.addWidget(delete_btn)
        
        self.refresh_btn = QPushButton("🔄 Yangilash")
        self.refresh_btn.setStyleSheet(self.get_refresh_button_stylesheet())
        self.refresh_btn.setMaximumWidth(120)
        self.refresh_btn.clicked.connect(self.on_refresh_clicked)
        top_layout.addWidget(self.refresh_btn)
        
        back_btn = QPushButton("⬅ Orqaga")
        back_btn.setStyleSheet(self.get_back_button_stylesheet())
        back_btn.setMaximumWidth(100)
        back_btn.clicked.connect(self.on_back_clicked)
        top_layout.addWidget(back_btn)
        
        main_layout.addLayout(top_layout)
        
        # ========== JADVALNI YARATISH ==========
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nomi", "Barcode", "Narx", "Miqdor", "Yaratildi", "Status", "✓"
        ])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 40)
        self.table.setStyleSheet(self.get_table_stylesheet())
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
    
    def load_products(self, search_query=""):
        """Mahsulotlarni yuklash"""
        products = ProductRequest.get_all_products()
        
        # Search filter
        if search_query:
            products = [p for p in products if search_query.lower() in p.name.lower()]
        
        self.table.setRowCount(0)
        
        for product in products:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # ID
            id_item = QTableWidgetItem(str(product.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 0, id_item)
            
            # Nomi
            name_item = QTableWidgetItem(product.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 1, name_item)
            
            # Barcode
            barcode_item = QTableWidgetItem(str(product.barcode))
            barcode_item.setFlags(barcode_item.flags() & ~Qt.ItemIsEditable)
            barcode_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 2, barcode_item)
            
            # Narx
            price_item = QTableWidgetItem(f"{product.price:,.0f} {product.currency if hasattr(product, 'currency') else 'UZS'}")
            price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
            price_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 3, price_item)
            
            # Miqdor
            quantity_item = QTableWidgetItem(str(product.quantity))
            quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemIsEditable)
            quantity_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 4, quantity_item)
            
            # Yaratildi
            created_at = product.created_at.strftime("%d.%m.%Y %H:%M:%S")
            created_item = QTableWidgetItem(created_at)
            created_item.setFlags(created_item.flags() & ~Qt.ItemIsEditable)
            created_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 5, created_item)
            
            # Status
            status_item = QTableWidgetItem(product.status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            status_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row_position, 6, status_item)
            
            # Checkbox (Tanlash)
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row_position, 7, checkbox_item)
    
    def on_search(self):
        """Qidirish"""
        search_query = self.search_input.text()
        self.load_products(search_query)
    
    def on_refresh_clicked(self):
        """Yangilash tugmasi"""
        self.refresh_btn.setEnabled(False)
        self.load_products()
        QTimer.singleShot(1000, lambda: self.refresh_btn.setEnabled(True))
        QMessageBox.information(self, "Muvaffaqiyat", "Ma'lumotlar yangilandi!")
    
    def on_back_clicked(self):
        """Orqaga tugmasi"""
        if self.parent_tabs:
            for i in range(self.parent_tabs.count()):
                if self.parent_tabs.tabText(i) == "Mahsulotlar":
                    self.parent_tabs.removeTab(i)
                    break
    
    def on_delete_selected(self):
        """Tanlangan mahsulotlarni o'chirish"""
        selected_rows = []
        
        for row in range(self.table.rowCount()):
            checkbox = self.table.item(row, 7)
            if checkbox.checkState() == Qt.Checked:
                product_id = int(self.table.item(row, 0).text())
                selected_rows.append(product_id)
        
        if not selected_rows:
            QMessageBox.warning(self, "Xato", "Hech qanday mahsulot tanlanmadi!")
            return
        
        reply = QMessageBox.question(
            self,
            "Tasdiqlash",
            f"{len(selected_rows)} ta mahsulot o'chirilishiga ishonchingiz komilmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for product_id in selected_rows:
                result = ProductRequest.delete_product(product_id)
                if not result["success"]:
                    QMessageBox.warning(self, "Xato", result["message"])
                    return
            
            QMessageBox.information(self, "Muvaffaqiyat", "Mahsulotlar muvaffaqiyatli o'chirildi!")
            self.load_products()
    
    def on_add_product(self):
        """Mahsulot qo'shish"""
        dialog = AddProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()
    
    def on_update_product(self):
        """Mahsulot yangilash"""
        selected_row = self.table.currentRow()
        
        if selected_row == -1:
            QMessageBox.warning(self, "Xato", "Mahsulotni tanlab oling!")
            return
        
        product_id = int(self.table.item(selected_row, 0).text())
        dialog = UpdateProductDialog(product_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()
    
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
                font-size: 13px;
            }
            QPushButton:hover { background-color: #D32F2F; }
            QPushButton:pressed { background-color: #C62828; }
        """
    
    def get_update_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 12px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #F57C00; }
            QPushButton:pressed { background-color: #E65100; }
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
                font-size: 13px;
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
    
    def get_input_stylesheet(self):
        return """
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mahsulot qo'shish")
        self.setGeometry(100, 100, 500, 450)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)
        
        # Nomi
        name_label = QLabel("Mahsulot nomi:")
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Mahsulot nomini kiriting")
        self.name_input.setStyleSheet(self.get_input_stylesheet())
        self.name_input.setMinimumHeight(35)
        layout.addWidget(self.name_input)
        
        # Barcode - AUTO GENERATE
        barcode_label = QLabel("Barcode:")
        barcode_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(barcode_label)
        
        barcode_layout = QHBoxLayout()
        
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Barcode ni kiriting")
        self.barcode_input.setStyleSheet(self.get_input_stylesheet())
        self.barcode_input.setMinimumHeight(35)
        self.barcode_input.setReadOnly(False)
        barcode_layout.addWidget(self.barcode_input)
        
        generate_btn = QPushButton("🔄 Auto")
        generate_btn.setMaximumWidth(80)
        generate_btn.setStyleSheet(self.get_generate_button_stylesheet())
        generate_btn.clicked.connect(self.generate_barcode)
        barcode_layout.addWidget(generate_btn)
        
        layout.addLayout(barcode_layout)
        
        # Narx
        price_label = QLabel("Narx (UZS):")
        price_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(price_label)
        
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Mahsulot narxini kiriting")
        self.price_input.setStyleSheet(self.get_input_stylesheet())
        self.price_input.setMinimumHeight(35)
        layout.addWidget(self.price_input)
        
        # Miqdor
        quantity_label = QLabel("Miqdor (Dona):")
        quantity_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(quantity_label)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(1000000)
        self.quantity_input.setStyleSheet(self.get_spinbox_stylesheet())
        self.quantity_input.setMinimumHeight(35)
        layout.addWidget(self.quantity_input)
        
        # Status
        status_label = QLabel("Status:")
        status_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(status_label)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "inactive"])
        self.status_combo.setStyleSheet(self.get_combo_stylesheet())
        self.status_combo.setMinimumHeight(35)
        layout.addWidget(self.status_combo)
        
        layout.addStretch()
        
        # Tugmalar
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
        
        # AUTO BARCODE GENERATE
        self.generate_barcode()
    
    def generate_barcode(self):
        """Barcode auto-generate qilish"""
        barcode = ProductRequest.generate_barcode()
        self.barcode_input.setText(barcode)
    
    def on_save(self):
        name = self.name_input.text().strip()
        barcode = self.barcode_input.text().strip()
        price = self.price_input.text().strip()
        quantity = self.quantity_input.value()
        status = self.status_combo.currentText()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Xato", "Mahsulot nomi kiritilmadi!")
            return
        
        if not barcode:
            QMessageBox.warning(self, "Xato", "Barcode kiritilmadi!")
            return
        
        if not price:
            QMessageBox.warning(self, "Xato", "Narx kiritilmadi!")
            return
        
        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Xato", "Narx raqam bo'lishi kerak!")
            return
        
        # Database ga saqlash
        result = ProductRequest.create_product(name, barcode, price, quantity, status)
        
        if result["success"]:
            QMessageBox.information(self, "Muvaffaqiyat", result["message"])
            self.accept()
        else:
            QMessageBox.warning(self, "Xato", result["message"])
    
    def get_generate_button_stylesheet(self):
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """
    
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
    
    def get_spinbox_stylesheet(self):
        return """
            QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QSpinBox:focus { border: 2px solid #2196F3; }
        """
    
    def get_combo_stylesheet(self):
        return """
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QComboBox:focus { border: 2px solid #2196F3; }
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


class UpdateProductDialog(QDialog):
    def __init__(self, product_id, parent=None):
        super().__init__(parent)
        self.product_id = product_id
        self.setWindowTitle("Mahsulot yangilash")
        self.setGeometry(100, 100, 500, 450)
        self.init_ui()
        self.load_product_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)
        
        # Nomi
        name_label = QLabel("Mahsulot nomi:")
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(self.get_input_stylesheet())
        self.name_input.setMinimumHeight(35)
        layout.addWidget(self.name_input)
        
        # Barcode
        barcode_label = QLabel("Barcode:")
        barcode_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(barcode_label)
        
        self.barcode_input = QLineEdit()
        self.barcode_input.setStyleSheet(self.get_input_stylesheet())
        self.barcode_input.setMinimumHeight(35)
        layout.addWidget(self.barcode_input)
        
        # Narx
        price_label = QLabel("Narx (UZS):")
        price_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(price_label)
        
        self.price_input = QLineEdit()
        self.price_input.setStyleSheet(self.get_input_stylesheet())
        self.price_input.setMinimumHeight(35)
        layout.addWidget(self.price_input)
        
        # Miqdor
        quantity_label = QLabel("Miqdor (Dona):")
        quantity_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(quantity_label)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(1000000)
        self.quantity_input.setStyleSheet(self.get_spinbox_stylesheet())
        self.quantity_input.setMinimumHeight(35)
        layout.addWidget(self.quantity_input)
        
        # Status
        status_label = QLabel("Status:")
        status_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(status_label)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "inactive"])
        self.status_combo.setStyleSheet(self.get_combo_stylesheet())
        self.status_combo.setMinimumHeight(35)
        layout.addWidget(self.status_combo)
        
        layout.addStretch()
        
        # Tugmalar
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("✅ Yangilash")
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
    
    def load_product_data(self):
        """Mahsulot ma'lumotlarini yuklash"""
        result = ProductRequest.get_product_by_id(self.product_id)
        
        if result["success"]:
            product = result["product"]
            self.name_input.setText(product["name"])
            self.barcode_input.setText(str(product["barcode"]))
            self.price_input.setText(str(product["price"]))
            self.quantity_input.setValue(product["quantity"])
            self.status_combo.setCurrentText(product["status"])
    
    def on_save(self):
        name = self.name_input.text().strip()
        barcode = self.barcode_input.text().strip()
        price = self.price_input.text().strip()
        quantity = self.quantity_input.value()
        status = self.status_combo.currentText()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Xato", "Mahsulot nomi kiritilmadi!")
            return
        
        if not barcode:
            QMessageBox.warning(self, "Xato", "Barcode kiritilmadi!")
            return
        
        if not price:
            QMessageBox.warning(self, "Xato", "Narx kiritilmadi!")
            return
        
        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Xato", "Narx raqam bo'lishi kerak!")
            return
        
        # Database ga yangilash
        result = ProductRequest.update_product(self.product_id, name, barcode, price, quantity, status)
        
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
    
    def get_spinbox_stylesheet(self):
        return """
            QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QSpinBox:focus { border: 2px solid #2196F3; }
        """
    
    def get_combo_stylesheet(self):
        return """
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QComboBox:focus { border: 2px solid #2196F3; }
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