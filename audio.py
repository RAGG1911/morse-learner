import numpy as np
import pygame
import pygame.sndarray
from data import get_morse

SAMPLE_RATE = 44100
FREQUENCY   = 700
_wpm        = 20

pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
_CHANNELS = pygame.mixer.get_init()[2]

def _dot_duration() -> float:
    return 1.2 / _wpm

def set_speed(wpm: int) -> None:
    global _wpm
    _wpm = wpm

def _make_tone(duration_s: float) -> np.ndarray:
    num_samples = int(SAMPLE_RATE * duration_s)
    t = np.linspace(0, duration_s, num_samples, endpoint=False)
    wave = (32767 * 0.5 * np.sin(2 * np.pi * FREQUENCY * t)).astype(np.int16)
    fade = min(int(SAMPLE_RATE * 0.004), num_samples // 10)
    if fade > 0:
        wave[:fade]  = (wave[:fade]  * np.linspace(0, 1, fade)).astype(np.int16)
        wave[-fade:] = (wave[-fade:] * np.linspace(1, 0, fade)).astype(np.int16)
    if _CHANNELS == 2:
        wave = np.column_stack((wave, wave))  # duplicate to stereo
    return wave

def _make_silence(duration_s: float) -> np.ndarray:
    num_samples = int(SAMPLE_RATE * duration_s)
    if _CHANNELS == 2:
        return np.zeros((num_samples, 2), dtype=np.int16)
    return np.zeros(num_samples, dtype=np.int16)

def _build_char_audio(morse: str) -> np.ndarray:
    dot = _dot_duration()
    segments = []
    for i, symbol in enumerate(morse):
        if symbol == '.':
            segments.append(_make_tone(dot))
        elif symbol == '-':
            segments.append(_make_tone(dot * 3))
        if i < len(morse) - 1:
            segments.append(_make_silence(dot))
    segments.append(_make_silence(0.05))
    return np.concatenate(segments)

def _play_blocking(audio: np.ndarray) -> None:
    audio = np.ascontiguousarray(audio)
    sound = pygame.sndarray.make_sound(audio)
    sound.play()
    duration_ms = int(audio.shape[0] / SAMPLE_RATE * 1000) + 50
    pygame.time.wait(duration_ms)

def play_char(char: str) -> None:
    morse = get_morse(char)
    if not morse:
        return
    _play_blocking(_build_char_audio(morse))

def play_word(word: str) -> None:
    dot = _dot_duration()
    segments = []
    for i, char in enumerate(word.upper()):
        morse = get_morse(char)
        if not morse:
            continue
        segments.append(_build_char_audio(morse))
        if i < len(word) - 1:
            segments.append(_make_silence(dot * 3))
    if segments:
        _play_blocking(np.concatenate(segments))

def play_string(text: str) -> None:
    dot = _dot_duration()
    words = text.upper().split()
    segments = []
    for i, word in enumerate(words):
        word_segments = []
        for j, char in enumerate(word):
            morse = get_morse(char)
            if not morse:
                continue
            word_segments.append(_build_char_audio(morse))
            if j < len(word) - 1:
                word_segments.append(_make_silence(dot * 3))
        if word_segments:
            segments.append(np.concatenate(word_segments))
        if i < len(words) - 1:
            segments.append(_make_silence(dot * 7))
    if segments:
        _play_blocking(np.concatenate(segments))

def stop_audio() -> None:
    pygame.mixer.stop()