import os
import sys
import time
import threading
import keyboard
import pygame
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import Scale, Label, Entry, Button
import pystray
from PIL import Image
import queue

# Initialize pygame mixer
pygame.mixer.init()

# Create a toast notifier object
toast = ToastNotifier()

# Default settings
chime_interval = 1200  # Default chime interval in seconds
chime_volume = 0.3  # Default chime volume
snooze_duration = 60  # Default snooze duration in minutes
snooze_shortcut = "ctrl+F8"  # Default snooze shortcut
update_queue = queue.Queue() # Create a queue to signal main thread for system tray updates

chime_interval_updated = False

def show_toast_notification(title, message):
    icon_path = os.path.join(sys._MEIPASS, "icon.ico")
    toast.show_toast(title, message, duration=2.5, icon_path=icon_path)

def play_chime():
    chime_sound = os.path.join(sys._MEIPASS, "sound.wav")
    pygame.mixer.music.load(chime_sound)
    pygame.mixer.music.set_volume(chime_volume)
    pygame.mixer.music.play()
    show_toast_notification("REST", "Your eyes")

def snooze(snooze_duration):
    global snooze_active
    snooze_active = True
    show_toast_notification("Chime Snooze", f"Chime snoozed for {snooze_duration} minutes.")
    time.sleep(snooze_duration * 60)  # Convert minutes to seconds
    snooze_active = False
    show_toast_notification("Chime Snooze Ended", "Chime snooze has ended.")

def change_snooze_settings(new_shortcut, new_duration):
    global snooze_shortcut, snooze_duration
    keyboard.remove_hotkey(snooze_shortcut)
    snooze_shortcut = new_shortcut
    snooze_duration = new_duration
    keyboard.add_hotkey(snooze_shortcut, on_snooze_pressed, args=(snooze_duration,))

def on_interval_changed():
    global chime_interval, chime_interval_updated
    new_interval = interval_entry.get()
    if new_interval.isdigit() and int(new_interval)>=2.5:
        chime_interval = int(new_interval) - 2.5
        chime_interval_updated = True
        update_queue.put(True)
    else:
        chime_interval = int(5)
        chime_interval_updated = True
        update_queue.put(True)

def on_volume_changed(value):
    global chime_volume
    chime_volume = float(value)

def on_snooze_pressed(duration):
    if not snooze_active:
        threading.Thread(target=snooze, args=(duration,)).start()

def apply_snooze_settings():
    new_snooze_shortcut = snooze_entry.get()
    new_snooze_duration = int(duration_entry.get())
    change_snooze_settings(new_snooze_shortcut, new_snooze_duration)

# def on_exit(icon, item):
#     icon.stop()
#     root.destroy()

def on_open_settings(icon, item):
    root.deiconify()

def setup_system_tray():
    image = Image.open("icon.ico")
    menu = (
        pystray.MenuItem("Open Settings", on_open_settings),
        # pystray.MenuItem("Exit", on_exit)
    )
    icon = pystray.Icon("name", image, "App Name", menu)
    return icon


def main():
    global snooze_active, chime_interval_updated
    snooze_active = False

    show_toast_notification("Running", "Eye notifier is running")

    keyboard.add_hotkey(snooze_shortcut, on_snooze_pressed, args=(snooze_duration,))

    icon = setup_system_tray()

    while True:
        if not snooze_active:
            play_chime()

        if chime_interval_updated:
            chime_interval_updated = False
            update_queue.put(True)  # Signal update to system tray

        time.sleep(chime_interval)

        try:
            if update_queue.get_nowait():
                icon.update_menu()
        except queue.Empty:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chime Settings")
    # root.withdraw()

    interval_label = Label(root, text="Chime Interval (seconds):")
    interval_label.pack()

    interval_entry = Entry(root)
    interval_entry.insert(0, str(chime_interval))
    interval_entry.pack()

    interval_button = Button(root, text="Apply Interval", command=on_interval_changed)
    interval_button.pack()

    snooze_label = Label(root, text="Snooze Shortcut:")
    snooze_label.pack()

    snooze_entry = Entry(root)
    snooze_entry.insert(0, snooze_shortcut)
    snooze_entry.pack()

    duration_label = Label(root, text="Snooze Duration (minutes):")
    duration_label.pack()

    duration_entry = Entry(root)
    duration_entry.insert(0, str(snooze_duration))
    duration_entry.pack()


    snooze_button = Button(root, text="Apply Snooze Settings", command=apply_snooze_settings)
    snooze_button.pack()


    volume_label = Label(root, text="Chime Volume:")
    volume_label.pack()

    volume_scale = Scale(root, from_=0.0, to=1.0, resolution=0.1, orient="horizontal", command=on_volume_changed)
    volume_scale.set(chime_volume)
    volume_scale.pack()

    threading.Thread(target=main).start()
    root.mainloop()
