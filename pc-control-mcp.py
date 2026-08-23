import asyncio, json, os, subprocess, sys, tempfile, time, platform, shutil, re, uuid, logging
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
log = logging.getLogger("pc-control-mcp")

FAILSAFE = True
FAILSAFE_CORNERS = [(0, 0)]
MOUSE_PAUSE = 0.1

try:
    import pyautogui
    pyautogui.FAILSAFE = FAILSAFE
    pyautogui.PAUSE = MOUSE_PAUSE
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

try:
    import pygetwindow as gw
    HAS_PYWIN = True
except ImportError:
    HAS_PYWIN = False

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

try:
    from PIL import Image, ImageGrab
    import io
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import mss
    import numpy as np
    HAS_MSS = True
except ImportError:
    HAS_MSS = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

from mcp.server import FastMCP

server = FastMCP("pc-control", log_level="WARNING")

@contextmanager
def safe_zone():
    try:
        yield
    except pyautogui.FailSafeException:
        log.warning("Fail-safe triggered")
        raise
    except Exception as e:
        log.error(f"Operation failed: {e}")
        raise

def coord(x: Optional[int], y: Optional[int]):
    if x is None or y is None:
        return pyautogui.position()
    return x, y

@server.tool()
def move_mouse(x: int, y: int, duration: float = 0.0):
    with safe_zone():
        pyautogui.moveTo(x, y, duration=duration)
        return f"Moved to ({x}, {y})"

@server.tool()
def click(x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1):
    with safe_zone():
        cx, cy = coord(x, y)
        if x is not None:
            pyautogui.click(cx, cy, clicks=clicks, button=button)
        else:
            pyautogui.click(clicks=clicks, button=button)
        return f"Clicked {button} at ({cx}, {cy}) x{clicks}"

@server.tool()
def double_click(x: Optional[int] = None, y: Optional[int] = None):
    return click(x, y, clicks=2)

@server.tool()
def right_click(x: Optional[int] = None, y: Optional[int] = None):
    return click(x, y, button="right")

@server.tool()
def drag(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5):
    with safe_zone():
        pyautogui.moveTo(from_x, from_y)
        pyautogui.drag(to_x, to_y, duration=duration)
        return f"Dragged from ({from_x}, {from_y}) to ({to_x}, {to_y})"

@server.tool()
def scroll(amount: int, x: Optional[int] = None, y: Optional[int] = None):
    with safe_zone():
        pyautogui.scroll(amount, x, y)
        return f"Scrolled {amount}"

@server.tool()
def mouse_position():
    x, y = pyautogui.position()
    return {"x": x, "y": y}

@server.tool()
def screen_size():
    w, h = pyautogui.size()
    return {"width": w, "height": h}

@server.tool()
def type_text(text: str, interval: float = 0.0):
    with safe_zone():
        pyautogui.typewrite(text, interval=interval)
        return f"Typed {len(text)} characters"

@server.tool()
def press_key(key: str):
    with safe_zone():
        pyautogui.press(key)
        return f"Pressed {key}"

@server.tool()
def hotkey(keys: str):
    parts = keys.split("+")
    with safe_zone():
        pyautogui.hotkey(*parts)
        return f"Hotkey: {keys}"

@server.tool()
def key_down(key: str):
    with safe_zone():
        pyautogui.keyDown(key)
        return f"Key down: {key}"

@server.tool()
def key_up(key: str):
    with safe_zone():
        pyautogui.keyUp(key)
        return f"Key up: {key}"

@server.tool()
def screenshot(save_to: Optional[str] = None):
    with safe_zone():
        img = pyautogui.screenshot()
        if save_to:
            img.save(save_to)
            return f"Screenshot saved to {save_to}"
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

@server.tool()
def screenshot_region(left: int, top: int, width: int, height: int, save_to: Optional[str] = None):
    with safe_zone():
        img = pyautogui.screenshot(region=(left, top, width, height))
        if save_to:
            img.save(save_to)
            return f"Region screenshot saved to {save_to}"
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

@server.tool()
def ocr_screen():
    if not HAS_TESSERACT:
        return "Tesseract OCR not installed"
    with safe_zone():
        img = pyautogui.screenshot()
        text = pytesseract.image_to_string(img)
        return text.strip()

@server.tool()
def ocr_region(left: int, top: int, width: int, height: int):
    if not HAS_TESSERACT:
        return "Tesseract OCR not installed"
    with safe_zone():
        img = pyautogui.screenshot(region=(left, top, width, height))
        text = pytesseract.image_to_string(img)
        return text.strip()

@server.tool()
def find_text_on_screen(text: str):
    if not HAS_TESSERACT:
        return "Tesseract OCR not installed"
    with safe_zone():
        img = pyautogui.screenshot()
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        results = []
        for i, word in enumerate(data["text"]):
            if word and text.lower() in word.lower():
                results.append({
                    "text": word,
                    "x": data["left"][i],
                    "y": data["top"][i],
                    "w": data["width"][i],
                    "h": data["height"][i],
                    "confidence": data["conf"][i]
                })
        return results

@server.tool()
def clipboard_get():
    if not HAS_CLIPBOARD:
        return "Clipboard module not available"
    return pyperclip.paste()

@server.tool()
def clipboard_set(text: str):
    if not HAS_CLIPBOARD:
        return "Clipboard module not available"
    pyperclip.copy(text)
    return f"Copied {len(text)} chars to clipboard"

@server.tool()
def list_windows():
    if not HAS_PYWIN:
        return "pygetwindow not available"
    windows = gw.getAllWindows()
    result = []
    for w in windows:
        if w.title.strip():
            result.append({"title": w.title, "left": w.left, "top": w.top, "width": w.width, "height": w.height, "visible": w.visible, "active": w.isActive})
    return result[:50]

@server.tool()
def activate_window(title: str):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    try:
        matches[0].activate()
        return f"Activated: {matches[0].title}"
    except Exception as e:
        return f"Could not activate: {e}"

@server.tool()
def close_window(title: str):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    matches[0].close()
    return f"Closed: {matches[0].title}"

@server.tool()
def minimize_window(title: str):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    matches[0].minimize()
    return f"Minimized: {matches[0].title}"

@server.tool()
def maximize_window(title: str):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    matches[0].maximize()
    return f"Maximized: {matches[0].title}"

@server.tool()
def resize_window(title: str, width: int, height: int):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    matches[0].resizeTo(width, height)
    return f"Resized: {matches[0].title} to {width}x{height}"

@server.tool()
def move_window(title: str, x: int, y: int):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    matches[0].moveTo(x, y)
    return f"Moved: {matches[0].title} to ({x}, {y})"

@server.tool()
def window_info(title: str):
    if not HAS_PYWIN:
        return "pygetwindow not available"
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    if not matches:
        return f"No window matching '{title}'"
    w = matches[0]
    return {"title": w.title, "left": w.left, "top": w.top, "width": w.width, "height": w.height, "visible": w.visible, "active": w.isActive, "maximized": w.isMaximized, "minimized": w.isMinimized}

if HAS_PSUTIL:
    @server.tool()
    def list_processes(filter_str: Optional[str] = None, max_results: int = 30):
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
            try:
                pinfo = proc.info
                if filter_str and filter_str.lower() not in pinfo["name"].lower():
                    continue
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(processes, key=lambda p: p.get("cpu_percent", 0) or 0, reverse=True)[:max_results]

    @server.tool()
    def kill_process(name: str):
        killed = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if name.lower() in proc.info["name"].lower():
                    proc.kill()
                    killed.append(proc.info["name"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return f"Killed {len(killed)} process(es): {killed}"

    @server.tool()
    def system_info():
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "cpu_count": psutil.cpu_count(),
            "memory": dict(psutil.virtual_memory()._asdict()),
            "disk": {p.mountpoint: dict(p._asdict()) for p in psutil.disk_partitions() if p.fstype},
            "boot_time": psutil.boot_time(),
            "platform": platform.platform(),
            "hostname": platform.node(),
            "username": os.environ.get("USERNAME", "")
        }

@server.tool()
def get_pixel(x: int, y: int):
    with safe_zone():
        px = pyautogui.pixel(x, y)
        return {"r": px[0], "g": px[1], "b": px[2]}

@server.tool()
def pixel_matches_color(x: int, y: int, r: int, g: int, b: int, tolerance: int = 10):
    with safe_zone():
        return pyautogui.pixelMatchesColor(x, y, (r, g, b), tolerance=tolerance)

@server.tool()
def locate_on_screen(image_path: str, confidence: float = 0.8):
    with safe_zone():
        pos = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if pos:
            return {"left": pos.left, "top": pos.top, "width": pos.width, "height": pos.height}
        return None

@server.tool()
def click_on_image(image_path: str, confidence: float = 0.8, button: str = "left"):
    with safe_zone():
        pos = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if pos:
            center = pyautogui.center(pos)
            pyautogui.click(center.x, center.y, button=button)
            return f"Clicked image at ({center.x}, {center.y})"
        return "Image not found on screen"

@server.tool()
def run_command(command: str, timeout: int = 30):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"stdout": result.stdout[-2000:], "stderr": result.stderr[-1000:], "return_code": result.returncode}
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout}s"
    except Exception as e:
        return f"Error: {e}"

@server.tool()
def run_powershell(script: str, timeout: int = 30):
    try:
        result = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True, timeout=timeout)
        return {"stdout": result.stdout[-3000:], "stderr": result.stderr[-1000:], "return_code": result.returncode}
    except subprocess.TimeoutExpired:
        return f"Script timed out after {timeout}s"
    except Exception as e:
        return f"Error: {e}"

@server.tool()
def open_file(path: str):
    os.startfile(path)
    return f"Opened: {path}"

@server.tool()
def open_url(url: str):
    import webbrowser
    webbrowser.open(url)
    return f"Opened URL: {url}"

@server.tool()
def get_screen_pixel_count():
    w, h = pyautogui.size()
    return {"width": w, "height": h, "total_pixels": w * h}

@server.tool()
def list_scripts():
    scripts_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    ps1_scripts = list(scripts_dir.glob("*.ps1"))
    bat_scripts = list(scripts_dir.glob("*.bat"))
    py_scripts = list(scripts_dir.glob("*.py"))
    result = []
    for f in ps1_scripts + bat_scripts + py_scripts:
        result.append({"name": f.name, "size": f.stat().st_size, "modified": f.stat().st_mtime})
    return result

if __name__ == "__main__":
    log.info("Starting pc-control MCP server...")
    server.run()
