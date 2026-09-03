"""
Experiment 05: Flow and Error Control Mechanisms Simulation
Protocols:
  1. Stop-and-Wait ARQ
  2. Go-Back-N (GBN) ARQ
  3. Selective Repeat (SR) ARQ
"""

import sys
from stop_and_wait import simulate_stop_and_wait
from go_back_n import simulate_go_back_n
from selective_repeat import simulate_selective_repeat

def main():
    while True:
        print("\n" + "=" * 55)
        print("   DCCN LAB - EXPERIMENT 05: FLOW & ERROR CONTROL")
        print("=" * 55)
        print("1. Stop-and-Wait ARQ Protocol")
        print("2. Go-Back-N (GBN) ARQ Protocol")
        print("3. Selective Repeat (SR) ARQ Protocol")
        print("4. Run All Three Protocols (Demo Mode)")
        print("5. Exit")
        print("=" * 55)
        
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            frames = int(input("Enter number of frames to send (e.g. 4): ") or "4")
            simulate_stop_and_wait(total_frames=frames, loss_prob=0.3, ack_loss_prob=0.2)
        elif choice == '2':
            frames = int(input("Enter number of frames to send (e.g. 7): ") or "7")
            window = int(input("Enter Sender Window Size N (e.g. 3): ") or "3")
            simulate_go_back_n(total_frames=frames, window_size=window, loss_prob=0.3)
        elif choice == '3':
            frames = int(input("Enter number of frames to send (e.g. 7): ") or "7")
            window = int(input("Enter Window Size Ws=Wr (e.g. 4): ") or "4")
            simulate_selective_repeat(total_frames=frames, window_size=window, loss_prob=0.3)
        elif choice == '4':
            print("\n>>> RUNNING 1. STOP-AND-WAIT ARQ <<<")
            simulate_stop_and_wait(total_frames=3, loss_prob=0.3, ack_loss_prob=0.2)
            print("\n>>> RUNNING 2. GO-BACK-N ARQ <<<")
            simulate_go_back_n(total_frames=6, window_size=3, loss_prob=0.3)
            print("\n>>> RUNNING 3. SELECTIVE REPEAT ARQ <<<")
            simulate_selective_repeat(total_frames=6, window_size=3, loss_prob=0.3)
        elif choice == '5':
            print("Exiting Experiment 05 simulation. Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1 to 5.")

if __name__ == "__main__":
    main()
