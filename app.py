import sys
from PyQt5.QtWidgets import QApplication
from database import init_db, get_session, close_session
from database.models import User
from datetime import datetime
from ui.auth_ui import AuthWindow
from ui.main_ui import MainWindow


def add_default_user():
    """Default user qo'shish"""
    session = get_session()
    try:
        # Allaqachon user mavjudligini tekshirish
        existing_user = session.query(User).filter(User.login == 'admin').first()
        
        if existing_user:
            print("✅ Default user allaqachon mavjud!")
            return
        
        # Default user yaratish
        default_user = User(
            login='Admin',
            password='1234',
            status='active',
            joined_at=datetime.now()
        )
        
        session.add(default_user)
        session.commit()
        
        print("✅ Default user muvaffaqiyatli qo'shildi!")
        print(f"   Login: admin")
        print(f"   Parol: 1234")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Xato: {str(e)}")
    
    finally:
        close_session(session)


def main():
    """Asosiy funksiya"""
    # Database jadvallarini yaratish
    init_db()
    
    # Default user qo'shish
    add_default_user()
    
    # PyQt5 ilovasini yaratish
    app = QApplication(sys.argv)
    
    # Auth oynani yaratish
    auth_window = AuthWindow()
    # auth_window = MainWindow()
    auth_window.show()
    
    # Ilovani ishga tushirish
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()