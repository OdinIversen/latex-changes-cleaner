LaTeX Changes Cleaner
A robust Python tool designed to "flatten" LaTeX documents that use the `changes` package.

It automatically "accepts" all tracked changes (additions, replacements) and removes deletions, producing a clean `.tex` file ready for the next round of peer review or final publication.

## The Problem it Solves

When using regex find-and-replace in editors like Overleaf, simple patterns fail when the tracked text contains nested commands (e.g., `\deleted{text with \cite{ref}}`). The regex often matches the wrong closing brace, breaking the LaTeX code.

This tool uses a parser-style brace matching algorithm to correctly identify the scope of every LaTeX command. It correctly handles:

*   Nested braces (`\textbf{...}`)
*   Escaped braces (`\{`, `\}`)
*   Comments containing braces (`% }`)

## Folder Structure

The script expects (and will create) a simple structure. **Note:** The `input` and `output` folders are ignored by Git to protect your private paper content.

```text
latex-changes-cleaner/
├── cleaner.py         # The script
├── test_cleaner.py    # Unit tests
├── input/             # [Put your .tex files here]
├── output/            # [Clean files appear here]
├── README.md
└── .gitignore
```

## Usage

1.  Clone this repository.
2.  Ensure you have Python 3 installed.
3.  Run the script:

    ```bash
    python cleaner.py
    ```

*   **First Run:** The script will create the `input/` folder for you.
*   **Add Files:** Copy your `.tex` files into the `input/` folder.
*   **Process:** Run the script again. Your clean files will be generated in the `output/` folder.

### Advanced Usage

You can override the default folders if you prefer:

```bash
python cleaner.py ./my_custom_source ./my_custom_output
```

## Testing

To ensure the script works correctly before applying it to your important documents, you can run the included test suite. This checks edge cases like escaped characters, math mode, and comments.

```bash
python test_cleaner.py
```

## Requirements

*   Python 3.x
*   No external dependencies (uses standard libraries only).

## License

MIT License. Feel free to use this for your academic submissions.
