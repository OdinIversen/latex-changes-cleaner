# LaTeX Changes Cleaner

A robust Python tool designed to "flatten" LaTeX documents that use the `changes` package.

It automatically "accepts" all tracked changes (additions, replacements) and removes deletions, producing a clean `.tex` file ready for the next round of peer review or final publication.

## Features

*   **Safeguards:** By default, it does not overwrite existing files in the output folder.
*   **Detailed Feedback:** Reports which files are converted and which are skipped.
*   **Parser Logic:** Handles nested braces (`\textbf{...}`), escaped braces (`\{`), and comments (`%`).

## Usage

Run the script:

```bash
python cleaner.py
```

**Default Behavior:**

*   Reads from `input/`
*   Writes to `output/`
*   Skips files if they already exist in `output/` to prevent accidental data loss.

**To Overwrite Files (Force Mode):**

If you want to update your clean files after making changes to the input, use the `--force` (or `-f`) flag:

```bash
python cleaner.py --force
```

## Folder Structure

```text
latex-changes-cleaner/
├── cleaner.py         # The script
├── test_cleaner.py    # Unit tests
├── input/             # [Put your .tex files here]
├── output/            # [Clean files appear here]
├── README.md
└── .gitignore
```

## Testing

To run the included test suite:

```bash
pip install pytest
pytest
```

## License

MIT License.