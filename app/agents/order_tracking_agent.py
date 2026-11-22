from sqlalchemy.orm import Session
from app.models import Order


class OrderTrackingAgent:

    def track_order(self, order_id: int, db: Session):

        order = db.query(Order).filter(
            Order.id == order_id
        ).first()

        if not order:
            return {"message": "Order not found"}

        return {
            "order_id": order.id,
            "customer_name": order.customer_name,
            "status": order.status,
            "total_amount": order.total_amount
        }
    def update_order_status(self, order_id: int, status: str, db: Session):
        order = db.query(Order).filter(
            Order.id == order_id
            ).first()
        if not order:
            return {"message": "Order not found"}
        allowed_statuses = ["Processing", "Shipped", "Delivered"]
        if status not in allowed_statuses:
            return {"message": "Invalid order status"}
        order.status = status
        db.commit()
        db.refresh(order)
        return {
            "message": "Order status updated successfully",
            "order_id": order.id,
            "status": order.status
            }