# ANT: ACO-based Truck Optimization Service

This project implements an Ant Colony Optimization (ACO) algorithm wrapped in a FastAPI service to assign trucks to composite orders with minimal idle time, minimal empty travel, and smart routing.

## 🚀 Features
- Lean mode: assigns one composite order per truck
- Multi-criteria scoring (distance, idle time, priority, delivery risk, utilization)
- FastAPI-based REST API with `/optimize` endpoint

## 📦 Installation

```bash
# Clone this repo
git clone https://github.com/soubhik-sen/ANT.git
cd ANT

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # or source venv/bin/activate (Linux/Mac)

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Run the API

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## 📬 Sample API Request (POST /optimize)
```json
{
  "trucks": [
    {
      "id": "T1",
      "location": [23.75, 90.40],
      "free_from": "2025-04-07T09:00:00",
      "capacity": 100.0
    }
  ],
  "orders": [
    {
      "id": "O1",
      "first_stop": [23.76, 90.43],
      "last_stop": [23.85, 90.50],
      "time_window": ["2025-04-07T10:00:00", "2025-04-07T11:30:00"],
      "delivery_deadline": "2025-04-07T12:00:00",
      "priority": 2.0,
      "load_size": 60.0
    }
  ],
  "iterations": 10
}
```

## 📄 License
MIT License
