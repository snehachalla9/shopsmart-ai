from app.llm import extract_shopping_requirements

message = "I need a mobile under 30000 for photography"

result = extract_shopping_requirements(message)

print(result)
print(type(result))