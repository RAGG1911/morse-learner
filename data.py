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

def is_supported(char: str) -> bool:
    """Return True if the character has a morse translation."""
    return char.upper() in MORSE_CODE

def get_morse(char: str) -> str | None:
    """Return the morse code for a character, or None if unsupported."""
    return MORSE_CODE.get(char.upper())


def get_char(morse: str) -> str | None:
    """Return the character for a morse string, or None if not found."""
    return REVERSE_MORSE.get(morse)

def normalize_input(text: str) -> str:
    """Strip unsupperted characters, uppercase, collapse whitespace"""
    text = text.upper().strip()
    text = ' '.join(text.split())
    return ''.join(c for c in text if is_supported(c))

def encode(text: str) -> str:
    """Convert a string to morse. Words separated by ' / '"""
    text = normalize_input(text)
    words = text.split(' ')
    encoded_words = []
    for word in words:
        encoded_words.append(' '.join(get_morse(c) for c in word))
    return ' / '.join(encoded_words)

def decode(morse: str) -> str:
    """Convert a morse string back to text. '/' is the word separator"""
    words =morse.strip().split(' / ')
    decoded_words = []
    for word in words:
        symbols = word.strip().split(' ')
        decoded_words.append(''.join(get_char(s) or '?' for s in symbols))
    return ' '.join(decoded_words)

def compare_answers(expected: str, given: str) -> bool:
    """Case-insensitive comparison ignoring extra whitespace"""
    return expected.strip().upper() == given.strip().upper()

def get_display_data() -> list[tuple[str, str, str]]:
    """Returns sorted (char, morse, category) tuples for the UI."""
    def category(char):
        if char.isalpha():   return 'letter'
        if char.isdigit():   return 'number'
        return 'punctuation'

    def sort_key(item):
        char = item[0]
        if char.isalpha():  return (0, char)
        if char.isdigit():  return (1, char)
        return (2, char)

    data = [
        (char, morse, category(char))
        for char, morse in MORSE_CODE.items()
        if char != ' '
    ]
    return sorted(data, key=sort_key)

