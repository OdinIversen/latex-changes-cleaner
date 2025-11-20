import pytest
from cleaner import process_content

# --- Basic Command Tests ---

def test_basic_added():
    raw = r"This is \added{new} text."
    expected = r"This is new text."
    assert process_content(raw) == expected

def test_basic_deleted():
    raw = r"This is \deleted{old} text."
    expected = r"This is  text."
    assert process_content(raw) == expected

def test_basic_replaced():
    raw = r"This is \replaced{new}{old} text."
    expected = r"This is new text."
    assert process_content(raw) == expected

def test_highlight():
    # Added this missing test case
    raw = r"This is \highlight{highlighted} text."
    expected = r"This is highlighted text."
    assert process_content(raw) == expected

# --- Structural Tests (The "Hard" Stuff) ---

def test_nested_braces_bold():
    # Ensures \textbf{} doesn't close the \added{} command early
    raw = r"Start \added{add \textbf{bold}} end."
    expected = r"Start add \textbf{bold} end."
    assert process_content(raw) == expected

def test_nested_changes_commands():
    # Handles recursive changes commands
    raw = r"\added{Outer \added{Inner}}"
    expected = r"Outer Inner"
    assert process_content(raw) == expected

def test_multiline():
    # Handles commands spanning newlines
    raw = "\\added{Line one\nLine two}"
    expected = "Line one\nLine two"
    assert process_content(raw) == expected

def test_multiple_changes_inline():
    # Handles multiple commands on one line
    raw = r"\added{One} \deleted{Two} \replaced{Three}{Four}"
    expected = r"One  Three"
    assert process_content(raw) == expected

# --- Edge Cases (Escaping, Comments, Whitespace) ---

def test_escaped_braces():
    # \{ and \} are printable characters, NOT syntax
    raw = r"Set \added{A = \{1, 2\}} end."
    expected = r"Set A = \{1, 2\} end."
    assert process_content(raw) == expected

def test_escaped_backslash_before_brace():
    # \\ is a newline, so the following { IS syntax
    raw = r"Start \added{Line \\{ Group }} end."
    expected = r"Start Line \\{ Group } end."
    assert process_content(raw) == expected

def test_comment_with_braces():
    # Braces inside comments % } must be ignored
    raw = "Start \\added{content % comment with closing brace } \n} end."
    expected = "Start content % comment with closing brace } \n end."
    assert process_content(raw) == expected
    
def test_whitespace_in_replaced():
    # Allows spaces like \replaced {new} {old}
    raw = r"\replaced {new} {old}"
    expected = r"new"
    assert process_content(raw) == expected