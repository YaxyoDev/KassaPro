from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
    QRadioButton, QButtonGroup, QMessageBox, QSplitter, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from database.request_product import ProductRequest
from datetime import datetime
from PyQt5.QtWidgets import QStyle


class SalesWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🛍️ SAVDO SISTEMA")
        self.setMinimumSize(1200, 700)
        self.showMaximized()

        self.cart_items = {}
        self.total_discount = 0
        self.is_dark_mode = False    
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.init_ui(central_widget)


    def init_ui(self, parent_widget):

        main_layout = QVBoxLayout()

                # ================= TOP RIGHT BUTTONS =================
        header_layout = QHBoxLayout()

        # 🕒 Rangli vaqt bloki
        time_container = QWidget()
        time_container.setStyleSheet("""
            QWidget {
                background-color: #1E1E2F;
                border-radius: 10px;
                padding: 5px 15px;
            }
        """)

        time_layout = QHBoxLayout()
        time_layout.setContentsMargins(10, 5, 10, 5)

        self.datetime_label = QLabel()
        time_font = QFont("Arial", 12)
        time_font.setBold(True)
        self.datetime_label.setFont(time_font)
        self.datetime_label.setStyleSheet("""
            color: #00E676;
            font-size: 14px;
            letter-spacing: 1px;
        """)

        time_layout.addWidget(self.datetime_label)
        time_container.setLayout(time_layout)

        header_layout.addWidget(time_container)
        header_layout.addStretch()

        # 🔄 Yangilash button
        refresh_btn = QPushButton(" Yangilash")
        refresh_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 6px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        refresh_btn.clicked.connect(self.on_refresh)

        # 🌗 Dark/Light toggle
        self.theme_btn = QPushButton(" 🌙 Dark")
        self.theme_btn.setMinimumHeight(40)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 6px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        self.theme_btn.clicked.connect(self.toggle_theme)

        header_layout.addWidget(self.theme_btn)

        # 🚪 Chiqish button
        exit_btn = QPushButton(" Chiqish")
        exit_btn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        exit_btn.setMinimumHeight(40)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 6px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        exit_btn.clicked.connect(self.close)

        header_layout.addWidget(refresh_btn)
        header_layout.addWidget(exit_btn)

        main_layout.addLayout(header_layout)

        top_layout = QHBoxLayout()

        # ================= LEFT =================
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        title = QLabel("🔍 BARCODE ORQALI QIDIRUV")
        title_font = QFont("Arial", 14)
        title_font.setBold(True)
        title.setFont(title_font)
        left_layout.addWidget(title)

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Barcode kiriting")
        self.barcode_input.setMinimumHeight(40)
        input_font = QFont("Arial", 12)
        self.barcode_input.setFont(input_font)
        self.barcode_input.returnPressed.connect(self.on_barcode_entered)
        left_layout.addWidget(self.barcode_input)

        cart_label = QLabel("🛒 SAVAT")
        cart_font = QFont("Arial", 12)
        cart_font.setBold(True)
        cart_label.setFont(cart_font)
        left_layout.addWidget(cart_label)

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(
            ["Mahsulot", "Miqdor", "Narx", "Jami"]
        )
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.cart_table)

        clear_btn = QPushButton("🗑 Savatni bo'shatish")
        clear_btn_font = QFont("Arial", 11)
        clear_btn_font.setBold(True)
        clear_btn.setFont(clear_btn_font)
        clear_btn.setMinimumHeight(45)
        clear_btn.setStyleSheet("background-color: #F44336; color: white; border-radius: 5px;")
        clear_btn.clicked.connect(self.on_clear_cart)
        left_layout.addWidget(clear_btn)

        left_widget.setLayout(left_layout)

        # ================= RIGHT =================
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        title2 = QLabel("📦 MAHSULOTLAR")
        title2_font = QFont("Arial", 14)
        title2_font.setBold(True)
        title2.setFont(title2_font)
        right_layout.addWidget(title2)

        self.name_search_input = QLineEdit()
        self.name_search_input.setPlaceholderText("Mahsulot nomi...")
        self.name_search_input.setMinimumHeight(40)
        search_font = QFont("Arial", 12)
        self.name_search_input.setFont(search_font)
        self.name_search_input.textChanged.connect(self.on_name_search)
        right_layout.addWidget(self.name_search_input)

        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(
            ["Mahsulot", "Narx", "Miqdor", "Qo'shish"]
        )
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.products_table)

        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 4)

        top_layout.addWidget(splitter)

        # ================= BOTTOM =================
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(15, 15, 15, 15)
        bottom_layout.setSpacing(15)

        # Chegirma va Jami summa
        summary_layout = QHBoxLayout()

        self.discount_label = QLabel("Chegirma: 0% (0 UZS)")
        discount_font = QFont("Arial", 13)
        discount_font.setBold(True)
        self.discount_label.setFont(discount_font)
        self.discount_label.setStyleSheet("color: #F44336;")
        summary_layout.addWidget(self.discount_label)

        summary_layout.addStretch()

        self.total_label = QLabel("📊 JAMI: 0 UZS")
        total_font = QFont("Arial", 18)
        total_font.setBold(True)
        self.total_label.setFont(total_font)
        self.total_label.setStyleSheet("color: #4CAF50; background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        summary_layout.addWidget(self.total_label)

        bottom_layout.addLayout(summary_layout)

        # To'lov usuli
        payment_label = QLabel("💳 TO'LOV USULI:")
        payment_font = QFont("Arial", 12)
        payment_font.setBold(True)
        payment_label.setFont(payment_font)
        bottom_layout.addWidget(payment_label)

        payment_layout = QHBoxLayout()

        self.payment_group = QButtonGroup()

        self.cash_radio = QRadioButton("Naqd")
        self.cash_radio.setChecked(True)
        radio_font = QFont("Arial", 11)
        self.cash_radio.setFont(radio_font)

        self.card_radio = QRadioButton("Karta")
        self.card_radio.setFont(radio_font)

        self.click_radio = QRadioButton("Click")
        self.click_radio.setFont(radio_font)

        self.payment_group.addButton(self.cash_radio, 1)
        self.payment_group.addButton(self.card_radio, 2)
        self.payment_group.addButton(self.click_radio, 3)

        payment_layout.addWidget(self.cash_radio)
        payment_layout.addWidget(self.card_radio)
        payment_layout.addWidget(self.click_radio)
        payment_layout.addStretch()

        bottom_layout.addLayout(payment_layout)

        # Chop etish tugmasi
        checkout_btn = QPushButton("🖨 CHOP ETISH")
        checkout_font = QFont("Arial", 13)
        checkout_font.setBold(True)
        checkout_btn.setFont(checkout_font)
        checkout_btn.setMinimumHeight(55)
        checkout_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; font-weight: bold;")
        checkout_btn.clicked.connect(self.on_print_and_checkout)
        bottom_layout.addWidget(checkout_btn)

        bottom_widget.setLayout(bottom_layout)

        main_layout.addLayout(top_layout, 4)
        main_layout.addWidget(bottom_widget, 1)

        parent_widget.setLayout(main_layout)

        # 🕒 Timer ishga tushirish
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # har 1 sekund
        self.update_datetime()  # darhol chiqarish

    # ====================================================
    # LOGIC
    # ====================================================

    def on_barcode_entered(self):
        text = self.barcode_input.text().strip()
        if not text:
            return

        # Foiz
        if text.startswith("%"):
            try:
                percent = float(text[1:])
                if 0 <= percent <= 100:
                    self.total_discount = percent
                    self.update_total()
            except:
                QMessageBox.warning(self, "Xato", "Noto'g'ri foiz formati!")
            self.barcode_input.clear()
            return

        # +/- amali
        if text.startswith("+"):
            try:
                qty = int(text[1:])
                if self.cart_items:
                    last_id = list(self.cart_items.keys())[-1]
                    self.cart_items[last_id]["quantity"] += qty
                    self.update_cart()
                    self.update_total()
            except:
                QMessageBox.warning(self, "Xato", "Noto'g'ri son formati!")
            self.barcode_input.clear()
            return

        if text.startswith("-"):
            try:
                qty = int(text[1:])
                if self.cart_items:
                    last_id = list(self.cart_items.keys())[-1]
                    if self.cart_items[last_id]["quantity"] > qty:
                        self.cart_items[last_id]["quantity"] -= qty
                    else:
                        del self.cart_items[last_id]
                    self.update_cart()
                    self.update_total()
            except:
                QMessageBox.warning(self, "Xato", "Noto'g'ri son formati!")
            self.barcode_input.clear()
            return

        # Oddiy barcode
        result = ProductRequest.get_product_by_barcode(text)
        if result["success"]:
            self.add_to_cart(result["product"])
        else:
            QMessageBox.warning(self, "Xato", "Mahsulot topilmadi")

        self.barcode_input.clear()

    def on_name_search(self):
        search = self.name_search_input.text().lower()
        self.products_table.setRowCount(0)

        if not search:
            return

        products = ProductRequest.get_all_products()

        for product in products:
            name = product.name if hasattr(product, 'name') else product['name']
            price = product.price if hasattr(product, 'price') else product['price']
            quantity = product.quantity if hasattr(product, 'quantity') else product['quantity']
            product_id = product.id if hasattr(product, 'id') else product['id']

            if search in name.lower():
                row = self.products_table.rowCount()
                self.products_table.insertRow(row)
                self.products_table.setRowHeight(row, 40)

                self.products_table.setItem(row, 0, QTableWidgetItem(name))
                self.products_table.setItem(row, 1, QTableWidgetItem(f"{price:,.0f}"))
                self.products_table.setItem(row, 2, QTableWidgetItem(str(quantity)))

                btn = QPushButton("➕ Qo'shish")
                btn.setStyleSheet("background-color: #2196F3; color: white; border-radius: 3px;")
                btn_font = QFont("Arial", 10)
                btn_font.setBold(True)
                btn.setFont(btn_font)
                btn.setMinimumHeight(35)
                btn.clicked.connect(lambda _, p=product: self.add_to_cart(p))
                self.products_table.setCellWidget(row, 3, btn)

    def add_to_cart(self, product):
        product_id = product.id if hasattr(product, 'id') else product['id']
        product_name = product.name if hasattr(product, 'name') else product['name']
        product_price = product.price if hasattr(product, 'price') else product['price']

        if product_id in self.cart_items:
            self.cart_items[product_id]["quantity"] += 1
        else:
            self.cart_items[product_id] = {
                "product": product,
                "quantity": 1,
                "price": product_price
            }

        self.update_cart()
        self.update_total()

    def update_cart(self):
        self.cart_table.setRowCount(0)

        for product_id, item in self.cart_items.items():
            product = item["product"]
            quantity = item["quantity"]
            price = item["price"]
            total = price * quantity

            product_name = product.name if hasattr(product, 'name') else product['name']

            row = self.cart_table.rowCount()
            self.cart_table.insertRow(row)
            self.cart_table.setRowHeight(row, 40)

            name_item = QTableWidgetItem(product_name)
            name_item.setFont(QFont("Arial", 11))
            self.cart_table.setItem(row, 0, name_item)

            qty_item = QTableWidgetItem(str(quantity))
            qty_item.setFont(QFont("Arial", 11, QFont.Bold))
            self.cart_table.setItem(row, 1, qty_item)

            price_item = QTableWidgetItem(f"{price:,.0f}")
            price_item.setFont(QFont("Arial", 11))
            self.cart_table.setItem(row, 2, price_item)

            total_item = QTableWidgetItem(f"{total:,.0f}")
            total_item.setFont(QFont("Arial", 11, QFont.Bold))
            self.cart_table.setItem(row, 3, total_item)

    def update_total(self):
        subtotal = sum(
            item["price"] * item["quantity"]
            for item in self.cart_items.values()
        )

        discount = (subtotal * self.total_discount) / 100
        total = subtotal - discount

        # ✅ TO'G'IRLANGAN
        if self.total_discount > 0:
            self.discount_label.setText(f"Chegirma: {self.total_discount}% ({discount:,.0f} UZS)")
        else:
            self.discount_label.setText("Chegirma: 0% (0 UZS)")

        self.total_label.setText(f"📊 JAMI: {total:,.0f} UZS")

    def on_clear_cart(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Xato", "Savat allaqachon bo'sh!")
            return

        self.cart_items = {}
        self.total_discount = 0
        self.update_cart()
        self.update_total()

    def update_datetime(self):
        """Tepada real vaqt ko'rsatish"""
        current_time = datetime.now().strftime("%d.%m.%Y-%H:%M")
        self.datetime_label.setText(current_time)    

    def on_refresh(self):
        """Ma'lumotlarni yangilash"""
        self.on_name_search()
        self.update_cart()
        self.update_total()
        QMessageBox.information(self, "Yangilandi", "Ma'lumotlar yangilandi!")

    def toggle_theme(self):
        if self.is_dark_mode:
            self.apply_light_mode()
            self.theme_btn.setText(" 🌙 Dark")
            self.is_dark_mode = False
        else:
            self.apply_dark_mode()
            self.theme_btn.setText(" ☀ Light")
            self.is_dark_mode = True


    def apply_dark_mode(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #121212;
        }

        QLabel {
            color: white;
        }

        QRadioButton {
            color: white;
            font-weight: bold;
        }

        QRadioButton::indicator {
            width: 15px;
            height: 15px;
        }

        QLineEdit, QTableWidget {
            background-color: #1E1E1E;
            color: white;
            border: 1px solid #333;
        }

        QHeaderView::section {
            background-color: #2A2A2A;
            color: white;
            padding: 5px;
            border: 1px solid #444;
        }

        QTableWidget::item {
            color: white;
        }

        QPushButton {
            color: white;
        }

        QMessageBox {
            background-color: #1E1E1E;
        }

        QMessageBox QLabel {
            color: white;
        }
                           
        QMessageBox QPushButton {
            background-color: #333;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        }

        QMessageBox QPushButton:hover {
            background-color: #555;
        }
    """)


    def apply_light_mode(self):
        self.setStyleSheet("")

    def on_print_and_checkout(self):
        """Chop etish va savdoni yakunlash"""
        if not self.cart_items:
            QMessageBox.warning(self, "Xato", "Savat bo'sh")
            return

        # To'lov usuli
        payment_method = ""
        if self.cash_radio.isChecked():
            payment_method = "NAQD"
        elif self.card_radio.isChecked():
            payment_method = "KARTA"
        elif self.click_radio.isChecked():
            payment_method = "CLICK"

        # Hisoblash
        subtotal = sum(
            item["price"] * item["quantity"]
            for item in self.cart_items.values()
        )
        discount = (subtotal * self.total_discount) / 100
        total = subtotal - discount

        # Chek
        items_list = ""
        for item in self.cart_items.values():
            product = item["product"]
            name = product.name if hasattr(product, 'name') else product['name']
            qty = item["quantity"]
            price = item["price"]
            item_total = price * qty
            items_list += f"\n  {name} x{qty} = {item_total:,.0f} UZS"

        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        message = f"═════════════════════════════════════════\n"
        message += f"                    BINO STROY CHEK\n"
        message += f"═════════════════════════════════════════\n\n"
        message += f"Sana: {current_time}\n"
        message += f"{items_list}\n\n"
        message += f"─────────────────────────────────────────\n"

        if self.total_discount > 0:
            message += f"Umumiy Summa:        {subtotal:,.0f} UZS\n"
            message += f"Chegirma ({self.total_discount}%):       -{discount:,.0f} UZS\n"
            message += f"═════════════════════════════════════════\n"
            message += f"JAMI SUMMA:          {total:,.0f} UZS\n"
        else:
            message += f"═════════════════════════════════════════\n"
            message += f"JAMI SUMMA:          {total:,.0f} UZS\n"

        message += f"═════════════════════════════════════════\n\n"
        message += f"To'lov Usuli:        {payment_method}\n\n"
        message += f"═════════════════════════════════════════\n"
        message += f"         Xaridingiz uchun rahmat!\n"
        message += f"═════════════════════════════════════════\n"

        QMessageBox.information(self, "✅ CHEK", message)

        # ✅ !!!!! QUYIDAGI QATORLARNI QO'SHING !!!!!
        # Bazada miqdorni kamaytirish
        for product_id, item in self.cart_items.items():
            quantity = item["quantity"]
            result = ProductRequest.decrease_quantity(product_id, quantity)
            if not result["success"]:
                QMessageBox.warning(self, "Xato", result["message"])
                return

        # Chop etish muvaffaq bo'lgach, savatni bo'shatish
        self.on_clear_cart()
        self.name_search_input.clear()

