"""
Input Blocker v3.0 - Control Panel GUI
Manage all settings with a visual interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path

APP_DIR = Path(os.environ["APPDATA"]) / "InputBlocker"
CONFIG_FILE = APP_DIR / "config.json"

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
        "quick": {"countdown": 3}, "afk": {"countdown": 10},
        "sleep": {"countdown": 30}, "long": {"countdown": 60}
    }
}

class InputBlockerGUI:
    def __init__(self):
        self.cfg = self.load_config()
        self.root = tk.Tk()
        self.root.title("Input Blocker v3.0 - Control Panel")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.build_ui()
    
    def load_config(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                cfg = json.load(f)
                for k, v in DEFAULT_CONFIG.items():
                    if k not in cfg: cfg[k] = v
                return cfg
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.cfg, f, indent=2)
        messagebox.showinfo("Saved", "Settings saved!")
    
    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tab 1: General
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text=" General ")
        
        ttk.Label(tab1, text="Countdown (seconds):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.countdown_var = tk.IntVar(value=self.cfg.get("countdown", 10))
        ttk.Spinbox(tab1, from_=1, to=60, textvariable=self.countdown_var, width=10).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(tab1, text="Unlock Hotkey:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.hotkey_var = tk.StringVar(value=self.cfg.get("unblock_hotkey", "ctrl+shift+b"))
        ttk.Entry(tab1, textvariable=self.hotkey_var, width=20).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(tab1, text="Language:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lang_var = tk.StringVar(value=self.cfg.get("language", "en"))
        ttk.Combobox(tab1, textvariable=self.lang_var, values=["en", "fr", "ar"], width=10, state="readonly").grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(tab1, text="Block Mode:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.block_mode_var = tk.StringVar(value="all")
        if self.cfg.get("mouse_only"): self.block_mode_var.set("mouse")
        elif self.cfg.get("keyboard_only"): self.block_mode_var.set("keyboard")
        ttk.Combobox(tab1, textvariable=self.block_mode_var, values=["all", "mouse", "keyboard"], width=10, state="readonly").grid(row=3, column=1, padx=10, pady=5)
        
        # Tab 2: Features
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text=" Features ")
        
        self.sound_var = tk.BooleanVar(value=self.cfg.get("sound_enabled", True))
        ttk.Checkbutton(tab2, text="Sound Alert", variable=self.sound_var).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.voice_var = tk.BooleanVar(value=self.cfg.get("voice_enabled", False))
        ttk.Checkbutton(tab2, text="Voice Alert", variable=self.voice_var).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.overlay_var = tk.BooleanVar(value=self.cfg.get("overlay_enabled", True))
        ttk.Checkbutton(tab2, text="Overlay Timer", variable=self.overlay_var).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.idle_var = tk.BooleanVar(value=self.cfg.get("idle_enabled", False))
        ttk.Checkbutton(tab2, text="Auto-block on Idle", variable=self.idle_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        ttk.Label(tab2, text="Idle Minutes:").grid(row=3, column=1, padx=10, pady=5)
        self.idle_min_var = tk.IntVar(value=self.cfg.get("idle_minutes", 5))
        ttk.Spinbox(tab2, from_=1, to=60, textvariable=self.idle_min_var, width=5).grid(row=3, column=2, padx=5, pady=5)
        
        self.schedule_var = tk.BooleanVar(value=self.cfg.get("schedule_enabled", False))
        ttk.Checkbutton(tab2, text="Scheduled Block", variable=self.schedule_var).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        
        ttk.Label(tab2, text="Time (HH:MM):").grid(row=4, column=1, padx=10, pady=5)
        self.schedule_time_var = tk.StringVar(value=self.cfg.get("schedule_time", "22:00"))
        ttk.Entry(tab2, textvariable=self.schedule_time_var, width=10).grid(row=4, column=2, padx=5, pady=5)
        
        self.timer_var = tk.BooleanVar(value=self.cfg.get("timer_enabled", False))
        ttk.Checkbutton(tab2, text="Auto-unblock Timer", variable=self.timer_var).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        
        ttk.Label(tab2, text="Minutes:").grid(row=5, column=1, padx=10, pady=5)
        self.timer_min_var = tk.IntVar(value=self.cfg.get("timer_minutes", 0))
        ttk.Spinbox(tab2, from_=0, to=480, textvariable=self.timer_min_var, width=5).grid(row=5, column=2, padx=5, pady=5)
        
        self.repeat_var = tk.BooleanVar(value=self.cfg.get("repeat_enabled", False))
        ttk.Checkbutton(tab2, text="Repeat Daily", variable=self.repeat_var).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        
        self.startup_var = tk.BooleanVar(value=self.cfg.get("startup_enabled", False))
        ttk.Checkbutton(tab2, text="Block on Windows Startup", variable=self.startup_var).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        
        # Tab 3: Security
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text=" Security ")
        
        self.pwd_req_var = tk.BooleanVar(value=self.cfg.get("require_password", False))
        ttk.Checkbutton(tab3, text="Require Password to Unblock", variable=self.pwd_req_var).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        ttk.Label(tab3, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.pwd_var = tk.StringVar(value=self.cfg.get("password", ""))
        ttk.Entry(tab3, textvariable=self.pwd_var, show="*", width=20).grid(row=1, column=1, padx=10, pady=5)
        
        # Tab 4: Presets
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text=" Presets ")
        
        presets = self.cfg.get("presets", {})
        for i, (name, data) in enumerate(presets.items()):
            ttk.Label(tab4, text=f"{name.upper()}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            var = tk.IntVar(value=data.get("countdown", 10))
            ttk.Spinbox(tab4, from_=1, to=60, textvariable=var, width=5).grid(row=i, column=1, padx=5, pady=5)
            ttk.Label(tab4, text="sec").grid(row=i, column=2, padx=5, pady=5)
            setattr(self, f"preset_{name}_var", var)
        
        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Save Settings", command=self.save_settings).pack(side="left", padx=5, pady=5)
        ttk.Button(btn_frame, text="Reset Default", command=self.reset_default).pack(side="left", padx=5, pady=5)
        ttk.Button(btn_frame, text="Run Blocker", command=self.run_blocker).pack(side="right", padx=5, pady=5)
        ttk.Button(btn_frame, text="View Stats", command=self.view_stats).pack(side="right", padx=5, pady=5)
        ttk.Button(btn_frame, text="View History", command=self.view_history).pack(side="right", padx=5, pady=5)
    
    def save_settings(self):
        self.cfg["countdown"] = self.countdown_var.get()
        self.cfg["unblock_hotkey"] = self.hotkey_var.get()
        self.cfg["language"] = self.lang_var.get()
        mode = self.block_mode_var.get()
        self.cfg["mouse_only"] = mode == "mouse"
        self.cfg["keyboard_only"] = mode == "keyboard"
        self.cfg["sound_enabled"] = self.sound_var.get()
        self.cfg["voice_enabled"] = self.voice_var.get()
        self.cfg["overlay_enabled"] = self.overlay_var.get()
        self.cfg["idle_enabled"] = self.idle_var.get()
        self.cfg["idle_minutes"] = self.idle_min_var.get()
        self.cfg["schedule_enabled"] = self.schedule_var.get()
        self.cfg["schedule_time"] = self.schedule_time_var.get()
        self.cfg["timer_enabled"] = self.timer_var.get()
        self.cfg["timer_minutes"] = self.timer_min_var.get()
        self.cfg["repeat_enabled"] = self.repeat_var.get()
        self.cfg["startup_enabled"] = self.startup_var.get()
        self.cfg["require_password"] = self.pwd_req_var.get()
        self.cfg["password"] = self.pwd_var.get()
        for name in ["quick", "afk", "sleep", "long"]:
            var = getattr(self, f"preset_{name}_var", None)
            if var: self.cfg["presets"][name]["countdown"] = var.get()
        self.save_config()
    
    def reset_default(self):
        if messagebox.askyesno("Reset", "Reset all settings to default?"):
            self.cfg = DEFAULT_CONFIG.copy()
            self.save_config()
            self.root.destroy()
            InputBlockerGUI()
    
    def run_blocker(self):
        self.save_settings()
        os.system(f'start python "{Path(__file__).parent / "block_input.py"}" --countdown {self.cfg["countdown"]}')
    
    def view_stats(self):
        history_file = APP_DIR / "block_history.json"
        if not history_file.exists():
            messagebox.showinfo("Stats", "No data yet.")
            return
        with open(history_file) as f:
            history = json.load(f)
        total = len(history)
        durations = [h.get("duration", 0) for h in history]
        avg = sum(durations) / len(durations) / 60 if durations else 0
        total_min = sum(durations) / 60
        msg = f"Total Blocks: {total}\nTotal Time: {total_min:.1f} min\nAverage: {avg:.1f} min"
        messagebox.showinfo("Stats", msg)
    
    def view_history(self):
        history_file = APP_DIR / "block_history.json"
        if not history_file.exists():
            messagebox.showinfo("History", "No history yet.")
            return
        with open(history_file) as f:
            history = json.load(f)
        lines = [f"[{h.get('start', '?')}] {h.get('duration', '?')}s" for h in history[-10:]]
        messagebox.showinfo("History", "\n".join(lines) if lines else "No history.")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    InputBlockerGUI().run()
