import time, threading
import tkinter as tk
import win32gui, win32con, win32api

TITRE = "watch"
DELAI = 0.00001


def taille_ecran():
    return win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


def trouver_fenetre(titre):
    if titre:
        res = []
        def cb(hwnd, _):
            text = win32gui.GetWindowText(hwnd)
            if win32gui.IsWindowVisible(hwnd) and titre.lower() in text.lower():
                res.append(hwnd)
        win32gui.EnumWindows(cb, None)
        if res:
            return res[0]

    hwnd = win32gui.GetForegroundWindow()
    if hwnd and win32gui.IsWindowVisible(hwnd):
        return hwnd
    return None


def clic(hwnd):
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    cx = (right - left) // 2
    cy = (bottom - top) // 2
    lp = win32api.MAKELONG(cx, cy)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lp)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lp)


actif = False


def boucle():
    while True:
        if actif:
            hwnd = trouver_fenetre(TITRE)
            if hwnd:
                clic(hwnd)
        time.sleep(DELAI)


threading.Thread(target=boucle, daemon=True).start()


def set_play():
    global actif
    actif = True
    status_var.set("PLAY")
    status_var_label.config(fg="#2ecc71")


def set_pause():
    global actif
    actif = False
    status_var.set("PAUSE")
    status_var_label.config(fg="#f39c12")


def set_stop():
    global actif
    actif = False
    status_var.set("STOP")
    status_var_label.config(fg="#e74c3c")
    root.destroy()


root = tk.Tk()
root.title("clicker overlay")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.9)
root.overrideredirect(True)
root.configure(bg="#111111")

frame = tk.Frame(root, bg="#111111", padx=12, pady=12)
frame.pack(fill="both", expand=True)

status_var = tk.StringVar(value="PAUSE")
status_var_label = tk.Label(frame, textvariable=status_var, fg="#f39c12", bg="#111111", font=("Segoe UI", 22, "bold"))
status_var_label.pack(pady=(0, 10))

btn_play = tk.Button(frame, text="Play", width=16, height=2, bg="#2ecc71", fg="white", command=set_play, bd=0, activebackground="#27ae60")
btn_play.pack(fill="x", pady=3)

btn_pause = tk.Button(frame, text="Pause", width=16, height=2, bg="#f39c12", fg="white", command=set_pause, bd=0, activebackground="#e67e22")
btn_pause.pack(fill="x", pady=3)

btn_stop = tk.Button(frame, text="Stop", width=16, height=2, bg="#e74c3c", fg="white", command=set_stop, bd=0, activebackground="#c0392b")
btn_stop.pack(fill="x", pady=3)

root.update_idletasks()
root.geometry("220x180+20+20")

# Positionne l'overlay directement sur la fenêtre "watch" quand elle existe.
def place_overlay():
    hwnd = trouver_fenetre(TITRE)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        x = left + 20
        y = top + 20
        root.geometry(f"220x180+{x}+{y}")
    else:
        root.geometry("220x180+20+20")
    root.after(200, place_overlay)

place_overlay()
root.deiconify()
root.update()

# Raccourci clavier en plus, pour garder la commande rapide
import keyboard  # pip install keyboard pywin32
keyboard.add_hotkey("F5", set_play)
keyboard.add_hotkey("F4", set_pause)
keyboard.add_hotkey("F7", lambda: root.destroy())

root.mainloop()