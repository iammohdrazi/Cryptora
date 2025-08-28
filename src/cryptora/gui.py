import os
import sys
import datetime
from tkinter import Tk, Label, Button, filedialog, StringVar, Frame, Entry, END
from cryptography.fernet import Fernet, InvalidToken

# ---------------- Paths ----------------
if getattr(sys, 'frozen', False):  # running as exe
    BASE_DIR = os.path.dirname(sys.executable)
else:  # running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEYS_DIR = os.path.join(BASE_DIR, "keys")
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)

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
        update_message("Key not found.")
        return None
    with open(path, "rb") as key_file:
        return key_file.read()

def update_message(text):
    message_var.set(text)

def check_existing_key():
    keys = sorted([f for f in os.listdir(KEYS_DIR) if f.endswith(".key")])
    if keys:
        update_message(f"Found {len(keys)} key(s). Latest: {keys[-1]}")
    else:
        update_message("No key found. Please generate one.")

def generate_key_action():
    key_path = save_key()
    key_path_entry.delete(0, END)
    key_path_entry.insert(0, key_path)
    update_message("New key generated successfully.")

def browse_key():
    key_path = filedialog.askopenfilename(initialdir=KEYS_DIR, filetypes=[("Key Files", "*.key")])
    if key_path:
        key_path_entry.delete(0, END)
        key_path_entry.insert(0, key_path)
        update_message("Key selected successfully.")

def browse_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_path_entry.delete(0, END)
        file_path_entry.insert(0, filename)

# ---------------- File Encryption ----------------
def encrypt_file():
    file_path = file_path_entry.get().strip()
    key_path = key_path_entry.get().strip()
    
    if not file_path or not os.path.exists(file_path):
        update_message("Please select a valid file.")
        return
    if not key_path or not os.path.exists(key_path):
        update_message("Please select a valid key.")
        return
    if ".enc_" in file_path:
        update_message("File is already encrypted.")
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
        update_message(f"Encrypted: {output_file}")
    except Exception as e:
        update_message(f"Error: {str(e)}")

# ---------------- File Decryption ----------------
def decrypt_file():
    file_path = file_path_entry.get().strip()
    key_path = key_path_entry.get().strip()
    
    if not file_path or not os.path.exists(file_path):
        update_message("Please select a valid file.")
        return
    if not key_path or not os.path.exists(key_path):
        update_message("Please select a valid key.")
        return
    if ".enc_" not in file_path:
        update_message("Please select a valid encrypted file.")
        return

    try:
        key = load_key(key_path)
        f = Fernet(key)
        with open(file_path, "rb") as file:
            decrypted = f.decrypt(file.read())

        output_file = file_path.split(".enc_")[0]
        with open(output_file, "wb") as file:
            file.write(decrypted)
        update_message(f"Decrypted: {output_file}")
    
    except InvalidToken:
        update_message("Decryption failed: Incorrect key for this file.")
    except Exception as e:
        update_message(f"Error: {str(e)}")

# ---------------- Modern Symmetrical GUI ----------------
root = Tk()
root.title("Cryptora - File Encryption Utility")
root.geometry("800x350")
root.configure(bg="#1e1e2f")
root.minsize(700, 350)

message_var = StringVar()

# ---------- Style Helpers ----------
def on_enter(e):
    e.widget['background'] = "#4a4aff"
    e.widget['foreground'] = "white"

def on_leave(e):
    e.widget['background'] = "#2e2e4e"
    e.widget['foreground'] = "white"

def create_button(frame, text, command, width=15):
    btn = Button(frame, text=text, command=command, width=width, bg="#2e2e4e", fg="white",
                 activebackground="#4a4aff", activeforeground="white", bd=0, relief="flat")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ---------- Title ----------
Label(root, text="Cryptora", bg="#1e1e2f", fg="#00ffae", font=("Segoe UI", 20, "bold")).pack(pady=10)

# ---------- Key Section ----------
frame_key = Frame(root, bg="#1e1e2f")
frame_key.pack(pady=10, padx=20, fill="x")

create_button(frame_key, "Generate Key", generate_key_action).pack(side="left", padx=10)
create_button(frame_key, "Browse Key", browse_key).pack(side="left", padx=10)

key_path_entry = Entry(frame_key, width=60, bg="#2e2e4e", fg="white", insertbackground="white", font=("Segoe UI", 10))
key_path_entry.pack(side="left", padx=10, expand=True, fill="x")

# ---------- File Section ----------
file_frame = Frame(root, bg="#1e1e2f")
file_frame.pack(pady=10, padx=20, fill="x")

Label(file_frame, text="Select File:", bg="#1e1e2f", fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=2)
file_entry_frame = Frame(file_frame, bg="#1e1e2f")
file_entry_frame.pack(fill="x")

file_path_entry = Entry(file_entry_frame, width=60, bg="#2e2e4e", fg="white", insertbackground="white", font=("Segoe UI", 10))
file_path_entry.pack(side="left", padx=10, expand=True, fill="x")

create_button(file_entry_frame, "Browse", browse_file).pack(side="left", padx=10)

# ---------- Action Buttons ----------
action_frame = Frame(root, bg="#1e1e2f")
action_frame.pack(pady=20)

create_button(action_frame, "Encrypt", encrypt_file, width=20).pack(side="left", padx=20)
create_button(action_frame, "Decrypt", decrypt_file, width=20).pack(side="left", padx=20)

# ---------- Status Message ----------
status_label = Label(root, textvariable=message_var, fg="#00ffae", bg="#1e1e2f", wraplength=750,
                     justify="center", font=("Segoe UI", 10, "bold"))
status_label.pack(pady=15, padx=10, anchor="center")

# ---------- Exit Button ----------
exit_btn = create_button(root, "Exit", root.quit, width=12)
exit_btn.pack(side="right", padx=20, pady=10)

check_existing_key()
root.mainloop()
