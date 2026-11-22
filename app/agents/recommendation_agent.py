
class RecommendationAgent:

    # Keywords associated with different shopping purposes
    purpose_keywords = {
        "photography": [
            "camera",
            "photography",
            "photo",
            "megapixel",
            "mp"
        ],

        "gaming": [
            "gaming",
            "game",
            "gpu",
            "graphics",
            "refresh rate"
        ],

        "programming": [
            "programming",
            "developer",
            "coding",
            "processor",
            "ram",
            "ssd"
        ]
    }

    def recommend_products(self, products, purpose):

        if not purpose:
            return [
                {
                    "product": p,
                    "score": 0,
                    "reason": "No specific purpose provided"
                }
                for p in products
            ]

        purpose = purpose.lower()

        # Find relevant keywords
        keywords = []

        for category, words in self.purpose_keywords.items():
            if category in purpose:
                keywords = words
                break

        recommendations = []

        for product in products:

            # Combine product information
            product_text = (
                f"{product.name} {product.description}"
            ).lower()

            # Calculate matching keyword score
            score = sum(
                1 for word in keywords
                if word in product_text
            )

            if score > 0:
                reason = "Matches your purpose: " + purpose
            else:
                reason = "No specific matching features found"

            recommendations.append({
                "product": product,
                "score": score,
                "reason": reason
            })

        # Highest score first
        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return recommendations
