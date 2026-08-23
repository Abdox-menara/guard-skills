"""
Enhanced Desktop Control MCP Server v3.0
Advanced Windows PC control with Win32 API, UIA, virtual desktops, clipboard monitor,
OCR-click, template matching, Chrome DevTools, Office COM, WMI, data processing,
IPC, accessibility, and more.
"""

import asyncio, json, os, subprocess, sys, tempfile, time, platform, shutil, re, uuid, logging, glob, socket
from pathlib import Path
from typing import Any, Optional, List, Dict, Tuple, Union
from dataclasses import dataclass, field
from contextlib import contextmanager
import threading
from datetime import datetime, timedelta
try:
    import ctypes
    import ctypes.wintypes
    HAS_CTYPES = True
except ImportError:
    HAS_CTYPES = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
log = logging.getLogger("pc-control-mcp-enhanced")

# Configuration
FAILSAFE = True
FAILSAFE_CORNERS = [(0, 0)]
MOUSE_PAUSE = 0.05
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
LOG_DIR = os.path.join(DESKTOP, "pc_control_logs")
TEMP_DIR = os.path.join(DESKTOP, "pc_control_temp")
DEBUG_DIR = os.path.join(DESKTOP, "pc_control_debug")

# Create directories
for d in [LOG_DIR, TEMP_DIR, DEBUG_DIR]:
    os.makedirs(d, exist_ok=True)

# Import dependencies with graceful fallbacks
try:
    import pyautogui
    pyautogui.FAILSAFE = FAILSAFE
    pyautogui.PAUSE = MOUSE_PAUSE
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False
    log.warning("pyautogui not available")

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
    from PIL import Image, ImageGrab, ImageFilter, ImageEnhance
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

try:
    import winreg
    HAS_REGISTRY = True
except ImportError:
    HAS_REGISTRY = False

# UIA imports
try:
    import comtypes
    import comtypes.client
    # Generate UIAutomationClient module on first run
    try:
        comtypes.client.GetModule("UIAutomationCore.dll")
    except Exception:
        pass
    HAS_UIA = True
except ImportError:
    HAS_UIA = False

try:
    import win32gui
    import win32con
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

from mcp.server import FastMCP

server = FastMCP("pc-control-enhanced", log_level="WARNING")

# ─────────────────────────────────────────────────────────────────────────────
# PERFORMANCE CACHE
# ─────────────────────────────────────────────────────────────────────────────
class PerformanceCache:
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, float] = {}

    def get(self, key: str, ttl: int = 60):
        if key in self.cache and time.time() - self.timestamps[key] < ttl:
            return self.cache[key]
        return None

    def set(self, key: str, value):
        self.cache[key] = value
        self.timestamps[key] = time.time()

    def invalidate(self, key: str):
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)

perf_cache = PerformanceCache()

# ─────────────────────────────────────────────────────────────────────────────
# DEBUG MODE
# ─────────────────────────────────────────────────────────────────────────────
class DebugMode:
    """Captures before/after screenshots for failed actions."""
    def __init__(self):
        self.enabled = True
        self.last_before: Optional[str] = None
        self.last_after: Optional[str] = None

    def capture_before(self, action_name: str) -> Optional[str]:
        if not self.enabled or not HAS_PYAUTOGUI:
            return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DEBUG_DIR, f"before_{action_name}_{ts}.png")
        try:
            pyautogui.screenshot(path)
            self.last_before = path
            return path
        except Exception:
            return None

    def capture_after(self, action_name: str) -> Optional[str]:
        if not self.enabled or not HAS_PYAUTOGUI:
            return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DEBUG_DIR, f"after_{action_name}_{ts}.png")
        try:
            pyautogui.screenshot(path)
            self.last_after = path
            return path
        except Exception:
            return None

    def get_last_pair(self) -> Dict[str, Optional[str]]:
        return {"before": self.last_before, "after": self.last_after}

debug = DebugMode()

# ─────────────────────────────────────────────────────────────────────────────
# SAFETY & UTILITY
# ─────────────────────────────────────────────────────────────────────────────
@contextmanager
def safe_zone():
    initial_mouse_pos = None
    if HAS_PYAUTOGUI:
        try:
            initial_mouse_pos = pyautogui.position()
        except Exception:
            pass
    try:
        yield
    except Exception as e:
        log.error(f"Operation failed: {e}")
        if initial_mouse_pos and HAS_PYAUTOGUI:
            try:
                pyautogui.moveTo(initial_mouse_pos)
            except Exception:
                pass
        raise

def coord(x: Optional[int], y: Optional[int]):
    if x is None or y is None:
        if HAS_PYAUTOGUI:
            return pyautogui.position()
        return (0, 0)
    return x, y

def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (2 ** attempt))
    return None

def safe_clipboard_paste() -> str:
    """Safely get clipboard content, returning empty string on failure."""
    if not HAS_CLIPBOARD:
        return ""
    try:
        return pyperclip.paste()
    except Exception:
        return ""

def safe_clipboard_copy(text: str):
    """Safely copy to clipboard."""
    if HAS_CLIPBOARD:
        try:
            pyperclip.copy(text)
        except Exception:
            pass

def _fuzzy_find_hwnd(title: str):
    """Find window handle by fuzzy title match."""
    if not HAS_WIN32:
        return None
    result = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title.lower() in window_title.lower():
                result.append(hwnd)
        return True
    win32gui.EnumWindows(callback, None)
    return result[0] if result else None

def _find_window(title: str):
    """Find window by partial title match."""
    if not HAS_PYWIN:
        return None
    matches = [w for w in gw.getAllWindows() if title.lower() in w.title.lower() and w.title.strip()]
    return matches[0] if matches else None

# ─────────────────────────────────────────────────────────────────────────────
# 1. UIA-BASED ELEMENT NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
if HAS_UIA:
    try:
        _UIAutomationCore = comtypes.client.GetModule('UIAutomationCore.dll')
        _uia = comtypes.client.CreateObject('{ff48dba4-60ef-4201-aa87-54103eef594e}')
        _uia_elem = _uia.QueryInterface(_UIAutomationCore.IUIAutomation)
    except Exception as _uia_err:
        log.warning(f'UIA init failed: {_uia_err}')
        HAS_UIA = False

    @dataclass
    class UIAElement:
        """Wrapper for UI Automation element."""
        name: str = ""
        control_type: str = ""
        automation_id: str = ""
        class_name: str = ""
        bounds: Dict[str, int] = field(default_factory=dict)
        is_enabled: bool = True
        has_keyboard_focus: bool = False

    def _uia_condition(prop_id: int, value: str):
        """Create a UIA property condition."""
        return _uia_elem.CreatePropertyCondition(prop_id, value)

    def _uia_walk(root, depth: int = 2):
        """Walk UIA tree and collect elements."""
        elements = []
        try:
            walker = _uia_elem.CreateTreeWalker(_uia_elem.RawViewCondition)
            child = walker.GetFirstChildElement(root)
            while child:
                try:
                    name = child.CurrentName or ""
                    ctrl = child.CurrentLocalizedControlType or ""
                    auto_id = child.CurrentAutomationId or ""
                    cls = child.CurrentClassName or ""
                    rect = child.CurrentBoundingRectangle

                    elem = UIAElement(
                        name=name,
                        control_type=ctrl,
                        automation_id=auto_id,
                        class_name=cls,
                        bounds={"left": rect.left, "top": rect.top, "width": rect.width, "height": rect.height} if rect else {},
                        is_enabled=child.CurrentIsEnabled != 0,
                        has_keyboard_focus=child.CurrentHasKeyboardFocus != 0,
                    )
                    elements.append(elem)

                    if depth > 0:
                        elements.extend(_uia_walk(child, depth - 1))
                except Exception:
                    pass
                child = walker.GetNextSiblingElement(child)
        except Exception:
            pass
        return elements

    @server.tool()
    def find_ui_element(name: str, control_type: Optional[str] = None, max_depth: int = 3) -> List[Dict[str, Any]]:
        """Find UI elements by name using Windows UIA (no OCR needed).

        Args:
            name: Element name to search for (partial match).
            control_type: Optional filter (Button, Edit, Text, ComboBox, etc.).
            max_depth: Tree traversal depth (1-5).
        """
        try:
            root = _uia_elem.GetRootElement()
            elements = _uia_walk(root, min(max_depth, 5))
            results = []
            for e in elements:
                if name.lower() in e.name.lower():
                    if control_type is None or control_type.lower() in e.control_type.lower():
                        results.append({
                            "name": e.name,
                            "control_type": e.control_type,
                            "automation_id": e.automation_id,
                            "class_name": e.class_name,
                            "bounds": e.bounds,
                            "is_enabled": e.is_enabled,
                        })
            return results[:20]
        except Exception as ex:
            return [{"error": str(ex)}]

    @server.tool()
    def click_ui_element(name: str, control_type: Optional[str] = None, button: str = "left") -> Dict[str, Any]:
        """Click a UI element by name using Windows UIA.

        Args:
            name: Element name to click.
            control_type: Optional filter.
            button: Mouse button (left/right/middle).
        """
        try:
            root = _uia_elem.GetRootElement()
            elements = _uia_walk(root, 3)
            for e in elements:
                if name.lower() in e.name.lower():
                    if control_type is None or control_type.lower() in e.control_type.lower():
                        b = e.bounds
                        if b and b.get("width", 0) > 0:
                            cx = b["left"] + b["width"] // 2
                            cy = b["top"] + b["height"] // 2
                            if HAS_PYAUTOGUI:
                                debug.capture_before("click_ui")
                                pyautogui.click(cx, cy, button=button)
                                debug.capture_after("click_ui")
                                return {"success": True, "clicked": e.name, "x": cx, "y": cy}
            return {"success": False, "error": f"Element '{name}' not found"}
        except Exception as ex:
            return {"success": False, "error": str(ex)}

    @server.tool()
    def type_in_ui_element(name: str, text: str, clear_first: bool = True) -> Dict[str, Any]:
        """Type text into a UI element (Edit/TextBox) by name using UIA.

        Args:
            name: Element name to type into.
            text: Text to type.
            clear_first: Select all before typing.
        """
        try:
            root = _uia_elem.GetRootElement()
            elements = _uia_walk(root, 3)
            for e in elements:
                if name.lower() in e.name.lower() and "edit" in e.control_type.lower():
                    b = e.bounds
                    if b and b.get("width", 0) > 0:
                        cx = b["left"] + b["width"] // 2
                        cy = b["top"] + b["height"] // 2
                        if HAS_PYAUTOGUI:
                            debug.capture_before("type_ui")
                            pyautogui.click(cx, cy)
                            time.sleep(0.1)
                            if clear_first:
                                pyautogui.hotkey("ctrl", "a")
                                time.sleep(0.05)
                            safe_clipboard_copy(text)
                            pyautogui.hotkey("ctrl", "v")
                            time.sleep(0.1)
                            debug.capture_after("type_ui")
                            return {"success": True, "typed_into": e.name, "length": len(text)}
            return {"success": False, "error": f"Edit element '{name}' not found"}
        except Exception as ex:
            return {"success": False, "error": str(ex)}

    @server.tool()
    def get_ui_tree(max_depth: int = 2, focus_only: bool = False) -> List[Dict[str, Any]]:
        """Get the UI Automation element tree.

        Args:
            max_depth: How deep to traverse (1-4).
            focus_only: Only get focused window subtree.
        """
        try:
            root = _uia_elem.GetRootElement()
            if focus_only:
                root = _uia_elem.FocusedElement()
            elements = _uia_walk(root, min(max_depth, 4))
            return [{
                "name": e.name,
                "control_type": e.control_type,
                "class_name": e.class_name,
                "bounds": e.bounds,
            } for e in elements[:50]]
        except Exception as ex:
            return [{"error": str(ex)}]

else:
    def find_ui_element(name: str, control_type: Optional[str] = None, max_depth: int = 3) -> List[Dict[str, Any]]:
        """Find UI elements by name using Windows UIA (no OCR needed)."""
        return [{"error": "UIA not available. Install comtypes: pip install comtypes"}]

    def click_ui_element(name: str, control_type: Optional[str] = None, button: str = "left") -> Dict[str, Any]:
        """Click a UI element by name using Windows UIA."""
        return {"success": False, "error": "UIA not available"}

    def type_in_ui_element(name: str, text: str, clear_first: bool = True) -> Dict[str, Any]:
        """Type text into a UI element by name using UIA."""
        return {"success": False, "error": "UIA not available"}

    def get_ui_tree(max_depth: int = 2, focus_only: bool = False) -> List[Dict[str, Any]]:
        """Get the UI Automation element tree."""
        return [{"error": "UIA not available"}]

# ─────────────────────────────────────────────────────────────────────────────
# 2. SELF-HEALING WRAPPERS
# ─────────────────────────────────────────────────────────────────────────────
def self_heal_click(x: int, y: int, retries: int = 3, button: str = "left") -> Dict[str, Any]:
    """Click with automatic retry and screenshot verification."""
    if not HAS_PYAUTOGUI:
        return {"success": False, "error": "pyautogui not available"}

    for attempt in range(retries):
        try:
            debug.capture_before(f"click_attempt{attempt}")
            pyautogui.click(x, y, button=button)
            time.sleep(0.1)
            debug.capture_after(f"click_attempt{attempt}")
            return {"success": True, "x": x, "y": y, "attempts": attempt + 1}
        except pyautogui.FailSafeException:
            log.warning(f"FailSafe triggered on attempt {attempt + 1}")
            time.sleep(0.5)
        except Exception as e:
            log.warning(f"Click attempt {attempt + 1} failed: {e}")
            time.sleep(0.3)

    return {"success": False, "error": f"Click failed after {retries} attempts", "x": x, "y": y}

def self_heal_type(text: str, retries: int = 3) -> Dict[str, Any]:
    """Type with clipboard fallback and retry."""
    if not HAS_PYAUTOGUI:
        return {"success": False, "error": "pyautogui not available"}

    original_clipboard = safe_clipboard_paste()

    try:
        for attempt in range(retries):
            try:
                debug.capture_before(f"type_attempt{attempt}")
                safe_clipboard_copy(text)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.1)
                debug.capture_after(f"type_attempt{attempt}")
                return {"success": True, "length": len(text), "attempts": attempt + 1}
            except Exception as e:
                log.warning(f"Type attempt {attempt + 1} failed: {e}")
                time.sleep(0.3)
        return {"success": False, "error": f"Type failed after {retries} attempts"}
    finally:
        safe_clipboard_copy(original_clipboard)

# ─────────────────────────────────────────────────────────────────────────────
# 3. SMART WAIT CONDITIONS
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def wait_for_text_on_screen(text: str, timeout: int = 30, region: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
    """Wait for text to appear on screen (smart wait, no fixed sleep).

    Args:
        text: Text to wait for.
        timeout: Max seconds to wait.
        region: Optional {"left", "top", "width", "height"} to limit OCR area.
    """
    if not HAS_TESSERACT or not HAS_PYAUTOGUI:
        return {"found": False, "error": "pyautogui or tesseract not available"}

    start = time.time()
    interval = 0.3
    while time.time() - start < timeout:
        try:
            if region:
                img = pyautogui.screenshot(region=(region["left"], region["top"], region["width"], region["height"]))
            else:
                img = pyautogui.screenshot()
            ocr_text = pytesseract.image_to_string(img)
            if text.lower() in ocr_text.lower():
                elapsed = time.time() - start
                return {"found": True, "elapsed_seconds": round(elapsed, 2)}
        except Exception:
            pass
        time.sleep(interval)
        interval = min(interval * 1.2, 2.0)

    return {"found": False, "timeout": timeout}

@server.tool()
def wait_for_image_on_screen(image_path: str, timeout: int = 30, confidence: float = 0.8) -> Dict[str, Any]:
    """Wait for an image to appear on screen (smart polling)."""
    if not HAS_PYAUTOGUI:
        return {"found": False, "error": "pyautogui not available"}

    start = time.time()
    interval = 0.3
    while time.time() - start < timeout:
        try:
            loc = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if loc:
                center = pyautogui.center(loc)
                return {"found": True, "x": center.x, "y": center.y, "elapsed_seconds": round(time.time() - start, 2)}
        except Exception:
            pass
        time.sleep(interval)
        interval = min(interval * 1.2, 2.0)

    return {"found": False, "timeout": timeout}

@server.tool()
def wait_for_pixel_color(x: int, y: int, r: int, g: int, b: int, tolerance: int = 20, timeout: int = 30) -> Dict[str, Any]:
    """Wait for a pixel to match a color."""
    if not HAS_PYAUTOGUI:
        return {"matched": False, "error": "pyautogui not available"}

    start = time.time()
    while time.time() - start < timeout:
        try:
            px = pyautogui.pixel(x, y)
            if all(abs(p - c) <= tolerance for p, c in zip(px, (r, g, b))):
                return {"matched": True, "elapsed_seconds": round(time.time() - start, 2)}
        except Exception:
            pass
        time.sleep(0.2)

    return {"matched": False, "timeout": timeout}

@server.tool()
def wait_for_window(title: str, timeout: int = 30) -> Dict[str, Any]:
    """Wait for a window to appear."""
    start = time.time()
    while time.time() - start < timeout:
        w = _find_window(title)
        if w:
            return {"found": True, "title": w.title, "elapsed_seconds": round(time.time() - start, 2)}
        time.sleep(0.3)

    return {"found": False, "timeout": timeout}

@server.tool()
def wait_for_process(name: str, timeout: int = 30) -> Dict[str, Any]:
    """Wait for a process to start."""
    if not HAS_PSUTIL:
        return {"found": False, "error": "psutil not available"}

    start = time.time()
    while time.time() - start < timeout:
        for proc in psutil.process_iter(["name"]):
            try:
                if name.lower() in proc.info["name"].lower():
                    return {"found": True, "pid": proc.pid, "elapsed_seconds": round(time.time() - start, 2)}
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        time.sleep(0.3)

    return {"found": False, "timeout": timeout}

@server.tool()
def wait_for_screen_change(x: int, y: int, width: int, height: int, timeout: int = 10, threshold: int = 5) -> Dict[str, Any]:
    """Wait for a screen region to change (smart polling)."""
    if not HAS_PYAUTOGUI or not HAS_PIL:
        return {"changed": False, "error": "pyautogui or PIL not available"}

    initial_img = pyautogui.screenshot(region=(x, y, width, height))
    initial_arr = np.array(initial_img)

    start_time = time.time()
    interval = 0.1
    while time.time() - start_time < timeout:
        current_img = pyautogui.screenshot(region=(x, y, width, height))
        current_arr = np.array(current_img)
        diff = np.abs(initial_arr - current_arr).mean()
        if diff > threshold:
            return {"changed": True, "diff": float(diff), "elapsed_seconds": round(time.time() - start_time, 2)}
        time.sleep(interval)
        interval = min(interval * 1.1, 1.0)

    return {"changed": False, "timeout": timeout}

# ─────────────────────────────────────────────────────────────────────────────
# 4. MULTI-MONITOR AWARENESS
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def list_monitors() -> List[Dict[str, Any]]:
    """List all connected monitors with their bounds."""
    if not HAS_MSS:
        return [{"error": "mss not available"}]

    monitors = []
    with mss.mss() as sct:
        for i, m in enumerate(sct.monitors):
            if i == 0:
                continue
            monitors.append({
                "id": i,
                "left": m["left"],
                "top": m["top"],
                "width": m["width"],
                "height": m["height"],
                "right": m["left"] + m["width"],
                "bottom": m["top"] + m["height"],
            })
    return monitors

@server.tool()
def take_screenshot_monitor(monitor_id: int = 1, save_to: Optional[str] = None) -> str:
    """Capture a specific monitor.

    Args:
        monitor_id: Monitor index (1-based, use list_monitors to see IDs).
        save_to: Optional path to save screenshot.
    """
    if not HAS_MSS:
        return "mss not available"

    with mss.mss() as sct:
        monitors = sct.monitors
        if monitor_id < 1 or monitor_id >= len(monitors):
            return f"Invalid monitor_id {monitor_id}. Available: 1-{len(monitors)-1}"

        screenshot = sct.grab(monitors[monitor_id])

        if save_to:
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_to)
            return f"Monitor {monitor_id} screenshot saved to {save_to}"

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(TEMP_DIR, f"monitor{monitor_id}_{ts}.png")
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
        return f"Monitor {monitor_id} screenshot saved to {path}"

@server.tool()
def take_screenshot_all_monitors(save_dir: Optional[str] = None) -> List[str]:
    """Capture all monitors individually."""
    if not HAS_MSS:
        return ["mss not available"]

    save_dir = save_dir or TEMP_DIR
    os.makedirs(save_dir, exist_ok=True)
    paths = []

    with mss.mss() as sct:
        for i, m in enumerate(sct.monitors):
            if i == 0:
                continue
            screenshot = sct.grab(m)
            path = os.path.join(save_dir, f"monitor_{i}.png")
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
            paths.append(path)

    return paths

@server.tool()
def get_mouse_monitor() -> Dict[str, Any]:
    """Get which monitor the mouse is currently on."""
    if not HAS_PYAUTOGUI or not HAS_MSS:
        return {"error": "pyautogui or mss not available"}

    mx, my = pyautogui.position()
    with mss.mss() as sct:
        for i, m in enumerate(sct.monitors):
            if i == 0:
                continue
            if (m["left"] <= mx < m["left"] + m["width"] and
                m["top"] <= my < m["top"] + m["height"]):
                return {
                    "monitor_id": i,
                    "mouse_x": mx,
                    "mouse_y": my,
                    "monitor_bounds": {
                        "left": m["left"], "top": m["top"],
                        "width": m["width"], "height": m["height"],
                    },
                    "local_x": mx - m["left"],
                    "local_y": my - m["top"],
                }
    return {"error": "Mouse not found on any monitor"}

# ─────────────────────────────────────────────────────────────────────────────
# 5. ACTION BATCHING
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class BatchResult:
    action: str
    success: bool
    result: Any
    elapsed_ms: float

@server.tool()
def batch_actions(actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Execute multiple actions in sequence (reduces MCP roundtrips).

    Each action: {"type": "click"|"type"|"hotkey"|"wait"|"screenshot"|"scroll", ...}

    Supported types:
      - {"type": "click", "x": int, "y": int, "button": "left"}
      - {"type": "double_click", "x": int, "y": int}
      - {"type": "right_click", "x": int, "y": int}
      - {"type": "type", "text": str}
      - {"type": "hotkey", "keys": "ctrl+c"}
      - {"type": "press", "key": "enter"}
      - {"type": "wait", "seconds": float}
      - {"type": "scroll", "amount": int}
      - {"type": "move", "x": int, "y": int}
      - {"type": "screenshot", "save_to": str}
    """
    if not HAS_PYAUTOGUI:
        return [{"error": "pyautogui not available"}]

    results = []
    for i, action in enumerate(actions):
        t0 = time.time()
        action_type = action.get("type", "")
        try:
            if action_type == "click":
                pyautogui.click(action["x"], action["y"], button=action.get("button", "left"))
                result = {"clicked": (action["x"], action["y"])}
            elif action_type == "double_click":
                pyautogui.doubleClick(action["x"], action["y"])
                result = {"double_clicked": (action["x"], action["y"])}
            elif action_type == "right_click":
                pyautogui.rightClick(action["x"], action["y"])
                result = {"right_clicked": (action["x"], action["y"])}
            elif action_type == "type":
                safe_clipboard_copy(action["text"])
                pyautogui.hotkey("ctrl", "v")
                result = {"typed": len(action["text"])}
            elif action_type == "hotkey":
                parts = [k.strip() for k in action["keys"].split("+")]
                pyautogui.hotkey(*parts)
                result = {"hotkey": action["keys"]}
            elif action_type == "press":
                pyautogui.press(action["key"])
                result = {"pressed": action["key"]}
            elif action_type == "wait":
                time.sleep(action["seconds"])
                result = {"waited": action["seconds"]}
            elif action_type == "scroll":
                pyautogui.scroll(action["amount"])
                result = {"scrolled": action["amount"]}
            elif action_type == "move":
                pyautogui.moveTo(action["x"], action["y"])
                result = {"moved": (action["x"], action["y"])}
            elif action_type == "screenshot":
                path = action.get("save_to", os.path.join(TEMP_DIR, f"batch_{i}.png"))
                pyautogui.screenshot(path)
                result = {"screenshot": path}
            else:
                result = {"error": f"Unknown action type: {action_type}"}

            elapsed = (time.time() - t0) * 1000
            results.append({
                "index": i,
                "type": action_type,
                "success": "error" not in result,
                "result": result,
                "elapsed_ms": round(elapsed, 1),
            })
        except Exception as e:
            elapsed = (time.time() - t0) * 1000
            results.append({
                "index": i,
                "type": action_type,
                "success": False,
                "result": {"error": str(e)},
                "elapsed_ms": round(elapsed, 1),
            })

    return results

@server.tool()
def batch_clicks(positions: List[Dict[str, int]], delay_ms: int = 50) -> List[Dict[str, Any]]:
    """Click multiple positions in rapid succession.

    Args:
        positions: List of {"x": int, "y": int}.
        delay_ms: Delay between clicks in milliseconds.
    """
    if not HAS_PYAUTOGUI:
        return [{"error": "pyautogui not available"}]

    results = []
    for i, pos in enumerate(positions):
        try:
            pyautogui.click(pos["x"], pos["y"])
            results.append({"index": i, "success": True, "x": pos["x"], "y": pos["y"]})
            if delay_ms > 0 and i < len(positions) - 1:
                time.sleep(delay_ms / 1000)
        except Exception as e:
            results.append({"index": i, "success": False, "error": str(e)})
    return results

# ─────────────────────────────────────────────────────────────────────────────
# 6. VOICE / NOTIFICATION FEEDBACK
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def speak(text: str, rate: int = 0, volume: int = 100) -> str:
    """Text-to-speech feedback using Windows SAPI.

    Args:
        text: Text to speak.
        rate: Speech rate (-10 to 10, default 0).
        volume: Volume (0-100, default 100).
    """
    try:
        # Use PowerShell SAPI
        escaped = text.replace("'", "''")
        ps_cmd = f'''
        $voice = New-Object -ComObject SAPI.SPVoice
        $voice.Rate = {rate}
        $voice.Volume = {volume}
        $voice.Speak('{escaped}')
        '''
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, timeout=15)
        return f"Spoken: {text[:100]}"
    except Exception as e:
        return f"TTS error: {e}"

@server.tool()
def toast_notification(title: str, message: str, duration: int = 5, sound: bool = True) -> str:
    """Show a Windows toast notification (Windows 10/11).

    Args:
        title: Notification title.
        message: Notification body.
        duration: How long to show (seconds).
        sound: Play notification sound.
    """
    try:
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null

        $template = @"
        <toast duration="long">
            <visual>
                <binding template="ToastGeneric">
                    <text>{title}</text>
                    <text>{message}</text>
                </binding>
            </visual>
            {"<audio src='ms-winsoundevent:Notification.Default'/>" if sound else "<audio silent='true'/>"}
        </toast>
"@

        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("PC Control").Show($toast)
        '''
        subprocess.run(["powershell", "-Command", ps_script], capture_output=True, timeout=10)
        return f"Toast shown: {title}"
    except Exception as e:
        return f"Toast error: {e}"

@server.tool()
def beep_notification(frequency: int = 800, duration_ms: int = 200) -> str:
    """Play a beep sound."""
    try:
        import winsound
        winsound.Beep(frequency, duration_ms)
        return f"Beep: {frequency}Hz for {duration_ms}ms"
    except ImportError:
        return "winsound not available (Windows only)"

# ─────────────────────────────────────────────────────────────────────────────
# 7. VISUAL DEBUG MODE
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def debug_toggle(enabled: bool) -> str:
    """Enable or disable visual debug mode (before/after screenshots)."""
    debug.enabled = enabled
    return f"Debug mode {'enabled' if enabled else 'disabled'}"

@server.tool()
def debug_get_last_screenshots() -> Dict[str, Optional[str]]:
    """Get the last before/after debug screenshots."""
    return debug.get_last_pair()

@server.tool()
def debug_cleanup(max_age_hours: int = 24) -> Dict[str, Any]:
    """Clean up old debug screenshots."""
    cutoff = time.time() - (max_age_hours * 3600)
    removed = 0
    for f in os.listdir(DEBUG_DIR):
        path = os.path.join(DEBUG_DIR, f)
        if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
            os.remove(path)
            removed += 1
    return {"removed": removed, "directory": DEBUG_DIR}

# ─────────────────────────────────────────────────────────────────────────────
# SCREENSHOT & CAPTURE TOOLS
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def take_screenshot(save_to: Optional[str] = None) -> Dict[str, Any]:
    """Take full screenshot with debug tracking."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}

    debug.capture_before("screenshot")
    img = pyautogui.screenshot()
    if save_to:
        img.save(save_to)
        debug.capture_after("screenshot")
        return {"path": save_to, "size": list(img.size)}

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(TEMP_DIR, f"screenshot_{ts}.png")
    img.save(path)
    debug.capture_after("screenshot")
    return {"path": path, "size": list(img.size)}

@server.tool()
def take_region_screenshot(left: int, top: int, width: int, height: int, save_to: Optional[str] = None) -> Dict[str, Any]:
    """Capture specific region."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}

    img = pyautogui.screenshot(region=(left, top, width, height))
    if save_to:
        img.save(save_to)
        return {"path": save_to, "size": [width, height]}

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(TEMP_DIR, f"region_{ts}.png")
    img.save(path)
    return {"path": path, "size": [width, height]}

@server.tool()
def screenshot_with_ocr(save_to: Optional[str] = None) -> Dict[str, Any]:
    """Take screenshot and extract text via OCR."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}
    if not HAS_TESSERACT:
        return {"error": "Tesseract OCR not installed"}

    img = pyautogui.screenshot()
    if save_to:
        img.save(save_to)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_to = os.path.join(TEMP_DIR, f"screenshot_ocr_{ts}.png")
        img.save(save_to)

    text = pytesseract.image_to_string(img)
    return {"screenshot_path": save_to, "text": text.strip(), "text_length": len(text.strip())}

@server.tool()
def compare_screenshots(img1_path: str, img2_path: str) -> Dict[str, Any]:
    """Compare two screenshots and return difference score."""
    if not HAS_PIL:
        return {"error": "PIL not available"}

    try:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        if img1.size != img2.size:
            return {"error": "Screenshots have different dimensions"}

        arr1 = np.array(img1)
        arr2 = np.array(img2)
        diff = np.abs(arr1 - arr2).mean()
        return {
            "difference_score": float(diff),
            "are_identical": diff < 1.0,
            "similarity_percent": round(max(0, 100 - diff), 2),
        }
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def record_screen(duration: int, fps: int = 10, save_to: Optional[str] = None) -> Dict[str, Any]:
    """Record screen for specified duration."""
    if not HAS_MSS:
        return {"error": "mss not available"}
    try:
        import cv2
    except ImportError:
        return {"error": "opencv-python not installed"}

    if save_to is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_to = os.path.join(TEMP_DIR, f"recording_{ts}.mp4")

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(save_to, fourcc, fps, (monitor["width"], monitor["height"]))

        start_time = time.time()
        frames = 0
        while time.time() - start_time < duration:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            out.write(cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR))
            frames += 1
            time.sleep(1 / fps)

        out.release()
        return {"path": save_to, "frames": frames, "duration": duration}

# ─────────────────────────────────────────────────────────────────────────────
# MOUSE AUTOMATION
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def move_mouse(x: int, y: int, duration: float = 0.0, tween: str = "linear") -> str:
    """Move mouse with optional easing."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"

    tween_map = {
        "linear": pyautogui.linear,
        "ease_in": pyautogui.easeInQuad,
        "ease_out": pyautogui.easeOutQuad,
        "ease_in_out": pyautogui.easeInOutQuad,
    }
    pyautogui.moveTo(x, y, duration=duration, tween=tween_map.get(tween, pyautogui.linear))
    return f"Moved to ({x}, {y})"

@server.tool()
def move_mouse_relative(dx: int, dy: int, duration: float = 0.5) -> str:
    """Move mouse relative to current position."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    pyautogui.moveRel(dx, dy, duration=duration)
    return f"Moved by ({dx}, {dy})"

@server.tool()
def click(x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
    """Click at position with self-healing retry."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}

    cx, cy = coord(x, y)
    if x is not None:
        return self_heal_click(cx, cy, retries=3, button=button)
    else:
        return self_heal_click(cx, cy, retries=3, button=button)

@server.tool()
def double_click(x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
    """Double click at position."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}
    cx, cy = coord(x, y)
    debug.capture_before("dblclick")
    pyautogui.doubleClick(cx, cy)
    debug.capture_after("dblclick")
    return {"success": True, "x": cx, "y": cy}

@server.tool()
def right_click(x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
    """Right click at position."""
    return click(x, y, button="right")

@server.tool()
def drag(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5, button: str = "left") -> str:
    """Drag from one position to another."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    pyautogui.moveTo(from_x, from_y)
    pyautogui.drag(to_x - from_x, to_y - from_y, duration=duration, button=button)
    return f"Dragged from ({from_x}, {from_y}) to ({to_x}, {to_y})"

@server.tool()
def scroll(amount: int, x: Optional[int] = None, y: Optional[int] = None) -> str:
    """Scroll up or down."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    pyautogui.scroll(amount, x, y)
    return f"Scrolled {amount}"

@server.tool()
def smooth_move(x: int, y: int, steps: int = 10) -> str:
    """Smooth mouse movement with interpolation."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    start_x, start_y = pyautogui.position()
    for i in range(steps + 1):
        t = i / steps
        current_x = int(start_x + (x - start_x) * t)
        current_y = int(start_y + (y - start_y) * t)
        pyautogui.moveTo(current_x, current_y)
        time.sleep(0.01)
    return f"Smooth move to ({x}, {y}) completed"

@server.tool()
def mouse_position() -> Dict[str, int]:
    """Get current mouse position."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}
    x, y = pyautogui.position()
    return {"x": x, "y": y}

@server.tool()
def screen_size() -> Dict[str, int]:
    """Get screen size."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}
    w, h = pyautogui.size()
    return {"width": w, "height": h}

# ─────────────────────────────────────────────────────────────────────────────
# KEYBOARD AUTOMATION
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def type_text(text: str, interval: float = 0.0) -> Dict[str, Any]:
    """Type text with self-healing clipboard fallback."""
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}
    return self_heal_type(text)

@server.tool()
def type_unicode(text: str) -> Dict[str, Any]:
    """Type unicode text using clipboard."""
    if not HAS_CLIPBOARD or not HAS_PYAUTOGUI:
        return {"error": "Clipboard or pyautogui not available"}

    original_clipboard = safe_clipboard_paste()
    try:
        safe_clipboard_copy(text)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        return {"success": True, "length": len(text)}
    finally:
        safe_clipboard_copy(original_clipboard)

@server.tool()
def press_key(key: str) -> str:
    """Press single key."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    pyautogui.press(key)
    return f"Pressed {key}"

@server.tool()
def hotkey(keys: str) -> str:
    """Press key combination (e.g., 'ctrl+c', 'alt+tab')."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    parts = [k.strip() for k in keys.split("+")]
    pyautogui.hotkey(*parts)
    return f"Hotkey: {keys}"

@server.tool()
def key_down(key: str) -> str:
    """Press and hold key."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    pyautogui.keyDown(key)
    return f"Key down: {key}"

@server.tool()
def key_up(key: str) -> str:
    """Release key."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not available"
    pyautogui.keyUp(key)
    return f"Key up: {key}"

@server.tool()
def type_password(password: str) -> Dict[str, Any]:
    """Type password securely using clipboard (auto-clears)."""
    if not HAS_CLIPBOARD or not HAS_PYAUTOGUI:
        return {"error": "Clipboard or pyautogui not available"}

    original_clipboard = safe_clipboard_paste()
    try:
        safe_clipboard_copy(password)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        return {"success": True, "length": len(password)}
    finally:
        safe_clipboard_copy("")
        time.sleep(0.05)
        safe_clipboard_copy(original_clipboard)

# ─────────────────────────────────────────────────────────────────────────────
# WINDOW MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def list_windows() -> List[Dict[str, Any]]:
    """List all visible windows."""
    if not HAS_PYWIN:
        return [{"error": "pygetwindow not available"}]

    windows = []
    for w in gw.getAllWindows():
        if w.title.strip():
            windows.append({
                "title": w.title,
                "left": w.left,
                "top": w.top,
                "width": w.width,
                "height": w.height,
                "visible": w.visible,
                "active": w.isActive,
                "maximized": w.isMaximized,
                "minimized": w.isMinimized,
            })
    return windows[:50]

@server.tool()
def activate_window(title: str) -> Dict[str, Any]:
    """Activate window by title."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    try:
        w.activate()
        return {"success": True, "title": w.title}
    except Exception as e:
        return {"success": False, "error": str(e)}

@server.tool()
def close_window(title: str) -> Dict[str, Any]:
    """Close window by title."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    w.close()
    return {"success": True, "title": w.title}

@server.tool()
def minimize_window(title: str) -> Dict[str, Any]:
    """Minimize window."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    w.minimize()
    return {"success": True, "title": w.title}

@server.tool()
def maximize_window(title: str) -> Dict[str, Any]:
    """Maximize window."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    w.maximize()
    return {"success": True, "title": w.title}

@server.tool()
def restore_window(title: str) -> Dict[str, Any]:
    """Restore window."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    w.restore()
    return {"success": True, "title": w.title}

@server.tool()
def resize_window(title: str, width: int, height: int) -> Dict[str, Any]:
    """Resize window."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    w.resizeTo(width, height)
    return {"success": True, "title": w.title, "width": width, "height": height}

@server.tool()
def move_window(title: str, x: int, y: int) -> Dict[str, Any]:
    """Move window."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    w.moveTo(x, y)
    return {"success": True, "title": w.title, "x": x, "y": y}

@server.tool()
def window_info(title: str) -> Dict[str, Any]:
    """Get window information."""
    w = _find_window(title)
    if not w:
        return {"error": f"No window matching '{title}'"}
    return {
        "title": w.title,
        "left": w.left, "top": w.top,
        "width": w.width, "height": w.height,
        "visible": w.visible, "active": w.isActive,
        "maximized": w.isMaximized, "minimized": w.isMinimized,
    }

@server.tool()
def tile_windows_side_by_side(title1: str, title2: str) -> Dict[str, Any]:
    """Tile two windows side by side."""
    w1, w2 = _find_window(title1), _find_window(title2)
    if not w1 or not w2:
        return {"success": False, "error": "Could not find both windows"}

    screen_w, screen_h = pyautogui.size() if HAS_PYAUTOGUI else (1920, 1080)
    half_w = screen_w // 2

    w1.resizeTo(half_w, screen_h)
    w1.moveTo(0, 0)
    w2.resizeTo(half_w, screen_h)
    w2.moveTo(half_w, 0)
    return {"success": True, "windows": [w1.title, w2.title]}

@server.tool()
def set_always_on_top(title: str) -> Dict[str, Any]:
    """Set window always on top."""
    w = _find_window(title)
    if not w:
        return {"success": False, "error": f"No window matching '{title}'"}
    hwnd = w._hWnd
    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    return {"success": True, "title": w.title}

# ─────────────────────────────────────────────────────────────────────────────
# OCR TOOLS
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def ocr_screen() -> Dict[str, Any]:
    """OCR the full screen."""
    if not HAS_TESSERACT or not HAS_PYAUTOGUI:
        return {"error": "pyautogui or tesseract not available"}
    img = pyautogui.screenshot()
    text = pytesseract.image_to_string(img)
    return {"text": text.strip(), "length": len(text.strip())}

@server.tool()
def ocr_region(left: int, top: int, width: int, height: int) -> Dict[str, Any]:
    """OCR specific region."""
    if not HAS_TESSERACT or not HAS_PYAUTOGUI:
        return {"error": "pyautogui or tesseract not available"}
    img = pyautogui.screenshot(region=(left, top, width, height))
    text = pytesseract.image_to_string(img)
    return {"text": text.strip(), "length": len(text.strip())}

@server.tool()
def find_text_on_screen(text: str) -> List[Dict[str, Any]]:
    """Find text on screen using OCR with positions."""
    if not HAS_TESSERACT or not HAS_PYAUTOGUI:
        return [{"error": "pyautogui or tesseract not available"}]

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
                "confidence": data["conf"][i],
            })
    return results

# ─────────────────────────────────────────────────────────────────────────────
# CLIPBOARD
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def clipboard_get() -> Dict[str, Any]:
    """Get clipboard content."""
    if not HAS_CLIPBOARD:
        return {"error": "Clipboard module not available"}
    text = pyperclip.paste()
    return {"text": text, "length": len(text)}

@server.tool()
def clipboard_set(text: str) -> Dict[str, Any]:
    """Set clipboard content."""
    if not HAS_CLIPBOARD:
        return {"error": "Clipboard module not available"}
    pyperclip.copy(text)
    return {"success": True, "length": len(text)}

@server.tool()
def clipboard_clear() -> str:
    """Clear clipboard."""
    if not HAS_CLIPBOARD:
        return "Clipboard module not available"
    pyperclip.copy("")
    return "Clipboard cleared"

# ─────────────────────────────────────────────────────────────────────────────
# PROCESS MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
if HAS_PSUTIL:
    @server.tool()
    def list_processes(filter_str: Optional[str] = None, max_results: int = 30) -> List[Dict[str, Any]]:
        """List running processes."""
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
    def kill_process(name: str) -> Dict[str, Any]:
        """Kill process by name."""
        killed = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if name.lower() in proc.info["name"].lower():
                    proc.kill()
                    killed.append(proc.info["name"])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return {"killed": killed, "count": len(killed)}

    @server.tool()
    def process_info(name: str) -> Dict[str, Any]:
        """Get detailed process information."""
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "create_time"]):
            try:
                if name.lower() in proc.info["name"].lower():
                    return proc.info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return {"error": f"Process '{name}' not found"}

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM INFORMATION
# ─────────────────────────────────────────────────────────────────────────────
if HAS_PSUTIL:
    @server.tool()
    def system_info() -> Dict[str, Any]:
        """Get comprehensive system information."""
        cached = perf_cache.get("system_info", 30)
        if cached:
            return cached

        info = {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": dict(psutil.cpu_freq()._asdict()) if psutil.cpu_freq() else None,
            "memory": dict(psutil.virtual_memory()._asdict()),
            "swap": dict(psutil.swap_memory()._asdict()),
            "disk": {p.mountpoint: dict(p._asdict()) for p in psutil.disk_partitions() if p.fstype},
            "boot_time": psutil.boot_time(),
            "platform": platform.platform(),
            "hostname": platform.node(),
            "username": os.environ.get("USERNAME", ""),
            "python_version": platform.python_version(),
        }
        perf_cache.set("system_info", info)
        return info

    @server.tool()
    def get_cpu_usage() -> Dict[str, Any]:
        return {"percent": psutil.cpu_percent(interval=0.5), "count": psutil.cpu_count()}

    @server.tool()
    def get_memory_usage() -> Dict[str, Any]:
        mem = psutil.virtual_memory()
        return {"total": mem.total, "available": mem.available, "percent": mem.percent, "used": mem.used, "free": mem.free}

    @server.tool()
    def get_disk_usage(drive: str = "C:\\") -> Dict[str, Any]:
        try:
            usage = psutil.disk_usage(drive)
            return {"total": usage.total, "used": usage.used, "free": usage.free, "percent": usage.percent}
        except Exception as e:
            return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# FILE OPERATIONS
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def read_file(path: str) -> Dict[str, Any]:
    """Read file content."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        truncated = len(content) > 5000
        return {"content": content[:5000] + "..." if truncated else content, "length": len(content), "truncated": truncated}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def write_file(path: str, content: str) -> Dict[str, Any]:
    """Write to file."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "length": len(content), "path": path}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def copy_file(src: str, dst: str) -> Dict[str, Any]:
    try:
        shutil.copy(src, dst)
        return {"success": True, "src": src, "dst": dst}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def move_file(src: str, dst: str) -> Dict[str, Any]:
    try:
        shutil.move(src, dst)
        return {"success": True, "src": src, "dst": dst}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def delete_file(path: str) -> Dict[str, Any]:
    try:
        if os.path.exists(path):
            os.remove(path)
            return {"success": True, "path": path}
        return {"error": f"File not found: {path}"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def make_directory(path: str) -> Dict[str, Any]:
    try:
        os.makedirs(path, exist_ok=True)
        return {"success": True, "path": path}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def find_files(pattern: str, recursive: bool = True) -> List[str]:
    """Find files matching glob pattern."""
    return glob.glob(pattern, recursive=recursive)

@server.tool()
def file_exists(path: str) -> bool:
    return os.path.exists(path)

@server.tool()
def get_file_info(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"error": f"File not found: {path}"}
    stat = os.stat(path)
    return {
        "name": os.path.basename(path),
        "path": path,
        "size": stat.st_size,
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path),
    }

@server.tool()
def get_directory_size(path: str) -> int:
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            total += os.path.getsize(os.path.join(dirpath, f))
    return total

# ─────────────────────────────────────────────────────────────────────────────
# COMMAND EXECUTION
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def run_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """Run command prompt command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"stdout": result.stdout[-3000:], "stderr": result.stderr[-1000:], "return_code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def run_powershell(script: str, timeout: int = 30) -> Dict[str, Any]:
    """Run PowerShell command."""
    try:
        result = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True, timeout=timeout)
        return {"stdout": result.stdout[-5000:], "stderr": result.stderr[-1000:], "return_code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": f"Script timed out after {timeout}s"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def open_file(path: str) -> str:
    try:
        os.startfile(path)
        return f"Opened: {path}"
    except Exception as e:
        return f"Error: {e}"

@server.tool()
def open_url(url: str) -> str:
    import webbrowser
    webbrowser.open(url)
    return f"Opened URL: {url}"

# ─────────────────────────────────────────────────────────────────────────────
# NETWORK
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def ping(host: str = "google.com") -> Dict[str, Any]:
    return run_command(f"ping -n 4 {host}")

@server.tool()
def get_ip() -> str:
    import socket
    return socket.gethostbyname(socket.gethostname())

@server.tool()
def is_connected() -> bool:
    import socket
    try:
        socket.create_connection(("google.com", 80))
        return True
    except Exception:
        return False

@server.tool()
def get_public_ip() -> str:
    try:
        import requests
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        return "Could not get public IP"

# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
if HAS_REGISTRY:
    @server.tool()
    def read_registry(hive: str, path: str, name: str) -> Any:
        try:
            hive_map = {
                "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
                "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
                "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
                "HKEY_USERS": winreg.HKEY_USERS,
                "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
            }
            key = winreg.OpenKey(hive_map.get(hive, winreg.HKEY_CURRENT_USER), path)
            val, _ = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return val
        except Exception as e:
            return f"Error: {e}"

    @server.tool()
    def write_registry(hive: str, path: str, name: str, value: str) -> str:
        try:
            hive_map = {
                "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
                "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
                "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
                "HKEY_USERS": winreg.HKEY_USERS,
                "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
            }
            h = hive_map.get(hive, winreg.HKEY_CURRENT_USER)
            try:
                key = winreg.OpenKey(h, path, 0, winreg.KEY_SET_VALUE)
            except Exception:
                key = winreg.CreateKey(h, path)
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)
            return f"Set {name} = {value}"
        except Exception as e:
            return f"Error: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# SERVICES
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def list_services() -> List[Dict[str, Any]]:
    result = run_powershell("Get-Service | Select-Object Name, Status, DisplayName | ConvertTo-Json")
    try:
        return json.loads(result.get("stdout", "[]"))
    except Exception:
        return []

@server.tool()
def service_status(name: str) -> str:
    result = run_powershell(f'Get-Service -Name "{name}" | Select-Object -ExpandProperty Status')
    return result.get("stdout", "Unknown")

@server.tool()
def start_service(name: str) -> str:
    result = run_powershell(f'Start-Service -Name "{name}"')
    return f"Started: {name}" if result.get("return_code") == 0 else f"Failed: {result.get('stderr')}"

@server.tool()
def stop_service(name: str) -> str:
    result = run_powershell(f'Stop-Service -Name "{name}"')
    return f"Stopped: {name}" if result.get("return_code") == 0 else f"Failed: {result.get('stderr')}"

# ─────────────────────────────────────────────────────────────────────────────
# SCHEDULED TASKS
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def list_scheduled_tasks() -> List[Dict[str, Any]]:
    result = run_powershell("Get-ScheduledTask | Select-Object TaskName, State | ConvertTo-Json")
    try:
        return json.loads(result.get("stdout", "[]"))
    except Exception:
        return []

# ─────────────────────────────────────────────────────────────────────────────
# WIFI
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def get_wifi_networks() -> List[str]:
    result = run_powershell("netsh wlan show networks mode=bssid")
    networks = []
    for line in result.get("stdout", "").split("\n"):
        if "SSID" in line and "BSSID" not in line:
            networks.append(line.split(":")[-1].strip())
    return networks

@server.tool()
def connect_wifi(ssid: str, password: Optional[str] = None) -> str:
    cmd = f'netsh wlan connect name="{ssid}"'
    result = run_powershell(cmd)
    return f"Connected to {ssid}" if result.get("return_code") == 0 else f"Failed: {result.get('stderr')}"

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM CONTROL
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def lock_screen() -> str:
    if HAS_CTYPES:
        ctypes.windll.user32.LockWorkStation()
        return "Screen locked"
    return "Cannot lock screen"

@server.tool()
def set_wallpaper(path: str) -> str:
    if HAS_CTYPES:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        return f"Wallpaper set to {path}"
    return "Cannot set wallpaper"

@server.tool()
def show_notification(title: str, message: str, duration: int = 3) -> str:
    """Show Windows notification (legacy messagebox)."""
    try:
        import threading
        from tkinter import Tk, messagebox

        def show():
            root = Tk()
            root.withdraw()
            root.after(duration * 1000, root.destroy)
            messagebox.showinfo(title, message)
            root.mainloop()

        threading.Thread(target=show, daemon=True).start()
        return f"Notification shown: {title}"
    except Exception as e:
        return f"Error: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE RECOGNITION
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def find_image_on_screen(image_path: str, confidence: float = 0.8) -> Optional[Dict[str, int]]:
    if not HAS_PYAUTOGUI:
        return None
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            return {"x": center.x, "y": center.y}
    except Exception as e:
        log.error(f"Image recognition failed: {e}")
    return None

@server.tool()
def click_image_on_screen(image_path: str, confidence: float = 0.8, button: str = "left") -> Dict[str, Any]:
    pos = find_image_on_screen(image_path, confidence)
    if pos:
        return self_heal_click(pos["x"], pos["y"], button=button)
    return {"success": False, "error": "Image not found on screen"}

# ─────────────────────────────────────────────────────────────────────────────
# PIXEL COLOR
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def get_pixel(x: int, y: int) -> Dict[str, int]:
    if not HAS_PYAUTOGUI:
        return {"error": "pyautogui not available"}
    px = pyautogui.pixel(x, y)
    return {"r": px[0], "g": px[1], "b": px[2]}

@server.tool()
def pixel_matches_color(x: int, y: int, r: int, g: int, b: int, tolerance: int = 10) -> bool:
    if not HAS_PYAUTOGUI:
        return False
    return pyautogui.pixelMatchesColor(x, y, (r, g, b), tolerance=tolerance)

# ─────────────────────────────────────────────────────────────────────────────
# MACRO RECORDING
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def record_macro(duration: int, save_to: str) -> Dict[str, Any]:
    """Record mouse and keyboard actions."""
    try:
        import pynput.mouse as pmouse
        import pynput.keyboard as pkeyboard
    except ImportError:
        return {"error": "pynput not installed"}

    actions = []

    def on_move(x, y):
        actions.append(("move", x, y, time.time()))

    def on_click(x, y, button, pressed):
        actions.append(("click", x, y, str(button), pressed, time.time()))

    def on_press(key):
        actions.append(("press", str(key), time.time()))

    mouse_listener = pmouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = pkeyboard.Listener(on_press=on_press)

    mouse_listener.start()
    keyboard_listener.start()
    time.sleep(duration)
    mouse_listener.stop()
    keyboard_listener.stop()

    with open(save_to, "w") as f:
        json.dump(actions, f)

    return {"path": save_to, "actions_count": len(actions), "duration": duration}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Win32 API Native Tools
# ═══════════════════════════════════════════════════════════════════════════════
import struct, mmap, ctypes.util

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
gdi32 = ctypes.windll.gdi32
shell32 = ctypes.windll.shell32
ntdll = ctypes.windll.ntdll

# Define missing ctypes structures
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.wintypes.DWORD),
        ("dwMemoryLoad", ctypes.wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ("ACLineStatus", ctypes.c_byte),
        ("BatteryFlag", ctypes.c_byte),
        ("BatteryLifePercent", ctypes.c_byte),
        ("Reserved1", ctypes.c_byte),
        ("BatteryLifeTime", ctypes.wintypes.DWORD),
        ("BatteryFullLifeTime", ctypes.wintypes.DWORD),
    ]

@server.tool()
def get_process_architecture(pid: int = 0) -> Dict[str, Any]:
    """Get process architecture (32-bit/64-bit) and bitness."""
    if pid == 0:
        pid = kernel32.GetCurrentProcessId()
    try:
        hproc = kernel32.OpenProcess(0x1000, False, pid)
        if not hproc:
            return {"error": "cannot_open_process"}
        is_wow64 = ctypes.c_bool(False)
        try:
            kernel32.IsWow64Process(hproc, ctypes.byref(is_wow64))
        except Exception:
            pass
        kernel32.CloseHandle(hproc)
        is_64bit = platform.machine().endswith('64')
        arch = "WoW64 (32-bit on 64-bit)" if is_wow64.value else ("x64" if is_64bit else "x86")
        return {"pid": pid, "architecture": arch, "is_wow64": is_wow64.value, "python_bits": struct.calcsize("P") * 8}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_clipboard_history_enabled() -> Dict[str, Any]:
    """Check if Windows clipboard history is enabled."""
    try:
        key = r"Software\Microsoft\Clipboard"
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
            val, _ = winreg.QueryValueEx(k, "EnableClipboardHistory")
            return {"enabled": bool(val), "registry_value": val}
    except FileNotFoundError:
        return {"enabled": False, "note": "Registry key not found"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_window_transparency(title: str) -> Dict[str, Any]:
    """Get window transparency/opacity level."""
    try:
        import win32gui
        hwnd = win32gui.FindWindow(None, title)
        if not hwnd:
            hwnd = _fuzzy_find_hwnd(title)
        if not hwnd:
            return {"error": "window_not_found"}
        try:
            import win32api, win32con
            ex_style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        except Exception:
            ex_style = 0
        return {"title": title, "hwnd": hwnd, "extended_style": hex(ex_style),
                "layered": bool(ex_style & 0x80000), "transparent": bool(ex_style & 0x20)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def set_window_transparency(title: str, opacity: int = 255) -> Dict[str, Any]:
    """Set window transparency (0=transparent, 255=opaque). Uses WS_EX_LAYERED + SetLayeredWindowAttributes."""
    try:
        import win32gui, win32con, win32api
        hwnd = win32gui.FindWindow(None, title)
        if not hwnd:
            hwnd = _fuzzy_find_hwnd(title)
        if not hwnd:
            return {"error": "window_not_found"}
        ex_style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if not (ex_style & 0x80000):
            win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | 0x80000)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, max(0, min(255, opacity)), 0x2)
        return {"title": title, "opacity": opacity, "success": True}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def set_dpi_awareness(mode: str = "per_monitor") -> Dict[str, Any]:
    """Set DPI awareness for this process. Modes: system, per_monitor, per_monitor_v2."""
    try:
        modes = {"system": 1, "per_monitor": 2, "per_monitor_v2": 3}
        m = modes.get(mode, 2)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(m)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass
        return {"mode": mode, "set": True}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_dpi() -> Dict[str, Any]:
    """Get current DPI scaling for all monitors."""
    try:
        monitors = []
        def enum_cb(hmon, hdc, lprect, data):
            try:
                info = ctypes.wintypes.MONITORINFOEX()
                info.cbSize = ctypes.sizeof(ctypes.wintypes.MONITORINFOEX)
                ctypes.windll.user32.GetMonitorInfoW(hmon, ctypes.byref(info))
                dpi_x = ctypes.wintypes.UINT()
                ctypes.windll.shcore.GetDpiForMonitor(hmon, 0, ctypes.byref(dpi_x))
                monitors.append({"name": info.szDevice, "dpi": dpi_x.value, "scale": round(dpi_x.value / 96 * 100)})
            except Exception:
                monitors.append({"error": "per_monitor_dpi_failed"})
            return True
        MONITORENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.wintypes.RECT), ctypes.c_void_p)
        ctypes.windll.user32.EnumDisplayMonitors(None, None, MONITORENUMPROC(enum_cb), 0)
        return {"monitors": monitors, "default_dpi": user32.GetDpiForSystem()}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def check_accessibility() -> Dict[str, Any]:
    """Check Windows accessibility settings (sticky keys, filter keys, toggle keys, high contrast)."""
    try:
        result = {}
        try:
            import winreg
            key = r"Control Panel\Accessibility\StickyKeys"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
                val, _ = winreg.QueryValueEx(k, "Flags")
                result["sticky_keys"] = "on" if "5" in val else "off"
        except Exception:
            result["sticky_keys"] = "unknown"
        try:
            key = r"Control Panel\Accessibility\Keyboard Response"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
                val, _ = winreg.QueryValueEx(k, "Flags")
                result["filter_keys"] = "on" if "5" in val else "off"
        except Exception:
            result["filter_keys"] = "unknown"
        try:
            key = r"Control Panel\Accessibility\ToggleKeys"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
                val, _ = winreg.QueryValueEx(k, "Flags")
                result["toggle_keys"] = "on" if "5" in val else "off"
        except Exception:
            result["toggle_keys"] = "unknown"
        try:
            key = r"Control Panel\Desktop"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
                val, _ = winreg.QueryValueEx(k, "UserPreferenceMask")
                result["high_contrast"] = bool(val[0] & 0x1)
        except Exception:
            result["high_contrast"] = False
        return result
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_system_resources() -> Dict[str, Any]:
    """Get detailed system resource usage via Win32 API (no psutil needed)."""
    try:
        mem = MEMORYSTATUSEX()
        mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
        return {
            "memory": {
                "total_gb": round(mem.ullTotalPhys / 1073741824, 2),
                "available_gb": round(mem.ullAvailPhys / 1073741824, 2),
                "used_percent": mem.dwMemoryLoad,
                "total_virtual_gb": round(mem.ullTotalVirtual / 1073741824, 2),
                "available_virtual_gb": round(mem.ullAvailVirtual / 1073741824, 2),
            },
            "handles_count": _count_handles(),
        }
    except Exception as e:
        return {"error": str(e)}

def _count_handles() -> int:
    """Count open handles in current process."""
    try:
        h = kernel32.GetCurrentProcess()
        count = ctypes.wintypes.DWORD()
        ntdll.NtQueryInformationProcess(h, 16, ctypes.byref(count), ctypes.sizeof(count), None)
        return count.value
    except Exception:
        return -1

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Virtual Desktop & Shell Tools (PowerShell fallback)
# ═══════════════════════════════════════════════════════════════════════════════
@server.tool()
def list_virtual_desktops() -> Dict[str, Any]:
    """List all virtual desktops (Win10 1903+). Uses PowerShell COM automation."""
    try:
        ps = """
Add-Type -AssemblyName System.Runtime.InteropServices
$shell = New-Object -ComObject Shell.Application
$desktops = $shell.Windows() | Select-Object -Property FullName, Title, HWND
$desktops | ConvertTo-Json -Depth 3
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return {"raw": r.stdout.strip(), "method": "PowerShell COM"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def switch_virtual_desktop(desktop_number: int = 0) -> Dict[str, Any]:
    """Switch to virtual desktop by number. Uses Ctrl+Win+Left/Right navigation."""
    try:
        import pyautogui
        current = 0
        if desktop_number == 0:
            return {"action": "stay_on_current", "desktop": current}
        key = "right" if desktop_number > current else "left"
        for _ in range(abs(desktop_number - current)):
            pyautogui.hotkey("ctrl", "win", key)
            time.sleep(0.3)
        return {"action": "switched", "target": desktop_number, "method": "keyboard"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def create_virtual_desktop() -> Dict[str, Any]:
    """Create a new virtual desktop. Uses Win+Ctrl+D."""
    try:
        import pyautogui
        pyautogui.hotkey("win", "ctrl", "d")
        time.sleep(0.5)
        return {"action": "created", "method": "Win+Ctrl+D"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def move_window_to_desktop(title: str, desktop_number: int = 1) -> Dict[str, Any]:
    """Move a window to a different virtual desktop."""
    try:
        import pyautogui, win32gui
        hwnd = win32gui.FindWindow(None, title)
        if not hwnd:
            hwnd = _fuzzy_find_hwnd(title)
        if not hwnd:
            return {"error": "window_not_found"}
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.2)
        current = 0
        diff = desktop_number - current
        if diff > 0:
            pyautogui.hotkey("win", "ctrl", "shift", "right")
        elif diff < 0:
            pyautogui.hotkey("win", "ctrl", "shift", "left")
        time.sleep(0.5)
        return {"action": "moved", "window": title, "target_desktop": desktop_number}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def toggle_taskbar_autohide() -> Dict[str, Any]:
    """Toggle taskbar auto-hide on/off."""
    try:
        import win32gui, win32api
        abm = ctypes.wintypes.APPBARDATA()
        abm.cbSize = ctypes.sizeof(ctypes.wintypes.APPBARDATA)
        abm.lParam = 2  # ABS_AUTOHIDE
        result = shell32.SHAppBarMessage(0x1, ctypes.byref(abm))  # ABM_GETSTATE
        current = bool(result & 1)
        abm.lParam = int(current)  # Toggle
        shell32.SHAppBarMessage(0x2, ctypes.byref(abm))  # ABM_SETSTATE
        return {"was_autohide": current, "now_autohide": not current}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def show_start_menu() -> Dict[str, Any]:
    """Open the Start Menu."""
    try:
        user32.keybd_event(0x5B, 0, 0, 0)  # Left Win key down
        user32.keybd_event(0x5B, 0, 2, 0)  # Left Win key up
        return {"action": "start_menu_opened"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def toggle_show_desktop() -> Dict[str, Any]:
    """Toggle Show Desktop (minimize all windows). Win+D."""
    try:
        user32.keybd_event(0x5B, 0, 0, 0)
        user32.keybd_event(0x44, 0, 0, 0)
        user32.keybd_event(0x44, 0, 2, 0)
        user32.keybd_event(0x5B, 0, 2, 0)
        return {"action": "show_desktop_toggled"}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Clipboard Monitor & History
# ═══════════════════════════════════════════════════════════════════════════════
_clipboard_history: List[Dict] = []
_clipboard_watch_active = False

@server.tool()
def start_clipboard_monitor() -> Dict[str, Any]:
    """Start monitoring clipboard changes in background."""
    global _clipboard_watch_active
    if _clipboard_watch_active:
        return {"status": "already_running"}
    _clipboard_watch_active = True
    last = clipboard_get()
    def _watch():
        global _clipboard_watch_active
        while _clipboard_watch_active:
            time.sleep(0.5)
            try:
                current = clipboard_get()
                if current and current != last:
                    _clipboard_history.append({
                        "text": current, "time": datetime.now().isoformat(),
                        "length": len(current)
                    })
                    if len(_clipboard_history) > 500:
                        _clipboard_history.pop(0)
            except Exception:
                pass
    t = threading.Thread(target=_watch, daemon=True)
    t.start()
    return {"status": "started", "history_max": 500}

@server.tool()
def stop_clipboard_monitor() -> Dict[str, Any]:
    """Stop clipboard monitoring."""
    global _clipboard_watch_active
    _clipboard_watch_active = False
    return {"status": "stopped", "entries_collected": len(_clipboard_history)}

@server.tool()
def get_clipboard_history_entries(max_entries: int = 50) -> Dict[str, Any]:
    """Get clipboard change history."""
    entries = _clipboard_history[-max_entries:]
    return {"entries": entries, "total": len(_clipboard_history)}

@server.tool()
def search_clipboard_history(query: str) -> Dict[str, Any]:
    """Search clipboard history by text content."""
    results = [e for e in _clipboard_history if query.lower() in e.get("text", "").lower()]
    return {"query": query, "results": results, "count": len(results)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — OCR-Click & Template Matching
# ═══════════════════════════════════════════════════════════════════════════════
@server.tool()
def ocr_find_and_click(target_text: str, confidence: int = 80, region: str = "", click_type: str = "left") -> Dict[str, Any]:
    """Find text on screen via OCR and click it. Region format: x,y,w,h or empty for full screen."""
    try:
        import pytesseract, pyautogui
        from PIL import Image
        if HAS_MSS:
            with mss.mss() as sct:
                if region:
                    x, y, w, h = [int(v.strip()) for v in region.split(",")]
                    monitor = {"left": x, "top": y, "width": w, "height": h}
                else:
                    monitor = sct.monitors[0]
                img = sct.grab(monitor)
                pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        else:
            pil = pyautogui.screenshot()
        data = pytesseract.image_to_data(pil, output_type=pytesseract.Output.DICT)
        clicks = []
        for i, text in enumerate(data["text"]):
            if target_text.lower() in text.lower() and int(data["conf"][i]) >= confidence:
                cx = data["left"][i] + data["width"][i] // 2
                cy = data["top"][i] + data["height"][i] // 2
                if region:
                    x_off, y_off = [int(v.strip()) for v in region.split(",")][:2]
                    cx += x_off
                    cy += y_off
                getattr(pyautogui, f"{click_type}_click" if click_type != "left" else "click")(cx, cy)
                clicks.append({"x": cx, "y": cy, "text": text, "confidence": int(data["conf"][i])})
                break
        return {"found": len(clicks) > 0, "clicks": clicks}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def template_match(template_path: str, region: str = "", threshold: float = 0.8) -> Dict[str, Any]:
    """Find a template image on screen using OpenCV matchTemplate."""
    try:
        import cv2
        if HAS_MSS:
            with mss.mss() as sct:
                if region:
                    x, y, w, h = [int(v.strip()) for v in region.split(",")]
                    monitor = {"left": x, "top": y, "width": w, "height": h}
                else:
                    monitor = sct.monitors[0]
                img = sct.grab(monitor)
                screen = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        else:
            screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        template = cv2.imread(template_path)
        if template is None:
            return {"error": "template_not_found"}
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        h, w = template.shape[:2]
        if max_val >= threshold:
            cx = max_loc[0] + w // 2
            cy = max_loc[1] + h // 2
            return {"found": True, "x": cx, "y": cy, "confidence": round(max_val, 4),
                    "bbox": {"x": max_loc[0], "y": max_loc[1], "w": w, "h": h}}
        return {"found": False, "best_confidence": round(max_val, 4), "threshold": threshold}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def template_click(template_path: str, click_type: str = "left", threshold: float = 0.8) -> Dict[str, Any]:
    """Find template on screen and click its center."""
    try:
        result = template_match(template_path, threshold=threshold)
        if not result.get("found"):
            return result
        import pyautogui
        x, y = result["x"], result["y"]
        getattr(pyautogui, f"{click_type}_click" if click_type != "left" else "click")(x, y)
        return {"clicked": True, "x": x, "y": y, "confidence": result.get("confidence")}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Chrome DevTools Protocol (remote debugging)
# ═══════════════════════════════════════════════════════════════════════════════
CHROME_CDP_PORT = 9222

def _chrome_cdp_available() -> bool:
    """Check if Chrome DevTools is available on default port."""
    try:
        import urllib.request
        resp = urllib.request.urlopen(f"http://127.0.0.1:{CHROME_CDP_PORT}/json/version", timeout=2)
        return True
    except Exception:
        return False

@server.tool()
def chrome_list_tabs() -> Dict[str, Any]:
    """List all open Chrome tabs via DevTools Protocol."""
    try:
        import urllib.request, json
        if not _chrome_cdp_available():
            return {"error": "chrome_cdp_not_available", "hint": "Launch Chrome with --remote-debugging-port=9222"}
        resp = urllib.request.urlopen(f"http://127.0.0.1:{CHROME_CDP_PORT}/json", timeout=5)
        tabs = json.loads(resp.read().decode())
        return {"tabs": [{"title": t.get("title"), "url": t.get("url"), "id": t.get("id")} for t in tabs]}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def chrome_navigate(url: str, tab_index: int = 0) -> Dict[str, Any]:
    """Navigate Chrome tab to a URL via DevTools Protocol."""
    try:
        import urllib.request, json, websocket
        tabs_resp = urllib.request.urlopen(f"http://127.0.0.1:{CHROME_CDP_PORT}/json", timeout=5)
        tabs = json.loads(tabs_resp.read().decode())
        if tab_index >= len(tabs):
            return {"error": "tab_index_out_of_range"}
        ws_url = tabs[tab_index].get("webSocketDebuggerUrl")
        if not ws_url:
            return {"error": "no_websocket_url"}
        ws = websocket.create_connection(ws_url, timeout=5)
        ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        result = ws.recv()
        ws.close()
        return {"navigated": True, "url": url, "response": json.loads(result)}
    except ImportError:
        return {"error": "websocket_client_not_installed", "pip": "pip install websocket-client"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def chrome_evaluate_js(expression: str, tab_index: int = 0) -> Dict[str, Any]:
    """Execute JavaScript in Chrome tab via DevTools Protocol."""
    try:
        import urllib.request, json, websocket
        tabs_resp = urllib.request.urlopen(f"http://127.0.0.1:{CHROME_CDP_PORT}/json", timeout=5)
        tabs = json.loads(tabs_resp.read().decode())
        if tab_index >= len(tabs):
            return {"error": "tab_index_out_of_range"}
        ws_url = tabs[tab_index].get("webSocketDebuggerUrl")
        if not ws_url:
            return {"error": "no_websocket_url"}
        ws = websocket.create_connection(ws_url, timeout=10)
        ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expression, "returnByValue": True}}))
        result = json.loads(ws.recv())
        ws.close()
        value = result.get("result", {}).get("result", {}).get("value")
        return {"result": value, "type": result.get("result", {}).get("result", {}).get("type")}
    except ImportError:
        return {"error": "websocket_client_not_installed"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def chrome_take_screenshot(tab_index: int = 0) -> Dict[str, Any]:
    """Take screenshot of Chrome tab via DevTools Protocol."""
    try:
        import urllib.request, json, websocket, base64
        tabs_resp = urllib.request.urlopen(f"http://127.0.0.1:{CHROME_CDP_PORT}/json", timeout=5)
        tabs = json.loads(tabs_resp.read().decode())
        if tab_index >= len(tabs):
            return {"error": "tab_index_out_of_range"}
        ws_url = tabs[tab_index].get("webSocketDebuggerUrl")
        if not ws_url:
            return {"error": "no_websocket_url"}
        ws = websocket.create_connection(ws_url, timeout=10)
        ws.send(json.dumps({"id": 1, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        result = json.loads(ws.recv())
        ws.close()
        data = result.get("result", {}).get("data", "")
        if data:
            path = os.path.join(TEMP_DIR, f"chrome_tab_{tab_index}.png")
            with open(path, "wb") as f:
                f.write(base64.b64decode(data))
            return {"path": path, "size": len(data)}
        return {"error": "no_screenshot_data"}
    except ImportError:
        return {"error": "websocket_client_not_installed"}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Office COM Automation
# ═══════════════════════════════════════════════════════════════════════════════
@server.tool()
def office_open_document(filepath: str) -> Dict[str, Any]:
    """Open a document in the appropriate Office app via COM."""
    try:
        ext = os.path.splitext(filepath)[1].lower()
        apps = {".docx": "Word.Application", ".doc": "Word.Application", ".xlsx": "Excel.Application",
                ".xls": "Excel.Application", ".pptx": "PowerPoint.Application", ".ppt": "PowerPoint.Application"}
        app_name = apps.get(ext)
        if not app_name:
            subprocess.Popen(["start", "", filepath], shell=True)
            return {"method": "shell_open", "filepath": filepath}
        ps = f'$app = New-Object -ComObject {app_name}; $app.Visible = $true; $doc = $app.Documents.Open("{filepath}"); Write-Output "opened"'
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=15, encoding='utf-8', errors='replace')
        return {"method": "COM", "app": app_name, "filepath": filepath, "success": "opened" in r.stdout.lower()}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def office_read_document(filepath: str) -> Dict[str, Any]:
    """Read text content from Office document via COM."""
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in (".docx", ".doc"):
            ps = f'$app = New-Object -ComObject Word.Application; $app.Visible = $false; $doc = $app.Documents.Open("{filepath}"); $text = $doc.Content.Text; $doc.Close(); $app.Quit(); Write-Output $text'
        elif ext in (".xlsx", ".xls"):
            ps = f'$app = New-Object -ComObject Excel.Application; $app.Visible = $false; $wb = $app.Workbooks.Open("{filepath}"); $ws = $wb.Sheets.Item(1); $text = $ws.UsedRange.Text; $wb.Close($false); $app.Quit(); Write-Output $text'
        else:
            return {"error": f"unsupported_extension: {ext}"}
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
        return {"content": r.stdout.strip()[:5000], "filepath": filepath}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — WMI & Performance Monitoring
# ═══════════════════════════════════════════════════════════════════════════════
@server.tool()
def wmi_query(wmi_class: str = "Win32_Processor", properties: str = "*") -> Dict[str, Any]:
    """Execute a WMI query and return results."""
    try:
        ps = f"Get-CimInstance -ClassName '{wmi_class}' | Select-Object -Property '{properties}' | ConvertTo-Json -Depth 4"
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=15, encoding='utf-8', errors='replace')
        return {"class": wmi_class, "data": json.loads(r.stdout) if r.stdout.strip() else [], "error": r.stderr.strip() if r.stderr else None}
    except json.JSONDecodeError:
        return {"class": wmi_class, "raw": r.stdout[:3000]}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_cpu_usage_wmi() -> Dict[str, Any]:
    """Get CPU usage via WMI (no psutil needed)."""
    try:
        ps = """
$cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object -Property Name, LoadPercentage, NumberOfCores, NumberOfLogicalProcessors, CurrentClockSpeed
$cpu | ConvertTo-Json -Depth 3
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return json.loads(r.stdout) if r.stdout.strip() else {"error": "no_data"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_memory_usage_wmi() -> Dict[str, Any]:
    """Get memory usage via WMI."""
    try:
        ps = """
$mem = Get-CimInstance -ClassName Win32_OperatingSystem
$total = [math]::Round($mem.TotalVisibleMemorySize/1MB, 2)
$free = [math]::Round($mem.FreePhysicalMemory/1MB, 2)
$used = $total - $free
$pct = [math]::Round(($used/$total)*100, 1)
ConvertTo-Json @{total_gb=$total; used_gb=$used; free_gb=$free; used_percent=$pct}
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return json.loads(r.stdout) if r.stdout.strip() else {"error": "no_data"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_disk_usage_wmi() -> Dict[str, Any]:
    """Get disk usage for all drives via WMI."""
    try:
        ps = """
Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID,
@{N='SizeGB';E={[math]::Round($_.Size/1GB,2)}},
@{N='FreeGB';E={[math]::Round($_.FreeSpace/1GB,2)}},
@{N='UsedPct';E={[math]::Round(($_.Size-$_.FreeSpace)/$_.Size*100,1)}} | ConvertTo-Json -Depth 3
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return json.loads(r.stdout) if r.stdout.strip() else {"error": "no_data"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_gpu_info() -> Dict[str, Any]:
    """Get GPU information via WMI."""
    try:
        ps = """
Get-CimInstance -ClassName Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion, VideoProcessor, CurrentHorizontalResolution, CurrentVerticalResolution | ConvertTo-Json -Depth 3
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return json.loads(r.stdout) if r.stdout.strip() else {"error": "no_data"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_network_usage() -> Dict[str, Any]:
    """Get network adapter info and current traffic."""
    try:
        ps = """
$adapters = Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled}
$stats = Get-CimInstance -ClassName Win32_PerfFormattedData_Tcpip_NetworkInterface | Select-Object Name, BytesTotalPersec, BytesSentPersec, BytesReceivedPersec
ConvertTo-Json @{adapters=$adapters; stats=$stats} -Depth 4
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return json.loads(r.stdout) if r.stdout.strip() else {"error": "no_data"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_top_processes(count: int = 10, sort_by: str = "cpu") -> Dict[str, Any]:
    """Get top processes by CPU or memory usage."""
    try:
        sort_prop = "CPU" if sort_by == "cpu" else "WorkingSet64"
        ps = f"""
Get-Process | Sort-Object -Property {sort_prop} -Descending | Select-Object -First {count} -Property ProcessName, Id, 
@{{N='CPU_s';E={{[math]::Round($_.CPU,1)}}}}, 
@{{N='Mem_MB';E={{[math]::Round($_.WorkingSet64/1MB,1)}}}} | ConvertTo-Json -Depth 3
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return json.loads(r.stdout) if r.stdout.strip() else {"error": "no_data"}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Data Processing Tools
# ═══════════════════════════════════════════════════════════════════════════════
@server.tool()
def json_parse_file(filepath: str) -> Dict[str, Any]:
    """Parse and validate a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {"valid": True, "type": type(data).__name__, "size": len(str(data)), "data": data if len(str(data)) < 5000 else f"(too large: {len(str(data))} chars)"}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e), "line": e.lineno, "column": e.colno}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def json_transform(json_str: str, path: str = "") -> Dict[str, Any]:
    """Parse JSON and extract value at a dot-notation path. Example: 'data.users.0.name'"""
    try:
        data = json.loads(json_str)
        if path:
            parts = path.split(".")
            for part in parts:
                if isinstance(data, dict):
                    data = data[part]
                elif isinstance(data, list):
                    data = data[int(part)]
                else:
                    return {"error": f"cannot navigate into {type(data).__name__}"}
        return {"result": data if len(str(data)) < 5000 else f"(large: {len(str(data))} chars)"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def csv_read_file(filepath: str, limit: int = 100) -> Dict[str, Any]:
    """Read a CSV file and return headers + rows."""
    try:
        import csv
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader, [])
            rows = []
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                rows.append(row)
            return {"headers": headers, "rows": rows, "row_count": len(rows), "limited": i >= limit}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def csv_write_file(filepath: str, headers: str, rows_json: str) -> Dict[str, Any]:
    """Write a CSV file. headers is comma-separated. rows_json is JSON array of arrays."""
    try:
        import csv
        header_list = [h.strip() for h in headers.split(",")]
        rows = json.loads(rows_json)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header_list)
            writer.writerows(rows)
        return {"success": True, "filepath": filepath, "rows_written": len(rows)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def xml_parse_file(filepath: str) -> Dict[str, Any]:
    """Parse XML file and return structure."""
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(filepath)
        root = tree.getroot()
        def elem_to_dict(el):
            d = {"tag": el.tag, "attrib": dict(el.attrib)}
            children = list(el)
            if children:
                d["children"] = [elem_to_dict(c) for c in children]
            if el.text and el.text.strip():
                d["text"] = el.text.strip()
            return d
        return {"valid": True, "root": elem_to_dict(root)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def toml_parse_file(filepath: str) -> Dict[str, Any]:
    """Parse TOML file."""
    try:
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        with open(filepath, 'r', encoding='utf-8') as f:
            data = tomllib.loads(f.read()) if hasattr(tomllib, 'loads') else tomllib.load(f)
        return {"valid": True, "data": data if len(str(data)) < 5000 else f"(large: {len(str(data))} chars)"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def ini_parse_file(filepath: str) -> Dict[str, Any]:
    """Parse INI configuration file."""
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read(filepath, encoding='utf-8')
        data = {section: dict(config.items(section)) for section in config.sections()}
        return {"valid": True, "sections": list(config.sections()), "data": data}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def ini_write_file(filepath: str, sections_json: str) -> Dict[str, Any]:
    """Write INI file from JSON dict of sections."""
    try:
        import configparser
        config = configparser.ConfigParser()
        data = json.loads(sections_json)
        for section, values in data.items():
            if isinstance(values, dict):
                for k, v in values.items():
                    config.set(section, str(k), str(v))
            else:
                config[section] = values
        with open(filepath, 'w', encoding='utf-8') as f:
            config.write(f)
        return {"success": True, "filepath": filepath}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — Display & Power Tools
# ═══════════════════════════════════════════════════════════════════════════════
@server.tool()
def list_displays() -> Dict[str, Any]:
    """List all connected displays with resolution and refresh rate."""
    try:
        displays = []
        def enum_display_devices(device, extra_data, flags, lparam):
            if extra_data.StateFlags & 1:
                displays.append({
                    "name": extra_data.DeviceName,
                    "description": extra_data.DeviceString,
                    "primary": bool(extra_data.StateFlags & 4),
                    "monitor_index": extra_data.StateFlags & 0xf,
                })
            return True
        EnumDisplayDevicesW = ctypes.windll.user32.EnumDisplayDevicesW
        DISPLAY_DEVICEW = ctypes.wintypes.DISPLAY_DEVICEW
        cb = ctypes.sizeof(DISPLAY_DEVICEW)
        ENUM_DISPLAY_SETTINGS_EX = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.POINTER(ctypes.wintypes.DEVMODEW), ctypes.c_ulong)
        i = 0
        while True:
            dd = DISPLAY_DEVICEW()
            dd.cb = cb
            if not EnumDisplayDevicesW(None, i, ctypes.byref(dd), 0):
                break
            if dd.StateFlags & 1:
                devmode = ctypes.wintypes.DEVMODEW()
                devmode.dmSize = ctypes.sizeof(devmode)
                if ctypes.windll.user32.EnumDisplaySettingsExW(dd.DeviceName, -1, ctypes.byref(devmode), 0):
                    displays.append({
                        "name": dd.DeviceName,
                        "description": dd.DeviceString,
                        "resolution": f"{devmode.dmPelsWidth}x{devmode.dmPelsHeight}",
                        "width": devmode.dmPelsWidth,
                        "height": devmode.dmPelsHeight,
                        "refresh_rate": devmode.dmDisplayFrequency,
                        "bpp": devmode.dmBitsPerPel,
                        "primary": bool(dd.StateFlags & 4),
                    })
            i += 1
        return {"displays": displays, "count": len(displays)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def set_display_resolution(width: int, height: int, display: str = None) -> Dict[str, Any]:
    """Set display resolution."""
    try:
        devmode = ctypes.wintypes.DEVMODEW()
        devmode.dmSize = ctypes.sizeof(devmode)
        devmode.dmPelsWidth = width
        devmode.dmPelsHeight = height
        devmode.dmFields = 0x1 | 0x2  # DM_PELSWIDTH | DM_PELSHEIGHT
        target = display or ctypes.windll.user32.GetDefaultPrinterW() if hasattr(ctypes.windll.user32, 'GetDefaultPrinterW') else None
        result = ctypes.windll.user32.ChangeDisplaySettingsExW(target, ctypes.byref(devmode), None, 0, None)
        return {"width": width, "height": height, "success": result == 0, "code": result}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_power_info() -> Dict[str, Any]:
    """Get battery/power status via Win32 API."""
    try:
        system_power = SYSTEM_POWER_STATUS()
        ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(system_power))
        ac = {0: "Offline", 1: "Online", 2: "Unknown"}.get(system_power.ACLineStatus, "Unknown")
        bat = {0: "Unknown", 1: "High", 2: "Low", 3: "Critical", 4: "Charging", 5: "No battery"}.get(system_power.BatteryFlag, "Unknown")
        pct = system_power.BatteryLifePercent
        if pct == 255:
            pct = -1
        return {"ac_power": ac, "battery_status": bat, "battery_percent": pct,
                "seconds_remaining": system_power.BatteryLifeTime if system_power.BatteryLifeTime != 0xFFFFFFFF else -1}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def set_power_plan(plan: str = "high") -> Dict[str, Any]:
    """Set Windows power plan (balanced, high, power_saver)."""
    try:
        plans = {"balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
                 "high": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                 "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a"}
        plan_guid = plans.get(plan.lower())
        if not plan_guid:
            return {"error": f"unknown_plan: {plan}", "valid_plans": list(plans.keys())}
        r = subprocess.run(["powercfg", "/setactive", plan_guid], capture_output=True, text=True, timeout=5)
        return {"success": r.returncode == 0, "plan": plan, "guid": plan_guid}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def prevent_sleep(minutes: int = 0) -> Dict[str, Any]:
    """Prevent system from sleeping for specified minutes (0=indefinite)."""
    try:
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x1
        ES_DISPLAY_REQUIRED = 0x2
        if minutes > 0:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
            def _reset():
                time.sleep(minutes * 60)
                ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            threading.Thread(target=_reset, daemon=True).start()
        else:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
        return {"prevented": True, "minutes": minutes, "note": "call prevent_sleep(0) to stop indefinite prevention"}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# V3.0 — IPC: Named Pipes, HTTP Server, Shared Memory
# ═══════════════════════════════════════════════════════════════════════════════
_named_pipe_server = None
_named_pipe_thread = None
_shared_memory_registry = {}

@server.tool()
def named_pipe_send(pipe_name: str, message: str) -> Dict[str, Any]:
    """Send a message to a named pipe server."""
    try:
        import win32file, win32pipe
        pipe_path = f"\\\\.\\pipe\\{pipe_name}"
        handle = win32file.CreateFile(pipe_path, win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
        msg_bytes = message.encode('utf-8')
        win32file.WriteFile(handle, msg_bytes)
        _, resp = win32file.ReadFile(handle, 65536)
        win32file.CloseHandle(handle)
        return {"sent": True, "response": resp.decode('utf-8', errors='replace')}
    except ImportError:
        ps = f'$pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", "{pipe_name}", [System.IO.Pipes.PipeDirection]::InOut); $pipe.Connect(5000); $sw = New-Object System.IO.StreamWriter($pipe); $sw.WriteLine("{message}"); $sw.Flush(); $sr = New-Object System.IO.StreamReader($pipe); $resp = $sr.ReadLine(); $pipe.Close(); Write-Output $resp'
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return {"sent": True, "response": r.stdout.strip(), "method": "PowerShell"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def shared_memory_write(name: str, data: str, size: int = 4096) -> Dict[str, Any]:
    """Write data to a named shared memory segment (memory-mapped file)."""
    try:
        path = os.path.join(TEMP_DIR, f"shm_{name}.dat")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data[:size])
        _shared_memory_registry[name] = {"path": path, "size": len(data), "time": datetime.now().isoformat()}
        return {"success": True, "name": name, "bytes_written": len(data[:size])}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def shared_memory_read(name: str) -> Dict[str, Any]:
    """Read data from a named shared memory segment."""
    try:
        info = _shared_memory_registry.get(name)
        if not info:
            path = os.path.join(TEMP_DIR, f"shm_{name}.dat")
            if not os.path.exists(path):
                return {"error": "not_found"}
            info = {"path": path}
        with open(info["path"], 'r', encoding='utf-8') as f:
            data = f.read()
        return {"success": True, "name": name, "data": data}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def shared_memory_list() -> Dict[str, Any]:
    """List all shared memory segments."""
    segments = {}
    for name, info in _shared_memory_registry.items():
        segments[name] = info
    # Also scan temp dir
    for f in glob.glob(os.path.join(TEMP_DIR, "shm_*.dat")):
        bn = os.path.basename(f).replace("shm_", "").replace(".dat", "")
        if bn not in segments:
            segments[bn] = {"path": f, "size": os.path.getsize(f)}
    return {"segments": segments, "count": len(segments)}

@server.tool()
def get_window_ui_tree(title: str = "", depth: int = 3) -> Dict[str, Any]:
    """Get the UI Automation tree for a window."""
    try:
        hwnd = None
        if title:
            hwnd = win32gui.FindWindow(None, title)
            if not hwnd:
                hwnd = _fuzzy_find_hwnd(title)
        if not hwnd:
            return {"error": "window_not_found"}
        ps = f"""
Add-Type -AssemblyName UIAutomationClient
$automation = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]{hwnd})
function Get-Children($element, $maxDepth, $currentDepth) {{
    if ($currentDepth -ge $maxDepth) {{ return @() }}
    $children = $element.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
    $result = @()
    foreach ($child in $children) {{
        $info = @{{
            Name = $child.Current.Name
            ControlType = $child.Current.ControlType.ProgrammaticName
            AutomationId = $child.Current.AutomationId
            ClassName = $child.Current.ClassName
            BoundingRectangle = $child.Current.BoundingRectangle.ToString()
        }}
        $result += $info
        $result += Get-Children $child $maxDepth ($currentDepth + 1)
    }}
    return $result
}}
$tree = Get-Children $automation {depth} 0
$tree | ConvertTo-Json -Depth 4
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=15, encoding='utf-8', errors='replace')
        try:
            elements = json.loads(r.stdout)
            return {"window": title, "hwnd": hwnd, "elements": elements if isinstance(elements, list) else [elements]}
        except json.JSONDecodeError:
            return {"window": title, "hwnd": hwnd, "raw": r.stdout[:3000]}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_element_properties(automation_id: str = "", class_name: str = "", name: str = "", hwnd: int = 0) -> Dict[str, Any]:
    """Get detailed properties of a specific UI element."""
    try:
        import win32gui
        if hwnd == 0:
            hwnd = win32gui.GetForegroundWindow()
        ps = f"""
Add-Type -AssemblyName UIAutomationClient
$automation = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]{hwnd})
$condition = [System.Windows.Automation.Condition]::TrueCondition
$props = @()
if ('{automation_id}') {{ $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::AutomationIdProperty, '{automation_id}') }}
elseif ('{class_name}') {{ $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ClassNameProperty, '{class_name}') }}
elseif ('{name}') {{ $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, '{name}') }}
$element = $automation.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
if ($element) {{
    $props = @(
        @{{
            Name = $element.Current.Name
            ControlType = $element.Current.ControlType.ProgrammaticName
            AutomationId = $element.Current.AutomationId
            ClassName = $element.Current.ClassName
            BoundingRectangle = $element.Current.BoundingRectangle.ToString()
            IsEnabled = $element.Current.IsEnabled
            HasKeyboardFocus = $element.Current.HasKeyboardFocus
            IsOffscreen = $element.Current.IsOffscreen
            HelpText = $element.Current.HelpText
        }}
    )
}}
$props | ConvertTo-Json -Depth 4
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        try:
            data = json.loads(r.stdout)
            return {"element": data if isinstance(data, list) else [data]}
        except json.JSONDecodeError:
            return {"raw": r.stdout[:2000]}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def invoke_element(automation_id: str = "", class_name: str = "", name: str = "", hwnd: int = 0) -> Dict[str, Any]:
    """Invoke (click/activate) a UI element by its automation properties."""
    try:
        import win32gui
        if hwnd == 0:
            hwnd = win32gui.GetForegroundWindow()
        where = "AutomationId" if automation_id else ("ClassName" if class_name else "Name")
        value = automation_id or class_name or name
        ps = f"""
Add-Type -AssemblyName UIAutomationClient
$automation = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]{hwnd})
$condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::{where}Property, '{value}')
$element = $automation.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
if ($element) {{
    $invokePattern = $element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
    $invokePattern.Invoke()
    Write-Output "invoked"
}} else {{
    Write-Output "not_found"
}}
"""
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return {"success": "invoked" in r.stdout, "element": {"automation_id": automation_id, "class_name": class_name, "name": name}}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def toggle_high_contrast(enable: bool = True) -> Dict[str, Any]:
    """Toggle Windows High Contrast mode."""
    try:
        SPI_SETHIGHCONTRAST = 0x0043
        hc = ctypes.wintypes.HIGHCONTRAST()
        hc.cbSize = ctypes.sizeof(ctypes.wintypes.HIGHCONTRAST)
        if enable:
            hc.dwFlags = 0x1  # HCF_HIGHCONTRASTON
        else:
            hc.dwFlags = 0  # HCF_HIGHCONTRASTOFF
        user32.SystemParametersInfoW(SPI_SETHIGHCONTRAST, hc.cbSize, ctypes.byref(hc), 0)
        return {"enabled": enable}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def magnifier_control(action: str = "start", zoom: int = 200) -> Dict[str, Any]:
    """Control Windows Magnifier. Actions: start, stop, zoom_in, zoom_out, set_zoom."""
    try:
        try:
            import win32gui, win32con
            if action == "stop":
                hwnd = win32gui.FindWindow("Magnifier", "Magnifier")
                if hwnd:
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                return {"action": "stopped"}
            if action == "start":
                subprocess.Popen(["magnify.exe"], creationflags=0x00000010 if hasattr(os, 'DETACHED_PROCESS') else 0)
                time.sleep(1)
            if action == "zoom_in":
                user32.keybd_event(0x6B, 0, 0, 0); user32.keybd_event(0x6B, 0, 2, 0)
            elif action == "zoom_out":
                user32.keybd_event(0x6D, 0, 0, 0); user32.keybd_event(0x6D, 0, 2, 0)
            elif action == "set_zoom":
                # Use registry to set magnifier zoom
                try:
                    import winreg
                    key = r"Software\Microsoft\Magnification"
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key) as k:
                        winreg.SetValueEx(k, "ZoomFactor", 0, winreg.REG_DWORD, zoom)
                except Exception:
                    pass
            return {"action": action, "zoom": zoom}
        except Exception as e:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_system_info_detailed() -> Dict[str, Any]:
    """Get comprehensive system information."""
    try:
        import psutil
        return {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python": platform.python_version(),
            "hostname": platform.node(),
            "cpu_count": os.cpu_count(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 1),
        }
    except ImportError:
        return {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python": platform.python_version(),
            "hostname": platform.node(),
            "cpu_count": os.cpu_count(),
        }

@server.tool()
def list_processes_detailed(sort_by: str = "cpu") -> Dict[str, Any]:
    """List running processes."""
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
            try:
                info = p.info
                procs.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "cpu": info.get('cpu_percent', 0),
                    "memory_mb": round(info['memory_info'].rss / 1024 / 1024, 1) if info.get('memory_info') else 0,
                    "status": info.get('status', 'unknown'),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        if sort_by == "memory":
            procs.sort(key=lambda x: x["memory_mb"], reverse=True)
        elif sort_by == "cpu":
            procs.sort(key=lambda x: x["cpu"], reverse=True)
        return {"processes": procs[:50], "total": len(procs)}
    except ImportError:
        r = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=5)
        return {"raw": r.stdout[:3000]}

@server.tool()
def kill_process_detailed(pid: int = 0, name: str = "") -> Dict[str, Any]:
    """Kill a process by PID or name."""
    try:
        import psutil
        if pid:
            p = psutil.Process(pid)
            p.terminate()
            return {"killed": True, "pid": pid, "name": p.name()}
        elif name:
            killed = []
            for p in psutil.process_iter(['pid', 'name']):
                if name.lower() in p.info['name'].lower():
                    p.terminate()
                    killed.append(p.info['pid'])
            return {"killed": True, "pids": killed, "name": name}
        return {"error": "specify_pid_or_name"}
    except ImportError:
        if pid:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
        elif name:
            subprocess.run(["taskkill", "/F", "/IM", name], capture_output=True)
        return {"method": "taskkill", "pid": pid, "name": name}

@server.tool()
def open_file_detailed(filepath: str) -> Dict[str, Any]:
    """Open a file with its default application."""
    try:
        os.startfile(filepath)
        return {"opened": True, "filepath": filepath}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def open_url_detailed(url: str) -> Dict[str, Any]:
    """Open a URL in the default browser."""
    try:
        import webbrowser
        webbrowser.open(url)
        return {"opened": True, "url": url}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def ping_host(host: str = "google.com", count: int = 4) -> Dict[str, Any]:
    """Ping a host."""
    try:
        r = subprocess.run(["ping", "-n", str(count), host], capture_output=True, text=True, timeout=15)
        return {"host": host, "success": r.returncode == 0, "output": r.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def get_ip_addresses() -> Dict[str, Any]:
    """Get local and public IP addresses."""
    try:
        import urllib.request
        local = socket.gethostbyname(socket.gethostname()) if 'socket' in dir() else "unknown"
        try:
            public = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
        except Exception:
            public = "unknown"
        return {"local_ip": local, "public_ip": public}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def list_services_detailed(filter_str: str = "") -> Dict[str, Any]:
    """List Windows services."""
    try:
        import psutil
        services = []
        for s in psutil.win_services_iter():
            try:
                if filter_str and filter_str.lower() not in s.name().lower():
                    continue
                services.append({
                    "name": s.name(),
                    "display_name": s.display_name(),
                    "status": s.status(),
                    "start_type": s.start_type() if hasattr(s, 'start_type') else "unknown",
                })
            except Exception:
                pass
        return {"services": services[:100], "total": len(services)}
    except ImportError:
        r = subprocess.run(["sc", "query", "type=service", "state=all"], capture_output=True, text=True, timeout=10)
        return {"raw": r.stdout[:3000]}

@server.tool()
def get_service_status_detailed(name: str) -> Dict[str, Any]:
    """Get status of a specific service."""
    try:
        import psutil
        s = psutil.win_service_get(name)
        info = s.as_dict()
        return {"name": info["name"], "display_name": info["display_name"],
                "status": info["status"], "start_type": info.get("start_type", "unknown"),
                "pid": info.get("pid")}
    except ImportError:
        r = subprocess.run(["sc", "query", name], capture_output=True, text=True, timeout=5)
        return {"name": name, "raw": r.stdout[:2000]}

@server.tool()
def start_service_detailed(name: str) -> Dict[str, Any]:
    """Start a Windows service."""
    try:
        r = subprocess.run(["net", "start", name], capture_output=True, text=True, timeout=30)
        return {"success": r.returncode == 0, "name": name, "output": r.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def stop_service_detailed(name: str) -> Dict[str, Any]:
    """Stop a Windows service."""
    try:
        r = subprocess.run(["net", "stop", name], capture_output=True, text=True, timeout=30)
        return {"success": r.returncode == 0, "name": name, "output": r.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def run_shell_command(cmd: str, timeout: int = 30) -> Dict[str, Any]:
    """Run a shell command."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True, encoding='utf-8', errors='replace')
        return {"stdout": r.stdout, "stderr": r.stderr, "returncode": r.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "timeout": timeout}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def run_powershell_script(script: str, timeout: int = 30) -> Dict[str, Any]:
    """Run a PowerShell script."""
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace')
        return {"stdout": r.stdout, "stderr": r.stderr, "returncode": r.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "timeout": timeout}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def lock_screen_win32() -> Dict[str, Any]:
    """Lock the Windows screen."""
    try:
        user32.LockWorkStation()
        return {"locked": True}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def set_wallpaper_win32(filepath: str) -> Dict[str, Any]:
    """Set desktop wallpaper."""
    try:
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02
        result = user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        return {"success": bool(result), "filepath": filepath}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def show_toast_notification(title: str, message: str) -> Dict[str, Any]:
    """Show a Windows toast notification."""
    try:
        ps = f'''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null
$template = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text>{title}</text>
            <text>{message}</text>
        </binding>
    </visual>
</toast>
"@
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Desktop Control").Show($toast)
Write-Output "shown"
'''
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        return {"shown": "shown" in r.stdout, "title": title}
    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# BROWSER AUTOMATION (Vercel agent-browser pattern)
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def browser_open(url: str) -> Dict[str, Any]:
    """Open URL in default browser."""
    try:
        import webbrowser
        webbrowser.open(url)
        return {"opened": url}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def browser_tabs() -> Dict[str, Any]:
    """List open browser tabs via Chrome DevTools Protocol."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-Process chrome | Select-Object -First 1"],
            capture_output=True, text=True, timeout=5
        )
        return {"chrome_running": result.returncode == 0, "note": "Use Playwright for full tab control"}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def browser_screenshot(url: str = None) -> Dict[str, Any]:
    """Take screenshot of browser page. Requires Playwright."""
    try:
        return {"note": "Use playwright_browser_take_screenshot tool for full browser automation"}
    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY VALIDATION (Vercel deepsec pattern)
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def security_check_secrets() -> Dict[str, Any]:
    """Scan current directory for exposed secrets (API keys, passwords)."""
    try:
        import re
        patterns = [
            r'api[_-]?key\s*[=:]\s*["\']([^"\']+)["\']',
            r'password\s*[=:]\s*["\']([^"\']+)["\']',
            r'secret\s*[=:]\s*["\']([^"\']+)["\']',
            r'token\s*[=:]\s*["\']([^"\']+)["\']',
        ]
        found = []
        for py_file in glob.glob("**/*.py", recursive=True)[:50]:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if len(match) > 8 and match not in ['your-api-key', 'xxx']:
                                found.append({"file": py_file, "type": pattern.split('\\')[0], "value": match[:8] + "..."})
            except:
                pass
        return {"secrets_found": len(found), "details": found[:10]}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def security_check_permissions(path: str = None) -> Dict[str, Any]:
    """Check file permissions for security issues."""
    try:
        if path is None:
            path = os.getcwd()
        issues = []
        for root, dirs, files in os.walk(path):
            for f in files[:100]:
                fp = os.path.join(root, f)
                try:
                    stat = os.stat(fp)
                    if stat.st_mode & 0o002:
                        issues.append({"file": fp, "issue": "world-writable"})
                    if f.endswith(('.key', '.pem', '.p12')):
                        issues.append({"file": fp, "issue": "sensitive file"})
                except:
                    pass
        return {"issues_found": len(issues), "details": issues[:10]}
    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# WORKFLOW ORCHESTRATION (Vercel Workflow DevKit pattern)
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def workflow_circuit_breaker(func_name: str, failure_threshold: int = 3) -> Dict[str, Any]:
    """Circuit breaker pattern - track failures and prevent cascading."""
    try:
        state_file = os.path.join(LOG_DIR, f"circuit_{func_name}.json")
        state = {"failures": 0, "state": "closed", "last_failure": None}
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                state = json.load(f)
        return {"function": func_name, "state": state}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def workflow_retry_with_backoff(func_name: str, max_retries: int = 3) -> Dict[str, Any]:
    """Retry pattern with exponential backoff."""
    try:
        return {
            "function": func_name,
            "max_retries": max_retries,
            "backoff_base": 2,
            "pattern": "exponential_backoff",
            "note": "Use retry_operation() function for implementation"
        }
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def workflow_dead_letter_queue() -> Dict[str, Any]:
    """Dead letter queue for failed operations."""
    try:
        dlq_file = os.path.join(LOG_DIR, "dead_letter_queue.json")
        queue = []
        if os.path.exists(dlq_file):
            with open(dlq_file, 'r') as f:
                queue = json.load(f)
        return {"queue_size": len(queue), "items": queue[-5:]}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
def workflow_event_sourcing(event_type: str, payload: Dict) -> Dict[str, Any]:
    """Event sourcing - log events for replay."""
    try:
        events_file = os.path.join(LOG_DIR, "events.jsonl")
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "payload": payload
        }
        with open(events_file, 'a') as f:
            f.write(json.dumps(event) + "\n")
        return {"logged": True, "event_type": event_type}
    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# QUICK REFERENCE
# ─────────────────────────────────────────────────────────────────────────────
@server.tool()
def quick_reference() -> Dict[str, List[str]]:
    """Get quick reference for all available operations."""
    return {
        "uia_navigation": [
            "find_ui_element(name) - Find UI element by name (no OCR)",
            "click_ui_element(name) - Click UI element by name",
            "type_in_ui_element(name, text) - Type into edit field",
            "get_ui_tree() - Get UI element tree",
        ],
        "self_healing": [
            "click(x, y) - Auto-retry click with debug screenshots",
            "type_text(text) - Auto-retry type with clipboard fallback",
        ],
        "smart_waits": [
            "wait_for_text_on_screen(text, timeout) - Wait for OCR text",
            "wait_for_image_on_screen(image, timeout) - Wait for image",
            "wait_for_pixel_color(x,y,r,g,b, timeout) - Wait for color",
            "wait_for_window(title, timeout) - Wait for window",
            "wait_for_process(name, timeout) - Wait for process start",
            "wait_for_screen_change(x,y,w,h, timeout) - Wait for change",
        ],
        "multi_monitor": [
            "list_monitors() - List all monitors",
            "take_screenshot_monitor(id) - Capture specific monitor",
            "take_screenshot_all_monitors() - Capture all monitors",
            "get_mouse_monitor() - Get monitor under mouse",
        ],
        "batching": [
            "batch_actions([...]) - Execute multiple actions at once",
            "batch_clicks([...]) - Click multiple positions rapidly",
        ],
        "feedback": [
            "speak(text) - Text-to-speech",
            "toast_notification(title, msg) - Windows toast",
            "beep_notification(freq, duration) - Play beep",
        ],
        "debug": [
            "debug_toggle(bool) - Enable/disable debug screenshots",
            "debug_get_last_screenshots() - Get last before/after",
            "debug_cleanup(hours) - Clean old debug files",
        ],
        "mouse": [
            "move_mouse(x, y) - Move mouse",
            "click(x, y) - Click with self-healing",
            "double_click(x, y) - Double click",
            "right_click(x, y) - Right click",
            "drag(x1,y1,x2,y2) - Drag",
            "scroll(amount) - Scroll up/down",
            "mouse_position() - Get position",
        ],
        "keyboard": [
            "type_text(text) - Type text (self-healing)",
            "press_key(key) - Press key",
            "hotkey('ctrl+c') - Key combination",
        ],
        "window": [
            "list_windows() - List windows",
            "activate_window(title) - Focus",
            "close_window(title) - Close",
        ],
        "system": [
            "system_info() - System info",
            "list_processes() - List processes",
            "kill_process(name) - Kill process",
            "run_command(cmd) - Run command",
            "run_powershell(script) - Run PowerShell",
        ],
        "browser": [
            "browser_open(url) - Open URL in browser",
            "browser_tabs() - List browser tabs",
            "browser_screenshot(url) - Screenshot browser page",
        ],
        "security": [
            "security_check_secrets() - Scan for exposed secrets",
            "security_check_permissions(path) - Check file permissions",
        ],
        "workflow": [
            "workflow_circuit_breaker(func) - Circuit breaker pattern",
            "workflow_retry_with_backoff(func) - Retry with backoff",
            "workflow_dead_letter_queue() - Failed operations queue",
            "workflow_event_sourcing(type, payload) - Log events",
        ],
    }

if __name__ == "__main__":
    log.info("Starting enhanced pc-control MCP server v2.0...")
    server.run()
