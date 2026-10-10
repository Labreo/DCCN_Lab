"""
Experiment 12: Dynamic Routing Algorithms Simulation Menu
Protocols:
  1. Link State Routing (Dijkstra SPF)
  2. Distance Vector Routing (Bellman-Ford)
  3. Path Vector Routing (BGP Path Vector)
"""

from link_state_routing import run_link_state_demo
from distance_vector_routing import run_distance_vector_demo
from path_vector_routing import run_path_vector_demo

def main():
    while True:
        print("\n" + "=" * 65)
        print("  DCCN LAB - EXPERIMENT 12: DYNAMIC ROUTING ALGORITHMS")
        print("=" * 65)
        print("1. Link State Routing (Dijkstra SPF)")
        print("2. Distance Vector Routing (Bellman-Ford)")
        print("3. Path Vector Routing (BGP-style Loop Prevention)")
        print("4. Run All Three Routing Algorithms (Full Demo)")
        print("5. Exit")
        print("=" * 65)

        choice = input("Enter your choice (1-5): ").strip()
        if choice == '1':
            run_link_state_demo()
        elif choice == '2':
            run_distance_vector_demo()
        elif choice == '3':
            run_path_vector_demo()
        elif choice == '4':
            run_link_state_demo()
            run_distance_vector_demo()
            run_path_vector_demo()
        elif choice == '5':
            print("Exiting Experiment 12. Goodbye!")
            break
        else:
            print("Invalid choice! Please choose 1-5.")

if __name__ == "__main__":
    main()
