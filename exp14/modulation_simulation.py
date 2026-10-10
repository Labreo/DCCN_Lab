"""
Experiment 14: Open Source Simulation of Digital Modulation (ASK, PSK, FSK)
Language: Python 3
Libraries: numpy, matplotlib, scipy
Description:
    Simulates digital modulation techniques:
      - Amplitude Shift Keying (ASK / OOK)
      - Frequency Shift Keying (BFSK)
      - Phase Shift Keying (BPSK)
    Generates time-domain waveforms and constellation diagrams,
    saves high-resolution plots, and verifies coherent demodulation.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless backend
import matplotlib.pyplot as plt

def run_modulation_simulation(bits=[1, 0, 1, 1, 0, 0, 1, 0]):
    print("=" * 65)
    print("   EXPERIMENT 14: DIGITAL MODULATION SIMULATION (ASK, PSK, FSK)")
    print("=" * 65)
    print(f"Input Digital Bit Sequence: {bits}")

    # Simulation Parameters
    bit_rate = 1.0           # 1 bit per second
    samples_per_bit = 1000
    fs = samples_per_bit * bit_rate  # Sampling frequency
    total_time = len(bits) * (1.0 / bit_rate)
    t = np.linspace(0, total_time, len(bits) * samples_per_bit, endpoint=False)

    # Carrier Frequencies
    fc = 4.0      # Base carrier frequency (4 Hz)
    f1 = 6.0      # FSK frequency for bit '1'
    f0 = 2.0      # FSK frequency for bit '0'
    Ac = 1.0      # Carrier Amplitude

    # Construct Digital NRZ Signal
    digital_signal = np.repeat(bits, samples_per_bit)

    # 1. Carrier Signal
    carrier = Ac * np.sin(2 * np.pi * fc * t)

    # 2. ASK (Amplitude Shift Keying): s_ASK(t) = b(t) * Ac * sin(2*pi*fc*t)
    ask_signal = digital_signal * Ac * np.sin(2 * np.pi * fc * t)

    # 3. FSK (Frequency Shift Keying):
    fsk_signal = np.zeros_like(t)
    for i, b in enumerate(bits):
        idx_start = i * samples_per_bit
        idx_end = (i + 1) * samples_per_bit
        t_segment = t[idx_start:idx_end]
        freq = f1 if b == 1 else f0
        fsk_signal[idx_start:idx_end] = Ac * np.sin(2 * np.pi * freq * t_segment)

    # 4. BPSK (Phase Shift Keying): s_PSK(t) = Ac * sin(2*pi*fc*t + phase)
    # Bit 1 -> 0 phase, Bit 0 -> pi phase (inverts wave)
    psk_signal = np.zeros_like(t)
    for i, b in enumerate(bits):
        idx_start = i * samples_per_bit
        idx_end = (i + 1) * samples_per_bit
        t_segment = t[idx_start:idx_end]
        phase = 0.0 if b == 1 else np.pi
        psk_signal[idx_start:idx_end] = Ac * np.sin(2 * np.pi * fc * t_segment + phase)

    # ---------------------------------------------------------
    # Plot 1: Waveforms (Time Domain)
    # ---------------------------------------------------------
    fig, axes = plt.subplots(5, 1, figsize=(10, 8), sharex=True)
    plt.subplots_adjust(hspace=0.4)

    # Digital Message Signal
    axes[0].plot(t, digital_signal, 'black', linewidth=2)
    axes[0].set_title('1. Binary Input Message Sequence: ' + str(bits), fontweight='bold')
    axes[0].set_ylabel('Amplitude')
    axes[0].set_ylim(-0.2, 1.3)
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # Carrier Signal
    axes[1].plot(t, carrier, 'gray', linewidth=1.2)
    axes[1].set_title(f'2. Carrier Signal (fc = {fc} Hz)', fontweight='bold')
    axes[1].set_ylabel('Amplitude')
    axes[1].grid(True, linestyle='--', alpha=0.6)

    # ASK Modulated
    axes[2].plot(t, ask_signal, 'blue', linewidth=1.5)
    axes[2].set_title('3. Amplitude Shift Keying (ASK) Waveform', fontweight='bold', color='blue')
    axes[2].set_ylabel('Amplitude')
    axes[2].grid(True, linestyle='--', alpha=0.6)

    # FSK Modulated
    axes[3].plot(t, fsk_signal, 'green', linewidth=1.5)
    axes[3].set_title(f'4. Frequency Shift Keying (FSK) Waveform (f0 = {f0} Hz, f1 = {f1} Hz)', fontweight='bold', color='green')
    axes[3].set_ylabel('Amplitude')
    axes[3].grid(True, linestyle='--', alpha=0.6)

    # PSK Modulated
    axes[4].plot(t, psk_signal, 'red', linewidth=1.5)
    axes[4].set_title('5. Phase Shift Keying (BPSK) Waveform (0 rad / π rad)', fontweight='bold', color='red')
    axes[4].set_ylabel('Amplitude')
    axes[4].set_xlabel('Time (seconds)')
    axes[4].grid(True, linestyle='--', alpha=0.6)

    waveforms_file = "exp14/ask_fsk_psk_waveforms.png"
    plt.savefig(waveforms_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] Waveform plots saved to: {waveforms_file}")

    # ---------------------------------------------------------
    # Plot 2: Constellation Diagrams
    # ---------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # ASK Constellation
    axes[0].scatter([0, Ac], [0, 0], color='blue', s=100, zorder=5)
    axes[0].axhline(0, color='gray', linestyle='--')
    axes[0].axvline(0, color='gray', linestyle='--')
    axes[0].set_title('BASK Constellation', fontweight='bold')
    axes[0].set_xlim(-1.5, 1.5)
    axes[0].set_ylim(-1.5, 1.5)
    axes[0].text(0, 0.2, 'Bit 0 (0)', ha='center', color='blue')
    axes[0].text(Ac, 0.2, f'Bit 1 ({Ac})', ha='center', color='blue')
    axes[0].grid(True, alpha=0.3)

    # FSK Constellation (Orthogonal 2D)
    axes[1].scatter([Ac, 0], [0, Ac], color='green', s=100, zorder=5)
    axes[1].axhline(0, color='gray', linestyle='--')
    axes[1].axvline(0, color='gray', linestyle='--')
    axes[1].set_title('BFSK Constellation (Orthogonal)', fontweight='bold')
    axes[1].set_xlim(-1.5, 1.5)
    axes[1].set_ylim(-1.5, 1.5)
    axes[1].text(Ac, 0.2, 'f1 (Bit 1)', ha='center', color='green')
    axes[1].text(0.2, Ac, 'f0 (Bit 0)', ha='left', color='green')
    axes[1].grid(True, alpha=0.3)

    # BPSK Constellation (Antipodal)
    axes[2].scatter([-Ac, Ac], [0, 0], color='red', s=100, zorder=5)
    axes[2].axhline(0, color='gray', linestyle='--')
    axes[2].axvline(0, color='gray', linestyle='--')
    axes[2].set_title('BPSK Constellation (Antipodal)', fontweight='bold')
    axes[2].set_xlim(-1.5, 1.5)
    axes[2].set_ylim(-1.5, 1.5)
    axes[2].text(-Ac, 0.2, 'Bit 0 (-1)', ha='center', color='red')
    axes[2].text(Ac, 0.2, 'Bit 1 (+1)', ha='center', color='red')
    axes[2].grid(True, alpha=0.3)

    constellations_file = "exp14/modulation_constellations.png"
    plt.savefig(constellations_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] Constellation plots saved to: {constellations_file}")

    # Demodulation Verification
    # Coherent BPSK Demodulation: integrate over bit duration
    demod_bpsk = []
    for i in range(len(bits)):
        idx_start = i * samples_per_bit
        idx_end = (i + 1) * samples_per_bit
        product = psk_signal[idx_start:idx_end] * carrier[idx_start:idx_end]
        metric = np.sum(product)
        demod_bpsk.append(1 if metric > 0 else 0)

    print(f"\n[DEMODULATION VERIFICATION]")
    print(f"  Transmitted Bits : {bits}")
    print(f"  Demodulated Bits : {demod_bpsk}")
    assert bits == demod_bpsk, "Demodulation error!"
    print("  --> BPSK Demodulation Successful: Bit Error Rate (BER) = 0.00%")
    print("=" * 65)

if __name__ == "__main__":
    run_modulation_simulation()
