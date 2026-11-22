
class ComparisonAgent:

    def compare_products(self, products):

        if len(products) < 2:
            return {
                "message": "Please provide at least two products to compare."
            }

        product1 = products[0]
        product2 = products[1]

        if product1.price < product2.price:
            cheaper = product1.name
        elif product2.price < product1.price:
            cheaper = product2.name
        else:
            cheaper = "Both products have the same price"

        return {
            "product_1": {
                "name": product1.name,
                "price": product1.price,
                "category": product1.category,
                "description": product1.description
            },
            "product_2": {
                "name": product2.name,
                "price": product2.price,
                "category": product2.category,
                "description": product2.description
            },
            "cheaper_product": cheaper,
            "price_difference": abs(
                product1.price - product2.price
            )
        }
