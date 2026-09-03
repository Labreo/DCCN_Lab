"""
Experiment 08 - Part 2: Hamming Code (Error Detection & Correction)
Author: DCCN Lab
Description:
    Implements Hamming Code (7,4 and general Hamming code) for:
      1. Parity bit placement at powers of 2 (1, 2, 4, 8...)
      2. Codeword generation at sender using even parity
      3. Syndrome calculation at receiver
      4. Single-bit error detection, localization, and automatic correction
"""

def calc_redundant_bits(m: int) -> int:
    """Calculates number of redundant bits r such that 2^r >= m + r + 1."""
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    return r

def generate_hamming_code(data: str) -> tuple[str, int]:
    """Generates Hamming codeword with even parity."""
    m = len(data)
    r = calc_redundant_bits(m)
    total_len = m + r

    # 1-indexed list for easy bit-position calculation
    res = ['0'] * (total_len + 1)
    
    # Place data bits (leaving positions that are powers of 2 for parity)
    data_idx = 0
    # Reverse data so bit 0 is MSB or keep standard left-to-right
    for i in range(1, total_len + 1):
        if (i & (i - 1)) == 0:
            # Power of 2 (Parity bit position)
            continue
        res[i] = data[data_idx]
        data_idx += 1

    # Calculate parity bits (even parity)
    for i in range(r):
        p_pos = 2 ** i
        parity = 0
        for j in range(1, total_len + 1):
            if j & p_pos:
                if j != p_pos:
                    parity ^= int(res[j])
        res[p_pos] = str(parity)

    codeword = "".join(res[1:])
    return codeword, r

def detect_and_correct(received_codeword: str, r: int) -> tuple[int, str, str]:
    """
    Calculates syndrome word.
    Returns: (error_position, corrected_codeword, extracted_data)
    """
    total_len = len(received_codeword)
    res = ['0'] + list(received_codeword)
    syndrome = 0

    # Calculate syndrome bits
    for i in range(r):
        p_pos = 2 ** i
        parity = 0
        for j in range(1, total_len + 1):
            if j & p_pos:
                parity ^= int(res[j])
        if parity != 0:
            syndrome += p_pos

    corrected = list(received_codeword)
    if syndrome != 0:
        # Error detected at 1-indexed position 'syndrome'
        err_idx = syndrome - 1
        corrected[err_idx] = '0' if corrected[err_idx] == '1' else '1'

    corrected_str = "".join(corrected)

    # Extract original data bits
    extracted_data = []
    for i in range(1, total_len + 1):
        if (i & (i - 1)) != 0:
            extracted_data.append(corrected[i - 1])

    return syndrome, corrected_str, "".join(extracted_data)

def run_hamming_demo(data="1011"):
    print("=" * 65)
    print("      2. HAMMING CODE ERROR DETECTION & CORRECTION")
    print("=" * 65)
    print(f"Input Data Bits (m)           : {data} (Length = {len(data)})")
    
    codeword, r = generate_hamming_code(data)
    print(f"Redundant / Parity Bits (r)   : {r} (Total Codeword Length = {len(codeword)})")
    print(f"Generated Hamming Codeword    : {codeword}")

    # Case 1: Error-Free
    print("\n[SCENARIO A: Error-Free Transmission]")
    print(f"  Received Codeword    : {codeword}")
    syn_0, corr_0, data_0 = detect_and_correct(codeword, r)
    print(f"  Calculated Syndrome  : {syn_0}")
    if syn_0 == 0:
        print("  --> STATUS: Syndrome is 0. NO ERROR DETECTED!")
        print(f"  --> Extracted Data   : {data_0}")

    # Case 2: Induced Error
    error_pos = 3 # 1-indexed bit position to flip
    corrupted = list(codeword)
    corrupted[error_pos - 1] = '0' if corrupted[error_pos - 1] == '1' else '1'
    corrupted_codeword = "".join(corrupted)

    print(f"\n[SCENARIO B: Single-Bit Error Injected at Bit Position {error_pos}]")
    print(f"  Transmitted Codeword : {codeword}")
    print(f"  Received (Corrupted) : {corrupted_codeword}")
    
    syn, corr, recovered_data = detect_and_correct(corrupted_codeword, r)
    print(f"  Calculated Syndrome  : {syn} (Binary: {bin(syn)[2:].zfill(r)})")
    print(f"  --> ERROR DETECTED at bit position: {syn}")
    print(f"  --> Corrected Bit at position {syn} from '{corrupted[syn-1]}' to '{corr[syn-1]}'")
    print(f"  --> Fully Corrected Codeword : {corr}")
    print(f"  --> Extracted Original Data  : {recovered_data}")
    assert recovered_data == data, "Hamming recovery mismatch!"
    print("  --> VERIFICATION: Recovered data matches original message exactly!")
    print("=" * 65)

if __name__ == "__main__":
    run_hamming_demo()
