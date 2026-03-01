from database import get_session, close_session
from database.models import Product
from datetime import datetime


class ProductRequest:
    """Mahsulot operatsiyalari uchun klass"""
    
    @staticmethod
    def create_product(name: str, barcode: str, price: float, quantity: int, status: str = 'active') -> dict:
        """Yangi mahsulot yaratish"""
        session = get_session()
        try:
            # Barcode mavjudligini tekshirish
            existing_product = session.query(Product).filter(Product.barcode == barcode).first()
            if existing_product:
                return {"success": False, "message": "Bu barcode allaqachon mavjud!"}
            
            # Yangi mahsulot yaratish
            new_product = Product(
                name=name,
                barcode=barcode,
                price=price,
                quantity=quantity,
                status=status,
                created_at=datetime.now()
            )
            session.add(new_product)
            session.commit()
            
            return {"success": True, "message": "Mahsulot muvaffaqiyatli yaratildi!", "product_id": new_product.id}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_all_products() -> list:
        """Barcha mahsulotlarni olish"""
        session = get_session()
        try:
            products = session.query(Product).all()
            return products
        
        except Exception as e:
            print(f"Xato: {str(e)}")
            return []
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_product_by_id(product_id: int) -> dict:
        """ID bo'yicha mahsulot olish"""
        session = get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return {"success": False, "message": "Mahsulot topilmadi!"}
            
            return {
                "success": True,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "barcode": product.barcode,
                    "price": product.price,
                    "quantity": product.quantity,
                    "status": product.status,
                    "created_at": product.created_at
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_product_by_barcode(barcode: str) -> dict:
        """Barcode bo'yicha mahsulot olish"""
        session = get_session()
        try:
            product = session.query(Product).filter(Product.barcode == barcode).first()
            
            if not product:
                return {"success": False, "message": "Mahsulot topilmadi!"}
            
            return {
                "success": True,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "barcode": product.barcode,
                    "price": product.price,
                    "quantity": product.quantity,
                    "status": product.status,
                    "created_at": product.created_at
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def update_product(product_id: int, name: str, barcode: str, price: float, quantity: int, status: str) -> dict:
        """Mahsulot yangilash"""
        session = get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return {"success": False, "message": "Mahsulot topilmadi!"}
            
            # Barcode o'zgartirilsa, yangi barcode mavjudligini tekshirish
            if product.barcode != barcode:
                existing = session.query(Product).filter(Product.barcode == barcode).first()
                if existing:
                    return {"success": False, "message": "Bu barcode allaqachon mavjud!"}
            
            product.name = name
            product.barcode = barcode
            product.price = price
            product.quantity = quantity
            product.status = status
            
            session.commit()
            
            return {"success": True, "message": "Mahsulot muvaffaqiyatli yangilandi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def delete_product(product_id: int) -> dict:
        """Mahsulotni o'chirish"""
        session = get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return {"success": False, "message": "Mahsulot topilmadi!"}
            
            session.delete(product)
            session.commit()
            
            return {"success": True, "message": "Mahsulot muvaffaqiyatli o'chirildi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def update_product_quantity(product_id: int, new_quantity: int) -> dict:
        """Mahsulot miqdorini yangilash"""
        session = get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return {"success": False, "message": "Mahsulot topilmadi!"}
            
            product.quantity = new_quantity
            session.commit()
            
            return {"success": True, "message": "Miqdor yangilandi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def decrease_quantity(product_id: int, amount: int) -> dict:
        """Mahsulot miqdorini kamaytirish (savdoda ishlatish)"""
        session = get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                return {"success": False, "message": "Mahsulot topilmadi!"}
            
            if product.quantity < amount:
                return {"success": False, "message": f"Yetarli miqdor yo'q! Mavjud: {product.quantity}"}
            
            product.quantity -= amount
            session.commit()
            
            return {"success": True, "message": "Miqdor kamaytildi!"}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)

    @staticmethod
    def generate_barcode() -> str:
        """Avtomatik barcode generate qilish"""
        session = get_session()
        try:
            # Oxirgi product ni olish
            last_product = session.query(Product).order_by(Product.id.desc()).first()
            
            if not last_product:
                # Birinchi product
                new_barcode = "1001"
            else:
                # Oxirgi barcode dan +1
                try:
                    last_code = int(last_product.barcode)
                    new_barcode = str(last_code + 1)
                except:
                    new_barcode = "1001"
            
            return new_barcode
        
        except Exception as e:
            print(f"Xato: {str(e)}")
            return "1001"
        
        finally:
            close_session(session)