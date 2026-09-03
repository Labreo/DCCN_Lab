"""
Experiment 05 - Part 1: Stop and Wait ARQ Protocol Simulation
Author: DCCN Lab
Description:
    Simulates the Stop-and-Wait ARQ protocol with 1-bit sequence numbers (0 and 1).
    Demonstrates:
      1. Normal Transmission and Acknowledgment
      2. Lost Data Frame & Timeout Retransmission
      3. Lost Acknowledgment (ACK) & Duplicate Detection
      4. Corrupted Frame / Negative Acknowledgment (NAK)
"""

import time
import random

TIMEOUT_DURATION = 2.0  # seconds

def simulate_stop_and_wait(total_frames=5, loss_prob=0.2, ack_loss_prob=0.15):
    print("=" * 65)
    print("        STOP-AND-WAIT ARQ PROTOCOL SIMULATION")
    print("=" * 65)
    print(f"Total Frames to Send: {total_frames}")
    print(f"Sequence Numbers    : Modulo-2 (0 and 1)")
    print(f"Window Size (Sender): 1  |  Window Size (Receiver): 1")
    print(f"Timeout Interval    : {TIMEOUT_DURATION}s")
    print("-" * 65)

    sender_seq = 0       # Sender starts with sequence number 0
    receiver_expected = 0 # Receiver expects sequence number 0
    frame_idx = 1

    while frame_idx <= total_frames:
        print(f"\n[FRAME {frame_idx}] Transmitting data packet (Seq = {sender_seq})...")
        time.sleep(0.5)

        # Event simulation: Normal, Lost Frame, Corrupted Frame
        rand_val = random.random()
        if rand_val < loss_prob:
            # Scenario 1: Frame Lost in transit
            print(f"  --> [NETWORK] Frame {sender_seq} was LOST in the channel!")
            print(f"  --> [SENDER]  Waiting for ACK{1 - sender_seq}...")
            time.sleep(TIMEOUT_DURATION)
            print(f"  --> [TIMER]   TIMEOUT expired for Frame {sender_seq}!")
            print(f"  --> [SENDER]  Retransmitting Frame (Seq = {sender_seq})...")
            continue

        elif rand_val < loss_prob + 0.1:
            # Scenario 2: Frame Damaged / Corrupted in transit
            print(f"  --> [RECEIVER] Frame {sender_seq} received but CORRUPTED (Checksum error)!")
            print(f"  --> [RECEIVER] Discarded corrupted frame. Sending NAK {sender_seq}...")
            time.sleep(0.5)
            print(f"  --> [SENDER]  Received NAK {sender_seq}. Retransmitting immediately...")
            continue

        else:
            # Scenario 3: Frame successfully received
            print(f"  --> [RECEIVER] Frame (Seq = {sender_seq}) received successfully.")
            
            # Check if sequence number matches expected
            if sender_seq == receiver_expected:
                print(f"  --> [RECEIVER] Frame matches expected Seq {receiver_expected}. Packet accepted & delivered to Network Layer.")
                # Toggle expected sequence number for the next frame
                receiver_expected = 1 - receiver_expected
            else:
                print(f"  --> [RECEIVER] Duplicate Frame detected (Expected {receiver_expected}, Got {sender_seq}). Discarding duplicate.")

            # Simulate ACK transmission
            ack_expected = receiver_expected  # In Stop-and-Wait ARQ, ACK announces next expected frame
            if random.random() < ack_loss_prob:
                # Scenario 4: ACK is Lost
                print(f"  --> [NETWORK] ACK {ack_expected} was LOST in transit!")
                print(f"  --> [SENDER]  Waiting for ACK {ack_expected}...")
                time.sleep(TIMEOUT_DURATION)
                print(f"  --> [TIMER]   TIMEOUT expired at sender!")
                print(f"  --> [SENDER]  Resending Frame (Seq = {sender_seq})...")
                continue
            else:
                # ACK received successfully
                time.sleep(0.4)
                print(f"  --> [SENDER]  ACK {ack_expected} received successfully before timeout.")
                sender_seq = ack_expected
                frame_idx += 1

    print("\n" + "=" * 65)
    print("  SUCCESS: All frames transmitted and acknowledged successfully!")
    print("=" * 65)

if __name__ == "__main__":
    simulate_stop_and_wait(total_frames=4, loss_prob=0.25, ack_loss_prob=0.2)
