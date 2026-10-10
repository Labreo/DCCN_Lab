"""
Experiment 12 - Part 1: Link State Routing (LSR) Protocol Simulation
Language: Python 3
Description:
    Simulates Link State Routing using Dijkstra's Shortest Path First (SPF) algorithm.
    Each router maintains:
      - Link State Database (LSDB) of the entire topology
      - Attached Dynamic IP subnets
      - SPF calculation to compute the best route to all remote subnets
"""

import heapq

class LinkStateRouter:
    def __init__(self, router_id: str, subnets: list[str]):
        self.router_id = router_id
        self.subnets = subnets  # Directly attached subnets
        self.lsdb = {}  # Link State Database: {node: {neighbor: cost}}
        self.subnet_map = {}  # {node: [subnets]}

    def update_lsdb(self, topology: dict[str, dict[str, int]], subnet_map: dict[str, list[str]]):
        """Receives LSAs and synchronizes the Link State Database (LSDB)."""
        self.lsdb = topology
        self.subnet_map = subnet_map

    def compute_spf_routing_table(self) -> list[dict]:
        """
        Runs Dijkstra's Algorithm to compute shortest path and next-hop
        for all reachable dynamic IP subnets.
        """
        distances = {node: float('inf') for node in self.lsdb}
        previous_hop = {node: None for node in self.lsdb}
        distances[self.router_id] = 0
        
        # Priority queue: (cost, node)
        pq = [(0, self.router_id)]

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            if curr_dist > distances[curr_node]:
                continue

            for neighbor, weight in self.lsdb.get(curr_node, {}).items():
                new_dist = curr_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous_hop[neighbor] = curr_node
                    heapq.heappush(pq, (new_dist, neighbor))

        # Build Routing Table
        routing_table = []
        
        # 1. Directly attached subnets
        for s in self.subnets:
            routing_table.append({
                "Destination Subnet": s,
                "Cost": 0,
                "Next Hop": "Directly Connected",
                "Interface": f"LAN-{self.router_id}"
            })

        # 2. Remote subnets via shortest path
        for dest_node, subnets in self.subnet_map.items():
            if dest_node == self.router_id:
                continue
            if distances[dest_node] == float('inf'):
                continue

            # Trace next-hop from self
            curr = dest_node
            while previous_hop[curr] != self.router_id and previous_hop[curr] is not None:
                curr = previous_hop[curr]
            next_hop_node = curr

            for s in subnets:
                routing_table.append({
                    "Destination Subnet": s,
                    "Cost": distances[dest_node],
                    "Next Hop": next_hop_node,
                    "Interface": f"WAN-{self.router_id}-{next_hop_node}"
                })

        return routing_table

def run_link_state_demo():
    print("=" * 75)
    print("     LINK STATE ROUTING (LSR) - DIJKSTRA SPF SIMULATION")
    print("=" * 75)

    # Topology Graph with Link Costs (Bandwidth Metric)
    topology = {
        "R1": {"R2": 2, "R3": 5},
        "R2": {"R1": 2, "R3": 1, "R4": 4},
        "R3": {"R1": 5, "R2": 1, "R4": 2, "R5": 6},
        "R4": {"R2": 4, "R3": 2, "R5": 1},
        "R5": {"R3": 6, "R4": 1}
    }

    subnet_map = {
        "R1": ["192.168.10.0/24"],
        "R2": ["192.168.20.0/24"],
        "R3": ["192.168.30.0/24"],
        "R4": ["192.168.40.0/24"],
        "R5": ["192.168.50.0/24"]
    }

    routers = {r_id: LinkStateRouter(r_id, subnets) for r_id, subnets in subnet_map.items()}

    print("\n1. Distributing Link State Advertisements (LSAs) across all routers...")
    for r in routers.values():
        r.update_lsdb(topology, subnet_map)

    print("\n2. Computing Link State Routing Table for Router R1:")
    table_r1 = routers["R1"].compute_spf_routing_table()
    
    print("-" * 75)
    print(f"{'Destination Subnet':<22} | {'Cost':<6} | {'Next Hop':<20} | {'Interface'}")
    print("-" * 75)
    for entry in table_r1:
        print(f"{entry['Destination Subnet']:<22} | {entry['Cost']:<6} | {entry['Next Hop']:<20} | {entry['Interface']}")
    print("-" * 75)

    # Simulate Link Failure (e.g. R2-R3 link breaks)
    print("\n3. Dynamic Event: Link between R2 and R3 failed! Flooding new LSA...")
    del topology["R2"]["R3"]
    del topology["R3"]["R2"]

    for r in routers.values():
        r.update_lsdb(topology, subnet_map)

    print("\n4. Recalculated Routing Table for R1 after Link Failure:")
    table_r1_updated = routers["R1"].compute_spf_routing_table()
    print("-" * 75)
    print(f"{'Destination Subnet':<22} | {'Cost':<6} | {'Next Hop':<20} | {'Interface'}")
    print("-" * 75)
    for entry in table_r1_updated:
        print(f"{entry['Destination Subnet']:<22} | {entry['Cost']:<6} | {entry['Next Hop']:<20} | {entry['Interface']}")
    print("-" * 75)
    print("SUCCESS: Link State Routing adapted dynamically to topology change!\n")

if __name__ == "__main__":
    run_link_state_demo()
