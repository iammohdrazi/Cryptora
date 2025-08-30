import os
import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QTextEdit, QCheckBox, QSizePolicy
)
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet, InvalidToken

# ---------------- Paths ----------------
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEYS_DIR = os.path.join(BASE_DIR, "keys")
LOGS_DIR = os.path.join(BASE_DIR, "cryplog")

os.makedirs(KEYS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


# ---------------- Encryption Logic ----------------
def generate_key_name():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"cryptora_{timestamp}.key"

def save_key():
    key = Fernet.generate_key()
    key_name = generate_key_name()
    key_path = os.path.join(KEYS_DIR, key_name)
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    return os.path.abspath(key_path)

def load_key(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as key_file:
        return key_file.read()


# ---------------- Main UI Class ----------------
class CryptoraUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔒 Cryptora - File Encryption Utility")
        self.setMinimumSize(700, 420)

        # Modern dark theme
        self.setStyleSheet("""
            QWidget { background-color: #1e1e2f; color: white; font-family: 'Segoe UI'; font-size: 11pt; }
            QPushButton { background-color: #2e2e4e; border: none; padding: 10px 18px; border-radius: 8px; font-size: 11pt; }
            QPushButton:hover { background-color: #4a4aff; }
            QLineEdit { background-color: #2e2e4e; border: 1px solid #444; padding: 8px; border-radius: 6px; color: white; font-size: 11pt; }
            QTextEdit { background-color: #2e2e4e; border: 1px solid #444; padding: 6px; border-radius: 6px; color: #00ffae; font-size: 11pt; }
            QCheckBox { font-size: 10pt; color: #cccccc; }
            QCheckBox::indicator { width: 16px; height: 16px; }
            QCheckBox::indicator:checked { background-color: #4a4aff; border-radius: 3px; }
            QScrollBar:vertical { border: none; background: #2e2e4e; width: 10px; margin: 0px 0px 0px 0px; border-radius: 5px; }
            QScrollBar::handle:vertical { background: #4a4aff; min-height: 20px; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #6a6aff; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar:horizontal { height: 0px; }
        """)

        self.key_path = ""
        self.file_path = ""
        self.log_file = None

        # ---------- Main Layout ----------
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # ---------- Title + Subtitle ----------
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("🔒 Cryptora")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00ffae;")
        title_layout.addWidget(title)

        subtitle = QLabel("Secure File Encryption & Decryption Utility")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #bbbbbb;")
        title_layout.addWidget(subtitle)

        layout.addLayout(title_layout, stretch=0)

        # ---------- Key Section ----------
        key_layout = QHBoxLayout()
        key_layout.setSpacing(12)

        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("Key file path...")

        btn_browse_key = QPushButton("Browse Key")
        btn_browse_key.setMinimumWidth(130)
        btn_browse_key.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_browse_key.clicked.connect(self.browse_key)
        btn_browse_key.setToolTip("Select an existing key file for encryption/decryption.")

        btn_generate = QPushButton("Generate Key")
        btn_generate.setMinimumWidth(130)
        btn_generate.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_generate.clicked.connect(self.generate_key)
        btn_generate.setToolTip("Generate a new encryption key and save it to the keys folder.")

        btn_list_keys = QPushButton("List Keys")
        btn_list_keys.setMinimumWidth(130)
        btn_list_keys.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_list_keys.clicked.connect(self.list_keys)
        btn_list_keys.setToolTip("Show all available keys in the log (not saved).")

        key_layout.addWidget(self.key_entry, stretch=2)
        key_layout.addWidget(btn_browse_key)
        key_layout.addWidget(btn_generate)
        key_layout.addWidget(btn_list_keys)
        layout.addLayout(key_layout, stretch=0)

        # ---------- File Section ----------
        file_layout = QHBoxLayout()
        file_layout.setSpacing(12)

        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("File to encrypt/decrypt...")

        btn_browse_file = QPushButton("Browse File")
        btn_browse_file.setMinimumWidth(130)
        btn_browse_file.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_browse_file.clicked.connect(self.browse_file)
        btn_browse_file.setToolTip("Select a file to encrypt or decrypt.")

        file_layout.addWidget(self.file_entry, stretch=2)
        file_layout.addWidget(btn_browse_file)
        layout.addLayout(file_layout, stretch=0)

        # ---------- Action Buttons ----------
        action_layout = QHBoxLayout()
        action_layout.setSpacing(30)

        btn_encrypt = QPushButton("Encrypt")
        btn_encrypt.setMinimumWidth(140)
        btn_encrypt.clicked.connect(self.encrypt_file)
        btn_encrypt.setToolTip("Encrypt the selected file using the chosen key.")

        btn_decrypt = QPushButton("Decrypt")
        btn_decrypt.setMinimumWidth(140)
        btn_decrypt.clicked.connect(self.decrypt_file)
        btn_decrypt.setToolTip("Decrypt the selected encrypted file using the chosen key.")

        action_layout.addStretch()
        action_layout.addWidget(btn_encrypt)
        action_layout.addWidget(btn_decrypt)
        action_layout.addStretch()
        layout.addLayout(action_layout, stretch=0)

        # ---------- Log Viewer Label ----------
        log_label = QLabel("Log Viewer :")
        layout.addWidget(log_label, stretch=0)

        # ---------- Status Log ----------
        self.status_label = QTextEdit()
        self.status_label.setReadOnly(True)
        self.status_label.setMinimumHeight(120)
        layout.addWidget(self.status_label, stretch=3)

        # ---------- Bottom Controls ----------
        bottom_layout = QHBoxLayout()

        self.save_logs_checkbox = QCheckBox("Save Logs")
        self.save_logs_checkbox.stateChanged.connect(self.toggle_log_saving)
        self.save_logs_checkbox.setToolTip("Enable or disable saving logs to file.")
        bottom_layout.addWidget(self.save_logs_checkbox)

        btn_load_logs = QPushButton("Load Logs")
        btn_load_logs.setMinimumWidth(120)
        btn_load_logs.clicked.connect(self.load_logs)
        btn_load_logs.setToolTip("Load today's saved log file into the viewer.")
        bottom_layout.addWidget(btn_load_logs)

        bottom_layout.addStretch()

        btn_clear_logs = QPushButton("Clear Logs")
        btn_clear_logs.setMinimumWidth(120)
        btn_clear_logs.clicked.connect(self.clear_logs)
        btn_clear_logs.setToolTip("Clear the log viewer (does not delete saved logs).")
        bottom_layout.addWidget(btn_clear_logs)

        layout.addLayout(bottom_layout, stretch=0)

        self.setLayout(layout)
        self.check_initial_status()

    # ---------------- New Methods ----------------
    def toggle_log_saving(self, state):
        today = datetime.datetime.now().strftime("%Y%m%d")
        log_filename = f"log_{today}.txt"
        log_path = os.path.join(LOGS_DIR, log_filename)
        if state == Qt.Checked:
            self.log_file = log_path
            if not os.path.exists(self.log_file):
                with open(self.log_file, "w", encoding="utf-8") as f:
                    f.write(f"--- Log started on {datetime.datetime.now()} ---\n")
            self.update_status("📝 Log saving enabled", save_to_file=False)
        else:
            self.update_status("🛑 Log saving disabled", save_to_file=False)
            self.log_file = None

    def load_logs(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        log_filename = f"log_{today}.txt"
        log_path = os.path.join(LOGS_DIR, log_filename)
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.status_label.setPlainText(content)
            self.update_status(f"📂 Loaded logs from {log_path}", save_to_file=False)
        else:
            self.update_status("⚠️ No logs available for today.", save_to_file=False)

    def clear_logs(self):
        self.status_label.clear()
        self.update_status("🧹 Logs cleared", save_to_file=False)

    def list_keys(self):
        keys = [f for f in os.listdir(KEYS_DIR) if f.endswith(".key")]
        if keys:
            self.update_status("🔑 Available keys:", save_to_file=False)
            for k in keys:
                self.update_status(f"  - {k}", save_to_file=False)
        else:
            self.update_status("⚠️ No keys available.", save_to_file=False)

    # ---------------- Actions ----------------
    def update_status(self, msg, save_to_file=True):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        log_line = f"{timestamp} {msg}"

        cursor = self.status_label.textCursor()
        cursor.movePosition(QTextCursor.End)
        highlight_format = QTextCharFormat()
        highlight_format.setForeground(QColor("#00ffae"))
        highlight_format.setFontWeight(QFont.Bold)
        cursor.insertText("\n" + log_line, highlight_format)
        self.status_label.setTextCursor(cursor)
        self.status_label.ensureCursorVisible()

        if self.log_file and save_to_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")

    def check_initial_status(self):
        keys = [f for f in os.listdir(KEYS_DIR) if f.endswith(".key")]
        if keys:
            self.update_status(f"🔑 {len(keys)} key(s) found. Ready to use.", save_to_file=False)
            latest_key = max(keys, key=lambda f: os.path.getctime(os.path.join(KEYS_DIR, f)))
            self.key_entry.setText(os.path.join(KEYS_DIR, latest_key))
        else:
            self.update_status("⚠️ No keys found. Generate a key to get started.", save_to_file=False)

    def generate_key(self):
        key_path = save_key()
        self.key_entry.setText(key_path)
        self.update_status(f"✅ New key generated → {key_path}")

    def browse_key(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Key File", KEYS_DIR, "Key Files (*.key)")
        if path:
            self.key_entry.setText(path)
            self.update_status(f"✅ Key selected → {path}", save_to_file=False)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.file_entry.setText(path)
            self.update_status(f"✅ File selected → {path}", save_to_file=False)

    def encrypt_file(self):
        file_path = self.file_entry.text().strip()
        key_path = self.key_entry.text().strip()
        if not os.path.exists(file_path):
            self.update_status("❌ Invalid file", save_to_file=False)
            return
        if not os.path.exists(key_path):
            self.update_status("❌ Invalid key", save_to_file=False)
            return
        if ".enc_" in file_path:
            self.update_status("⚠️ File already encrypted", save_to_file=False)
            return
        try:
            key = load_key(key_path)
            f = Fernet(key)
            with open(file_path, "rb") as file:
                encrypted = f.encrypt(file.read())
            key_name = os.path.splitext(os.path.basename(key_path))[0]
            output_file = file_path + f".enc_{key_name}"
            with open(output_file, "wb") as file:
                file.write(encrypted)
            self.update_status(f"🔒 Encrypted → {output_file}")
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")

    def decrypt_file(self):
        file_path = self.file_entry.text().strip()
        key_path = self.key_entry.text().strip()
        if not os.path.exists(file_path):
            self.update_status("❌ Invalid file", save_to_file=False)
            return
        if not os.path.exists(key_path):
            self.update_status("❌ Invalid key", save_to_file=False)
            return
        if ".enc_" not in file_path:
            self.update_status("⚠️ Not an encrypted file", save_to_file=False)
            return
        try:
            key = load_key(key_path)
            f = Fernet(key)
            with open(file_path, "rb") as file:
                decrypted = f.decrypt(file.read())
            output_file = file_path.split(".enc_")[0]
            with open(output_file, "wb") as file:
                file.write(decrypted)
            self.update_status(f"✅ Decrypted → {output_file}")
        except InvalidToken:
            self.update_status("❌ Decryption failed: Incorrect key")
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")


# ---------------- Run ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoraUI()
    window.show()
    sys.exit(app.exec_())
