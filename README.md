# Network Configuration Differ

A Python-based tool for generating detailed diffs between network device configuration files. This tool highlights changes in configuration files while providing context and intelligent detection of modified lines.

## Features

- Identifies added, removed, and modified lines
- Intelligent detection of modified lines using similarity matching
- Configurable context lines around changes
- Support for different output formats
- Validation of input files

## Installation

```bash
git clone https://github.com/MediocreTriumph/network-config-differ.git
cd network-config-differ
```

## Usage

Basic usage:
```bash
python config_differ.py old_config.txt new_config.txt
```

With custom output file and context lines:
```bash
python config_differ.py old_config.txt new_config.txt --output custom_diff.txt --context 5
```

### Arguments

- `old_file`: Path to the old configuration file
- `new_file`: Path to the new configuration file
- `--output`: Path to the output diff file (optional)
- `--context`: Number of context lines (default: 10)

## Output Format

The diff file uses the following format:
- `(Added): ` - New lines in the configuration
- `(Removed): ` - Lines removed from the configuration
- `(Modified): ` - Lines that were changed (with # Modified suffix)
- `(Context): ` - Unchanged lines around the modifications