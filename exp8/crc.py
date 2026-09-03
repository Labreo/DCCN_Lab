"""
Experiment 08 - Part 1: Cyclic Redundancy Check (CRC)
Author: DCCN Lab
Description:
    Implements CRC generation at sender and error detection at receiver
    using Modulo-2 binary division (XOR).
"""

def xor(a: str, b: str) -> str:
    """Performs bitwise XOR between two binary strings of equal length."""
    result = []
    for bit_a, bit_b in zip(a, b):
        result.append('0' if bit_a == bit_b else '1')
    return "".join(result)

def modulo2_divide(dividend: str, divisor: str) -> tuple[str, list[str]]:
    """
    Performs Modulo-2 division (XOR division) and returns (remainder, step_logs).
    """
    pick = len(divisor)
    tmp = dividend[0:pick]
    steps = []

    while pick < len(dividend):
        if tmp[0] == '1':
            res = xor(divisor, tmp)
            steps.append(f"  {tmp} XOR {divisor} = {res}")
            tmp = res[1:] + dividend[pick]
        else:
            res = xor('0' * pick, tmp)
            steps.append(f"  {tmp} XOR {'0'*pick} = {res}")
            tmp = res[1:] + dividend[pick]
        pick += 1

    # For the last bits
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)[1:]
    else:
        tmp = xor('0' * pick, tmp)[1:]

    return tmp, steps

def crc_sender(data: str, generator: str) -> tuple[str, str]:
    """Generates CRC checksum and codeword."""
    r = len(generator) - 1
    appended_data = data + ('0' * r)
    remainder, _ = modulo2_divide(appended_data, generator)
    codeword = data + remainder
    return remainder, codeword

def crc_receiver(received_codeword: str, generator: str) -> tuple[bool, str]:
    """Checks received codeword for transmission errors."""
    remainder, _ = modulo2_divide(received_codeword, generator)
    # If remainder is all 0s, no error
    is_valid = (remainder == '0' * (len(generator) - 1))
    return is_valid, remainder

def run_crc_demo(data="100100", generator="1101"):
    print("=" * 65)
    print("      1. CYCLIC REDUNDANCY CHECK (CRC) SIMULATION")
    print("=" * 65)
    print(f"Data Word (k bits)         : {data}")
    print(f"Generator Polynomial (G(x)): {generator} (Degree = {len(generator)-1})")
    print("-" * 65)

    # Sender Side
    crc_bits, codeword = crc_sender(data, generator)
    print("\n[SENDER SIDE]")
    print(f"  1. Appending {len(generator)-1} zero(s) : {data + '0'*(len(generator)-1)}")
    print(f"  2. Calculated CRC Checksum (Remainder): {crc_bits}")
    print(f"  3. Transmitted Codeword (Data + CRC)  : {codeword}")

    # Receiver Side - Case 1: Error-Free Transmission
    print("\n[RECEIVER SIDE - Scenario A: Error-Free]")
    print(f"  Received Codeword : {codeword}")
    valid, rem = crc_receiver(codeword, generator)
    print(f"  Syndrome Remainder: {rem}")
    if valid:
        print("  --> STATUS: Remainder is 0. NO ERROR DETECTED! Packet accepted.")
    else:
        print("  --> STATUS: Remainder != 0. ERROR DETECTED! Packet rejected.")

    # Receiver Side - Case 2: Bit Flip Error Induced
    corrupted_codeword = list(codeword)
    flip_idx = len(data) - 1 # Flip one bit in payload
    corrupted_codeword[flip_idx] = '0' if corrupted_codeword[flip_idx] == '1' else '1'
    corrupted_codeword = "".join(corrupted_codeword)

    print("\n[RECEIVER SIDE - Scenario B: Bit Corrupted During Transit]")
    print(f"  Original Codeword : {codeword}")
    print(f"  Corrupted Codeword: {corrupted_codeword} (Bit at index {flip_idx} flipped)")
    valid_err, rem_err = crc_receiver(corrupted_codeword, generator)
    print(f"  Syndrome Remainder: {rem_err}")
    if valid_err:
        print("  --> STATUS: Remainder is 0. Packet accepted.")
    else:
        print("  --> STATUS: Non-zero remainder detected! ERROR DETECTED! Packet rejected.")

    print("=" * 65)

if __name__ == "__main__":
    run_crc_demo()
