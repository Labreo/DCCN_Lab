"""
Experiment 15: Simulator for FDM, WDM, TDM, and DSSS
Language: Python 3
Libraries: numpy, matplotlib, scipy.signal
Description:
    Implements a multi-channel communications multiplexing simulator:
      1. Frequency Division Multiplexing (FDM): Subcarrier modulation & BPF demux
      2. Time Division Multiplexing (TDM): Slot interleaving & frame deinterleaving
      3. Wavelength Division Multiplexing (WDM): Optical spectrum multiplexing (1310/1490/1550 nm)
      4. Direct Sequence Spread Spectrum (DSSS): 11-chip Barker code spreading & correlation despreading
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def run_multiplexing_simulator():
    print("=" * 70)
    print("   EXPERIMENT 15: MULTIPLEXING & SPREAD SPECTRUM SIMULATOR")
    print("=" * 70)

    fs = 2000.0  # Sampling frequency (Hz)
    t = np.linspace(0, 1.0, int(fs), endpoint=False)

    # -------------------------------------------------------------
    # 1. Frequency Division Multiplexing (FDM)
    # -------------------------------------------------------------
    print("\n1. Simulating Frequency Division Multiplexing (FDM)...")
    # 3 Message signals
    m1 = np.sin(2 * np.pi * 3 * t)
    m2 = np.cos(2 * np.pi * 5 * t)
    m3 = np.sin(2 * np.pi * 8 * t)

    # Carrier Frequencies
    fc1, fc2, fc3 = 60.0, 140.0, 220.0

    # Modulated Signals (AM-DSB-SC)
    s1 = m1 * np.cos(2 * np.pi * fc1 * t)
    s2 = m2 * np.cos(2 * np.pi * fc2 * t)
    s3 = m3 * np.cos(2 * np.pi * fc3 * t)

    # FDM Composite Multiplexed Signal
    composite_fdm = s1 + s2 + s3

    # Receiver Demultiplexing via Bandpass Filters
    rec_s1 = butter_bandpass_filter(composite_fdm, 45, 75, fs)
    rec_s2 = butter_bandpass_filter(composite_fdm, 125, 155, fs)
    rec_s3 = butter_bandpass_filter(composite_fdm, 205, 235, fs)

    fig, axes = plt.subplots(4, 1, figsize=(10, 7), sharex=True)
    plt.subplots_adjust(hspace=0.4)
    axes[0].plot(t[:400], s1[:400], 'blue', label='Channel 1 (fc = 60 Hz)')
    axes[0].set_title('FDM Channel 1 Modulated Signal', fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(t[:400], s2[:400], 'green', label='Channel 2 (fc = 140 Hz)')
    axes[1].set_title('FDM Channel 2 Modulated Signal', fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[2].plot(t[:400], s3[:400], 'red', label='Channel 3 (fc = 220 Hz)')
    axes[2].set_title('FDM Channel 3 Modulated Signal', fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    axes[3].plot(t[:400], composite_fdm[:400], 'black', label='Composite Signal')
    axes[3].set_title('FDM Combined Composite Multiplexed Signal in Transmission Medium', fontweight='bold')
    axes[3].set_xlabel('Time (s)')
    axes[3].grid(True, alpha=0.3)

    fdm_file = "exp15/fdm_simulation.png"
    plt.savefig(fdm_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] FDM plot saved to: {fdm_file}")

    # -------------------------------------------------------------
    # 2. Time Division Multiplexing (TDM)
    # -------------------------------------------------------------
    print("\n2. Simulating Time Division Multiplexing (TDM)...")
    ch1_bits = [1, 0, 1, 1]
    ch2_bits = [0, 1, 0, 0]
    ch3_bits = [1, 1, 0, 1]

    # Interleave into TDM frames: Frame i = [Ch1_i, Ch2_i, Ch3_i]
    tdm_frames = []
    for i in range(len(ch1_bits)):
        tdm_frames.extend([ch1_bits[i], ch2_bits[i], ch3_bits[i]])

    print(f"  Channel 1 Data: {ch1_bits}")
    print(f"  Channel 2 Data: {ch2_bits}")
    print(f"  Channel 3 Data: {ch3_bits}")
    print(f"  TDM Multiplexed Stream: {tdm_frames}")

    # Demux
    demux_ch1 = tdm_frames[0::3]
    demux_ch2 = tdm_frames[1::3]
    demux_ch3 = tdm_frames[2::3]
    assert ch1_bits == demux_ch1 and ch2_bits == demux_ch2 and ch3_bits == demux_ch3

    fig, ax = plt.subplots(figsize=(10, 3.5))
    x_pos = np.arange(len(tdm_frames))
    colors = ['blue', 'green', 'red'] * len(ch1_bits)
    bars = ax.bar(x_pos, tdm_frames, color=colors, width=0.6, edgecolor='black')
    ax.set_title('Synchronous Time Division Multiplexing (TDM) Frame Structure', fontweight='bold')
    ax.set_xlabel('Time Slots (Ch 1: Blue, Ch 2: Green, Ch 3: Red)')
    ax.set_ylabel('Bit Value')
    ax.set_ylim(-0.2, 1.3)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"S{i+1}" for i in range(len(tdm_frames))])
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    tdm_file = "exp15/tdm_simulation.png"
    plt.savefig(tdm_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] TDM plot saved to: {tdm_file}")

    # -------------------------------------------------------------
    # 3. Wavelength Division Multiplexing (WDM)
    # -------------------------------------------------------------
    print("\n3. Simulating Wavelength Division Multiplexing (WDM)...")
    wavelengths = np.linspace(1250, 1650, 1000)
    # 3 Laser Optical Carriers (Gaussian spectra)
    opt1 = np.exp(-0.5 * ((wavelengths - 1310) / 4)**2)
    opt2 = np.exp(-0.5 * ((wavelengths - 1490) / 4)**2)
    opt3 = np.exp(-0.5 * ((wavelengths - 1550) / 4)**2)
    opt_composite = opt1 + opt2 + opt3

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(wavelengths, opt1, 'purple', linestyle='--', label='Laser 1: λ = 1310 nm (O-Band)')
    ax.plot(wavelengths, opt2, 'teal', linestyle='--', label='Laser 2: λ = 1490 nm (S-Band)')
    ax.plot(wavelengths, opt3, 'darkorange', linestyle='--', label='Laser 3: λ = 1550 nm (C-Band)')
    ax.plot(wavelengths, opt_composite, 'black', linewidth=1.5, label='Multiplexed Fiber Spectrum')
    ax.set_title('Wavelength Division Multiplexing (WDM) Optical Carrier Spectrum', fontweight='bold')
    ax.set_xlabel('Wavelength λ (nm)')
    ax.set_ylabel('Normalized Optical Power')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)

    wdm_file = "exp15/wdm_simulation.png"
    plt.savefig(wdm_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] WDM plot saved to: {wdm_file}")

    # -------------------------------------------------------------
    # 4. Direct Sequence Spread Spectrum (DSSS)
    # -------------------------------------------------------------
    print("\n4. Simulating Direct Sequence Spread Spectrum (DSSS)...")
    data_bits = np.array([1, -1, 1, -1])  # BPSK format (+1 and -1)
    barker_code = np.array([1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1])  # 11-chip Barker Code
    chips_per_bit = len(barker_code)

    # Spread data: multiply each bit by the 11-chip sequence
    spread_signal = np.repeat(data_bits, chips_per_bit) * np.tile(barker_code, len(data_bits))

    # Channel noise (AWGN)
    noise = np.random.normal(0, 0.4, len(spread_signal))
    received_signal = spread_signal + noise

    # Despreading via cross-correlation with identical Barker code
    despread_bits = []
    for i in range(len(data_bits)):
        segment = received_signal[i * chips_per_bit : (i + 1) * chips_per_bit]
        correlation = np.dot(segment, barker_code) / chips_per_bit
        recovered_bit = 1 if correlation > 0 else -1
        despread_bits.append(recovered_bit)

    print(f"  Transmitted Data Bits : {data_bits}")
    print(f"  Barker Chip Sequence  : {barker_code}")
    print(f"  Recovered Data Bits   : {despread_bits}")
    assert np.array_equal(data_bits, despread_bits), "DSSS despreading failure!"

    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    plt.subplots_adjust(hspace=0.4)
    axes[0].step(np.arange(len(data_bits)), data_bits, where='post', color='blue', linewidth=2)
    axes[0].set_title('1. Narrowband Original Data Signal', fontweight='bold')
    axes[0].set_ylim(-1.5, 1.5)
    axes[0].grid(True, alpha=0.3)

    axes[1].step(np.arange(len(spread_signal)), spread_signal, where='post', color='green', linewidth=1)
    axes[1].set_title('2. Wideband Spread DSSS Signal (Spread with 11-chip Barker Code)', fontweight='bold')
    axes[1].set_ylim(-1.5, 1.5)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(received_signal, color='red', alpha=0.8, label='Noisy Received')
    axes[2].set_title('3. Transmitted Signal with Channel Noise (AWGN)', fontweight='bold')
    axes[2].set_xlabel('Chip Index')
    axes[2].grid(True, alpha=0.3)

    dsss_file = "exp15/dsss_simulation.png"
    plt.savefig(dsss_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[*] DSSS plot saved to: {dsss_file}")
    print("=" * 70)

if __name__ == "__main__":
    run_multiplexing_simulator()
