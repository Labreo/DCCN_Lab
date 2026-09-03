"""
Experiment 08 - Part 3: Internet Checksum (1's Complement Addition)
Author: DCCN Lab
Description:
    Implements 1's complement Checksum generation and verification:
      1. Segments data into n-bit blocks (default: 8 bits)
      2. Computes 1's complement sum with end-around carry
      3. Generates checksum by inverting sum
      4. Validates at receiver (sum of all segments + checksum must equal all 1s)
"""

def ones_complement_add(a: int, b: int, bit_width=8) -> int:
    """Adds two integers using 1's complement (wraps around carry)."""
    mask = (1 << bit_width) - 1
    total = a + b
    # While there is a carry beyond bit_width, wrap it around
    while (total >> bit_width) > 0:
        carry = total >> bit_width
        total = (total & mask) + carry
    return total & mask

def calculate_checksum(segments: list[int], bit_width=8) -> int:
    """Computes the checksum (1's complement of the sum of segments)."""
    total = 0
    for seg in segments:
        total = ones_complement_add(total, seg, bit_width)
    mask = (1 << bit_width) - 1
    return ~total & mask

def verify_checksum(segments_with_checksum: list[int], bit_width=8) -> tuple[bool, int]:
    """
    Validates received segments.
    Returns: (is_valid, final_complement_value)
    """
    total = 0
    for seg in segments_with_checksum:
        total = ones_complement_add(total, seg, bit_width)
    mask = (1 << bit_width) - 1
    final_val = ~total & mask
    return (final_val == 0), final_val

def run_checksum_demo():
    print("=" * 65)
    print("          3. INTERNET CHECKSUM SIMULATION (8-BIT)")
    print("=" * 65)
    
    # 3 sample 8-bit blocks
    segments = [0b10101001, 0b00111001, 0b11000011]
    bit_width = 8

    print("Data Segments (Hex & Binary):")
    for idx, seg in enumerate(segments, 1):
        print(f"  Segment {idx}: {bin(seg)[2:].zfill(bit_width)}  (0x{seg:02X})")

    # Sender Side
    checksum = calculate_checksum(segments, bit_width)
    print("\n[SENDER SIDE]")
    print(f"  Sum with End-Around Carry : {bin(~checksum & 0xFF)[2:].zfill(bit_width)}")
    print(f"  Generated Checksum (~Sum) : {bin(checksum)[2:].zfill(bit_width)}  (0x{checksum:02X})")
    
    transmitted = segments + [checksum]

    # Receiver Side - Error Free
    print("\n[RECEIVER SIDE - Scenario A: Error-Free Transmission]")
    valid, check_val = verify_checksum(transmitted, bit_width)
    print(f"  Sum of all blocks + Checksum: {bin(~check_val & 0xFF)[2:].zfill(bit_width)}")
    print(f"  Final Complemented Result   : {bin(check_val)[2:].zfill(bit_width)}")
    if valid:
        print("  --> STATUS: Result is 0. NO ERROR DETECTED! Data accepted.")
    else:
        print("  --> STATUS: Non-zero result! ERROR DETECTED! Data rejected.")

    # Receiver Side - Bit Error
    corrupted = list(transmitted)
    corrupted[0] ^= 0b00000001 # Flip 1 bit in segment 1
    print("\n[RECEIVER SIDE - Scenario B: Bit Corrupted in Segment 1]")
    print(f"  Corrupted Segment 1 : {bin(corrupted[0])[2:].zfill(bit_width)}")
    valid_err, check_err = verify_checksum(corrupted, bit_width)
    print(f"  Final Complemented Result   : {bin(check_err)[2:].zfill(bit_width)}")
    if valid_err:
        print("  --> STATUS: Result is 0. Data accepted.")
    else:
        print("  --> STATUS: Result is non-zero (0x{:02X})! ERROR DETECTED! Data rejected.".format(check_err))

    print("=" * 65)

if __name__ == "__main__":
    run_checksum_demo()
