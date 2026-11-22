from app.rag import index_documents
from app.agents.customer_support_agent import CustomerSupportAgent

# Index policy documents first
index_documents()

# Create agent
agent = CustomerSupportAgent()

# Ask a question
question = "How many days do I have to return a product?"

result = agent.answer_question(question)

print("\nCustomer Question:")
print(result["question"])

print("\nRetrieved Documents:")
for doc in result["retrieved_documents"]:
    print(doc)

print("\nAI Answer:")
print(result["answer"])