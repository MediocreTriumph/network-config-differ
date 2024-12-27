#!/usr/bin/env python3
import difflib
import argparse
from pathlib import Path
import sys

def validate_files(old_file, new_file):
    if not old_file.exists():
        raise FileNotFoundError(f"The old file does not exist: {old_file}")
    if not new_file.exists():
        raise FileNotFoundError(f"The new file does not exist: {new_file}")
    if old_file.suffix != new_file.suffix:
        raise ValueError("The two files have different extensions. Please ensure you're comparing files of the same type.")
    if old_file.stat().st_size == 0:
        raise ValueError(f"The old file is empty: {old_file}")
    if new_file.stat().st_size == 0:
        raise ValueError(f"The new file is empty: {new_file}")

def create_diff_file(old_file, new_file, diff_file, context_lines=10):
    try:
        with open(old_file, 'r') as f1, open(new_file, 'r') as f2:
            old_lines = f1.readlines()
            new_lines = f2.readlines()
    except UnicodeDecodeError:
        raise ValueError("One or both files are not text files or use an unsupported encoding.")

    matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
    
    with open(diff_file, 'w') as f:
        for opcode in matcher.get_opcodes():
            tag, i1, i2, j1, j2 = opcode
            
            if tag == 'replace':
                old_block = old_lines[max(0, i1-context_lines):min(len(old_lines), i2+context_lines)]
                new_block = new_lines[max(0, j1-context_lines):min(len(new_lines), j2+context_lines)]
                
                for line in old_lines[i1:i2]:
                    if any(difflib.SequenceMatcher(None, line, new_line).ratio() > 0.8 for new_line in new_block):
                        f.write("(Modified): " + line.rstrip() + " # Modified\n")
                    else:
                        f.write("(Removed): " + line)
                
                for line in new_lines[j1:j2]:
                    if all(difflib.SequenceMatcher(None, line, old_line).ratio() <= 0.8 for old_line in old_block):
                        f.write("(Added): " + line)
            
            elif tag == 'delete':
                for line in old_lines[i1:i2]:
                    f.write("(Removed): " + line)
            
            elif tag == 'insert':
                for line in new_lines[j1:j2]:
                    f.write("(Added): " + line)
            
            elif tag == 'equal':
                if i2 - i1 <= 2:
                    for line in old_lines[i1:i2]:
                        f.write("(Context): " + line)

        f.write('\n')

def main():
    parser = argparse.ArgumentParser(description='Generate a diff file between two configuration files.')
    parser.add_argument('old_file', type=str, help='Path to the old configuration file')
    parser.add_argument('new_file', type=str, help='Path to the new configuration file')
    parser.add_argument('--output', type=str, help='Path to the output diff file (optional)')
    parser.add_argument('--context', type=int, default=10, help='Number of context lines (default: 10)')

    args = parser.parse_args()

    old_file = Path(args.old_file)
    new_file = Path(args.new_file)

    try:
        validate_files(old_file, new_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not args.output:
        old_timestamp = old_file.stem.split('_')[-1]
        new_timestamp = new_file.stem.split('_')[-1]
        diff_file = f"{old_timestamp}_{new_timestamp}-diff.txt"
    else:
        diff_file = args.output

    try:
        create_diff_file(str(old_file), str(new_file), diff_file, args.context)
        print(f"Diff file created: {diff_file}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()