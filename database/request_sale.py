from database import get_session, close_session
from database.models import Sale
from datetime import datetime


class SaleRequest:
    """Savdo operatsiyalari uchun klass"""
    
    @staticmethod
    def create_sale(user_id: int, product_id: int, quantity: int, price: float, 
                   total: float, discount: float, payment_method: str) -> dict:
        """Yangi savdoni yaratish"""
        session = get_session()
        try:
            new_sale = Sale(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                price=price,
                total=total,
                discount=discount,
                payment_method=payment_method,
                created_at=datetime.now()
            )
            session.add(new_sale)
            session.commit()
            
            return {"success": True, "message": "Savdo muvaffaqiyatli saqlandi!", "sale_id": new_sale.id}
        
        except Exception as e:
            session.rollback()
            return {"success": False, "message": f"Xato: {str(e)}"}
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_all_sales() -> list:
        """Barcha savdolarni olish"""
        session = get_session()
        try:
            sales = session.query(Sale).all()
            return sales
        
        except Exception as e:
            print(f"Xato: {str(e)}")
            return []
        
        finally:
            close_session(session)
    
    @staticmethod
    def get_sales_by_date(start_date, end_date) -> list:
        """Sana bo'yicha savdolarni olish"""
        session = get_session()
        try:
            sales = session.query(Sale).filter(
                Sale.saled_at >= start_date,
                Sale.saled_at <= end_date
            ).all()
            return sales
        
        except Exception as e:
            print(f"Xato: {str(e)}")
            return []
        
        finally:
            close_session(session)