from app.agents.supervisor_agent import SupervisorAgent

supervisor = SupervisorAgent()

messages = [
    "Show me mobiles under 30000",
    "Suggest a laptop for programming",
    "Compare Samsung and OnePlus",
    "Add Samsung to my cart",
    "Where is my order?",
    "What is your refund policy?"
]

for message in messages:

    intent = supervisor.classify_intent(message)

    print("\nCustomer:", message)
    print("Selected Agent:", intent)