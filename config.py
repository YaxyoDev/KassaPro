import os
from pathlib import Path

# Asosiy papka yo'li
BASE_DIR = Path(__file__).resolve().parent

# Database konfiguratsiya
DB_PATH = os.path.join(BASE_DIR, 'database', 'sqlite3.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

# Ilova konfiguratsiya
APP_NAME = "Kassa Pro App"
APP_VERSION = "1.0.0"

# Oyna o'lchamlari
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Rang va stil
PRIMARY_COLOR = "#2196F3"
SECONDARY_COLOR = "#FFC107"
DANGER_COLOR = "#F44336"
SUCCESS_COLOR = "#4CAF50"

# Currency (Valyuta)
CURRENCY = "UZS"
CURRENCY_SYMBOL = "сўм"

# Kutubxonalar
PYQT5_VERSION = "5.15.9"
SQLALCHEMY_VERSION = "2.0.23"
PYCOPG2_VERSION = "2.9.9"

# Log fayli
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')