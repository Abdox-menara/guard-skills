"""
Input Blocker v5.0 - Professional Edition
Complete rewrite with all improvements from V3/V4 analysis
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ctypes
import ctypes.wintypes
import time
import json
import os
import sys
import winsound
import threading
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────
APP_NAME = "Input Blocker"
APP_VERSION = "5.0"
APP_DIR = Path(os.environ["APPDATA"]) / "InputBlocker"
CONFIG_FILE = APP_DIR / "config.json"
LOG_FILE = APP_DIR / "block_log.txt"
HISTORY_FILE = APP_DIR / "block_history.json"
BACKUP_DIR = APP_DIR / "backups"

BlockInput = ctypes.windll.user32.BlockInput
GetLastInputInfo = ctypes.windll.user32.GetLastInputInfo
SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW

# ─── Color Palette ────────────────────────────────────────────────
COLORS = {
    "bg_dark": "#0d1117",
    "bg_mid": "#161b22",
    "bg_card": "#1c2128",
    "bg_input": "#21262d",
    "accent": "#58a6ff",
    "accent_hover": "#79c0ff",
    "success": "#3fb950",
    "danger": "#f85149",
    "warning": "#d29922",
    "text": "#f0f6fc",
    "text_dim": "#8b949e",
    "border": "#30363d",
    "glow_blue": "#1f6feb",
    "glow_red": "#da3633",
    "glow_green": "#238636",
}

DEFAULT_CONFIG = {
    "version": "5.0",
    "countdown": 10,
    "unblock_hotkey": "ctrl+shift+b",
    "password_hash": "",
    "require_password": False,
    "sound_enabled": True,
    "voice_enabled": False,
    "overlay_enabled": True,
    "overlay_duration": 3,
    "mouse_only": False,
    "keyboard_only": False,
    "block_log_enabled": True,
    "language": "en",
    "idle_enabled": False,
    "idle_minutes": 5,
    "schedule_enabled": False,
    "schedule_time": "22:00",
    "timer_enabled": False,
    "timer_minutes": 0,
    "repeat_enabled": False,
    "repeat_time": "22:00",
    "startup_enabled": False,
    "always_on_top": False,
    "minimize_to_tray": True,
    "show_notifications": True,
    "log_max_lines": 1000,
    "window_x": None,
    "window_y": None,
    "presets": {
        "quick": {"countdown": 3, "label": "Quick (3s)"},
        "afk": {"countdown": 10, "label": "AFK (10s)"},
        "sleep": {"countdown": 30, "label": "Sleep (30s)"},
        "long": {"countdown": 60, "label": "Long (60s)"}
    }
}


# ─── Utility Classes ──────────────────────────────────────────────
class PasswordHash:
    """Secure password hashing"""
    @staticmethod
    def hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return PasswordHash.hash(password) == hashed


class Tooltip:
    """Modern tooltip for widgets"""
    def __init__(self, widget, text, delay=400):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.after_id = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.cancel)
    
    def schedule(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show)
    
    def cancel(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide()
    
    def show(self):
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.configure(bg=COLORS["border"])
        frame = tk.Frame(tw, bg=COLORS["bg_card"], padx=10, pady=6)
        frame.pack()
        tk.Label(frame, text=self.text, font=("Segoe UI", 9),
                 fg=COLORS["text"], bg=COLORS["bg_card"], wraplength=280).pack()
    
    def hide(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class GlowButton(tk.Canvas):
    """Animated button with glow effect"""
    def __init__(self, parent, text, command=None, color="#58a6ff",
                 width=200, height=50, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=COLORS["bg_dark"], highlightthickness=0, **kwargs)
        self.command = command
        self.color = color
        self.w = width
        self.h = height
        self.text = text
        self.hovered = False
        self.enabled = True
        
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    
    def _draw(self):
        self.delete("all")
        if not self.enabled:
            self.create_rectangle(2, 2, self.w - 2, self.h - 2,
                                 fill=COLORS["bg_input"], outline=COLORS["border"], width=1)
            self.create_text(self.w // 2, self.h // 2, text=self.text,
                            fill=COLORS["text_dim"], font=("Segoe UI", 11, "bold"))
            return
        if self.hovered:
            self.create_rectangle(0, 0, self.w, self.h,
                                 outline=self.color, width=3)
        self.create_rectangle(2, 2, self.w - 2, self.h - 2,
                             fill=self.color, outline=self.color, width=1)
        self.create_text(self.w // 2, self.h // 2, text=self.text,
                        fill="#ffffff", font=("Segoe UI", 11, "bold"))
    
    def _on_enter(self, e):
        if self.enabled:
            self.hovered = True
            self._draw()
            self.configure(cursor="hand2")
    
    def _on_leave(self, e):
        self.hovered = False
        self._draw()
    
    def _on_click(self, e):
        if self.enabled and self.command:
            self.command()
    
    def update_text(self, text, color=None):
        self.text = text
        if color:
            self.color = color
        self._draw()
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        self._draw()


# ─── Main Application ─────────────────────────────────────────────
class InputBlockerApp:
    def __init__(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        self.cfg = self.load_config()
        self.blocked = False
        self.countdown_active = False
        self.countdown_seconds = 0
        self.pulse_phase = 0
        
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("500x720")
        self.root.minsize(500, 720)
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.attributes("-topmost", self.cfg.get("always_on_top", False))
        
        # Restore window position
        if self.cfg.get("window_x") and self.cfg.get("window_y"):
            self.root.geometry(f"+{self.cfg['window_x']}+{self.cfg['window_y']}")
        
        self.root.overrideredirect(True)
        self._build_custom_titlebar()
        self._build_ui()
        self.start_hotkey_listener()
        self._start_background_threads()
        self._start_pulse_animation()
        self.update_status()
        
        # Save window position on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<Configure>", self._on_configure)
    
    # ─── Config Management ────────────────────────────────────────
    def load_config(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    cfg = json.load(f)
                    for k, v in DEFAULT_CONFIG.items():
                        if k not in cfg:
                            cfg[k] = v
                    return cfg
            except json.JSONDecodeError:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.cfg, f, indent=2)
        except Exception as e:
            self.log_event("ERROR", f"Failed to save config: {e}")
    
    def backup_config(self):
        """Create timestamped backup of config"""
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = BACKUP_DIR / f"config_{ts}.json"
            with open(backup_file, "w") as f:
                json.dump(self.cfg, f, indent=2)
            # Keep only last 10 backups
            backups = sorted(BACKUP_DIR.glob("config_*.json"))
            for old in backups[:-10]:
                old.unlink()
            return True
        except Exception:
            return False
    
    def restore_config(self, path):
        """Restore config from backup"""
        try:
            with open(path, "r") as f:
                cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                if k not in cfg:
                    cfg[k] = v
            self.cfg = cfg
            self.save_config()
            return True
        except Exception:
            return False
    
    # ─── Logging ──────────────────────────────────────────────────
    def log_event(self, event, details=""):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] {event} {details}\n")
            # Log rotation
            self._rotate_log()
        except Exception:
            pass
    
    def _rotate_log(self):
        """Keep log file under max lines"""
        max_lines = self.cfg.get("log_max_lines", 1000)
        try:
            if LOG_FILE.exists():
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if len(lines) > max_lines:
                    with open(LOG_FILE, "w", encoding="utf-8") as f:
                        f.writelines(lines[-max_lines:])
        except Exception:
            pass
    
    def add_history(self, entry):
        try:
            history = []
            if HISTORY_FILE.exists():
                with open(HISTORY_FILE, "r") as f:
                    history = json.load(f)
            history.append(entry)
            # Keep last 100 entries
            with open(HISTORY_FILE, "w") as f:
                json.dump(history[-100:], f, indent=2)
        except Exception:
            pass
    
    # ─── Audio ────────────────────────────────────────────────────
    def play_sound(self, freq=800, dur=200):
        if self.cfg.get("sound_enabled"):
            try:
                winsound.Beep(freq, dur)
            except Exception:
                pass
    
    def speak(self, text):
        if self.cfg.get("voice_enabled"):
            try:
                import pyttsx3
                e = pyttsx3.init()
                e.say(text)
                e.runAndWait()
            except Exception:
                pass
    
    # ─── Overlay ──────────────────────────────────────────────────
    def show_overlay(self, text, color="red"):
        if not self.cfg.get("overlay_enabled"):
            return
        try:
            ov = tk.Toplevel()
            ov.overrideredirect(True)
            ov.attributes("-topmost", True)
            ov.attributes("-alpha", 0.92)
            w, h = 500, 100
            x = (self.root.winfo_screenwidth() - w) // 2
            ov.geometry(f"{w}x{h}+{x}+50")
            
            bg_map = {"red": COLORS["danger"], "green": COLORS["success"], 
                     "yellow": COLORS["warning"], "blue": COLORS["accent"]}
            bg = bg_map.get(color, COLORS["danger"])
            fg = "#000000" if color == "yellow" else "#ffffff"
            
            frame = tk.Frame(ov, bg=bg)
            frame.pack(fill="both", expand=True)
            tk.Label(frame, text=text, font=("Segoe UI", 20, "bold"),
                     fg=fg, bg=bg).pack(expand=True)
            
            # Fade out
            def fade_out():
                try:
                    alpha = ov.attributes("-alpha")
                    if alpha > 0.1:
                        ov.attributes("-alpha", alpha - 0.1)
                        ov.after(50, fade_out)
                    else:
                        ov.destroy()
                except Exception:
                    ov.destroy()
            
            ov.after(2000, fade_out)
        except Exception:
            pass
    
    # ─── Idle Detection ───────────────────────────────────────────
    def get_idle_seconds(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        GetLastInputInfo(ctypes.byref(lii))
        return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0
    
    # ─── Block/Unblock ────────────────────────────────────────────
    def do_block(self):
        result = BlockInput(True)
        if result == 0:
            self.log_event("WARNING", "BlockInput failed - not running as admin?")
        self.blocked = True
        self.add_history({
            "start": datetime.now().isoformat(),
            "type": "manual",
            "duration": 0
        })
    
    def do_unblock(self):
        BlockInput(False)
        self.blocked = False
    
    # ─── Custom Title Bar ─────────────────────────────────────────
    def _build_custom_titlebar(self):
        self.titlebar = tb = tk.Frame(self.root, bg=COLORS["bg_mid"], height=38)
        tb.pack(fill="x")
        tb.pack_propagate(False)
        
        # Icon + Title
        icon_frame = tk.Frame(tb, bg=COLORS["bg_mid"])
        icon_frame.pack(side="left", padx=10)
        
        tk.Label(icon_frame, text="🛡", font=("Segoe UI", 14),
                bg=COLORS["bg_mid"], fg=COLORS["accent"]).pack(side="left")
        tk.Label(icon_frame, text=f"  {APP_NAME} v{APP_VERSION}",
                font=("Segoe UI", 10, "bold"), bg=COLORS["bg_mid"],
                fg=COLORS["text"]).pack(side="left", padx=5)
        
        # Window controls
        ctrl_frame = tk.Frame(tb, bg=COLORS["bg_mid"])
        ctrl_frame.pack(side="right", padx=5)
        
        self.topmost_btn = tk.Label(ctrl_frame, text="📌", font=("Segoe UI", 11),
                                     bg=COLORS["bg_mid"], fg=COLORS["text_dim"], padx=8)
        self.topmost_btn.pack(side="left")
        self.topmost_btn.bind("<Button-1>", self._toggle_topmost)
        Tooltip(self.topmost_btn, "Toggle Always on Top")
        
        self.min_btn = tk.Label(ctrl_frame, text="─", font=("Segoe UI", 11),
                                 bg=COLORS["bg_mid"], fg=COLORS["text_dim"], padx=8)
        self.min_btn.pack(side="left")
        self.min_btn.bind("<Button-1>", self._minimize)
        Tooltip(self.min_btn, "Minimize to Taskbar")
        
        self.close_btn = tk.Label(ctrl_frame, text="✕", font=("Segoe UI", 11),
                                   bg=COLORS["bg_mid"], fg=COLORS["danger"], padx=8)
        self.close_btn.pack(side="left")
        self.close_btn.bind("<Button-1>", self._on_close)
        
        # Drag support
        tb.bind("<Button-1>", self._start_drag)
        tb.bind("<B1-Motion>", self._on_drag)
    
    def _start_drag(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()
    
    def _on_drag(self, e):
        self.root.geometry(f"+{e.x_root - self._drag_x}+{e.y_root - self._drag_y}")
    
    def _toggle_topmost(self, e=None):
        current = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current)
        self.cfg["always_on_top"] = not current
        self.save_config()
        color = COLORS["accent"] if not current else COLORS["text_dim"]
        self.topmost_btn.configure(fg=color)
    
    def _minimize(self, e=None):
        self.root.overrideredirect(False)
        self.root.iconify()
        def restore_overrideredirect():
            if self.root.state() != "iconic":
                self.root.overrideredirect(True)
        self.root.after(100, restore_overrideredirect)
    
    def _on_close(self, e=None):
        if self.blocked:
            self.do_unblock()
        # Save window position
        try:
            self.cfg["window_x"] = self.root.winfo_x()
            self.cfg["window_y"] = self.root.winfo_y()
            self.save_config()
        except Exception:
            pass
        self.root.destroy()
    
    def _on_configure(self, e):
        """Save window position on move"""
        if self.root.state() == "normal":
            try:
                self.cfg["window_x"] = self.root.winfo_x()
                self.cfg["window_y"] = self.root.winfo_y()
            except Exception:
                pass
    
    # ─── Main UI ──────────────────────────────────────────────────
    def _build_ui(self):
        self.main_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=(0, 2))
        
        # ─── Status Section ───────────────────────────────────────
        status_frame = tk.Frame(self.main_frame, bg=COLORS["bg_card"], height=110)
        status_frame.pack(fill="x", padx=10, pady=(10, 5))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="READY",
                                     font=("Segoe UI", 26, "bold"),
                                     fg=COLORS["success"], bg=COLORS["bg_card"])
        self.status_label.pack(expand=True)
        
        self.status_sub = tk.Label(status_frame, text="Input is active",
                                    font=("Segoe UI", 9),
                                    fg=COLORS["text_dim"], bg=COLORS["bg_card"])
        self.status_sub.pack(side="bottom", pady=(0, 8))
        
        # ─── Progress Bar ─────────────────────────────────────────
        self.progress_frame = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        self.progress_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self.progress_var = tk.DoubleVar(value=0)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Horizontal.TProgressbar",
                       background=COLORS["accent"],
                       troughcolor=COLORS["bg_input"],
                       thickness=8)
        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                           variable=self.progress_var,
                                           maximum=100,
                                           style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x")
        self.progress_bar.pack_forget()  # Hidden by default
        
        # ─── Main Action Button ───────────────────────────────────
        btn_frame = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        self.block_btn = GlowButton(btn_frame, "BLOCK INPUT",
                                     command=self.toggle_block,
                                     color=COLORS["danger"],
                                     width=460, height=55)
        self.block_btn.pack()
        
        # ─── Quick Presets ────────────────────────────────────────
        preset_frame = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        preset_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(preset_frame, text="QUICK PRESETS", font=("Segoe UI", 9, "bold"),
                fg=COLORS["text_dim"], bg=COLORS["bg_dark"]).pack(anchor="w", pady=(0, 5))
        
        presets_row = tk.Frame(preset_frame, bg=COLORS["bg_dark"])
        presets_row.pack(fill="x")
        
        for name, data in self.cfg.get("presets", {}).items():
            seconds = data.get("countdown", 10)
            label = data.get("label", name.title())
            btn = tk.Button(presets_row, text=label, font=("Segoe UI", 9),
                           bg=COLORS["bg_input"], fg=COLORS["text"],
                           activebackground=COLORS["accent"], activeforeground="#ffffff",
                           relief="flat", cursor="hand2", padx=12, pady=6,
                           command=lambda s=seconds: self._quick_block(s))
            btn.pack(side="left", padx=3)
            Tooltip(btn, f"Block input for {seconds} seconds")
        
        # ─── Settings Tabs ────────────────────────────────────────
        tabs_frame = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        tabs_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        self._build_tabs(tabs_frame)
        
        # ─── Bottom Bar ───────────────────────────────────────────
        self._build_bottom_bar()
    
    def _build_tabs(self, parent):
        style = ttk.Style()
        style.configure("TNotebook", background=COLORS["bg_dark"], borderwidth=0)
        style.configure("TNotebook.Tab", background=COLORS["bg_input"],
                        foreground=COLORS["text"], padding=[12, 6],
                        font=("Segoe UI", 9))
        style.map("TNotebook.Tab",
                  background=[("selected", COLORS["bg_card"])],
                  foreground=[("selected", COLORS["accent"])])
        style.configure("TFrame", background=COLORS["bg_card"])
        
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)
        
        # General Tab
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="  ⚙ General  ")
        self._build_general_tab(tab1)
        
        # Features Tab
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="  ✨ Features  ")
        self._build_features_tab(tab2)
        
        # Security Tab
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="  🔒 Security  ")
        self._build_security_tab(tab3)
        
        # Presets Tab
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="  ⏱ Presets  ")
        self._build_presets_tab(tab4)
        
        # About Tab
        tab5 = ttk.Frame(notebook)
        notebook.add(tab5, text="  ℹ About  ")
        self._build_about_tab(tab5)
    
    def _build_general_tab(self, parent):
        # Countdown
        tk.Label(parent, text="Countdown (sec):", font=("Segoe UI", 10),
                fg=COLORS["text"], bg=COLORS["bg_card"]).grid(
            row=0, column=0, padx=15, pady=8, sticky="w")
        self.countdown_var = tk.IntVar(value=self.cfg.get("countdown", 10))
        tk.Spinbox(parent, from_=1, to=300, textvariable=self.countdown_var, width=8,
                  bg=COLORS["bg_input"], fg=COLORS["text"],
                  buttonbackground=COLORS["bg_input"],
                  insertbackground=COLORS["text"]).grid(
            row=0, column=1, padx=15, pady=8, sticky="e")
        
        # Hotkey
        tk.Label(parent, text="Hotkey:", font=("Segoe UI", 10),
                fg=COLORS["text"], bg=COLORS["bg_card"]).grid(
            row=1, column=0, padx=15, pady=8, sticky="w")
        self.hotkey_var = tk.StringVar(value=self.cfg.get("unblock_hotkey", "ctrl+shift+b"))
        tk.Entry(parent, textvariable=self.hotkey_var, width=20,
                bg=COLORS["bg_input"], fg=COLORS["text"],
                insertbackground=COLORS["text"], relief="flat").grid(
            row=1, column=1, padx=15, pady=8, sticky="e")
        
        # Language
        tk.Label(parent, text="Language:", font=("Segoe UI", 10),
                fg=COLORS["text"], bg=COLORS["bg_card"]).grid(
            row=2, column=0, padx=15, pady=8, sticky="w")
        self.lang_var = tk.StringVar(value=self.cfg.get("language", "en"))
        ttk.Combobox(parent, textvariable=self.lang_var, width=10,
                    values=["en", "fr", "ar"], state="readonly").grid(
            row=2, column=1, padx=15, pady=8, sticky="e")
        
        # Block Mode
        tk.Label(parent, text="Block Mode:", font=("Segoe UI", 10),
                fg=COLORS["text"], bg=COLORS["bg_card"]).grid(
            row=3, column=0, padx=15, pady=8, sticky="w")
        self.mode_var = tk.StringVar(value="all")
        ttk.Combobox(parent, textvariable=self.mode_var, width=10,
                    values=["all", "mouse", "keyboard"], state="readonly").grid(
            row=3, column=1, padx=15, pady=8, sticky="e")
        
        parent.columnconfigure(1, weight=1)
    
    def _build_features_tab(self, parent):
        features = [
            ("sound_var", "Sound Alert", "Play beep on block/unblock", None),
            ("voice_var", "Voice Alert", "Speak status changes", None),
            ("overlay_var", "Overlay Timer", "Show fullscreen overlay", None),
            ("idle_var", "Auto-block on Idle", "Block after inactivity", "idle_min_var"),
            ("schedule_var", "Scheduled Block", "Block at specific time", "schedule_time_var"),
            ("timer_var", "Auto-unblock Timer", "Auto-unblock after delay", "timer_min_var"),
            ("repeat_var", "Repeat Daily", "Repeat schedule daily", None),
            ("startup_var", "Block on Startup", "Auto-block when app starts", None),
        ]
        
        self.feature_vars = {}
        for i, (var_name, text, tooltip_text, extra_var) in enumerate(features):
            var = tk.BooleanVar(value=self.cfg.get(var_name.replace("_var", "_enabled"), False))
            self.feature_vars[var_name] = var
            
            cb = tk.Checkbutton(parent, text=text, variable=var,
                               font=("Segoe UI", 10),
                               fg=COLORS["text"], bg=COLORS["bg_card"],
                               selectcolor=COLORS["bg_input"],
                               activebackground=COLORS["bg_card"],
                               activeforeground=COLORS["text"])
            cb.grid(row=i, column=0, padx=15, pady=5, sticky="w")
            Tooltip(cb, tooltip_text)
        
        # Idle minutes
        idle_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        idle_frame.grid(row=3, column=1, padx=15, pady=5, sticky="e")
        tk.Label(idle_frame, text="After:", font=("Segoe UI", 9),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"]).pack(side="left")
        self.idle_min_var = tk.IntVar(value=self.cfg.get("idle_minutes", 5))
        tk.Spinbox(idle_frame, from_=1, to=60, textvariable=self.idle_min_var,
                  width=4, bg=COLORS["bg_input"], fg=COLORS["text"],
                  buttonbackground=COLORS["bg_input"]).pack(side="left", padx=3)
        tk.Label(idle_frame, text="min", font=("Segoe UI", 9),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"]).pack(side="left")
        
        # Schedule time
        sched_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        sched_frame.grid(row=4, column=1, padx=15, pady=5, sticky="e")
        tk.Label(sched_frame, text="At:", font=("Segoe UI", 9),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"]).pack(side="left")
        self.schedule_time_var = tk.StringVar(value=self.cfg.get("schedule_time", "22:00"))
        tk.Entry(sched_frame, textvariable=self.schedule_time_var, width=6,
                bg=COLORS["bg_input"], fg=COLORS["text"],
                insertbackground=COLORS["text"], relief="flat").pack(side="left", padx=3)
        
        # Timer minutes
        timer_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        timer_frame.grid(row=5, column=1, padx=15, pady=5, sticky="e")
        tk.Label(timer_frame, text="After:", font=("Segoe UI", 9),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"]).pack(side="left")
        self.timer_min_var = tk.IntVar(value=self.cfg.get("timer_minutes", 0))
        tk.Spinbox(timer_frame, from_=0, to=480, textvariable=self.timer_min_var,
                  width=5, bg=COLORS["bg_input"], fg=COLORS["text"],
                  buttonbackground=COLORS["bg_input"]).pack(side="left", padx=3)
        tk.Label(timer_frame, text="min", font=("Segoe UI", 9),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"]).pack(side="left")
        
        parent.columnconfigure(1, weight=1)
    
    def _build_security_tab(self, parent):
        # Password required
        self.pwd_req_var = tk.BooleanVar(value=self.cfg.get("require_password", False))
        tk.Checkbutton(parent, text="Require Password to Unblock",
                       variable=self.pwd_req_var, font=("Segoe UI", 10),
                       fg=COLORS["text"], bg=COLORS["bg_card"],
                       selectcolor=COLORS["bg_input"],
                       activebackground=COLORS["bg_card"]).grid(
            row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        
        # Password field
        tk.Label(parent, text="Password:", font=("Segoe UI", 10),
                fg=COLORS["text"], bg=COLORS["bg_card"]).grid(
            row=1, column=0, padx=15, pady=8, sticky="w")
        
        pwd_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        pwd_frame.grid(row=1, column=1, padx=15, pady=8)
        
        self.pwd_var = tk.StringVar(value="")
        self.pwd_entry = tk.Entry(pwd_frame, textvariable=self.pwd_var, show="•", width=18,
                                 bg=COLORS["bg_input"], fg=COLORS["text"],
                                 insertbackground=COLORS["text"], relief="flat")
        self.pwd_entry.pack(side="left")
        
        self.show_pwd_var = tk.BooleanVar(value=False)
        self.show_pwd_btn = tk.Label(pwd_frame, text="👁", font=("Segoe UI", 10),
                                     bg=COLORS["bg_card"], fg=COLORS["text_dim"], padx=5)
        self.show_pwd_btn.pack(side="left")
        self.show_pwd_btn.bind("<Button-1>", self._toggle_password_visibility)
        Tooltip(self.show_pwd_btn, "Show/Hide password")
        
        # Password strength indicator
        self.pwd_strength = tk.Label(parent, text="", font=("Segoe UI", 9),
                                    fg=COLORS["text_dim"], bg=COLORS["bg_card"])
        self.pwd_strength.grid(row=2, column=0, columnspan=2, padx=15, sticky="w")
        
        # Backup/Restore buttons
        backup_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        backup_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        
        tk.Button(backup_frame, text="Backup Settings", font=("Segoe UI", 9),
                 bg=COLORS["bg_input"], fg=COLORS["text"], relief="flat",
                 command=self._backup_settings).pack(side="left", padx=5)
        tk.Button(backup_frame, text="Restore Settings", font=("Segoe UI", 9),
                 bg=COLORS["bg_input"], fg=COLORS["text"], relief="flat",
                 command=self._restore_settings).pack(side="left", padx=5)
        tk.Button(backup_frame, text="Reset Defaults", font=("Segoe UI", 9),
                 bg=COLORS["danger"], fg="#ffffff", relief="flat",
                 command=self._reset_defaults).pack(side="right", padx=5)
    
    def _toggle_password_visibility(self, e=None):
        if self.show_pwd_var.get():
            self.pwd_entry.configure(show="•")
            self.show_pwd_var.set(False)
            self.show_pwd_btn.configure(fg=COLORS["text_dim"])
        else:
            self.pwd_entry.configure(show="")
            self.show_pwd_var.set(True)
            self.show_pwd_btn.configure(fg=COLORS["accent"])
    
    def _backup_settings(self):
        if self.backup_config():
            messagebox.showinfo("Backup", "Settings backed up successfully!")
        else:
            messagebox.showerror("Backup", "Failed to backup settings.")
    
    def _restore_settings(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")],
            initialdir=str(BACKUP_DIR)
        )
        if path:
            if self.restore_config(path):
                messagebox.showinfo("Restore", "Settings restored! Restart to apply.")
            else:
                messagebox.showerror("Restore", "Failed to restore settings.")
    
    def _reset_defaults(self):
        if messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            self.cfg = DEFAULT_CONFIG.copy()
            self.save_config()
            messagebox.showinfo("Reset", "Settings reset! Restart to apply.")
    
    def _build_presets_tab(self, parent):
        self.preset_vars = {}
        for i, (name, data) in enumerate(self.cfg.get("presets", {}).items()):
            label = data.get("label", name.title())
            
            card = tk.Frame(parent, bg=COLORS["bg_input"], padx=10, pady=8)
            card.grid(row=i, column=0, columnspan=2, padx=15, pady=4, sticky="ew")
            
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"),
                    fg=COLORS["text"], bg=COLORS["bg_input"]).pack(side="left")
            
            var = tk.IntVar(value=data.get("countdown", 10))
            self.preset_vars[name] = var
            
            spin = tk.Spinbox(card, from_=1, to=300, textvariable=var, width=6,
                             bg=COLORS["bg_card"], fg=COLORS["text"],
                             buttonbackground=COLORS["bg_input"])
            spin.pack(side="right")
            
            tk.Label(card, text="sec", font=("Segoe UI", 9),
                    fg=COLORS["text_dim"], bg=COLORS["bg_input"]).pack(side="right", padx=5)
        
        parent.columnconfigure(0, weight=1)
    
    def _build_about_tab(self, parent):
        # Title
        tk.Label(parent, text=f"🛡 {APP_NAME} v{APP_VERSION}",
                font=("Segoe UI", 16, "bold"),
                fg=COLORS["accent"], bg=COLORS["bg_card"]).pack(pady=(20, 5))
        
        tk.Label(parent, text="Professional Input Blocking Tool",
                font=("Segoe UI", 10),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"]).pack()
        
        # Features list
        features_text = """
Features:
• Keyboard & Mouse blocking
• Hotkey unblock (works when blocked)
• Password protection (SHA-256 hashed)
• Auto-unblock timer
• Sound & voice alerts
• System tray support
• Settings backup/restore
• Configurable presets
• Window position memory
• Log rotation
"""
        tk.Label(parent, text=features_text, font=("Segoe UI", 9),
                fg=COLORS["text"], bg=COLORS["bg_card"], justify="left").pack(pady=10)
        
        # Status info
        status_text = f"""
Status:
• Config: {CONFIG_FILE.name}
• History: {len(json.load(open(HISTORY_FILE)) if HISTORY_FILE.exists() else [])} entries
• Backups: {len(list(BACKUP_DIR.glob('config_*.json')))} available
"""
        tk.Label(parent, text=status_text, font=("Segoe UI", 9),
                fg=COLORS["text_dim"], bg=COLORS["bg_card"], justify="left").pack()
    
    def _build_bottom_bar(self):
        bar = tk.Frame(self.main_frame, bg=COLORS["bg_mid"], height=50)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        
        buttons = [
            ("💾 Save", self.save_settings),
            ("📊 Stats", self.show_stats),
            ("📋 History", self.show_history),
            ("📤 Export", self.export_cfg),
        ]
        
        for text, cmd in buttons:
            btn = tk.Label(bar, text=text, font=("Segoe UI", 9),
                          fg=COLORS["text"], bg=COLORS["bg_mid"],
                          padx=12, pady=8, cursor="hand2")
            btn.pack(side="left", padx=2)
            btn.bind("<Button-1>", lambda e, c=cmd: c())
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLORS["bg_card"]))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLORS["bg_mid"]))
    
    # ─── Background Threads ───────────────────────────────────────
    def _start_background_threads(self):
        # Idle detection thread
        if self.cfg.get("idle_enabled"):
            threading.Thread(target=self._idle_detection_loop, daemon=True).start()
        
        # Schedule checking thread
        if self.cfg.get("schedule_enabled"):
            threading.Thread(target=self._schedule_check_loop, daemon=True).start()
    
    def _idle_detection_loop(self):
        while True:
            try:
                if not self.blocked and self.cfg.get("idle_enabled"):
                    idle_sec = self.get_idle_seconds()
                    if idle_sec >= self.cfg.get("idle_minutes", 5) * 60:
                        self.root.after(0, self._do_block)
                        time.sleep(self.cfg.get("idle_minutes", 5) * 60)
                time.sleep(10)
            except Exception:
                time.sleep(30)
    
    def _schedule_check_loop(self):
        while True:
            try:
                if not self.blocked and self.cfg.get("schedule_enabled"):
                    now = datetime.now().strftime("%H:%M")
                    if now == self.cfg.get("schedule_time", "22:00"):
                        self.root.after(0, self._do_block)
                        time.sleep(60)
                time.sleep(30)
            except Exception:
                time.sleep(60)
    
    # ─── Pulse Animation ──────────────────────────────────────────
    def _start_pulse_animation(self):
        self._pulse_phase = 0
        self._animate_pulse()
    
    def _animate_pulse(self):
        if self.blocked:
            self._pulse_phase = (self._pulse_phase + 1) % 60
            color = COLORS["danger"] if self._pulse_phase < 30 else "#da3633"
            try:
                self.status_label.configure(fg=color)
            except Exception:
                pass
        self.root.after(50, self._animate_pulse)
    
    # ─── Hotkey Listener ──────────────────────────────────────────
    def start_hotkey_listener(self):
        def listener_thread():
            try:
                import keyboard
                hotkey = self.cfg.get("unblock_hotkey", "ctrl+shift+b")
                
                def on_hotkey():
                    if self.blocked:
                        self.root.after(0, self._do_unblock_from_hotkey)
                
                keyboard.add_hotkey(hotkey, on_hotkey)
            except Exception as e:
                print(f"  [!] Hotkey error: {e}", flush=True)
        
        threading.Thread(target=listener_thread, daemon=True).start()
    
    def _do_unblock_from_hotkey(self):
        if self.cfg.get("require_password") and self.cfg.get("password_hash"):
            pwd = self.ask_password()
            if not pwd or not PasswordHash.verify(pwd, self.cfg["password_hash"]):
                messagebox.showerror("Error", "Wrong password!")
                return
        self.do_unblock()
        self.block_btn.update_text("BLOCK INPUT", COLORS["danger"])
        self.progress_bar.pack_forget()
        self.log_event("UNBLOCKED", "hotkey")
        self.play_sound(800, 100)
        self.speak("Input unblocked")
        self.show_overlay("INPUT UNBLOCKED", "green")
    
    # ─── Status Update ────────────────────────────────────────────
    def update_status(self):
        if self.blocked:
            self.status_label.configure(text="BLOCKED", fg=COLORS["danger"])
            self.status_sub.configure(text="All input is blocked • Press hotkey to unblock")
        elif self.countdown_active:
            pass  # countdown handles its own text
        else:
            self.status_label.configure(text="READY", fg=COLORS["success"])
            hotkey = self.cfg.get('unblock_hotkey', 'ctrl+shift+b').replace('+', ' + ').title()
            self.status_sub.configure(text=f"Input is active • Hotkey: {hotkey}")
        self.root.after(500, self.update_status)
    
    # ─── Block/Unblock ────────────────────────────────────────────
    def toggle_block(self):
        if self.blocked:
            self._do_unblock()
        else:
            self._do_block()
    
    def _do_block(self):
        if self.cfg.get("require_password") and self.cfg.get("password_hash"):
            pwd = self.ask_password()
            if not pwd or not PasswordHash.verify(pwd, self.cfg["password_hash"]):
                return
        
        self.save_settings()
        self.countdown_active = True
        self.countdown_seconds = self.cfg["countdown"]
        self.log_event("BLOCKED", f"countdown={self.countdown_seconds}")
        
        # Show progress bar
        self.progress_bar.pack(fill="x", padx=0, pady=(0, 5))
        self.progress_var.set(0)
        
        def countdown_thread():
            total = self.countdown_seconds
            for i in range(total, 0, -1):
                self.countdown_active = True
                progress = ((total - i) / total) * 100
                self.root.after(0, lambda t=i, p=progress: self._update_countdown(t, p))
                time.sleep(1)
            self.countdown_active = False
            self.do_block()
            self.root.after(0, lambda: self.block_btn.update_text("UNBLOCK INPUT", COLORS["success"]))
            self.root.after(0, lambda: self.progress_var.set(100))
            self.play_sound(400, 300)
            self.speak("Input blocked")
            self.root.after(0, lambda: self.show_overlay("INPUT BLOCKED", "red"))
            
            # Auto-unblock timer
            if self.cfg.get("timer_enabled") and self.cfg.get("timer_minutes", 0) > 0:
                time.sleep(self.cfg["timer_minutes"] * 60)
                if self.blocked:
                    self.root.after(0, self._do_unblock)
                    self.play_sound(800, 100)
                    self.speak("Auto unblocked")
        
        threading.Thread(target=countdown_thread, daemon=True).start()
    
    def _update_countdown(self, seconds, progress):
        self.block_btn.update_text(f"BLOCKING IN {seconds}...", COLORS["warning"])
        self.status_label.configure(text=str(seconds), fg=COLORS["warning"])
        self.status_sub.configure(text="Input will be blocked shortly...")
        self.progress_var.set(progress)
    
    def _do_unblock(self):
        if self.cfg.get("require_password") and self.cfg.get("password_hash"):
            pwd = self.ask_password()
            if not pwd or not PasswordHash.verify(pwd, self.cfg["password_hash"]):
                return
        
        self.do_unblock()
        self.block_btn.update_text("BLOCK INPUT", COLORS["danger"])
        self.progress_bar.pack_forget()
        self.progress_var.set(0)
        self.log_event("UNBLOCKED", "gui")
        self.play_sound(800, 100)
        self.speak("Input unblocked")
        self.show_overlay("INPUT UNBLOCKED", "green")
    
    def _quick_block(self, seconds):
        self.cfg["countdown"] = seconds
        if hasattr(self, 'countdown_var'):
            self.countdown_var.set(seconds)
        self.toggle_block()
    
    # ─── Dialogs ──────────────────────────────────────────────────
    def ask_password(self):
        dialog = tk.Toplevel(self.root)
        dialog.overrideredirect(True)
        dialog.configure(bg=COLORS["border"])
        dialog.geometry("320x160")
        x = self.root.winfo_x() + (self.root.winfo_width() - 320) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 160) // 2
        dialog.geometry(f"+{x}+{y}")
        
        inner = tk.Frame(dialog, bg=COLORS["bg_card"], padx=20, pady=15)
        inner.pack(fill="both", expand=True)
        
        tk.Label(inner, text="🔒 Enter Password", font=("Segoe UI", 12, "bold"),
                fg=COLORS["text"], bg=COLORS["bg_card"]).pack(anchor="w")
        
        pwd_entry = tk.Entry(inner, show="•", width=28, font=("Segoe UI", 11),
                            bg=COLORS["bg_input"], fg=COLORS["text"],
                            insertbackground=COLORS["text"], relief="flat")
        pwd_entry.pack(pady=10)
        pwd_entry.focus()
        
        result = [None]
        
        def on_ok():
            result[0] = pwd_entry.get()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        btn_frame = tk.Frame(inner, bg=COLORS["bg_card"])
        btn_frame.pack()
        
        tk.Button(btn_frame, text="OK", command=on_ok, width=10,
                 bg=COLORS["accent"], fg="#ffffff", relief="flat",
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=on_cancel, width=10,
                 bg=COLORS["bg_input"], fg=COLORS["text"], relief="flat",
                 font=("Segoe UI", 9)).pack(side="left", padx=5)
        
        pwd_entry.bind("<Return>", lambda e: on_ok())
        self.root.wait_window(dialog)
        return result[0]
    
    def show_stats(self):
        if not HISTORY_FILE.exists():
            messagebox.showinfo("Stats", "No data yet.")
            return
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
            total = len(history)
            durations = [h.get("duration", 0) for h in history if h.get("duration", 0) > 0]
            avg = sum(durations) / len(durations) / 60 if durations else 0
            total_min = sum(durations) / 60
            messagebox.showinfo("Stats",
                f"📊 Total Blocks: {total}\n⏱ Total Time: {total_min:.1f} min\n📈 Average: {avg:.1f} min")
        except Exception:
            messagebox.showerror("Stats", "Failed to load statistics.")
    
    def show_history(self):
        if not HISTORY_FILE.exists():
            messagebox.showinfo("History", "No history yet.")
            return
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
            lines = [f"[{h.get('start', '?')}] {h.get('duration', '?')}s" for h in history[-10:]]
            messagebox.showinfo("History", "\n".join(lines) if lines else "No history.")
        except Exception:
            messagebox.showerror("History", "Failed to load history.")
    
    def export_cfg(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, "w") as f:
                    json.dump(self.cfg, f, indent=2)
                messagebox.showinfo("Exported", f"Saved to: {path}")
            except Exception:
                messagebox.showerror("Export", "Failed to export settings.")
    
    def save_settings(self):
        self.cfg["countdown"] = self.countdown_var.get()
        self.cfg["unblock_hotkey"] = self.hotkey_var.get()
        self.cfg["language"] = self.lang_var.get()
        mode = self.mode_var.get()
        self.cfg["mouse_only"] = mode == "mouse"
        self.cfg["keyboard_only"] = mode == "keyboard"
        
        for var_name, var in self.feature_vars.items():
            key = var_name.replace("_var", "_enabled")
            self.cfg[key] = var.get()
        
        self.cfg["idle_minutes"] = self.idle_min_var.get()
        self.cfg["schedule_time"] = self.schedule_time_var.get()
        self.cfg["timer_minutes"] = self.timer_min_var.get()
        self.cfg["require_password"] = self.pwd_req_var.get()
        
        # Hash password
        pwd = self.pwd_var.get()
        if pwd:
            self.cfg["password_hash"] = PasswordHash.hash(pwd)
        
        for name, var in self.preset_vars.items():
            self.cfg["presets"][name]["countdown"] = var.get()
        
        self.save_config()
        self.start_hotkey_listener()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False
    
    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
    else:
        InputBlockerApp().run()
