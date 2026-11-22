
from sqlalchemy.orm import Session

from app.models import Product


class ProductSearchAgent:

    def search_products(self, requirements: dict, db: Session):

        # Extract requirements
        category = requirements.get("category")
        max_price = requirements.get("max_price")

        # Start database query
        query = db.query(Product)

        # Filter by category
        if category:
            query = query.filter(
                Product.category.ilike(f"%{category}%")
            )

        # Filter by maximum price
        if max_price is not None:
            query = query.filter(
                Product.price <= max_price
            )

        # Fetch matching products
        products = query.all()

        return products
