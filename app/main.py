from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.dependencies import get_db
from app.models import Product
from app.schemas import ChatRequest,ProductCreate, ProductResponse,OrderCreate
from app.llm import extract_shopping_requirements
from app.agents.product_search_agent import ProductSearchAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.comparison_agent import ComparisonAgent
from app.agents.cart_agent import CartAgent
from app.models import Order
from app.agents.order_tracking_agent import OrderTrackingAgent
from app.agents.customer_support_agent import CustomerSupportAgent
from app.agents.shop_graph import run_shop_graph

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShopSmart AI")
product_agent = ProductSearchAgent()
recommendation_agent = RecommendationAgent()
comparison_agent = ComparisonAgent()
cart_agent = CartAgent()
order_tracking_agent = OrderTrackingAgent()
customer_support_agent = CustomerSupportAgent()


@app.get("/")
def home():
    return {"message": "Welcome to ShopSmart AI"}


# 1. CREATE PRODUCT
@app.post("/products/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# 2. GET ALL PRODUCTS
@app.get("/products/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()

    return products


# 3. GET PRODUCT BY ID
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# 4. UPDATE PRODUCT
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_data: ProductCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


# 5. DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
@app.get("/search/")
def search_products(
    category: str = None,
    max_price: float = None,
    db: Session = Depends(get_db)
):

    query = db.query(Product)

    if category:
        query = query.filter(
            Product.category.ilike(f"%{category}%")
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    return query.all()

@app.post("/ai-search/")
def ai_search(message: str, db: Session = Depends(get_db)):

    # Step 1: Understand user request
    requirements = extract_shopping_requirements(message)

    # Step 2: Find matching products
    products = product_agent.search_products(requirements, db)

    # Step 3: Rank products based on purpose
    recommendations = recommendation_agent.recommend_products(
        products,
        requirements.get("purpose")
    )

    # Step 4: Return recommendations
    return {
        "requirements": requirements,
        "recommendations": [
            {
                "id": item["product"].id,
                "name": item["product"].name,
                "category": item["product"].category,
                "price": item["product"].price,
                "description": item["product"].description,
                "score": item["score"],
                "reason": item["reason"]
            }
            for item in recommendations
        ]
    }

@app.get("/compare/")
def compare_products(
    product_id_1: int,
    product_id_2: int,
    db: Session = Depends(get_db)
):

    # Fetch first product
    product1 = db.query(Product).filter(
        Product.id == product_id_1
    ).first()

    # Fetch second product
    product2 = db.query(Product).filter(
        Product.id == product_id_2
    ).first()

    # Check whether products exist
    if not product1 or not product2:
        raise HTTPException(
            status_code=404,
            detail="One or both products not found"
        )

    # Compare products
    result = comparison_agent.compare_products(
        [product1, product2]
    )

    return result
@app.post("/cart/add/")
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    result = cart_agent.add_to_cart(
        product_id,
        quantity,
        db
    )

    if result.get("message") == "Product not found":
        raise HTTPException(status_code=404, detail=result["message"])

    if result.get("message") != "Product added to cart successfully":
        raise HTTPException(status_code=400, detail=result["message"])

    return result
@app.get("/cart/")
def view_cart(db: Session = Depends(get_db)):
    return cart_agent.view_cart(db)

@app.put("/cart/update/")
def update_cart(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    result = cart_agent.update_quantity(
        product_id,
        quantity,
        db
    )

    if result["message"] == "Product not found in cart":
        raise HTTPException(status_code=404, detail=result["message"])

    if result["message"] != "Cart quantity updated successfully":
        raise HTTPException(status_code=400, detail=result["message"])

    return result

@app.delete("/cart/remove/")
def remove_cart_item(
    product_id: int,
    db: Session = Depends(get_db)
):
    result = cart_agent.remove_from_cart(product_id, db)

    if result["message"] == "Product not found in cart":
        raise HTTPException(status_code=404, detail=result["message"])

    return result
@app.post("/orders/")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    new_order = Order(
        customer_name=order.customer_name,
        total_amount=order.total_amount,
        status="Processing"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order
@app.get("/orders/{order_id}")
def track_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    result = order_tracking_agent.track_order(order_id, db)

    if result.get("message") == "Order not found":
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result
@app.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    result = order_tracking_agent.update_order_status(
        order_id, status, db
    )

    if result.get("message") == "Order not found":
        raise HTTPException(status_code=404, detail=result["message"])

    if result.get("message") == "Invalid order status":
        raise HTTPException(status_code=400, detail=result["message"])

    return result
@app.post("/support/")
def customer_support(message: str):

    result = customer_support_agent.answer_question(message)

    return result
@app.post("/chat/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    result = run_shop_graph(request.message, db)

    return {
        "user_message": request.message,
        "selected_agent": result["intent"],
        "response": result["response"]
    }

