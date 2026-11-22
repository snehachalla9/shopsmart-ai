
from app.agents.shop_graph import run_shop_graph
from app.database import SessionLocal


db = SessionLocal()

try:
    messages = [
        "Show me mobiles under 30000",
        "Suggest a mobile under 30000 for photography"
    ]

    for message in messages:

        result = run_shop_graph(message, db)

        print("\nCustomer:", message)
        print("Selected Agent:", result["intent"])
        print("Actual Result:", result["response"])
        print("-" * 60)

finally:
    db.close()
