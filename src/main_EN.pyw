import threading
import time
import re
from tkinter import *
from tkinter import filedialog
from pynput import mouse, keyboard

root = Tk()
root.title("Instruction Sequence Console V3.1 - By ShiroDye")
root.geometry("700x600+500+150")
root.configure(bg='#f4f4f9')

m_mouse = mouse.Controller()
k_control = keyboard.Controller()
send_speed = DoubleVar(value=0.5)
stop_flag = False
recording = False
record_listener = None

VALID_KEYS = {
    "esc", "ctrl", "alt", "win", "del", "ins", "enter", "space", 
    "tab", "shift", "backspace", "up", "down", "left", "right", "cmd"
}
for i in range(1, 13): VALID_KEYS.add(f"f{i}")

def get_key_obj(name):
    name = name.lower().strip().replace('[', '').replace(']', '').replace('+', '')
    if name in ['cmd', 'win', 'windows']: return keyboard.Key.cmd
    key_map = {
        "esc": keyboard.Key.esc, "ctrl": keyboard.Key.ctrl, "alt": keyboard.Key.alt,
        "del": keyboard.Key.delete, "ins": keyboard.Key.insert,
        "enter": keyboard.Key.enter, "space": keyboard.Key.space, "tab": keyboard.Key.tab,
        "shift": keyboard.Key.shift, "backspace": keyboard.Key.backspace,
        "up": keyboard.Key.up, "down": keyboard.Key.down, 
        "left": keyboard.Key.left, "right": keyboard.Key.right
    }
    for i in range(1, 13): key_map[f"f{i}"] = getattr(keyboard.Key, f'f{i}')
    if len(name) == 1: return name
    return key_map.get(name)

def force_reset_keys():
    """Release all modifiers to prevent key sticking"""
    for k in [keyboard.Key.ctrl, keyboard.Key.alt, keyboard.Key.shift, keyboard.Key.cmd]:
        k_control.release(k)

def run_task():
    global stop_flag
    try:
        content = text_area.get("1.0", "end-1c")
        c_val = entry2.get().strip().lower()
        count = float('inf') if c_val == 'inf' else (int(c_val) if c_val.isdigit() else 1)
        
        btn.config(text="STOP EXECUTION", bg='#e53935', command=stop_task)
        time.sleep(2) 
        
        loop_idx = 0
        while loop_idx < count:
            if stop_flag: break
            status_text = f"Loop: {loop_idx+1}" + (" (Infinite)" if count == float('inf') else f" / {count}")
            counter_label.config(text=status_text)
            
            tokens = re.finditer(r'(\{.*?\})|(\[.*?\])|(\n)|.', content, re.DOTALL)
            
            for match in tokens:
                if stop_flag: break
                token = match.group()
                
                # 1. Hotkey combination {}
                if token.startswith('{') and token.endswith('}'):
                    inner = token[1:-1].strip()
                    if inner.upper().startswith('BLANK:'):
                        try: time.sleep(float(inner.split(':')[1]))
                        except: pass
                    else:
                        inner_key_names = re.findall(r'\[(.*?)\]', inner)
                        objs = [get_key_obj(k) for k in inner_key_names if get_key_obj(k)]
                        if objs:
                            try:
                                for o in objs:
                                    k_control.press(o)
                                    time.sleep(0.05)
                                time.sleep(0.1)     
                            finally:
                                for o in reversed(objs):
                                    k_control.release(o)
                                    time.sleep(0.03)
                
                # 2. Single Key []
                elif token.startswith('[') and token.endswith(']'):
                    name = token[1:-1].lower().strip()
                    if name in VALID_KEYS or (name.startswith('f') and name[1:].isdigit()):
                        obj = get_key_obj(name)
                        if obj:
                            k_control.press(obj)
                            time.sleep(0.05)
                            k_control.release(obj)
                    else:
                        k_control.type(token)
                
                # 3. Newline and Normal Text
                elif token == '\n':
                    k_control.press(keyboard.Key.enter)
                    k_control.release(keyboard.Key.enter)
                else:
                    k_control.type(token)
            
            loop_idx += 1
            force_reset_keys() 
            if not stop_flag: time.sleep(send_speed.get())
            
    except: pass
    finally:
        force_reset_keys()
        stop_flag = False
        btn.config(text="START EXECUTION", bg='#5c6bc0', command=start_task)

def start_task():
    global stop_flag
    stop_flag = False
    threading.Thread(target=run_task, daemon=True).start()

def stop_task():
    global stop_flag
    stop_flag = True

# --- Recording Mode (Manual) ---
def toggle_record():
    global recording, record_listener
    if recording: return
    recording = True
    rec_win = Toplevel(root)
    rec_win.attributes("-topmost", True)
    rec_win.geometry("240x90+20+20")
    rec_win.overrideredirect(True)
    rec_win.configure(bg="#c0392b")
    Label(rec_win, text="[RECORDING MODE]\nSystem Keys Intercepted", fg="white", bg="#c0392b", font=("Arial", 9, "bold")).pack(pady=10)
    
    def stop_rec():
        global recording
        recording = False
        if record_listener: record_listener.stop()
        rec_win.destroy()
    
    Button(rec_win, text="Stop & Save", command=stop_rec, bg="white", relief=FLAT, font=("Arial", 8)).pack()

    def on_press(key):
        if not recording: return False
        try:
            if hasattr(key, 'char') and key.char:
                text_area.insert(END, key.char)
            else:
                name = str(key).replace('Key.', '').upper()
                text_area.insert(END, f"[{name}]")
        except: pass

    record_listener = keyboard.Listener(on_press=on_press, suppress=True)
    record_listener.start()

# --- Menu and UI ---
def import_txt():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_area.delete("1.0", END)
            text_area.insert("1.0", f.read())

def insert_key(key_str):
    text_area.insert(INSERT, f"[{key_str}]")

main_menu = Menu(root)
debug_menu = Menu(main_menu, tearoff=0)

speed_menu = Menu(debug_menu, tearoff=0)
for l, v in [("Fast (0.1s)", 0.1), ("Standard (0.5s)", 0.5), ("Slow (1.0s)", 1.0)]:
    speed_menu.add_radiobutton(label=l, variable=send_speed, value=v)

key_list_menu = Menu(debug_menu, tearoff=0)
for sk in ["ESC", "CTRL", "ALT", "WIN", "DEL", "INS", "BACKSPACE", "SPACE", "TAB", "ENTER"]:
    key_list_menu.add_command(label=sk, command=lambda s=sk: insert_key(s))

debug_menu.add_command(label="Record Mode", command=toggle_record)
debug_menu.add_command(label="Import File", command=import_txt)
debug_menu.add_separator()
debug_menu.add_cascade(label="Insert Key", menu=key_list_menu)
debug_menu.add_cascade(label="Set Speed", menu=speed_menu)
main_menu.add_cascade(label="Debug Menu", menu=debug_menu)
root.config(menu=main_menu)

f_top = Frame(root, bg='#3b3e4b', height=40); f_top.pack(fill=X)
Label(f_top, text="Instruction Console V3.1", fg='white', bg='#3b3e4b', font=('Arial', 11, 'bold')).pack(pady=5)

f_body = Frame(root, bg='#f4f4f9', padx=15, pady=10); f_body.pack(fill=BOTH, expand=True)

Label(f_body, text="Instruction Area (Supports {} combinations):", bg='#f4f4f9', fg='#555', font=('Arial', 9)).pack(anchor=W)
text_area = Text(f_body, font=('Consolas', 11), bd=1, relief=SOLID, height=12, undo=True)
text_area.pack(fill=BOTH, expand=True, pady=(5, 10))

Label(f_body, text="Loop Count (Enter 'inf' for infinite):", bg='#f4f4f9', fg='#555', font=('Arial', 9)).pack(anchor=W)
entry2 = Entry(f_body, font=('Consolas', 12), bd=1, relief=SOLID)
entry2.insert(0, "1"); entry2.pack(fill=X, pady=(5, 10), ipady=5)

counter_label = Label(f_body, text="Ready", bg='#f4f4f9', fg='#5c6bc0', font=('Arial', 10, 'bold'))
counter_label.pack(pady=2)

btn = Button(f_body, text="START EXECUTION", bg='#5c6bc0', fg='white', font=('Arial', 12, 'bold'), relief=FLAT, command=start_task)
btn.pack(fill=X, ipady=8)

root.mainloop()
