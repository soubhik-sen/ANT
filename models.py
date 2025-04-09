from pydantic import BaseModel
from typing import List, Tuple
from datetime import datetime

class Truck(BaseModel):
    id: str
    location: Tuple[float, float]
    free_from: datetime
    capacity: float = 100.0

class CompositeOrder(BaseModel):
    id: str
    first_stop: Tuple[float, float]
    last_stop: Tuple[float, float]
    time_window: Tuple[datetime, datetime]
    delivery_deadline: datetime
    priority: float = 1.0
    load_size: float = 50.0
