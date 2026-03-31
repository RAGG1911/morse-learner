MORSE_CODE = {
    # Letters
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.',    'F': '..-.', 'G': '--.',  'H': '....',
    'I': '..',   'J': '.---', 'K': '-.-',  'L': '.-..',
    'M': '--',   'N': '-.',   'O': '---',  'P': '.--.',
    'Q': '--.-', 'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    # Numbers
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    # Punctuation
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.',  ')': '-.--.-',
    '&': '.-...',  ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.',  '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-','@': '.--.-.', ' ': '/'
}

# Reverse lookup table — built once at import time
REVERSE_MORSE = {v: k for k, v in MORSE_CODE.items()}


def get_morse(char: str) -> str | None:
    """Return the morse code for a character, or None if unsupported."""
    return MORSE_CODE.get(char.upper())


def get_char(morse: str) -> str | None:
    """Return the character for a morse string, or None if not found."""
    return REVERSE_MORSE.get(morse)


def is_supported(char: str) -> bool:
    """Return True if the character has a morse translation."""
    return char.upper() in MORSE_CODE