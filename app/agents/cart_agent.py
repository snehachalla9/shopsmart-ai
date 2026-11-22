
from sqlalchemy.orm import Session

from app.models import Product, CartItem


class CartAgent:

    def add_to_cart(self, product_id: int, quantity: int, db: Session):

        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            return {"message": "Product not found"}

        if quantity <= 0:
            return {"message": "Quantity must be greater than zero"}

        if product.stock < quantity:
            return {"message": "Insufficient stock"}

        cart_item = db.query(CartItem).filter(
            CartItem.product_id == product_id
        ).first()

        if cart_item:
            if product.stock < cart_item.quantity + quantity:
                return {"message": "Insufficient stock"}

            cart_item.quantity += quantity

        else:
            cart_item = CartItem(
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)

        db.commit()

        return {"message": "Product added to cart successfully"}

    def view_cart(self, db: Session):

        items = db.query(CartItem).all()

        result = []
        grand_total = 0

        for item in items:

            total = item.product.price * item.quantity
            grand_total += total

            result.append({
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price,
                "total": total
            })

        return {
            "items": result,
            "grand_total": grand_total
        }
    
    def update_quantity(self, product_id: int, quantity: int, db: Session):

        if quantity <= 0:
            return {"message": "Quantity must be greater than zero"}

        cart_item = db.query(CartItem).filter(
            CartItem.product_id == product_id
        ).first()

        if not cart_item:
            return {"message": "Product not found in cart"}

        if cart_item.product.stock < quantity:
            return {"message": "Insufficient stock"}

        cart_item.quantity = quantity

        db.commit()

        return {"message": "Cart quantity updated successfully"}

    def remove_from_cart(self, product_id: int, db: Session):

        cart_item = db.query(CartItem).filter(
            CartItem.product_id == product_id
        ).first()

        if not cart_item:
            return {"message": "Product not found in cart"}

        db.delete(cart_item)
        db.commit()

        return {"message": "Product removed from cart successfully"}
