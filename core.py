import math
from typing import List, Tuple
from models import Truck, CompositeOrder

# Distance calculator
def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ACO Optimizer class
class ACO:
    def __init__(self, trucks: List[Truck], orders: List[CompositeOrder],
                 W1=1.0, W2=1.0, W3=-1.0, W4=1.0, W5=-1.0,
                 iterations=10):
        self.trucks = trucks
        self.orders = orders
        self.iterations = iterations
        self.ants = len(trucks)
        self.pheromones = {(t.id, o.id): 1.0 for t in trucks for o in orders}
        self.W1 = W1
        self.W2 = W2
        self.W3 = W3
        self.W4 = W4
        self.W5 = W5

    def calculate_score(self, truck: Truck, order: CompositeOrder) -> float:
        empty_distance = haversine_distance(truck.location, order.first_stop)
        idle_time = max(0, (order.time_window[0] - truck.free_from).total_seconds() / 60)
        order_priority_score = order.priority

        delivery_end = order.time_window[1]
        deadline_buffer = max(0, (order.delivery_deadline - delivery_end).total_seconds() / 60)
        delivery_risk_penalty = 0 if deadline_buffer >= 0 else abs(deadline_buffer)

        utilization = min(order.load_size / truck.capacity, 1.0)

        score = (
            self.W1 * empty_distance +
            self.W2 * idle_time +
            self.W3 * order_priority_score +
            self.W4 * delivery_risk_penalty +
            self.W5 * utilization
        )
        return score

    def run(self) -> Tuple[List[Tuple[str, str]], float]:
        best_assignment = None
        best_score = float("inf")

        for _ in range(self.iterations):
            all_solutions = []

            for ant in range(self.ants):
                truck = self.trucks[ant]
                # available_orders = sorted(self.orders, key=lambda o: haversine_distance(truck.location, o.first_stop))
                sorted_orders = sorted(self.orders, key=lambda o: haversine_distance(truck.location, o.first_stop))
                top_n = sorted_orders[:5]
                random.shuffle(top_n)
                available_orders = top_n + sorted_orders[5:]
                assignment = []
                total_cost = 0

                for order in available_orders:
                    key = (truck.id, order.id)
                    pheromone = self.pheromones.get(key, 1.0)
                    heuristic = 1.0 / (self.calculate_score(truck, order) + 1e-5)
                    desirability = pheromone * heuristic
                    score = 1.0 / heuristic
                    assignment.append((truck.id, order.id))
                    total_cost += score
                    break

                all_solutions.append((assignment, total_cost))

            self.evaporate()
            for assignment, cost in all_solutions:
                if cost == 0: continue
                for pair in assignment:
                    self.pheromones[pair] += 1.0 / cost

            best_in_iter = min(all_solutions, key=lambda x: x[1])
            if best_in_iter[1] < best_score:
                best_assignment, best_score = best_in_iter

        return best_assignment, best_score

    def evaporate(self, evaporation_rate=0.1):
        for key in self.pheromones:
            self.pheromones[key] *= (1 - evaporation_rate)
