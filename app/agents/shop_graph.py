
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from app.llm import extract_shopping_requirements
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.product_search_agent import ProductSearchAgent
from app.agents.recommendation_agent import RecommendationAgent
import re
from app.agents.comparison_agent import ComparisonAgent
from app.models import Product
from app.agents.cart_agent import CartAgent
from app.agents.order_tracking_agent import OrderTrackingAgent
from app.models import Order
from app.llm import client,extract_shopping_requirements
from app.agents.customer_support_agent import CustomerSupportAgent


# Shared workflow state
class ShopState(TypedDict):
    message: str
    intent: str
    response: Any
    db: Any


# Initialize agents
supervisor = SupervisorAgent()
product_agent = ProductSearchAgent()
recommendation_agent = RecommendationAgent()
comparison_agent = ComparisonAgent()
cart_agent = CartAgent()
order_agent = OrderTrackingAgent()
support_agent = CustomerSupportAgent()


# Supervisor node
def supervisor_node(state: ShopState):

    intent = supervisor.classify_intent(state["message"])

    return {"intent": intent}


# Actual Product Search node
def product_search_node(state: ShopState):

    requirements = extract_shopping_requirements(
        state["message"]
    )

    products = product_agent.search_products(
        requirements,
        state["db"]
    )

    result = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "description": p.description
        }
        for p in products
    ]

    return {
        "response": {
            "requirements": requirements,
            "products": result
        }
    }


# Actual Recommendation node
def recommendation_node(state: ShopState):

    requirements = extract_shopping_requirements(
        state["message"]
    )

    products = product_agent.search_products(
        requirements,
        state["db"]
    )

    recommendations = recommendation_agent.recommend_products(
        products,
        requirements.get("purpose")
    )

    result = [
        {
            "id": item["product"].id,
            "name": item["product"].name,
            "category": item["product"].category,
            "price": item["product"].price,
            "score": item["score"],
            "reason": item["reason"]
        }
        for item in recommendations
    ]

    return {
        "response": {
            "requirements": requirements,
            "recommendations": result
        }
    }


# Temporary placeholder nodes for remaining agents
def comparison_node(state: ShopState):
    message = state["message"]

    # Extract product IDs from the customer's message
    product_ids = re.findall(r'\d+', message)

    if len(product_ids) < 2:
        return {
            "response": {
                "message": "Please provide two product IDs to compare.",
                "example": "Compare product 2 and product 3"
            }
        }

    product_id_1 = int(product_ids[0])
    product_id_2 = int(product_ids[1])

    db = state["db"]

    product1 = db.query(Product).filter(
        Product.id == product_id_1
    ).first()

    product2 = db.query(Product).filter(
        Product.id == product_id_2
    ).first()

    if not product1 or not product2:
        return {
            "response": {
                "message": "One or both products were not found."
            }
        }

    result = comparison_agent.compare_products(
        [product1, product2]
    )

    return {"response": result}


def cart_node(state: ShopState):
    message = state["message"]
    db = state["db"]

    # Extract cart operation and product details
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
                Extract the cart operation from the user message.

                Return ONLY valid JSON with:
                action, product_name, quantity

                action must be one of:
                add, view, update, remove

                product_name must be a string or null.
                quantity must be an integer or null.
                Do not invent missing information.
                """
            },
            {"role": "user", "content": message}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    import json
    details = json.loads(response.choices[0].message.content)

    action = details.get("action")
    product_name = details.get("product_name")
    quantity = details.get("quantity") or 1

    if action == "view":
        result = cart_agent.view_cart(db)

    elif action in ["add", "update", "remove"]:
        if not product_name:
            return {"response": "Please specify the product name."}

        product = db.query(Product).filter(
            Product.name.ilike(f"%{product_name}%")
        ).first()

        if not product:
            return {"response": "Product not found."}

        if action == "add":
            result = cart_agent.add_to_cart(
                product.id, quantity, db
            )

        elif action == "update":
            result = cart_agent.update_quantity(
                product.id, quantity, db
            )

        else:
            result = cart_agent.remove_from_cart(
                product.id, db
            )

    else:
        result = {
            "message": "I couldn't understand the cart operation."
        }

    return {"response": result}

def order_tracking_node(state: ShopState):
    import json

    message = state["message"]
    db = state["db"]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
                Extract order information from the user's message.

                Return ONLY valid JSON with:
                action, order_id, status

                action must be:
                track or update

                order_id must be an integer or null.
                status must be a string or null.

                Do not invent missing information.
                """
            },
            {"role": "user", "content": message}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    details = json.loads(response.choices[0].message.content)

    action = details.get("action")
    order_id = details.get("order_id")
    status = details.get("status")

    if not order_id:
        return {
            "response": "Please provide your order ID."
        }

    if action == "track":
        result = order_agent.track_order(order_id, db)

    elif action == "update":
        if not status:
            return {
                "response": "Please provide the new order status."
            }

        result = order_agent.update_order_status(
            order_id, status.strip().title(), db
        )

    else:
        result = {
            "message": "I couldn't understand your order request."
        }

    return {"response": result}

def customer_support_node(state: ShopState):
    message = state["message"]

    result = support_agent.answer_question(message)

    return {"response": result}


# Routing function
def route_request(state: ShopState):
    return state["intent"]


# Build workflow
workflow = StateGraph(ShopState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("product_search", product_search_node)
workflow.add_node("recommendation", recommendation_node)
workflow.add_node("comparison", comparison_node)
workflow.add_node("cart", cart_node)
workflow.add_node("order_tracking", order_tracking_node)
workflow.add_node("customer_support", customer_support_node)

workflow.add_edge(START, "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    route_request,
    {
        "product_search": "product_search",
        "recommendation": "recommendation",
        "comparison": "comparison",
        "cart": "cart",
        "order_tracking": "order_tracking",
        "customer_support": "customer_support"
    }
)

workflow.add_edge("product_search", END)
workflow.add_edge("recommendation", END)
workflow.add_edge("comparison", END)
workflow.add_edge("cart", END)
workflow.add_edge("order_tracking", END)
workflow.add_edge("customer_support", END)

shop_graph = workflow.compile()


# Run workflow with a database session
def run_shop_graph(message: str, db):

    return shop_graph.invoke({
        "message": message,
        "intent": "",
        "response": "",
        "db": db
    })
