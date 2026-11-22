from app.rag import index_documents, retrieve_documents

# Index policy documents
count = index_documents()

print("Documents indexed:", count)

# Test retrieval
question = "What is the return policy?"

results = retrieve_documents(question)

print("\nRetrieved information:")

for result in results:
    print(result)
    print("--------------------")