"""
Input Blocker v3.0 - Block keyboard/mouse until manually unblocked
20 Features: Hotkey, Sound, Overlay, Password, Presets, Mouse/Keyboard only, Tray, Log,
             Idle detect, Schedule, Timer, Repeat, Startup, History, Stats, Export, Language, Voice
"""
import ctypes
import time
import sys
import os
import json
import winsound
import threading
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# --- Constants ---
APP_NAME = "Input Blocker"
APP_DIR = Path(os.environ["APPDATA"]) / "InputBlocker"
CONFIG_FILE = APP_DIR / "config.json"
LOG_FILE = APP_DIR / "block_log.txt"
HISTORY_FILE = APP_DIR / "block_history.json"

BlockInput = ctypes.windll.user32.BlockInput
GetLastInputInfo = ctypes.windll.user32.GetLastInputInfo

# --- Languages ---
LANGS = {
    "en": {
        "blocked": "INPUT BLOCKED", "unblocked": "INPUT UNBLOCKED",
        "countdown": "BLOCKING IN {0}", "preparing": "PREPARING ({0}s)",
        "wrong_pwd": "Wrong password!", "session_end": "Session ended.",
        "no_admin": "Requesting Admin...", "history_empty": "No history.",
        "stats_title": "=== BLOCK STATS ===",
    },
    "fr": {
        "blocked": "ENTREE BLOQUEE", "unblocked": "ENTREE DEBLOQUEE",
        "countdown": "BLOCAGE DANS {0}", "preparing": "PREPARATION ({0}s)",
        "wrong_pwd": "Mot de passe incorrect!", "session_end": "Session terminee.",
        "no_admin": "Droits admin demandes...", "history_empty": "Aucun historique.",
        "stats_title": "=== STATS BLOCAGE ===",
    },
    "ar": {
        "blocked": "تم حظر الإدخال", "unblocked": "تم فتح الإدخال",
        "countdown": "الحظر خلال {0}", "preparing": "جاري التحضير ({0}s)",
        "wrong_pwd": "كلمة المرور خاطئة!", "session_end": "انتهت الجلسة.",
        "no_admin": "طلب صلاحيات المشرف...", "history_empty": "لا يوجد سجل.",
        "stats_title": "=== إحصائيات الحظر ===",
    }
}

def get_text(key, lang="en", *args):
    text = LANGS.get(lang, LANGS["en"]).get(key, key)
    return text.format(*args) if args else text

# --- Default Config ---
DEFAULT_CONFIG = {
    "version": "3.0", "countdown": 10, "unblock_hotkey": "ctrl+shift+b",
    "password": "", "require_password": False, "sound_enabled": True,
    "voice_enabled": False, "overlay_enabled": True, "overlay_duration": 3,
    "mouse_only": False, "keyboard_only": False, "block_log_enabled": True,
    "language": "en", "idle_enabled": False, "idle_minutes": 5,
    "schedule_enabled": False, "schedule_time": "22:00",
    "timer_enabled": False, "timer_minutes": 0,
    "repeat_enabled": False, "repeat_time": "22:00", "startup_enabled": False,
    "presets": {
        "quick": {"countdown": 3, "label": "Quick (3s)"},
        "afk": {"countdown": 10, "label": "AFK (10s)"},
        "sleep": {"countdown": 30, "label": "Sleep (30s)"},
        "long": {"countdown": 60, "label": "Long (60s)"}
    }
}

# --- Config ---
def load_config():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                if k not in cfg: cfg[k] = v
            return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# --- Logging ---
def log_event(event, details=""):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {event}" + (f" - {details}" if details else "")
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

# --- History (Feature 16) ---
def add_history(entry):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    history = json.load(open(HISTORY_FILE)) if HISTORY_FILE.exists() else []
    history.append(entry)
    with open(HISTORY_FILE, "w") as f: json.dump(history[-100:], f, indent=2)

def get_history():
    return json.load(open(HISTORY_FILE)) if HISTORY_FILE.exists() else []

# --- Stats (Feature 17) ---
def get_stats():
    h = get_history()
    if not h: return None
    durations = [x.get("duration", 0) for x in h if x.get("duration")]
    return {
        "total_blocks": len(h), "total_minutes": round(sum(durations) / 60, 1),
        "avg_minutes": round(sum(durations) / len(durations) / 60, 1) if durations else 0,
        "last_block": h[-1].get("start", "N/A")
    }

def print_stats(lang="en"):
    s = get_stats()
    print(f"\n{get_text('stats_title', lang)}")
    if s:
        print(f"  Total blocks    : {s['total_blocks']}")
        print(f"  Total time      : {s['total_minutes']} min")
        print(f"  Average session : {s['avg_minutes']} min")
        print(f"  Last block      : {s['last_block']}")
    else: print("  No data yet.\n")

def print_history(lang="en", limit=10):
    h = get_history()
    print(f"\n  {get_text('history_empty', lang) if not h else f'Last {limit} blocks:'}")
    for x in h[-limit:]:
        print(f"  [{x.get('start', '?')}] {x.get('duration', '?')}s - {x.get('method', '?')}")
    print()

# --- Export/Import (Feature 18) ---
def export_config(output):
    if CONFIG_FILE.exists(): shutil.copy(CONFIG_FILE, output); print(f"  Exported: {output}")

def import_config(source):
    if os.path.exists(source): shutil.copy(source, CONFIG_FILE); print(f"  Imported: {source}")

# --- Voice (Feature 20) ---
def speak(text, enabled=True):
    if not enabled: return
    try:
        import pyttsx3; e = pyttsx3.init(); e.say(text); e.runAndWait()
    except: pass

# --- Sound ---
def play_sound(freq=800, dur=200):
    try: winsound.Beep(freq, dur)
    except: pass

def sound_blocked(): play_sound(400, 300)
def sound_unblocked(): play_sound(800, 100); time.sleep(0.1); play_sound(1000, 100)
def sound_countdown(t): play_sound(600, 100)

# --- Overlay ---
def show_overlay(text, duration=3, color="red"):
    try:
        import tkinter as tk
        root = tk.Tk(); root.overrideredirect(True); root.attributes("-topmost", True); root.attributes("-alpha", 0.85)
        w, h = 400, 100
        root.geometry(f"{w}x{h}+{(root.winfo_screenwidth()-w)//2}+50")
        colors = {"red": ("#ff0000", "#fff"), "green": ("#00ff00", "#000"), "yellow": ("#ffff00", "#000")}
        bg, fg = colors.get(color, ("#ff0000", "#fff"))
        root.configure(bg=bg)
        tk.Label(root, text=text, font=("Consolas", 18, "bold"), fg=fg, bg=bg).pack(expand=True)
        root.after(int(duration*1000), root.destroy); root.mainloop()
    except: pass

# --- Password ---
def ask_password():
    try:
        import tkinter as tk; from tkinter import simpledialog
        root = tk.Tk(); root.withdraw()
        pwd = simpledialog.askstring("Unlock", "Password:", show="*"); root.destroy()
        return pwd
    except: return None

# --- Idle Detection (Feature 11) ---
def get_idle_seconds():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO(); lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    GetLastInputInfo(ctypes.byref(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def idle_monitor(cfg, callback):
    while True:
        time.sleep(30)
        if get_idle_seconds() / 60 >= cfg.get("idle_minutes", 5):
            print(f"  [IDLE] PC idle - blocking...", flush=True); callback(); break

# --- Block Logic ---
def do_block(cfg): BlockInput(True)
def do_unblock(): BlockInput(False)

# --- Countdown ---
def run_countdown(seconds, cfg, lang="en"):
    print(f"  {get_text('preparing', lang, seconds)}")
    for i in range(seconds, 0, -1):
        print(f"  {i}", flush=True)
        if cfg.get("sound_enabled"): sound_countdown(i)
        if cfg.get("overlay_enabled"): show_overlay(get_text("countdown", lang, i), 1, "yellow")
        if cfg.get("voice_enabled") and i == seconds: speak(get_text("countdown", lang, i), True)
        time.sleep(1)

# --- Main Block ---
def run_block(cfg, lang="en"):
    run_countdown(cfg["countdown"], cfg, lang)
    print(f"\n  [{get_text('blocked', lang)}]", flush=True)
    if cfg.get("sound_enabled"): sound_blocked()
    if cfg.get("voice_enabled"): speak(get_text("blocked", lang), True)
    if cfg.get("overlay_enabled"): show_overlay(get_text("blocked", lang), cfg.get("overlay_duration", 3), "red")
    do_block(cfg); log_event("BLOCKED", f"hotkey={cfg.get('unblock_hotkey')}")
    print(f"  Unblock: {cfg.get('unblock_hotkey', 'ctrl+shift+b')}\n  Or press Ctrl+Alt+Del", flush=True)

# --- Timer (Feature 13) ---
def timer_unblock(cfg, stop_event, duration_min):
    time.sleep(duration_min * 60)
    if not stop_event.is_set():
        print("  [TIMER] Auto-unblock!", flush=True); do_unblock()
        log_event("UNBLOCKED", "timer")
        if cfg.get("sound_enabled"): sound_unblocked()
        if cfg.get("voice_enabled"): speak("Input unblocked", True)
        stop_event.set()

# --- Schedule (Feature 12) ---
def wait_for_schedule(time_str):
    while True:
        now = datetime.now()
        target = datetime.strptime(time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
        if target <= now: target += timedelta(days=1)
        diff = (target - now).total_seconds()
        if diff <= 60: return True
        time.sleep(min(diff - 55, 60))

# --- Hotkey ---
def hotkey_listener(cfg, stop_event, lang="en"):
    try:
        import keyboard
        def on_hotkey():
            if stop_event.is_set(): return
            if cfg.get("require_password") and cfg.get("password"):
                if ask_password() != cfg.get("password"):
                    print(f"  [!] {get_text('wrong_pwd', lang)}", flush=True)
                    if cfg.get("sound_enabled"): play_sound(200, 500)
                    return
            print(f"  [{get_text('unblocked', lang)}]", flush=True); do_unblock()
            log_event("UNBLOCKED", "hotkey")
            if cfg.get("sound_enabled"): sound_unblocked()
            if cfg.get("voice_enabled"): speak(get_text("unblocked", lang), True)
            if cfg.get("overlay_enabled"): show_overlay(get_text("unblocked", lang), 2, "green")
            stop_event.set()
        keyboard.add_hotkey(cfg.get("unblock_hotkey", "ctrl+shift+b"), on_hotkey)
    except Exception as e: print(f"  [!] Hotkey error: {e}")

# --- Tray ---
def tray_listener(cfg, stop_event, lang="en"):
    try:
        import pystray; from PIL import Image, ImageDraw
        img = Image.new("RGB", (64, 64), "red")
        ImageDraw.Draw(img).rectangle([16, 16, 48, 48], fill="white")
        def on_unblock(icon, item):
            if cfg.get("require_password") and cfg.get("password"):
                if ask_password() != cfg.get("password"): return
            do_unblock(); log_event("UNBLOCKED", "tray")
            if cfg.get("sound_enabled"): sound_unblocked()
            stop_event.set(); icon.stop()
        def on_quit(icon, item): do_unblock(); stop_event.set(); icon.stop()
        menu = pystray.Menu(
            pystray.MenuItem(f"Unblock ({cfg.get('unblock_hotkey')})", on_unblock, default=True),
            pystray.MenuItem("Quit", on_quit))
        pystray.Icon(APP_NAME, img, APP_NAME, menu).run()
    except Exception as e: print(f"  [!] Tray error: {e}")

# --- Startup (Feature 15) ---
def set_startup(enabled):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "InputBlocker"
    if enabled:
        cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}" --nosplash'
        try:
            ctypes.windll.shell32.SHRegSetUSValueW(key, name, ctypes.REG_SZ, cmd, len(cmd)*2, 0)
            print(f"  Startup enabled: {name}")
        except Exception as e: print(f"  Startup error: {e}")
    else:
        try: ctypes.windll.shell32.SHRegDeleteUSValueW(key, name, 0); print(f"  Startup disabled")
        except: pass

# --- CLI ---
def main():
    p = argparse.ArgumentParser(description="Input Blocker v3.0")
    p.add_argument("-c", "--countdown", type=int, help="Seconds before lock")
    p.add_argument("--preset", choices=["quick", "afk", "sleep", "long"])
    p.add_argument("--mouse-only", action="store_true")
    p.add_argument("--keyboard-only", action="store_true")
    p.add_argument("--no-sound", action="store_true")
    p.add_argument("--no-overlay", action="store_true")
    p.add_argument("--voice", action="store_true")
    p.add_argument("--password", type=str)
    p.add_argument("--lang", choices=["en", "fr", "ar"])
    p.add_argument("--config", action="store_true")
    p.add_argument("--history", action="store_true")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--export", type=str)
    p.add_argument("--import", type=str, dest="import_cfg")
    p.add_argument("--idle", type=int)
    p.add_argument("--schedule", type=str)
    p.add_argument("--timer", type=int)
    p.add_argument("--repeat", type=str)
    p.add_argument("--startup", action="store_true")
    p.add_argument("--nosplash", action="store_true")
    args = p.parse_args()

    cfg = load_config()
    lang = args.lang or cfg.get("language", "en")

    if args.config: print(json.dumps(cfg, indent=2)); return
    if args.history: print_history(lang); return
    if args.stats: print_stats(lang); return
    if args.export: export_config(args.export); return
    if args.import_cfg: import_config(args.import_cfg); return
    if args.startup: set_startup(True); return

    if args.preset: cfg["countdown"] = cfg.get("presets", {}).get(args.preset, {}).get("countdown", cfg["countdown"])
    if args.countdown: cfg["countdown"] = args.countdown
    if args.mouse_only: cfg["mouse_only"] = True; cfg["keyboard_only"] = False
    if args.keyboard_only: cfg["keyboard_only"] = True; cfg["mouse_only"] = False
    if args.no_sound: cfg["sound_enabled"] = False
    if args.no_overlay: cfg["overlay_enabled"] = False
    if args.voice: cfg["voice_enabled"] = True
    if args.password: cfg["password"] = args.password; cfg["require_password"] = True
    if args.idle: cfg["idle_enabled"] = True; cfg["idle_minutes"] = args.idle
    if args.schedule: cfg["schedule_enabled"] = True; cfg["schedule_time"] = args.schedule
    if args.timer: cfg["timer_enabled"] = True; cfg["timer_minutes"] = args.timer
    if args.repeat: cfg["repeat_enabled"] = True; cfg["repeat_time"] = args.repeat
    save_config(cfg)

    if not args.nosplash:
        print(f"\n{'='*40}\n  {APP_NAME} v3.0\n{'='*40}")
        print(f"  Countdown  : {cfg['countdown']}s\n  Unblock    : {cfg.get('unblock_hotkey')}")
        print(f"  Sound      : {'ON' if cfg.get('sound_enabled') else 'OFF'}")
        print(f"  Voice      : {'ON' if cfg.get('voice_enabled') else 'OFF'}")
        print(f"  Overlay    : {'ON' if cfg.get('overlay_enabled') else 'OFF'}")
        print(f"  Password   : {'YES' if cfg.get('require_password') else 'NO'}")
        print(f"  Language   : {lang}\n")

    try: is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except: is_admin = False
    if not is_admin:
        print(f"  {get_text('no_admin', lang)}", flush=True)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe",
            f'/c python "{os.path.abspath(__file__)}" --countdown {cfg["countdown"]}', None, 1)
        sys.exit()
    if not args.nosplash: print("  [OK] Admin mode\n")

    stop_event = threading.Event()
    threading.Thread(target=hotkey_listener, args=(cfg, stop_event, lang), daemon=True).start()
    threading.Thread(target=tray_listener, args=(cfg, stop_event, lang), daemon=True).start()

    if cfg.get("timer_enabled") and cfg.get("timer_minutes", 0) > 0:
        threading.Thread(target=timer_unblock, args=(cfg, stop_event, cfg["timer_minutes"]), daemon=True).start()
    if cfg.get("idle_enabled"):
        threading.Thread(target=idle_monitor, args=(cfg, lambda: run_block(cfg, lang)), daemon=True).start()
    if cfg.get("schedule_enabled"):
        threading.Thread(target=lambda: (wait_for_schedule(cfg["schedule_time"]), run_block(cfg, lang)), daemon=True).start()
    if cfg.get("repeat_enabled"):
        threading.Thread(target=lambda: (wait_for_schedule(cfg["repeat_time"]), run_block(cfg, lang)), daemon=True).start()

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not cfg.get("idle_enabled") and not cfg.get("schedule_enabled"):
        run_block(cfg, lang)

    try:
        while not stop_event.is_set(): stop_event.wait(1)
    except KeyboardInterrupt: do_unblock(); log_event("UNBLOCKED", "ctrl+c")

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dur = int((datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")).total_seconds())
    add_history({"start": start_time, "end": end_time, "duration": dur, "method": "hotkey"})
    log_event("SESSION_END")
    if not args.nosplash: print(f"\n  {get_text('session_end', lang)}")

if __name__ == "__main__":
    main()
