from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
from models import Truck, CompositeOrder
from core import ACO

app = FastAPI(title="ACO Truck Assignment API")

class OptimizationRequest(BaseModel):
    trucks: List[Truck]
    orders: List[CompositeOrder]
    iterations: int = 10
    W1: float = 1.0
    W2: float = 1.0
    W3: float = -1.0
    W4: float = 1.0
    W5: float = -1.0

class OptimizationResponse(BaseModel):
    assignment: List[Tuple[str, str]]
    total_score: float

@app.post("/optimize", response_model=OptimizationResponse)
def optimize(request: OptimizationRequest):
    optimizer = ACO(
        trucks=request.trucks,
        orders=request.orders,
        iterations=request.iterations,
        W1=request.W1,
        W2=request.W2,
        W3=request.W3,
        W4=request.W4,
        W5=request.W5
    )
    assignment, score = optimizer.run()
    return OptimizationResponse(assignment=assignment, total_score=score)
