from database import get_session, close_session
from database.models import User
from datetime import datetime


class UserRequest:
    """User operatsiyalari uchun klass"""
    
    @staticmethod
    def create_user(login: str, password: str) -> dict:
        """Yangi user yaratish"""
        session = get_session()
        try:
            # Login mavjudligini tekshirish
            existing_user = session.query(User).filter(User.login == login).first()
            if existing_user:
                return {"success": False, "message": "Bu login allaqachon ro'yxatdan o'tgan!"}
            
            # Yangi user yaratish
            new_user = User(
                login=login,
                password=password,
                status='active',
                joined_at=datetime.now()
            )
            session.add(new_user)
            session.commit()
            
            return {"success": True, "message": "User muvaffaqiyatli yaratildi!", "user_id": new_user.id}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def login_user(login: str, password: str) -> dict:
        """User login qilish"""
        session = get_session()
        try:
            # User izlash
            user = session.query(User).filter(User.login == login).first()
            
            if not user:
                return {"success": False, "message": "Bu login topilmadi!"}
            
            # Parol tekshirish
            if user.password != password:
                return {"success": False, "message": "Parol notog'ri!"}
            
            # User status tekshirish
            if user.status != 'active':
                return {"success": False, "message": "Bu user faol emas!"}
            
            return {
                "success": True,
                "message": "Login muvaffaqiyatli!",
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "status": user.status,
                    "joined_at": user.joined_at
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_all_users() -> list:
        """Barcha userlarni olish"""
        session = get_session()
        try:
            users = session.query(User).all()
            return users
        
        except Exception as e:
            print(f"Xato: {str(e)}")
            return []
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_user_by_id(user_id: int) -> dict:
        """ID bo'yicha user olish"""
        session = get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "message": "User topilmadi!"}
            
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "status": user.status,
                    "joined_at": user.joined_at
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def delete_user(user_id: int) -> dict:
        """Userni o'chirish"""
        session = get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "message": "User topilmadi!"}
            
            session.delete(user)
            session.commit()
            
            return {"success": True, "message": "User o'chirildi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def update_user_status(user_id: int, status: str) -> dict:
        """User statusini o'zgartirish"""
        session = get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "message": "User topilmadi!"}
            
            if status not in ['active', 'inactive']:
                return {"success": False, "message": "Status notog'ri!"}
            
            user.status = status
            session.commit()
            
            return {"success": True, "message": f"User status '{status}' ga o'zgartirildi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> dict:
        """Parol o'zgartirish"""
        session = get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "message": "User topilmadi!"}
            
            if user.password != old_password:
                return {"success": False, "message": "Eski parol notog'ri!"}
            
            user.password = new_password
            session.commit()
            
            return {"success": True, "message": "Parol o'zgartirildi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)

