# LaTeX Changes Cleaner

A robust Python tool designed to *flatten* LaTeX documents that use the `changes` package.

It automatically “accepts” all tracked changes (additions, replacements) and removes deletions, producing a clean `.tex` file ready for the next round of peer review or final publication.

---

## The Problem It Solves

When using regex find-and-replace in editors like Overleaf, simple patterns fail when the tracked text contains nested commands (e.g., `\deleted{text with \cite{ref}}`). The regex often matches the wrong closing brace, breaking the LaTeX code.

This tool uses a stack-based brace-matching algorithm to correctly identify the scope of every LaTeX command, ensuring complex, nested edits are handled safely.

---

## Features

- Accepts `\added{text}` → `text`
- Removes `\deleted{text}` → *(empty)*
- Resolves `\replaced{new}{old}` → `new`
- Flattens `\highlight{text}` → `text`
- **Batch processing:** Processes all `.tex` files in a given input directory
- **Safety:** Handles nested brackets (citations, bold text, math) inside change commands
- **Non-destructive:** Saves clean files to a separate output folder

---

## Usage

1. Clone this repository.
2. Ensure you have Python 3 installed.
3. Run the script:

    ```bash
    python cleaner.py
    ```

### First Run

If the `input` folder does not exist, the script will create it and ask you to place your files there.

### Subsequent Runs

Place your `.tex` files in the `input` folder and run the script again.  
Your clean files will appear in the `output` folder.

---

## Advanced Usage

You can specify custom folders if you prefer:

```bash
python cleaner.py ./my_custom_source ./my_custom_output
```

---

## Requirements

- Python 3.x
- No external dependencies (uses standard libraries only)

---

## License

MIT License.  
Feel free to use this for your academic submissions.