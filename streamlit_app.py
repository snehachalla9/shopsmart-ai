
import streamlit as st
import requests

st.set_page_config(
    page_title="ShopSmart AI",
    page_icon="🛍️",
    layout="centered"
)

API_URL = "http://127.0.0.1:8000/chat/"

def format_response(agent, answer):
    """Convert agent JSON results into readable shopping responses."""

    if not isinstance(answer, dict):
        return str(answer)

    # Product Search
    if agent == "product_search":
        products = answer.get("products", [])

        if not products:
            return "Sorry! I couldn't find products matching your requirements."

        text = "Here are the products I found for you:\n\n"

        for p in products:
            text += (
                f"### {p['name']}\n"
                f"- Price: ₹{p['price']:,.0f}\n"
                f"- Category: {p['category']}\n"
                f"- Description: {p.get('description', 'Not available')}\n\n"
            )

        return text

    # Recommendation
    if agent == "recommendation":
        products = answer.get("recommendations", [])

        if not products:
            return "I couldn't find suitable recommendations."

        text = "Here are my recommendations for you:\n\n"

        for p in products:
            text += (
                f"### {p['name']}\n"
                f"- Price: ₹{p['price']:,.0f}\n"
                f"- Match score: {p['score']}\n"
                f"- Reason: {p['reason']}\n\n"
            )

        return text

    # Product Comparison
    if agent == "comparison":
        if "product_1" in answer and "product_2" in answer:
            p1 = answer["product_1"]
            p2 = answer["product_2"]

            return (
                f"## Product Comparison\n\n"
                f"| Feature | {p1['name']} | {p2['name']} |\n"
                f"|---|---:|---:|\n"
                f"| Price | ₹{p1['price']:,.0f} | ₹{p2['price']:,.0f} |\n"
                f"| Category | {p1['category']} | {p2['category']} |\n\n"
                f"**Cheaper product:** {answer['cheaper_product']}\n\n"
                f"**Price difference:** ₹{answer['price_difference']:,.0f}"
            )

    # Shopping Cart
    if agent == "cart":
        items = answer.get("items")

        if items is not None:
            if not items:
                return "Your shopping cart is currently empty."

            text = "## Your Shopping Cart\n\n"

            for item in items:
                text += (
                    f"- **{item['product']}** — "
                    f"Quantity: {item['quantity']}, "
                    f"Price: ₹{item['price']:,.0f}, "
                    f"Total: ₹{item['total']:,.0f}\n"
                )

            text += f"\n**Grand Total: ₹{answer['grand_total']:,.0f}**"
            return text

        return answer.get("message", str(answer))

    # Order Tracking
    if agent == "order_tracking":
        if "order_id" in answer:
            return (
                f"## Order Details\n\n"
                f"- Order ID: {answer['order_id']}\n"
                f"- Customer: {answer['customer_name']}\n"
                f"- Status: **{answer['status']}**\n"
                f"- Total: ₹{answer['total_amount']:,.0f}"
            )

        return answer.get("message", str(answer))

    # Customer Support
    if agent == "customer_support":
        return answer.get("answer", str(answer))

    return answer.get("message", str(answer))


st.title("🛍️ ShopSmart AI")
st.caption("Your intelligent multi-agent shopping assistant")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Customer input
user_input = st.chat_input("What are you looking for?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("ShopSmart AI is thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input},
                    timeout=90
                )

                response.raise_for_status()
                result = response.json()

                agent = result.get("selected_agent", "unknown")
                answer = result.get("response", {})

                st.caption(
                    f"Handled by: {agent.replace('_', ' ').title()}"
                )

                display_text = format_response(agent, answer)
                st.markdown(display_text)

            except requests.exceptions.RequestException as error:
                display_text = f"Backend connection error: {error}"
                st.error(display_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": display_text
            })

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
