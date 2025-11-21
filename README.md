# Memory Leak Detector

A graphical application to detect memory leaks in C programs using Valgrind. Designed for Windows with WSL (Windows Subsystem for Linux), with a simpler version available for Linux users.

---

## Features

- **Easy-to-use graphical interface** with file browser
- **Automatic tool detection** - checks for GCC and Valgrind availability
- **Automatic C program compilation** with debugging symbols (-g flag)
- **Memory leak detection** with detailed Valgrind analysis
- **Clear, formatted output** showing memory issues and leak types
- **WSL integration** for Windows users
- **Status bar** showing current operation status
- **Color-coded buttons** for better UX
- **Two versions**: Full-featured (Windows/WSL) and lightweight (Linux)

---

## Prerequisites

- **Python 3.6+** with **tkinter** library
  - Check if tkinter is installed: `python -c "import tkinter"`
- **Windows 10/11** (for Windows version) or **Linux** (for Linux version)
- **WSL** (Windows Subsystem for Linux) - for Windows users
- **GCC** (C compiler) - installed in WSL or natively
- **Valgrind** (memory analysis tool) - installed in WSL or natively

---

## Installation

### For Windows Users

#### 1. Install WSL

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart your computer when prompted.

#### 2. Install GCC and Valgrind in WSL

**Option A: Use the automated setup script**

Open Ubuntu from Start Menu and navigate to the project directory, then run:

```bash
bash setup_wsl.sh
```

**Option B: Manual installation**

Open Ubuntu from Start Menu and run:

```bash
sudo apt update && sudo apt install -y gcc valgrind
```

For detailed instructions, see [`setup_wsl.md`](setup_wsl.md).

#### 3. Install Python (if not already installed)

Download from [python.org](https://www.python.org/downloads/) and ensure tkinter is included (it's usually bundled by default).

### For Linux Users

Install the required packages:

```bash
sudo apt update
sudo apt install -y gcc valgrind python3 python3-tk
```

---

## Usage

### Choose Your Version

**For Windows (with WSL):**
```powershell
python valgrindGUI_windows.py
```

**For Linux:**
```bash
python3 valgrindGUI.py
```

### Using the GUI

1. **Tool Detection** - On startup, the application checks for available tools
2. **Browse** - Click "Browse" to select your C source file (`.c`)
3. **Compile C File** - Compiles your program with debugging symbols
4. **Analyze Memory** - Runs Valgrind to detect memory leaks
5. **Review Results** - Check the formatted output for leak information
6. **Clear Output** - Clears the display and re-checks tool availability

---

## Understanding Output

### No Memory Leaks

```
✓ RESULT: No memory leaks detected!
Memory usage: total heap usage: 3 allocs, 3 frees, 4,120 bytes allocated
```

All memory was properly freed.

### Memory Leaks Detected

```
⚠ RESULT: Memory leaks detected!

Leak Summary:
  Definitely lost: 48 bytes in 1 blocks
  Possibly lost: 24 bytes in 3 blocks
```

**Leak Types:**
- **Definitely lost** - Memory never freed (must fix)
- **Indirectly lost** - Memory lost due to parent pointer loss (must fix)
- **Possibly lost** - Potential leak (should investigate)
- **Still reachable** - Memory accessible at exit (usually OK)

---

## Example Programs

### example1.c - Clean Code ✓
Properly allocates memory using `malloc()` and `calloc()`, and **frees all allocated memory**. Demonstrates correct memory management practices.

**Expected Result:** No memory leaks detected

### example2.c - Complex Leaks ⚠️
Multiple nested structure allocations (`struct numbers` with dynamic arrays) without **any `free()` calls**. Demonstrates both direct and indirect memory leaks.

**Expected Result:** Multiple memory leaks (definitely lost, indirectly lost)

### example3.c - Simple Leak ⚠️
Allocates two memory blocks but **only frees one** (`ptr1`). The `ptr2` allocation is never freed, causing a simple memory leak.

**Expected Result:** Memory leak detected (one missing `free()` call)

---

## File Structure

```
Memory-Leak-Detector/
├── valgrindGUI_windows.py  # Main GUI (Windows/WSL compatible)
├── valgrindGUI.py          # Lightweight GUI (Linux native)
├── example1.c              # Example: Clean code
├── example2.c              # Example: Complex memory leaks
├── example3.c              # Example: Simple memory leak
├── setup_wsl.sh            # Automated WSL setup script
├── setup_wsl.md            # Detailed setup instructions
└── README.md               # This file
```

---

## Troubleshooting

### "WSL not available"
- Ensure WSL is installed: `wsl --status` in PowerShell
- Install WSL: `wsl --install` (as Administrator)
- Restart your computer after installation

### "GCC not installed in WSL"
- Open Ubuntu from Start Menu
- Run: `sudo apt update && sudo apt install -y gcc`
- Or use the automated script: `bash setup_wsl.sh`

### "Valgrind not installed in WSL"
- Open Ubuntu from Start Menu
- Run: `sudo apt install -y valgrind`
- Or use the automated script: `bash setup_wsl.sh`

### "tkinter not found" error
- **Windows:** Reinstall Python with tkinter option checked
- **Linux:** `sudo apt install python3-tk`

### Compilation fails
- Ensure your C file has no syntax errors
- Check that GCC is properly installed
- Verify the file path is correct

### Analysis shows no memory leak information
- Ensure Valgrind is installed and accessible
- The program must be compiled with `-g` flag (done automatically)
- Check that the executable was created successfully

---

## GUI Versions Comparison

### valgrindGUI_windows.py (Recommended for Windows)
- **Full-featured** with comprehensive tool detection
- **WSL integration** - automatically converts Windows paths to WSL format
- **Fallback support** - tries WSL first, then native tools
- **Status bar** showing current operation
- **Color-coded buttons** for better user experience
- **Detailed error messages** and setup instructions
- **File browser** for easy file selection
- **Compilation support** built into the GUI

### valgrindGUI.py (Lightweight for Linux)
- **Simple and lightweight** design
- **Direct Valgrind execution** (no WSL overhead)
- **Manual executable path entry**
- **Basic output formatting**
- Best for Linux users with native Valgrind installation

---

## How It Works

1. **Tool Detection**: On startup, checks for WSL, GCC, and Valgrind availability
2. **File Selection**: User selects a C source file via file browser
3. **Compilation**: Compiles the C file with debugging symbols using GCC
   - Windows: Uses WSL GCC (`wsl gcc -g -o output source.c`)
   - Linux: Uses native GCC (`gcc -g -o output source.c`)
4. **Memory Analysis**: Runs Valgrind with leak detection enabled
   - Command: `valgrind --leak-check=full --track-origins=yes executable`
5. **Output Parsing**: Parses Valgrind output and displays formatted results
6. **Result Display**: Shows memory usage, leak types, and recommendations

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

---

## License

This project is open source and available for educational purposes.

---