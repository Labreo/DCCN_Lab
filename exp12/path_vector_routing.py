"""
Experiment 12 - Part 3: Path Vector Routing (PVR) Protocol Simulation
Language: Python 3
Description:
    Simulates Path Vector Routing (BGP-style). Instead of just distance metrics,
    advertisements include the exact sequence of hops (Path Vector).
    Demonstrates:
      1. Explicit loop detection (rejecting paths containing own ID)
      2. Multi-hop Autonomous System / Router propagation
      3. Dynamic subnet reachability
"""

class PathVectorRouter:
    def __init__(self, as_id: str, subnets: list[str]):
        self.as_id = as_id
        self.subnets = subnets
        self.neighbors = []
        # Routing table: {dest_subnet: {"path": [AS_list], "next_hop": neighbor}}
        self.routing_table = {}

        for s in self.subnets:
            self.routing_table[s] = {"path": [self.as_id], "next_hop": "Local"}

    def add_peer(self, neighbor_id: str):
        if neighbor_id not in self.neighbors:
            self.neighbors.append(neighbor_id)

    def generate_advertisements(self) -> dict[str, list[str]]:
        """Generates path vector advertisements: {dest_subnet: [path]}"""
        return {subnet: data["path"] for subnet, data in self.routing_table.items()}

    def process_advertisement(self, neighbor_id: str, subnet: str, path: list[str]) -> bool:
        """
        Processes an incoming path vector update.
        Loop Detection Rule: If self.as_id is already in path, DISCARD update!
        """
        if self.as_id in path:
            print(f"  [LOOP DETECTED at {self.as_id}] Discarding advertisement for {subnet} via {path} (Contains {self.as_id})")
            return False

        extended_path = [self.as_id] + path
        path_len = len(extended_path)

        # Check if new route or shorter route
        if subnet not in self.routing_table:
            self.routing_table[subnet] = {"path": extended_path, "next_hop": neighbor_id}
            return True
        else:
            curr_path = self.routing_table[subnet]["path"]
            if path_len < len(curr_path):
                self.routing_table[subnet] = {"path": extended_path, "next_hop": neighbor_id}
                return True

        return False

def run_path_vector_demo():
    print("=" * 75)
    print("      PATH VECTOR ROUTING (PVR) - BGP-STYLE SIMULATION")
    print("=" * 75)

    # Autonomous Systems (AS100, AS200, AS300, AS400)
    routers = {
        "AS100": PathVectorRouter("AS100", ["172.16.1.0/24"]),
        "AS200": PathVectorRouter("AS200", ["172.16.2.0/24"]),
        "AS300": PathVectorRouter("AS300", ["172.16.3.0/24"]),
        "AS400": PathVectorRouter("AS400", ["172.16.4.0/24"])
    }

    # BGP Peering Topology: AS100 - AS200 - AS300 - AS400 - AS100 (Loop)
    peerings = [
        ("AS100", "AS200"),
        ("AS200", "AS300"),
        ("AS300", "AS400"),
        ("AS400", "AS100")
    ]

    for u, v in peerings:
        routers[u].add_peer(v)
        routers[v].add_peer(u)

    print("\n1. Propagating Path Vector Advertisements across BGP Autonomous Systems...")
    converged = False
    rounds = 1

    while not converged and rounds <= 5:
        print(f"\n--- BGP Update Exchange Round {rounds} ---")
        converged = True
        
        for u, v in peerings:
            # U sends to V
            u_advs = routers[u].generate_advertisements()
            for subnet, path in u_advs.items():
                if routers[v].process_advertisement(u, subnet, path):
                    converged = False

            # V sends to U
            v_advs = routers[v].generate_advertisements()
            for subnet, path in v_advs.items():
                if routers[u].process_advertisement(v, subnet, path):
                    converged = False

        rounds += 1

    print("\n2. Converged BGP Path Vector Routing Table for AS100:")
    print("-" * 75)
    print(f"{'Destination Subnet':<20} | {'Next Hop Peer':<15} | {'Autonomous System Path (AS-PATH)'}")
    print("-" * 75)
    for subnet, data in sorted(routers["AS100"].routing_table.items()):
        as_path_str = " -> ".join(data["path"])
        print(f"{subnet:<20} | {data['next_hop']:<15} | {as_path_str}")
    print("-" * 75)
    print("SUCCESS: Path Vector Routing eliminated all routing loops!\n")

if __name__ == "__main__":
    run_path_vector_demo()
