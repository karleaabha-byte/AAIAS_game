"""
sounds.py - Generate simple sound effects dynamically using numpy + scipy.

These are synthesized in-memory, so no external audio files needed.
"""
import io
import numpy as np
from scipy.io import wavfile
import streamlit as st


def generate_beep(frequency=1000, duration=0.2, sample_rate=22050):
    """Generate a simple beep tone."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t) * 0.3
    wave = (wave * 32767).astype(np.int16)
    
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, wave)
    buffer.seek(0)
    return buffer


def typewriter_click():
    """Typewriter key click sound."""
    return generate_beep(frequency=2000, duration=0.05)


def suspicion_whoosh():
    """Whoosh/ascending tone for suspicion increase."""
    sample_rate = 22050
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration))
    freq = np.linspace(800, 1400, len(t))
    wave = np.sin(2 * np.pi * freq * t) * 0.3
    wave = (wave * 32767).astype(np.int16)
    
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, wave)
    buffer.seek(0)
    return buffer


def contradiction_alert():
    """Sharp alert for contradiction found."""
    sample_rate = 22050
    duration = 0.15
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave1 = np.sin(2 * np.pi * 1200 * t)
    wave2 = np.sin(2 * np.pi * 900 * t)
    wave = (wave1 + wave2) * 0.25
    wave = (wave * 32767).astype(np.int16)
    
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, wave)
    buffer.seek(0)
    return buffer


def success_chime():
    """Success/victory chime."""
    sample_rate = 22050
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    # C, E, G arpeggio
    freq_progression = np.concatenate([
        np.full(len(t)//3, 262),  # C
        np.full(len(t)//3, 330),  # E
        np.full(len(t)//3, 392),  # G
    ])
    wave = np.sin(2 * np.pi * freq_progression[:len(t)] * t) * 0.3
    wave = (wave * 32767).astype(np.int16)
    
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, wave)
    buffer.seek(0)
    return buffer
