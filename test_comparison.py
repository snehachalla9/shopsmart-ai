
from app.database import SessionLocal
from app.models import Product
from app.agents.comparison_agent import ComparisonAgent

db = SessionLocal()

products = db.query(Product).filter(
    Product.category.ilike("%Mobile%")
).limit(2).all()

agent = ComparisonAgent()

result = agent.compare_products(products)

print(result)

db.close()
