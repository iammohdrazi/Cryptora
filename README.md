# Cryptora - File Encryption/Decryption Utility

Cryptora is a Python utility that allows you to **encrypt and decrypt files/folders** using a secure symmetric key (Fernet encryption).  
It provides both a **GUI application** and a **CLI script**.

---

## ✨ Features
- File and folder encryption/decryption  
- Secure key generation and management  
- GUI for easy usage  
- CLI for advanced users and automation  
- Cross-platform (Windows, Linux, macOS)  

---

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Cryptora
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ GUI Usage

The GUI is the main interface for normal users.

1. Open a terminal and move into the `src` folder:

   ```bash
   cd Cryptora\src
   ```

2. Run the GUI:

   ```bash
   python -m cryptora.gui
   ```

3. Features:

   * Generate or browse keys
   * Encrypt/decrypt files or folders
   * Status messages for success or errors
   * Automatically uses the latest key unless you pick one

---

## 🔑 CLI Usage

The CLI script is useful for automation, scripting, or advanced users.

1. Open a terminal and move into the `src` folder:

   ```bash
   cd Cryptora\src
   ```

2. Run the CLI help to see available commands:

   ```bash
   python -m cryptora.cli --help
   ```

3. **Encrypt a file**:

   ```bash
   python -m cryptora.cli encrypt -f path\to\file.txt -k ..\keys\cryptora_YYYYMMDD_HHMMSS.key
   ```

4. **Decrypt a file**:

   ```bash
   python -m cryptora.cli decrypt -f path\to\file.txt.enc -k ..\keys\cryptora_YYYYMMDD_HHMMSS.key
   ```

5. **Encrypt a folder**:

   ```bash
   python -m cryptora.cli encrypt -d path\to\folder -k ..\keys\cryptora_YYYYMMDD_HHMMSS.key
   ```

6. **Decrypt a folder**:

   ```bash
   python -m cryptora.cli decrypt -d path\to\folder -k ..\keys\cryptora_YYYYMMDD_HHMMSS.key
   ```

---

## 🔐 Key Management

* Keys are stored in the `keys/` folder (sibling of `src/`).
* Filenames are timestamped for uniqueness:

  ```
  cryptora_YYYYMMDD_HHMMSS.key
  ```
* The latest key is automatically used in the GUI if no key is selected.
* CLI requires explicit `-k` option to specify the key.

---

## 📦 Building a Standalone `.exe` (Windows)

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Move into the `src` directory:

   ```bash
   cd Cryptora\src
   ```

3. Run PyInstaller on the GUI:

   ```bash
   pyinstaller --onefile --windowed -n cryptora_gui cryptora\gui.py
   ```

   * `--onefile` → single `.exe` output
   * `--windowed` → no console window pops up (for GUI apps)
   * `-n cryptora_gui` → output filename will be `cryptora_gui.exe`

4. The built `.exe` will be inside:

   ```
   dist/cryptora_gui.exe
   ```

---


## 🐧 Linux Usage Notes

### Example (GUI)

```bash
git clone <repo-url>
cd Cryptora
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

source venv/bin/activate
export QT_QPA_PLATFORM=xcb

cd src
python3 -m cryptora.gui
```
If GUI fails to load few lib:
```bash
sudo apt update && sudo apt install -y \
libxcb-xinerama0 libxcb-xinerama0-dev libx11-xcb1 libxrender1 libxext6 libxfixes3 libx11-dev \
libxcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
libxcb-shm0 libxcb-sync1 libxcb-xfixes0
```

### Example (CLI)

```bash
cd Cryptora/src
python3 -m cryptora.cli --help

# Encrypt a file
python3 -m cryptora.cli encrypt -f path/to/file.txt -k ../keys/cryptora_YYYYMMDD_HHMMSS.key

# Decrypt a file
python3 -m cryptora.cli decrypt -f path/to/file.txt.enc -k ../keys/cryptora_YYYYMMDD_HHMMSS.key
```

⚠️ On some Linux distributions you may need to install Tkinter separately:

```bash
sudo apt-get install python3-tk
```


## 📜 License & Trademark

This project is under the **MIT License**. See [LICENSE](./LICENSE).

The name **Cryptora** (™) is a claimed trademark.

* Free for non-commercial, personal, or educational use.
* Commercial use requires permission.


---
