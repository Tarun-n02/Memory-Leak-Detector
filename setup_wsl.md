# WSL Setup Guide for Memory Leak Detector

## Step 1: Install GCC and Valgrind in WSL

Open WSL (Ubuntu) terminal and run these commands:

```bash
sudo apt update
sudo apt install -y gcc valgrind
```

Enter your WSL password when prompted.

## Step 2: Verify Installation

Check if the tools are installed:

```bash
gcc --version
valgrind --version
```

## Step 3: Test with Example

1. Navigate to your project directory in WSL:
   ```bash
   cd /mnt/c/Users/t-jkoppula/Downloads/Memory-Leak-Detector-main
   ```

2. Compile an example:
   ```bash
   gcc -g -o example1 example1.c
   ```

3. Run Valgrind:
   ```bash
   valgrind --leak-check=full --track-origins=yes ./example1
   ```

## Alternative: Use the GUI with WSL

The Python GUI script can automatically use WSL if configured. Just ensure:
- WSL is installed (✓ You have Ubuntu)
- GCC and Valgrind are installed in WSL (needs setup)
- The script will detect and use WSL automatically

## Quick Install Command

Open **Ubuntu** from Start Menu and paste:
```bash
sudo apt update && sudo apt install -y gcc valgrind
```
