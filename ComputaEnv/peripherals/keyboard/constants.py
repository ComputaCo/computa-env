NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
ALPHABET = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
MISCELLANEOUS = ["`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/"]
SHIFT_MISCELLANEOUS = [
    "~",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "_",
    "+",
    "{",
    "}",
    "|",
    ":",
    '"',
    "<",
    ">",
    "?",
]
MODIFIERS = ["alt", "ctrl", "shift", "windows"]
SPECIAL = [
    "backspace",
    "caps lock",
    "delete",
    "down",
    "end",
    "enter",
    "escape",
    "home",
    "insert",
    "left",
    "page down",
    "page up",
    "right",
    "tab",
    "up",
]
# these keys are what you get when you do shift+MISCELLANEOUS
FUNCTION_KEYS = [
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
]

STANDARD_ENGLISH_US_KEYBOARD_KEYS = (
    NUMBERS + ALPHABET + MISCELLANEOUS + MODIFIERS + SPECIAL + FUNCTION_KEYS
)
EXTENDED_ENGLISH_US_KEYBOARD_KEYS = (
    STANDARD_ENGLISH_US_KEYBOARD_KEYS + SHIFT_MISCELLANEOUS
)

# It looks like these characters should cover the requirements for most cases
# https://www.gaijin.at/en/infos/ascii-ansi-character-table
ASCII_128_KEYS = list(range(128))
