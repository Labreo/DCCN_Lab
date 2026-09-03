"""
Experiment 05 - Part 3: Selective Repeat (SR) ARQ Protocol Simulation
Author: DCCN Lab
Description:
    Simulates the Selective Repeat ARQ protocol with Sender & Receiver Windows > 1.
    Demonstrates:
      1. Pipelined frame transmission within Window Size (Ws = Wr = N)
      2. Out-of-order reception & buffering at Receiver
      3. Individual ACKs / NAKs for each frame
      4. Selective retransmission of ONLY the lost/damaged frame
      5. In-order delivery to Network Layer once missing frame is received
"""

import time
import random

def simulate_selective_repeat(total_frames=8, window_size=4, loss_prob=0.3):
    print("=" * 75)
    print("        SELECTIVE REPEAT (SR) ARQ PROTOCOL SIMULATION")
    print("=" * 75)
    print(f"Total Frames to Send    : {total_frames}")
    print(f"Sender Window Size (Ws) : {window_size}")
    print(f"Receiver Window Size(Wr): {window_size}")
    print("-" * 75)

    sender_base = 0      # Start of sender window
    receiver_base = 0    # Start of receiver window
    next_frame_to_send = 0

    # Track status of each frame
    # sender_status: 'NOT_SENT', 'SENT', 'ACKED'
    sender_status = ['NOT_SENT'] * total_frames
    # receiver_buffer: True if received and buffered, False otherwise
    receiver_buffer = [False] * total_frames

    while sender_base < total_frames:
        # 1. Send all available frames in current sender window [sender_base .. sender_base + window_size - 1]
        sent_in_this_round = []
        for f in range(sender_base, min(sender_base + window_size, total_frames)):
            if sender_status[f] == 'NOT_SENT':
                print(f"\n[SENDER]   Transmitting Frame {f}  |  Sender Window: [{sender_base} .. {min(sender_base + window_size - 1, total_frames - 1)}]")
                sender_status[f] = 'SENT'
                sent_in_this_round.append(f)
                time.sleep(0.3)

        # 2. Simulate channel & receiver processing for all currently sent (unacknowledged) frames
        unacked_frames = [f for f in range(sender_base, min(sender_base + window_size, total_frames)) if sender_status[f] == 'SENT']
        
        print(f"\n--- Channel Transmission for Outstanding Frames {unacked_frames} ---")
        time.sleep(0.4)

        for f in unacked_frames:
            # Check for packet loss
            if random.random() < loss_prob:
                print(f"  --> [NETWORK]  Frame {f} was LOST / DAMAGED in transit!")
                print(f"  --> [TIMER]    Timer running for Frame {f}...")
            else:
                # Frame arrived at receiver
                if f < receiver_base or f >= receiver_base + window_size:
                    print(f"  --> [RECEIVER] Frame {f} outside receive window [{receiver_base} .. {receiver_base + window_size - 1}]. Discarded.")
                else:
                    receiver_buffer[f] = True
                    if f == receiver_base:
                        print(f"  --> [RECEIVER] Frame {f} received IN-ORDER. Sending ACK {f}...")
                    else:
                        print(f"  --> [RECEIVER] Frame {f} received OUT-OF-ORDER. BUFFERED at receiver! Sending ACK {f}...")
                    
                    sender_status[f] = 'ACKED'
                    print(f"  --> [SENDER]   Received ACK {f} for Frame {f}.")

        # 3. Slide receiver window forward for all consecutive delivered frames
        while receiver_base < total_frames and receiver_buffer[receiver_base]:
            print(f"  --> [RECEIVER] Frame {receiver_base} delivered to Network Layer. Sliding receiver window forward...")
            receiver_base += 1

        # 4. Slide sender window forward for all consecutive ACKed frames
        while sender_base < total_frames and sender_status[sender_base] == 'ACKED':
            sender_base += 1

        # 5. Check if any frame in current window timed out
        for f in range(sender_base, min(sender_base + window_size, total_frames)):
            if sender_status[f] == 'SENT':
                # Frame was lost, timer expired
                print(f"\n[TIMER]    TIMEOUT expired for Frame {f}!")
                print(f"[SENDER]   Selective Retransmission: Resending ONLY Frame {f} (Frame {f} was lost earlier)...")
                # Mark as NOT_SENT to resend in the next cycle
                sender_status[f] = 'NOT_SENT'
                time.sleep(0.5)

    print("\n" + "=" * 75)
    print("  SUCCESS: All frames transmitted, buffered, and delivered via Selective Repeat!")
    print("=" * 75)

if __name__ == "__main__":
    simulate_selective_repeat(total_frames=7, window_size=4, loss_prob=0.3)
