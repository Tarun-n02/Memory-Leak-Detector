#!/bin/bash
# WSL Setup Script for Memory Leak Detector
# Run this script inside WSL/Ubuntu terminal

echo "=========================================="
echo "Memory Leak Detector - WSL Setup"
echo "=========================================="
echo ""

# Check if running in WSL
if ! grep -qi microsoft /proc/version; then
    echo "⚠ This script must be run inside WSL/Ubuntu terminal"
    exit 1
fi

echo "📦 Updating package list..."
sudo apt update

echo ""
echo "📦 Installing GCC compiler..."
sudo apt install -y gcc

echo ""
echo "📦 Installing Valgrind..."
sudo apt install -y valgrind

echo ""
echo "✅ Installation complete!"
echo ""
echo "Verifying installation:"
echo "----------------------"

if command -v gcc &> /dev/null; then
    echo "✓ GCC: $(gcc --version | head -n1)"
else
    echo "✗ GCC installation failed"
fi

if command -v valgrind &> /dev/null; then
    echo "✓ Valgrind: $(valgrind --version | head -n1)"
else
    echo "✗ Valgrind installation failed"
fi

echo ""
echo "=========================================="
echo "Setup complete! You can now use the GUI."
echo "=========================================="
