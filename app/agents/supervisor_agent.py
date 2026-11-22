
import json

from app.llm import client


class SupervisorAgent:

    def classify_intent(self, message: str):

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are the Supervisor of an e-commerce AI system.

                    Identify the user's intent.

                    Choose exactly one category:
                    product_search
                    recommendation
                    comparison
                    cart
                    order_tracking
                    customer_support

                    Return ONLY valid JSON:
                    {
                        "intent": "category"
                    }
                    """
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = json.loads(
            response.choices[0].message.content
        )

        allowed_intents = {
            "product_search",
            "recommendation",
            "comparison",
            "cart",
            "order_tracking",
            "customer_support"
        }

        intent = result.get("intent")

        if intent not in allowed_intents:
            intent = "customer_support"

        return intent
