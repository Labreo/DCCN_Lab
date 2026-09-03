"""
Experiment 05 - Part 2: Go-Back-N (GBN) ARQ Protocol Simulation
Author: DCCN Lab
Description:
    Simulates the Go-Back-N ARQ protocol with sliding window.
    Demonstrates:
      1. Pipelined frame transmission up to Sender Window Size (N)
      2. In-order frame processing by Receiver (Receiver Window = 1)
      3. Discarding of out-of-order frames
      4. Timeout of oldest unacknowledged frame & Go-Back-N retransmission
"""

import time
import random

def simulate_go_back_n(total_frames=8, window_size=4, loss_prob=0.2):
    print("=" * 70)
    print("           GO-BACK-N (GBN) ARQ PROTOCOL SIMULATION")
    print("=" * 70)
    print(f"Total Frames to Send  : {total_frames}")
    print(f"Sender Window Size (N): {window_size}")
    print(f"Receiver Window Size  : 1")
    print("-" * 70)

    base = 0         # Oldest unacknowledged frame (Sf)
    next_seq_num = 0 # Next frame to be sent (Sn)
    expected_frame = 0 # Receiver expected frame (Rn)
    
    # Track which frames have been delivered to network layer
    delivered = [False] * total_frames

    while base < total_frames:
        # 1. Send all frames available in current window [base, base + window_size)
        while next_seq_num < base + window_size and next_seq_num < total_frames:
            print(f"\n[SENDER] Transmitting Frame {next_seq_num}  |  Current Window: [{base} .. {min(base + window_size - 1, total_frames - 1)}]")
            time.sleep(0.3)
            next_seq_num += 1

        # 2. Simulate channel transmission for outstanding frames
        print(f"\n--- Channel & Receiver Processing for Window [{base} .. {next_seq_num - 1}] ---")
        time.sleep(0.5)

        first_lost_frame = None
        for frame in range(base, next_seq_num):
            # Check if this frame is lost
            if first_lost_frame is None and random.random() < loss_prob:
                first_lost_frame = frame
                print(f"  --> [NETWORK] Frame {frame} was LOST / CORRUPTED in transit!")

            if first_lost_frame is not None:
                if frame > first_lost_frame:
                    print(f"  --> [RECEIVER] Received Frame {frame} OUT OF ORDER (Expecting Frame {expected_frame}). Discarding Frame {frame}!")
            else:
                # Frame successfully received
                if frame == expected_frame:
                    print(f"  --> [RECEIVER] Frame {frame} received in-order. Delivered to Network Layer. Sending ACK {frame + 1}...")
                    delivered[frame] = True
                    expected_frame += 1
                else:
                    print(f"  --> [RECEIVER] Frame {frame} discarded (Expecting {expected_frame}). Sending duplicate ACK {expected_frame}...")

        # 3. Handle ACKs & Timeouts
        if first_lost_frame is not None:
            # Timeout for the lost frame
            print(f"\n[TIMER]   TIMEOUT expired for Frame {first_lost_frame}!")
            print(f"[SENDER]  GO-BACK-N Triggered: Rolling back from {next_seq_num} to Frame {first_lost_frame}.")
            print(f"[SENDER]  Will retransmit all frames in window starting from Frame {first_lost_frame}...")
            base = first_lost_frame
            next_seq_num = first_lost_frame
            time.sleep(0.6)
        else:
            # All frames in the batch were acknowledged
            print(f"\n[SENDER]  Cumulative ACK received up to Frame {next_seq_num}. Sliding window forward...")
            base = next_seq_num
            time.sleep(0.4)

    print("\n" + "=" * 70)
    print("  SUCCESS: All frames delivered in-order via Go-Back-N ARQ!")
    print("=" * 70)

if __name__ == "__main__":
    simulate_go_back_n(total_frames=7, window_size=3, loss_prob=0.25)
