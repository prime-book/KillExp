import tkinter as tk
import subprocess
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading

def kill_explorer():
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error killing explorer.exe: {e}")

def start_explorer():
    try:
        subprocess.run(["start", "explorer.exe"], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting explorer.exe: {e}")

def set_kill_key(event):
    global kill_key, setting_kill_key
    kill_key = event.name
    setting_kill_key = False
    update_labels()
    if hotkeys_enabled:
        keyboard.add_hotkey(kill_key, kill_explorer)
    keyboard.unhook_all()

def set_start_key(event):
    global start_key, setting_start_key
    start_key = event.name
    setting_start_key = False
    update_labels()
    if hotkeys_enabled:
        keyboard.add_hotkey(start_key, start_explorer)
    keyboard.unhook_all()

def ask_kill_key():
    global setting_kill_key
    setting_kill_key = True
    update_labels()
    keyboard.unhook_all()
    keyboard.on_press(set_kill_key)

def ask_start_key():
    global setting_start_key
    setting_start_key = True
    update_labels()
    keyboard.unhook_all()
    keyboard.on_press(set_start_key)

def on_closing():
    root.quit()  # Close the application

def minimize_to_tray():
    root.withdraw()
    if not icon.visible:
        icon.visible = True

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (30, 30, 30))  # Dark grey background
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=(60, 60, 60))  # Darker grey rectangle
    return image

def show_window():
    root.deiconify()
    icon.visible = False

def create_tray_icon():
    global icon
    icon = pystray.Icon("explorer_control", create_image(), menu=pystray.Menu(
        item(labels["show"], show_window),
        item(labels["exit"], on_exit)
    ))
    icon.run()

def on_exit():
    icon.stop()
    root.quit()

def set_language(language):
    global current_language
    current_language = language
    update_labels()

def update_labels():
    global setting_kill_key, setting_start_key
    labels["kill_key_label_var"] = f"{translations[current_language]['kill_key_label_var']}: {kill_key}" if kill_key else translations[current_language]["kill_key_label_var"]
    labels["start_key_label_var"] = f"{translations[current_language]['start_key_label_var']}: {start_key}" if start_key else translations[current_language]["start_key_label_var"]
    labels["kill_key_btn"] = translations[current_language]["kill_key_btn"]
    labels["start_key_btn"] = translations[current_language]["start_key_btn"]
    labels["minimize_btn"] = translations[current_language]["minimize_btn"]
    labels["start_btn"] = translations[current_language]["start_btn"]
    labels["stop_btn"] = translations[current_language]["stop_btn"]
    labels["show"] = translations[current_language]["show"]
    labels["exit"] = translations[current_language]["exit"]
    if setting_kill_key:
        labels["kill_key_label_var"] = translations[current_language]["press_kill_key"]
    if setting_start_key:
        labels["start_key_label_var"] = translations[current_language]["press_start_key"]

    kill_key_label_var.set(labels["kill_key_label_var"])
    start_key_label_var.set(labels["start_key_label_var"])
    kill_key_btn.config(text=labels["kill_key_btn"], bg="#444", fg="#fff", relief="flat")
    start_key_btn.config(text=labels["start_key_btn"], bg="#444", fg="#fff", relief="flat")
    minimize_btn.config(text=labels["minimize_btn"], bg="#444", fg="#fff", relief="flat")
    start_btn.config(text=labels["start_btn"], bg="#007bff", fg="#fff", relief="flat")
    stop_btn.config(text=labels["stop_btn"], bg="#dc3545", fg="#fff", relief="flat")

def toggle_hotkeys(state):
    global hotkeys_enabled
    hotkeys_enabled = state
    if hotkeys_enabled:
        if kill_key:
            keyboard.add_hotkey(kill_key, kill_explorer)
        if start_key:
            keyboard.add_hotkey(start_key, start_explorer)
    else:
        keyboard.unhook_all()

# Localization dictionaries
translations = {
    "en": {
        "kill_key_label_var": "Hotkey for closing Explorer",
        "start_key_label_var": "Hotkey for starting Explorer",
        "kill_key_btn": "Set Hotkey",
        "start_key_btn": "Set Hotkey",
        "minimize_btn": "Minimize to Tray",
        "start_btn": "Start Hotkeys",
        "stop_btn": "Stop Hotkeys",
        "show": "Show",
        "exit": "Exit",
        "press_kill_key": "Press the key you want to set for closing Explorer.",
        "press_start_key": "Press the key you want to set for starting Explorer."
    },
    "ru": {
        "kill_key_label_var": "Горячая клавиша для закрытия Explorer",
        "start_key_label_var": "Горячая клавиша для запуска Explorer",
        "kill_key_btn": "Назначить клавишу",
        "start_key_btn": "Назначить клавишу",
        "minimize_btn": "Свернуть в трей",
        "start_btn": "Включить клавиши",
        "stop_btn": "Выключить клавиши",
        "show": "Показать",
        "exit": "Выход",
        "press_kill_key": "Нажмите клавишу, которую хотите назначить для закрытия Explorer.",
        "press_start_key": "Нажмите клавишу, которую хотите назначить для запуска Explorer."
    }
}

# Initialize variables
kill_key = None
start_key = None
current_language = "ru"
setting_kill_key = False
setting_start_key = False
hotkeys_enabled = True

root = tk.Tk()
root.title("KillExp")

# Apply dark theme
root.configure(bg="#333")
frame = tk.Frame(root, bg="#333")
frame.pack(pady=10)

kill_key_label_var = tk.StringVar()
start_key_label_var = tk.StringVar()

kill_key_label = tk.Label(frame, textvariable=kill_key_label_var, bg="#333", fg="#fff", font=("Helvetica", 12))
kill_key_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
kill_key_btn = tk.Button(frame, text="Назначить клавишу", command=ask_kill_key, bg="#444", fg="#fff", relief="flat")
kill_key_btn.grid(row=0, column=2, padx=5, pady=5)

start_key_label = tk.Label(frame, textvariable=start_key_label_var, bg="#333", fg="#fff", font=("Helvetica", 12))
start_key_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
start_key_btn = tk.Button(frame, text="Назначить клавишу", command=ask_start_key, bg="#444", fg="#fff", relief="flat")
start_key_btn.grid(row=1, column=2, padx=5, pady=5)

minimize_btn = tk.Button(frame, text="Свернуть в трей", command=minimize_to_tray, bg="#444", fg="#fff", relief="flat")
minimize_btn.grid(row=2, column=0, padx=5, pady=10)

start_btn = tk.Button(frame, text="Включить клавиши", command=lambda: toggle_hotkeys(True), bg="#007bff", fg="#fff", relief="flat")
start_btn.grid(row=2, column=1, padx=5, pady=10)

stop_btn = tk.Button(frame, text="Выключить клавиши", command=lambda: toggle_hotkeys(False), bg="#dc3545", fg="#fff", relief="flat")
stop_btn.grid(row=2, column=2, padx=5, pady=10)

language_frame = tk.Frame(root, bg="#333")
language_frame.pack(pady=10)

language_label = tk.Label(language_frame, text="Язык / Language:", bg="#333", fg="#fff")
language_label.grid(row=0, column=0, padx=5)

ru_btn = tk.Button(language_frame, text="RU", command=lambda: set_language("ru"), bg="#444", fg="#fff", relief="flat")
ru_btn.grid(row=0, column=1, padx=5)

en_btn = tk.Button(language_frame, text="EN", command=lambda: set_language("en"), bg="#444", fg="#fff", relief="flat")
en_btn.grid(row=0, column=2, padx=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

labels = {}
update_labels()

icon = pystray.Icon("explorer_control", create_image(), menu=pystray.Menu(
    item(labels["show"], show_window),
    item(labels["exit"], on_exit)
))
icon.visible = False

tray_thread = threading.Thread(target=icon.run)
tray_thread.daemon = True
tray_thread.start()

root.mainloop()
