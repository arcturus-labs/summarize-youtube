#!/bin/bash

# Create a dedicated virtual environment
VENV_PATH="$HOME/.local/venvs/summarize_youtube"
python3 -m venv "$VENV_PATH"

# Install the package
"$VENV_PATH/bin/pip" install .

# Create a shell script to use the tool
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/summarize-youtube" << 'EOF'
#!/bin/bash
"$HOME/.local/venvs/summarize_youtube/bin/summarize-youtube" "$@"
EOF

chmod +x "$HOME/.local/bin/summarize-youtube"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo "Added ~/.local/bin to your PATH in ~/.zshrc"
    echo "Please run: source ~/.zshrc"
fi

echo "Global installation complete!"
echo "You can now use 'summarize-youtube' from anywhere" 