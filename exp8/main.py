"""
Experiment 08: Error Detection and Correction Mechanisms
Protocols:
  1. Cyclic Redundancy Check (CRC)
  2. Hamming Code (Error Detection & Correction)
  3. Internet Checksum (1's Complement)
"""

from crc import run_crc_demo, crc_sender, crc_receiver
from hamming_code import run_hamming_demo, generate_hamming_code, detect_and_correct
from checksum import run_checksum_demo

def main():
    while True:
        print("\n" + "=" * 60)
        print("   DCCN LAB - EXPERIMENT 08: ERROR DETECTION & CORRECTION")
        print("=" * 60)
        print("1. Cyclic Redundancy Check (CRC)")
        print("2. Hamming Code (Detection & Correction)")
        print("3. Checksum (1's Complement Addition)")
        print("4. Run All Three (Demo Mode)")
        print("5. Exit")
        print("=" * 60)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            data = input("Enter data bits (default: 100100): ").strip() or "100100"
            gen = input("Enter generator polynomial (default: 1101): ").strip() or "1101"
            run_crc_demo(data, gen)
        elif choice == '2':
            data = input("Enter 4-bit data word (default: 1011): ").strip() or "1011"
            run_hamming_demo(data)
        elif choice == '3':
            run_checksum_demo()
        elif choice == '4':
            print("\n>>> 1. CRC DEMO <<<")
            run_crc_demo()
            print("\n>>> 2. HAMMING CODE DEMO <<<")
            run_hamming_demo()
            print("\n>>> 3. CHECKSUM DEMO <<<")
            run_checksum_demo()
        elif choice == '5':
            print("Exiting Experiment 08. Goodbye!")
            break
        else:
            print("Invalid choice! Please choose 1 to 5.")

if __name__ == "__main__":
    main()
