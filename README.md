# LaTeX Changes Cleaner

A robust Python tool designed to "flatten" LaTeX documents that use the `changes` package.

It automatically "accepts" all tracked changes (additions, replacements) and removes deletions, producing a clean `.tex` file ready for the next round of peer review or final publication.

## The Problem it Solves

When using regex find-and-replace in editors like Overleaf, simple patterns fail when the tracked text contains nested commands (e.g., `\deleted{text with \cite{ref}}`). The regex often matches the wrong closing brace, breaking the LaTeX code.

This tool uses a stack-based brace matching algorithm to correctly identify the scope of every LaTeX command, ensuring complex, nested edits are handled safely.

## Folder Structure

The script expects (and will create) a simple structure. Note: The `input` and `output` folders are ignored by Git to protect your private paper content.

```
latex-changes-cleaner/
├── cleaner.py         # The script
├── input/             # [Put your .tex files here]
├── output/            # [Clean files appear here]
├── README.md
└── .gitignore
```

## Features

- Accepts `\added{text}` → `text`
- Removes `\deleted{text}` → (empty)
- Resolves `\replaced{new}{old}` → `new`
- Flattens `\highlight{text}` → `text`
- **Batch Processing**: Processes all `.tex` files in the `input` directory.
- **Safety**: Handles nested brackets (citations, bold text, math) inside change commands.

## Usage

1. Clone this repository.
2. Ensure you have Python 3 installed.
3. Run the script:

    ```bash
    python cleaner.py
    ```

4. **First Run**: The script will create the `input/` folder for you.
5. **Add Files**: Copy your `.tex` files into the `input/` folder.
6. **Process**: Run the script again. Your clean files will be generated in the `output/` folder.

### Advanced Usage

You can override the default folders if you prefer:

```bash
python cleaner.py ./my_custom_source ./my_custom_output
```

## Requirements

- Python 3.x
- No external dependencies (uses standard libraries only).

## License

MIT License. Feel free to use this for your academic submissions.
