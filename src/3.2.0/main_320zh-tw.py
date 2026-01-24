import threading
import time
import re
from tkinter import *
from tkinter import filedialog
from pynput import mouse, keyboard

root = Tk()
root.title("指令序列主控台 Version 3.2.0 By ShiroDye")
root.geometry("700x600+500+150")
root.configure(bg='#f4f4f9')

m_mouse = mouse.Controller()
k_control = keyboard.Controller()
send_speed = DoubleVar(value=0.5)
show_countdown_flag = BooleanVar(value=True)
stop_flag = False
recording = False
record_listener = None
hotkey_listener = None
keys_pressed = {}

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
    for k in [keyboard.Key.ctrl, keyboard.Key.alt, keyboard.Key.shift, keyboard.Key.cmd]:
        k_control.release(k)

def run_task():
    global stop_flag
    try:
        content = text_area.get("1.0", "end-1c")
        c_val = entry2.get().strip().lower()
        count = float('inf') if c_val == 'inf' else (int(c_val) if c_val.isdigit() else 1)
        
        btn.config(text="停止執行", bg='#e53935', command=stop_task)
        
        loop_idx = 0
        while loop_idx < count:
            if stop_flag: break
            counter_label.config(text=f"進度: 第 {loop_idx+1} 輪" + (" (無限)" if count == float('inf') else f" / {count}"))
            
            tokens = re.finditer(r'(\{.*?\})|(\[.*?\])|(\n)|.', content, re.DOTALL)
            
            for match in tokens:
                if stop_flag: break
                token = match.group()
                
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
        btn.config(text="開始執行 [Ctrl+Shift+F12]", bg='#5c6bc0', command=start_task)

def start_task():
    global stop_flag
    stop_flag = False
    if show_countdown_flag.get():
        show_countdown()
    else:
        time.sleep(3)
        threading.Thread(target=run_task, daemon=True).start()

def show_countdown():
    countdown_win = Toplevel(root)
    countdown_win.title("倒數計時")
    countdown_win.geometry("300x200+700+150")
    countdown_win.attributes("-topmost", True)
    countdown_win.resizable(False, False)
    countdown_win.configure(bg='#e53935')
    
    hint_label = Label(countdown_win, text="⚠ 即將開始執行，請儘快切換至目標視窗！\nℹ 若不需要此功能，可在左上角「偵錯選單」中關閉倒數。", 
                      fg='white', bg='#e53935', font=('Microsoft JhengHei', 10, 'bold'), wraplength=320)
    hint_label.pack(pady=15)
    
    countdown_label = Label(countdown_win, text="3", fg='white', bg='#e53935', 
                           font=('Microsoft JhengHei', 48, 'bold'))
    countdown_label.pack(pady=10)
    
    def countdown_loop(remaining):
        if remaining > 0:
            countdown_label.config(text=str(remaining))
            countdown_win.after(1000, countdown_loop, remaining - 1)
        else:
            countdown_win.destroy()
            threading.Thread(target=run_task, daemon=True).start()
    
    countdown_loop(3)

def stop_task():
    global stop_flag
    stop_flag = True

def toggle_record():
    global recording, record_listener
    if recording: return
    recording = True
    rec_win = Toplevel(root)
    rec_win.attributes("-topmost", True)
    rec_win.geometry("200x80+20+20")
    rec_win.overrideredirect(True)
    rec_win.configure(bg="#c0392b")
    Label(rec_win, text="錄製中 (系統鍵已攔截)", fg="white", bg="#c0392b").pack(pady=10)
    
    def stop_rec():
        global recording
        recording = False
        if record_listener: record_listener.stop()
        rec_win.destroy()
    
    Button(rec_win, text="結束並儲存", command=stop_rec, bg="white", relief=FLAT).pack()

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

def setup_hotkey_listener():
    global hotkey_listener, keys_pressed
    
    def on_hotkey_press(key):
        try:
            key_str = str(key).replace("Key.", "").lower()
            keys_pressed[key_str] = True
            
            ctrl_pressed = keys_pressed.get("ctrl_l", False) or keys_pressed.get("ctrl", False) or keys_pressed.get("ctrl_r", False)
            shift_pressed = keys_pressed.get("shift_l", False) or keys_pressed.get("shift", False) or keys_pressed.get("shift_r", False)
            f12_pressed = keys_pressed.get("f12", False)
            
            if ctrl_pressed and shift_pressed and f12_pressed:
                root.after(0, start_task)
        except: pass
    
    def on_hotkey_release(key):
        try:
            key_str = str(key).replace("Key.", "").lower()
            keys_pressed[key_str] = False
        except: pass
    
    hotkey_listener = keyboard.Listener(on_press=on_hotkey_press, on_release=on_hotkey_release)
    hotkey_listener.start()

def import_txt():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_area.delete("1.0", END)
            text_area.insert("1.0", f.read())

def insert_key(key_str):
    text_area.insert(INSERT, f"[{key_str}]")

main_menu = Menu(root)
debug_menu = Menu(main_menu, tearoff=0)
speed_menu = Menu(debug_menu, tearoff=0)
for l, v in [("極速 (0.1s)", 0.1), ("標準 (0.5s)", 0.5), ("慢速 (1.0s)", 1.0)]:
    speed_menu.add_radiobutton(label=l, variable=send_speed, value=v)

key_list_menu = Menu(debug_menu, tearoff=0)
fn_menu = Menu(key_list_menu, tearoff=0)

for sk in ["ESC", "CTRL", "ALT", "SHIFT", "WIN", "CMD", "DEL", "INS", "BACKSPACE", "SPACE", "TAB", "ENTER", "UP", "DOWN", "LEFT", "RIGHT"]:
    key_list_menu.add_command(label=sk, command=lambda s=sk: insert_key(s))

key_list_menu.add_separator()
for i in range(1, 13):
    fn_menu.add_command(label=f"F{i}", command=lambda i=i: insert_key(f"F{i}"))
key_list_menu.add_cascade(label="功能鍵 (FN)", menu=fn_menu)

debug_menu.add_command(label="開啟錄製模式", command=toggle_record)
debug_menu.add_command(label="匯入檔案", command=import_txt)
debug_menu.add_separator()
debug_menu.add_checkbutton(label="啟用倒數計時", variable=show_countdown_flag)
debug_menu.add_separator()
debug_menu.add_cascade(label="快速插入按鍵", menu=key_list_menu)
debug_menu.add_cascade(label="調整執行速度", menu=speed_menu)
main_menu.add_cascade(label="偵錯選單 (Debug)", menu=debug_menu)
root.config(menu=main_menu)

f_top = Frame(root, bg='#3b3e4b', height=40); f_top.pack(fill=X)
Label(f_top, text="指令序列控制台 Version 3.2.0", fg='white', bg='#3b3e4b', font=('Microsoft JhengHei', 11)).pack(pady=5)
f_body = Frame(root, bg='#f4f4f9', padx=15, pady=10); f_body.pack(fill=BOTH, expand=True)
text_area = Text(f_body, font=('Consolas', 11), bd=1, relief=SOLID, height=12, undo=True)
text_area.pack(fill=BOTH, expand=True, pady=(5, 10))
Label(f_body, text="循環次數 (輸入 inf 代表無限):", bg='#f4f4f9', fg='#555', font=('Microsoft JhengHei', 9)).pack(anchor=W)
entry2 = Entry(f_body, font=('Consolas', 12), bd=1, relief=SOLID)
entry2.insert(0, "1"); entry2.pack(fill=X, pady=(5, 10), ipady=5)
counter_label = Label(f_body, text="就緒", bg='#f4f4f9', fg='#5c6bc0', font=('Microsoft JhengHei', 10, 'bold'))
counter_label.pack(pady=2)
btn = Button(f_body, text="開始執行 [Ctrl+Shift+F12]", bg='#5c6bc0', fg='white', font=('Microsoft JhengHei', 12, 'bold'), relief=FLAT, command=start_task)
btn.pack(fill=X, ipady=8)

setup_hotkey_listener()

root.mainloop()