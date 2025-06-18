# Converting Python Projects to Command-Line Utilities

This guide explains how to convert any Python project with a command-line interface into an installable command-line utility that can be used globally on your system.

## Project Structure

Here's the minimal structure needed to create an installable command-line utility:

```
your_project/
├── pyproject.toml
├── your_package/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
└── README.md
```

### Key Files

1. **cli.py** - Your main CLI implementation
2. **__main__.py** - Entry point that calls your CLI
3. **pyproject.toml** - Project configuration and dependencies

## Step-by-Step Guide

### 1. Create the Basic Structure

```bash
mkdir -p your_project/your_package
touch your_project/your_package/__init__.py
touch your_project/your_package/__main__.py
touch your_project/your_package/cli.py
touch your_project/pyproject.toml
```

### 2. Set Up Your CLI File (cli.py)

```python
# your_package/cli.py

def main():
    """Your CLI implementation here."""
    print("Hello from your CLI!")

if __name__ == "__main__":
    main()
```

### 3. Create the Entry Point (__main__.py)

```python
# your_package/__main__.py

from .cli import main

if __name__ == "__main__":
    main()
```

### 4. Configure Your Project (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "your_package"
version = "0.1.0"
description = "Description of your tool"
requires-python = ">=3.8"
dependencies = [
    # Add your dependencies here
]

[project.scripts]
your_command = "your_package.cli:main"
```

### 5. Installation Scripts

#### Development Installation

Create a script called `install_dev.sh`:

```bash
#!/bin/bash

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e .

echo "Development installation complete!"
echo "Run your command with: your_command"
```

#### Global Installation

Create a script called `install_global.sh`:

```bash
#!/bin/bash

# Create a dedicated virtual environment
VENV_PATH="$HOME/.local/venvs/your_package"
python3 -m venv "$VENV_PATH"

# Install the package
"$VENV_PATH/bin/pip" install .

# Create a shell script to use the tool
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/your_command" << 'EOF'
#!/bin/bash
"$HOME/.local/venvs/your_package/bin/your_command" "$@"
EOF

chmod +x "$HOME/.local/bin/your_command"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo "Added ~/.local/bin to your PATH in ~/.zshrc"
    echo "Please run: source ~/.zshrc"
fi

echo "Global installation complete!"
echo "You can now use 'your_command' from anywhere"
```

### 6. Make the Scripts Executable

```bash
chmod +x install_dev.sh install_global.sh
```

## Usage

### Development Installation
```bash
./install_dev.sh
```

### Global Installation
```bash
./install_global.sh
```

## Optional Components

The following components are optional but recommended for larger projects:

- **tests/** - Directory for your test files
- **models.py** - For data models and validation
- **exceptions.py** - For custom exception handling
- **requirements.txt** - For development dependencies

## Notes

1. Replace `your_package` with your actual package name
2. Replace `your_command` with your desired command name
3. Update the Python version requirement in pyproject.toml if needed
4. Add your project's dependencies to pyproject.toml
5. The global installation script assumes you're using zsh. For bash, change `.zshrc` to `.bashrc`

## Troubleshooting

If your command isn't found after installation:

1. Check if the virtual environment is activated (for development installation)
2. Verify that `~/.local/bin` is in your PATH
3. Try running `which your_command` to see where the command is installed
4. Check the permissions of the installed scripts

## Uninstallation

### Development Installation
```bash
pip uninstall your_package
rm -rf .venv
```

### Global Installation
```bash
rm -rf ~/.local/venvs/your_package
rm ~/.local/bin/your_command
``` 