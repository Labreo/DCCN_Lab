"""
================================================================================
Experiment No: 07
Title: Implement Different Framing Methods and Analyze Their Efficiency & Impact
Subject: Data Communication & Computer Networks (DCCN) Lab
================================================================================

Framing Methods Implemented:
  1. Character Count Method
  2. Character (Byte) Stuffing & De-stuffing
  3. Bit Stuffing & De-stuffing (HDLC standard)

Includes:
  - Header, Trailer, and Flag management
  - Bit/Byte insertion and extraction
  - Transmission Efficiency (η) Calculation
  - Vulnerability and Channel Impact Analysis
================================================================================
"""

def character_count_framing(frames: list[str]):
    print("\n" + "=" * 65)
    print("           1. CHARACTER COUNT FRAMING METHOD")
    print("=" * 65)
    print(f"Original Input Frames : {frames}")
    
    transmitted_stream = ""
    total_data_chars = sum(len(f) for f in frames)
    total_transmitted_chars = 0

    print("\n[SENDER] Framing Process:")
    for i, frame in enumerate(frames):
        # Length includes the count character itself
        frame_len = len(frame) + 1
        framed_str = f"{frame_len}{frame}"
        transmitted_stream += framed_str
        total_transmitted_chars += len(framed_str)
        print(f"  Frame {i + 1}: '{frame}' (Length={len(frame)}) --> Framed: '{framed_str}' (Header Count = {frame_len})")

    print(f"\n[SENDER] Transmitted Bitstream / Chars : '{transmitted_stream}'")
    
    # Receiver Side Recovery
    print("\n[RECEIVER] Decoding Frame Stream:")
    idx = 0
    recovered_frames = []
    f_num = 1
    while idx < len(transmitted_stream):
        count = int(transmitted_stream[idx])
        payload = transmitted_stream[idx + 1 : idx + count]
        print(f"  Frame {f_num}: Read Count = {count} --> Extracted Payload = '{payload}'")
        recovered_frames.append(payload)
        idx += count
        f_num += 1

    # Efficiency Calculation
    efficiency = (total_data_chars / total_transmitted_chars) * 100
    overhead = total_transmitted_chars - total_data_chars
    print(f"\n[EFFICIENCY & IMPACT ANALYSIS]")
    print(f"  Payload Characters       : {total_data_chars}")
    print(f"  Total Transmitted Chars  : {total_transmitted_chars}")
    print(f"  Framing Overhead Added   : {overhead} characters")
    print(f"  Transmission Efficiency  : {efficiency:.2f}%")
    print(f"  Impact / Vulnerability   : If any count digit is corrupted in transit, framing synchronization")
    print(f"                             for ALL subsequent frames is permanently lost.")
    return efficiency


def byte_stuffing(data: str, flag="FLAG", esc="ESC"):
    print("\n" + "=" * 65)
    print("        2. BYTE / CHARACTER STUFFING & DE-STUFFING")
    print("=" * 65)
    print(f"Original Payload : '{data}'")
    print(f"Delimiters       : FLAG = '{flag}' | ESC = '{esc}'")

    # Sender: Stuffing
    tokens = data.split()
    stuffed_tokens = [flag]
    for token in tokens:
        if token == flag:
            stuffed_tokens.extend([esc, flag])
        elif token == esc:
            stuffed_tokens.extend([esc, esc])
        else:
            stuffed_tokens.append(token)
    stuffed_tokens.append(flag)

    stuffed_stream = " ".join(stuffed_tokens)
    print(f"\n[SENDER] Stuffed Frame Sent : {stuffed_stream}")

    # Receiver: De-stuffing
    print("\n[RECEIVER] De-stuffing and recovering payload:")
    raw_tokens = stuffed_stream.split()
    content_tokens = raw_tokens[1:-1]  # Strip starting and ending flags
    
    recovered = []
    i = 0
    while i < len(content_tokens):
        if content_tokens[i] == esc:
            recovered.append(content_tokens[i + 1])
            i += 2
        else:
            recovered.append(content_tokens[i])
            i += 1

    recovered_str = " ".join(recovered)
    print(f"  Recovered Payload : '{recovered_str}'")

    # Efficiency Calculation
    payload_len = len(data)
    total_len = len(stuffed_stream)
    efficiency = (payload_len / total_len) * 100
    print(f"\n[EFFICIENCY & IMPACT ANALYSIS]")
    print(f"  Original Payload Length  : {payload_len} chars")
    print(f"  Transmitted Frame Length : {total_len} chars (including FLAGS & ESCs)")
    print(f"  Transmission Efficiency  : {efficiency:.2f}%")
    print(f"  Impact / Vulnerability   : Safe against delimiter collisions, but causes variable frame size")
    print(f"                             and higher byte overhead when escape sequences occur frequently.")
    return efficiency


def bit_stuffing(bit_string: str, flag="01111110"):
    print("\n" + "=" * 65)
    print("           3. BIT STUFFING & DE-STUFFING (HDLC)")
    print("=" * 65)
    print(f"Original Bit String : {bit_string}")
    print(f"Flag Sequence       : {flag}")

    # Sender: Insert '0' after five consecutive '1's
    count_ones = 0
    stuffed_bits = ""
    for bit in bit_string:
        if bit == '1':
            count_ones += 1
            stuffed_bits += bit
            if count_ones == 5:
                stuffed_bits += '0'  # Stuffed zero
                count_ones = 0
        else:
            count_ones = 0
            stuffed_bits += bit

    transmitted_frame = f"{flag}{stuffed_bits}{flag}"
    print(f"\n[SENDER] After Bit Stuffing : {stuffed_bits}")
    print(f"[SENDER] Transmitted Frame  : {transmitted_frame}")

    # Receiver: De-stuffing
    received_payload = transmitted_frame[len(flag) : -len(flag)]
    destuffed_bits = ""
    count_ones = 0
    i = 0
    while i < len(received_payload):
        bit = received_payload[i]
        if bit == '1':
            count_ones += 1
            destuffed_bits += bit
            if count_ones == 5:
                # Skip the next stuffed '0'
                if i + 1 < len(received_payload) and received_payload[i + 1] == '0':
                    i += 1
                count_ones = 0
        else:
            count_ones = 0
            destuffed_bits += bit
        i += 1

    print(f"\n[RECEIVER] De-stuffed Bit String : {destuffed_bits}")
    assert destuffed_bits == bit_string, "De-stuffing mismatch!"
    print("  Verification: De-stuffed data matches original bit string exactly!")

    # Efficiency Calculation
    payload_bits = len(bit_string)
    total_bits = len(transmitted_frame)
    stuffed_count = len(stuffed_bits) - payload_bits
    efficiency = (payload_bits / total_bits) * 100

    print(f"\n[EFFICIENCY & IMPACT ANALYSIS]")
    print(f"  Data Payload Bits        : {payload_bits} bits")
    print(f"  Stuffed Bits Added       : {stuffed_count} bits")
    print(f"  Flag Delimiters Overhead : {2 * len(flag)} bits (Header + Trailer)")
    print(f"  Total Transmitted Bits   : {total_bits} bits")
    print(f"  Transmission Efficiency  : {efficiency:.2f}%")
    print(f"  Impact / Vulnerability   : Highly robust and bit-oriented; prevents false flags with minimal")
    print(f"                             overhead. Hardware implementations are extremely fast.")
    return efficiency


def main():
    print("=" * 70)
    print("   EXPERIMENT NO: 07 - FRAMING METHODS & EFFICIENCY ANALYSIS")
    print("=" * 70)

    # 1. Character Count Demonstration
    sample_frames = ["GATE", "ACADEMY", "DCCN", "LAB"]
    eff_cc = character_count_framing(sample_frames)

    # 2. Byte Stuffing Demonstration
    sample_byte_data = "A B FLAG C ESC D FLAG E"
    eff_byte = byte_stuffing(sample_byte_data)

    # 3. Bit Stuffing Demonstration
    sample_bits = "011111101111101011111100"
    eff_bit = bit_stuffing(sample_bits)

    print("\n" + "=" * 70)
    print("                COMPARATIVE EFFICIENCY & IMPACT TABLE")
    print("=" * 70)
    print(f"| {'Framing Method':<24} | {'Efficiency (η)':<15} | {'Vulnerability & Channel Impact':<23} |")
    print("|" + "-" * 26 + "|" + "-" * 17 + "|" + "-" * 33 + "|")
    print(f"| {'Character Count':<24} | {eff_cc:>13.2f}% | {'High (Catastrophic framing desync)':<31} |")
    print(f"| {'Byte / Char Stuffing':<24} | {eff_byte:>13.2f}% | {'Medium (Variable length overhead)':<31} |")
    print(f"| {'Bit Stuffing (HDLC)':<24} | {eff_bit:>13.2f}% | {'Low / Robust (Minimal bit overhead)':<31} |")
    print("=" * 70)

if __name__ == "__main__":
    main()
