"""
DCCN Lab - Experiment: Framing Methods and Efficiency Analysis
Methods Implemented:
  1. Character Count
  2. Character (Byte) Stuffing & De-stuffing
  3. Bit Stuffing & De-stuffing
Includes:
  - Transmission Efficiency Calculation
  - Comparative Impact Analysis
"""

def character_count_framing(frames: list[str]):
    print("\n" + "=" * 60)
    print("        1. CHARACTER COUNT FRAMING METHOD")
    print("=" * 60)
    print(f"Original Input Frames: {frames}")
    
    transmitted_stream = ""
    total_data_chars = sum(len(f) for f in frames)
    total_transmitted_chars = 0

    for i, frame in enumerate(frames):
        # Length includes the count character itself
        frame_len = len(frame) + 1
        framed_str = f"{frame_len}{frame}"
        transmitted_stream += framed_str
        total_transmitted_chars += len(framed_str)
        print(f"  Frame {i + 1}: '{frame}' (Len={len(frame)}) --> Framed: '{framed_str}' (Header Count = {frame_len})")

    print(f"\n[SENDER] Transmitted Stream : '{transmitted_stream}'")
    
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

    # Efficiency
    efficiency = (total_data_chars / total_transmitted_chars) * 100
    print(f"\n[EFFICIENCY ANALYSIS]")
    print(f"  Payload Characters     : {total_data_chars}")
    print(f"  Total Transmitted Chars: {total_transmitted_chars}")
    print(f"  Framing Overhead       : {total_transmitted_chars - total_data_chars} characters")
    print(f"  Efficiency (η)         : {efficiency:.2f}%")
    print(f"  Impact/Vulnerability   : If count digit is corrupted in transit, entire framing sync is lost.")
    return efficiency


def byte_stuffing(data: str, flag="FLAG", esc="ESC"):
    print("\n" + "=" * 60)
    print("      2. BYTE / CHARACTER STUFFING & DE-STUFFING")
    print("=" * 60)
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
    print(f"\n[SENDER] Stuffed Frame Sent: {stuffed_stream}")

    # Receiver: De-stuffing
    print("\n[RECEIVER] De-stuffing and recovering payload:")
    raw_tokens = stuffed_stream.split()
    # Strip start and end flags
    content_tokens = raw_tokens[1:-1]
    
    recovered = []
    i = 0
    while i < len(content_tokens):
        if content_tokens[i] == esc:
            # Next token is literal
            recovered.append(content_tokens[i + 1])
            i += 2
        else:
            recovered.append(content_tokens[i])
            i += 1

    recovered_str = " ".join(recovered)
    print(f"  Recovered Payload: '{recovered_str}'")

    # Efficiency
    payload_len = len(data)
    total_len = len(stuffed_stream)
    efficiency = (payload_len / total_len) * 100
    print(f"\n[EFFICIENCY ANALYSIS]")
    print(f"  Original Length : {payload_len} chars")
    print(f"  Transmitted Len : {total_len} chars (including FLAGS & ESCs)")
    print(f"  Efficiency (η)  : {efficiency:.2f}%")
    return efficiency


def bit_stuffing(bit_string: str, flag="01111110"):
    print("\n" + "=" * 60)
    print("         3. BIT STUFFING & DE-STUFFING (HDLC)")
    print("=" * 60)
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
    print(f"[SENDER] After Stuffing  : {stuffed_bits}")
    print(f"[SENDER] Full Frame Sent : {transmitted_frame}")

    # Receiver: De-stuffing
    # Strip start and end flags
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

    print(f"\n[RECEIVER] De-stuffed String: {destuffed_bits}")
    assert destuffed_bits == bit_string, "De-stuffing error!"
    print("  Verification: Recovered bits match original data exactly!")

    # Efficiency Calculation
    payload_bits = len(bit_string)
    total_bits = len(transmitted_frame)
    stuffed_count = len(stuffed_bits) - payload_bits
    efficiency = (payload_bits / total_bits) * 100

    print(f"\n[EFFICIENCY ANALYSIS]")
    print(f"  Data Payload Bits  : {payload_bits} bits")
    print(f"  Stuffed Bits Added : {stuffed_count} bits")
    print(f"  Flag Delimiters    : {2 * len(flag)} bits (Header + Trailer)")
    print(f"  Total Transmitted  : {total_bits} bits")
    print(f"  Efficiency (η)     : {efficiency:.2f}%")
    return efficiency


def main():
    print("=" * 65)
    print(" DCCN LAB: IMPLEMENTATION OF FRAMING METHODS & EFFICIENCY")
    print("=" * 65)

    # 1. Character Count Demonstration
    sample_frames = ["GATE", "ACADEMY", "DCCN", "LAB"]
    eff_cc = character_count_framing(sample_frames)

    # 2. Byte Stuffing Demonstration
    sample_byte_data = "A B FLAG C ESC D FLAG E"
    eff_byte = byte_stuffing(sample_byte_data)

    # 3. Bit Stuffing Demonstration (Pattern with >= 5 consecutive 1s)
    sample_bits = "011111101111101011111100"
    eff_bit = bit_stuffing(sample_bits)

    print("\n" + "=" * 65)
    print("             SUMMARY OF EFFICIENCY & IMPACT")
    print("=" * 65)
    print(f"| {'Framing Method':<25} | {'Efficiency (η)':<15} | {'Vulnerability / Impact':<18} |")
    print("|" + "-" * 27 + "|" + "-" * 17 + "|" + "-" * 20 + "|")
    print(f"| {'Character Count':<25} | {eff_cc:>13.2f}% | {'High (Sync loss)':<18} |")
    print(f"| {'Byte / Char Stuffing':<25} | {eff_byte:>13.2f}% | {'Medium (ESC overhead)':<18} |")
    print(f"| {'Bit Stuffing (HDLC)':<25} | {eff_bit:>13.2f}% | {'Low / Robust':<18} |")
    print("=" * 65)

if __name__ == "__main__":
    main()
