from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    description: str
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str
    stock: int

    class Config:
        from_attributes = True
class OrderCreate(BaseModel):
    customer_name: str
    total_amount: float


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    total_amount: float

    class Config:
        from_attributes = True
class ChatRequest(BaseModel):
    message: str