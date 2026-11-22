# 🛍️ ShopSmart AI – Multi-Agent E-Commerce Assistant

ShopSmart AI is an AI-powered e-commerce shopping assistant that helps customers search for products, get personalized recommendations, compare products, manage shopping carts, track orders, and ask questions about store policies using natural language.

The project uses a multi-agent architecture powered by **LangGraph and Groq**, with FastAPI as the backend and Streamlit as the frontend.

## 🚀 Features

- **Product Search:** Find products based on category and budget.
- **Product Recommendations:** Recommend products based on user requirements and purpose.
- **Product Comparison:** Compare products and identify price differences.
- **Cart Management:** Add, view, update, and remove products from the shopping cart.
- **Order Tracking:** Retrieve order information and manage order statuses.
- **AI Customer Support:** Answer store-policy questions using Retrieval-Augmented Generation (RAG).
- **Multi-Agent Workflow:** Route customer requests to specialized agents using a Supervisor Agent and LangGraph.
- **Conversational Interface:** Interact with the application through a Streamlit chat interface.

## 🏗️ Architecture

```text
                  CUSTOMER
                     |
                     v
              STREAMLIT FRONTEND
                     |
                     v
               FASTAPI BACKEND
                     |
                     v
              LANGGRAPH WORKFLOW
                     |
                     v
               SUPERVISOR AGENT
                     |
          Intent Classification
                     |
        +------------+-------------+
        |            |             |
        v            v             v
   Product Search Recommendation Comparison
        |            |             |
        +------------+-------------+
                     |
        +------------+-------------+
        |            |             |
        v            v             v
      Cart      Order Tracking  Customer Support
        |            |             |
        v            v             v
      SQLITE       SQLITE       RAG PIPELINE
                                  |
                             CHROMADB
                                  |
                           RETRIEVED CONTEXT
                                  |
                               GROQ LLM
                                  |
                                  v
                            FINAL RESPONSE
                                  |
                                  v
                             STREAMLIT
```

## 🧠 AI Agents

| Agent | Responsibility |
|---|---|
| Supervisor Agent | Identifies user intent and selects the appropriate agent |
| Product Search Agent | Searches products using category and price filters |
| Recommendation Agent | Ranks products using purpose-related keyword matching |
| Comparison Agent | Compares product details and prices |
| Cart Agent | Manages cart operations |
| Order Tracking Agent | Retrieves and updates order statuses |
| Customer Support Agent | Answers questions using store-policy documents and RAG |

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend and chat interface |
| FastAPI | Backend API framework |
| LangGraph | Multi-agent orchestration |
| Groq | LLM API access |
| GPT-OSS-20B | Language model used by the application |
| SQLite | Relational database |
| SQLAlchemy | Database ORM |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| Pydantic | Data validation |

## 📁 Project Structure

```text
shopsmart-ai/
│
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── product_search_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── comparison_agent.py
│   │   ├── cart_agent.py
│   │   ├── order_tracking_agent.py
│   │   ├── customer_support_agent.py
│   │   ├── supervisor_agent.py
│   │   └── shop_graph.py
│   │
│   ├── data/
│   │   └── store_policies.txt
│   │
│   ├── main.py
│   ├── llm.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── dependencies.py
│   └── rag.py
│
├── streamlit_app.py
├── requirements.txt
├── .env
├── .gitignore
│
└── test_*.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/snehachalla9/shopsmart-ai.git
cd shopsmart-ai
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

**Important:** Never commit your `.env` file or expose your API key.

### 5. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit frontend

Open another terminal:

```bash
cd shopsmart-ai
source venv/bin/activate
streamlit run streamlit_app.py
```

The Streamlit application will open in your browser.

## 💬 Example User Queries

**Product Search**

```text
Show me mobiles under 30000
```

**Product Recommendation**

```text
Recommend a mobile under 30000 for photography
```

**Product Comparison**

```text
Compare Samsung Galaxy and OnePlus Mobile
```

**Cart Management**

```text
Add Samsung Galaxy to my cart
Show my cart
```

**Order Tracking**

```text
Track my order 1
```

**Customer Support**

```text
What is your return policy?
```

## 📚 RAG Workflow

The Customer Support Agent uses Retrieval-Augmented Generation to answer questions using store-policy documents.

1. Load the store policy document.
2. Split the document into smaller text chunks.
3. Generate embeddings using Sentence Transformers.
4. Store document chunks and embeddings in ChromaDB.
5. Convert the customer's question into an embedding.
6. Retrieve relevant policy chunks using similarity search.
7. Pass the retrieved context and question to the Groq LLM.
8. Generate a context-based response.

## 🔌 API Endpoints

The FastAPI backend provides endpoints for:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Welcome endpoint |
| `/products/` | GET | Retrieve products |
| `/products/` | POST | Create a product |
| `/products/{product_id}` | GET | Retrieve a product |
| `/products/{product_id}` | PUT | Update a product |
| `/products/{product_id}` | DELETE | Delete a product |
| `/search/` | GET | Search products |
| `/ai-search/` | POST | AI-based product search |
| `/compare/` | GET | Compare products |
| `/cart/add/` | POST | Add an item to cart |
| `/cart/` | GET | View cart |
| `/cart/update/` | PUT | Update cart quantity |
| `/cart/remove/` | DELETE | Remove an item |
| `/orders/` | POST | Create an order |
| `/orders/{order_id}` | GET | Track an order |
| `/orders/{order_id}/status` | PUT | Update order status |
| `/support/` | POST | Ask customer support |
| `/chat/` | POST | Unified multi-agent chat endpoint |

## 🔐 Security and Configuration

- Store API keys in environment variables.
- Keep `.env` out of version control.
- Keep virtual environments and local databases out of Git.
- Configure production secrets separately from development settings.

## 🛣️ Future Improvements

- Product images and rich product cards.
- Semantic product recommendations using embeddings.
- Customer authentication and personalized carts.
- Secure checkout and payment integration.
- Improved inventory and stock management.
- Docker-based deployment.
- Cloud deployment and monitoring.
- Automated tests and CI/CD pipeline.

## 👩‍💻 Author

**Sneha Challa**

GitHub: [@snehachalla9](https://github.com/snehachalla9)

## ⭐ Support

If you find this project interesting, consider giving the repository a star!
