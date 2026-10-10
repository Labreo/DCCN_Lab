"""
Experiment 12 - Part 2: Distance Vector Routing (DVR) Protocol Simulation
Language: Python 3
Description:
    Simulates Distance Vector Routing using Bellman-Ford algorithm with periodic
    vector exchanges between direct neighbors until global convergence.
"""

class DistanceVectorRouter:
    def __init__(self, router_id: str, subnets: list[str]):
        self.router_id = router_id
        self.subnets = subnets
        self.neighbors = {}  # {neighbor_id: link_cost}
        self.routing_table = {}  # {dest_subnet: (cost, next_hop)}

        # Initialize directly connected subnets
        for s in self.subnets:
            self.routing_table[s] = (0, "Directly Connected")

    def add_neighbor(self, neighbor_id: str, cost: int):
        self.neighbors[neighbor_id] = cost

    def get_distance_vector(self) -> dict[str, int]:
        """Returns distance vector: {dest_subnet: cost}"""
        return {subnet: cost for subnet, (cost, _) in self.routing_table.items()}

    def update_from_neighbor(self, neighbor_id: str, neighbor_vector: dict[str, int]) -> bool:
        """
        Applies Bellman-Ford equation: D_x(y) = min_v { c(x,v) + D_v(y) }
        Returns True if any route changed.
        """
        changed = False
        link_cost = self.neighbors[neighbor_id]

        for dest_subnet, cost_from_neighbor in neighbor_vector.items():
            new_cost = link_cost + cost_from_neighbor
            
            if dest_subnet not in self.routing_table:
                self.routing_table[dest_subnet] = (new_cost, neighbor_id)
                changed = True
            else:
                curr_cost, curr_next_hop = self.routing_table[dest_subnet]
                if new_cost < curr_cost:
                    self.routing_table[dest_subnet] = (new_cost, neighbor_id)
                    changed = True
                elif curr_next_hop == neighbor_id and new_cost != curr_cost:
                    # Update if metric changed from current next-hop
                    self.routing_table[dest_subnet] = (new_cost, neighbor_id)
                    changed = True

        return changed

def run_distance_vector_demo():
    print("=" * 75)
    print("    DISTANCE VECTOR ROUTING (DVR) - BELLMAN-FORD SIMULATION")
    print("=" * 75)

    # Initialize Routers with Attached Subnets
    routers = {
        "A": DistanceVectorRouter("A", ["10.0.1.0/24"]),
        "B": DistanceVectorRouter("B", ["10.0.2.0/24"]),
        "C": DistanceVectorRouter("C", ["10.0.3.0/24"]),
        "D": DistanceVectorRouter("D", ["10.0.4.0/24"])
    }

    # Interconnect Neighbors (Topology)
    links = [
        ("A", "B", 1),
        ("B", "C", 3),
        ("A", "C", 7),
        ("C", "D", 2),
        ("B", "D", 8)
    ]

    for u, v, w in links:
        routers[u].add_neighbor(v, w)
        routers[v].add_neighbor(u, w)

    print("\n1. Initial State: Routers only know directly connected subnets.")
    iteration = 1
    converged = False

    while not converged:
        print(f"\n--- Exchange Iteration {iteration} ---")
        converged = True
        
        # Collect vectors
        vectors = {r_id: r.get_distance_vector() for r_id, r in routers.items()}

        # Exchange between neighbors
        for u, v, _ in links:
            if routers[u].update_from_neighbor(v, vectors[v]):
                converged = False
            if routers[v].update_from_neighbor(u, vectors[u]):
                converged = False

        if converged:
            print("  --> No route changes detected. Network has CONVERGED!")
            break
        else:
            print("  --> Route tables updated. Propagating updates...")
            iteration += 1

    print("\n2. Final Converged Routing Table for Router A:")
    print("-" * 65)
    print(f"{'Destination Subnet':<22} | {'Metric (Cost)':<14} | {'Next Hop'}")
    print("-" * 65)
    for subnet, (cost, next_hop) in sorted(routers["A"].routing_table.items()):
        print(f"{subnet:<22} | {cost:<14} | {next_hop}")
    print("-" * 65)
    print("SUCCESS: Distance Vector Routing converged in all routers!\n")

if __name__ == "__main__":
    run_distance_vector_demo()
