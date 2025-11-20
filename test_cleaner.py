import pytest
from cleaner import process_content

# Pytest allows us to use simple assert statements
# and simple functions instead of classes.

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

def test_nested_braces_bold():
    # \added{... \textbf{...} ...}
    raw = r"Start \added{add \textbf{bold}} end."
    expected = r"Start add \textbf{bold} end."
    assert process_content(raw) == expected

def test_escaped_braces():
    # \{ and \} should not be counted as structural braces
    raw = r"Set \added{A = \{1, 2\}} end."
    expected = r"Set A = \{1, 2\} end."
    assert process_content(raw) == expected

def test_escaped_backslash_before_brace():
    # Case: \\ is a newline, followed by a real brace group { Group }
    # Input must have a matching closing brace to be valid.
    raw = r"Start \added{Line \\{ Group }} end."
    expected = r"Start Line \\{ Group } end."
    assert process_content(raw) == expected

def test_comment_with_braces():
    # % } should be ignored inside the changes command
    raw = "Start \\added{content % comment with closing brace } \n} end."
    # The brace inside the comment is ignored by parser.
    # The parser finds the final brace after \n.
    # The content extracted includes the comment.
    expected = "Start content % comment with closing brace } \n end."
    assert process_content(raw) == expected

def test_multiple_changes_inline():
    raw = r"\added{One} \deleted{Two} \replaced{Three}{Four}"
    expected = r"One  Three"
    assert process_content(raw) == expected

def test_multiline():
    raw = "\\added{Line one\nLine two}"
    expected = "Line one\nLine two"
    assert process_content(raw) == expected

def test_nested_changes_commands():
    # While 'changes' package struggles with this, the script should just accept them
    raw = r"\added{Outer \added{Inner}}"
    expected = r"Outer Inner"
    assert process_content(raw) == expected
    
def test_whitespace_in_replaced():
    # \replaced {new} {old}
    raw = r"\replaced {new} {old}"
    expected = r"new"
    assert process_content(raw) == expected