import re
import os
import argparse
import sys

def find_matching_brace(text, start_index):
    """
    Finds the index of the matching closing brace '}' for the opening brace '{'
    located at start_index.
    """
    if start_index >= len(text) or text[start_index] != '{':
        return -1
    
    stack = 1
    i = start_index + 1
    length = len(text)
    
    while i < length:
        char = text[i]
        
        # 1. Handle Escape Sequences (e.g. \{, \\, \%)
        if char == '\\':
            # Skip the backslash AND the next character
            i += 2
            continue
        
        # 2. Handle Comments
        if char == '%':
            # Skip everything until the next newline
            while i < length and text[i] != '\n':
                i += 1
            # Now i is at \n (or end of string). 
            # We continue the outer loop. The next iteration will read \n 
            # and process it normally (incrementing i).
            continue

        # 3. Handle Braces
        if char == '{':
            stack += 1
        elif char == '}':
            stack -= 1
            
        if stack == 0:
            return i
        
        i += 1
        
    return -1

def process_content(content):
    """
    Iteratively finds changes package commands and resolves them.
    REGEX UPDATE: Now allows whitespace before the brace (e.g., \added {text})
    """
    
    # 1. Handle \added{...} -> ...
    while True:
        match = re.search(r'\\added\s*\{', content)
        if not match: break
        
        start_cmd = match.start()
        start_brace = match.end() - 1 
        end_brace = find_matching_brace(content, start_brace)
        
        if end_brace == -1:
            print("  [Warning] Unmatched brace in \\added command. Skipping rest of file.")
            break
            
        inner_text = content[start_brace+1 : end_brace]
        content = content[:start_cmd] + inner_text + content[end_brace+1:]

    # 2. Handle \deleted{...} -> (empty string)
    while True:
        match = re.search(r'\\deleted\s*\{', content)
        if not match: break
        
        start_cmd = match.start()
        start_brace = match.end() - 1
        end_brace = find_matching_brace(content, start_brace)
        
        if end_brace == -1:
            print("  [Warning] Unmatched brace in \\deleted command. Skipping rest of file.")
            break
            
        content = content[:start_cmd] + content[end_brace+1:]

    # 3. Handle \replaced{new}{old} -> new
    while True:
        match = re.search(r'\\replaced\s*\{', content)
        if not match: break
        
        start_cmd = match.start()
        
        # First argument (New Text)
        start_brace_1 = match.end() - 1
        end_brace_1 = find_matching_brace(content, start_brace_1)
        
        if end_brace_1 == -1: break

        # Second argument (Old Text)
        remaining = content[end_brace_1+1:]
        
        # Find first '{' that isn't whitespace
        next_brace_rel = -1
        for idx, c in enumerate(remaining):
            if c.isspace(): continue
            if c == '{':
                next_brace_rel = idx
                break
            break 
        
        if next_brace_rel == -1: break
        
        start_brace_2 = end_brace_1 + 1 + next_brace_rel
        end_brace_2 = find_matching_brace(content, start_brace_2)

        if end_brace_2 == -1: break
        
        new_text = content[start_brace_1+1 : end_brace_1]
        
        # Replace the whole \replaced{new}{old} block with just 'new'
        content = content[:start_cmd] + new_text + content[end_brace_2+1:]

    # 4. Handle \highlight{...} -> ...
    while True:
        match = re.search(r'\\highlight\s*\{', content)
        if not match: break
        
        start_cmd = match.start()
        start_brace = match.end() - 1
        end_brace = find_matching_brace(content, start_brace)
        
        if end_brace == -1: break
            
        inner_text = content[start_brace+1 : end_brace]
        content = content[:start_cmd] + inner_text + content[end_brace+1:]

    return content

def clean_directory(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' not found.")
        os.makedirs(input_dir)
        print(f"Created '{input_dir}' for you. Please place your .tex files inside it and run the script again.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    files_processed = 0
    tex_files_found = False

    for filename in os.listdir(input_dir):
        if filename.endswith(".tex"):
            tex_files_found = True
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"Processing: {filename}...")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                
                cleaned_content = process_content(raw_content)
                
                # Comment out changes package import
                cleaned_content = re.sub(r'(\\usepackage(\[.*?\])?\{changes\})', r'% \1', cleaned_content)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                files_processed += 1
                
            except Exception as e:
                print(f"  [Error] Failed to process {filename}: {e}")
    
    if not tex_files_found:
        print(f"No .tex files found in '{input_dir}/'. Please add your files there.")
    else:
        print(f"\nDone! {files_processed} .tex files processed.")
        print(f"Clean files are located in: {output_dir}/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten LaTeX files by accepting 'changes' package edits.")
    parser.add_argument("input_dir", nargs='?', default='input', help="Path to source folder")
    parser.add_argument("output_dir", nargs='?', default='output', help="Path to output folder")
    args = parser.parse_args()
    
    print(f"--- LaTeX Changes Cleaner ---")
    clean_directory(args.input_dir, args.output_dir)