from pynput import keyboard
import time
import os
from datetime import datetime
from config import display_reverse_alphabetical, hotkey

timestamps = []
start_time = time.time()
folder_path = "txt-summaries"

#output_folder = "/Users/tunadorable/Local_Repositories/Quickly_Extract_Science_Papers/timestamps"
#if not os.path.exists(output_folder):
#    os.makedirs(output_folder)

# reverse=True because when I bulk open files in safari it displays them in reverse-chronological order. 
text_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')], reverse=display_reverse_alphabetical)
file_iter = iter(text_files)

def on_activate():
    print("Hotkey activated")  # Debug line
    global file_iter
    try:
        filename = next(file_iter).replace('.txt', '')
    except StopIteration:
        filename = "Outro"
    
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    timestamps.append(f"{minutes}:{seconds:02d} {filename}")

timestamps.append("0:00 Intro")

current_keys = set()

def on_press(key):
    if key == keyboard.KeyCode.from_char(hotkey):
        on_activate()
    elif key == keyboard.Key.esc:
        return False  # Stop listener

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


with open(f"timestamps.txt", "w") as f:
    f.write("\n".join(timestamps))
