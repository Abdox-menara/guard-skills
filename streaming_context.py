import json, time, queue, threading
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from collections import deque

@dataclass
class ContextEntry:
    key: str
    value: Any
    timestamp: float
    session_id: str
    ttl: float = 3600.0

class StreamingOutput:
    def __init__(self):
        self.buffer = queue.Queue()
        self.tokens = []
        self.is_streaming = False
        self._callbacks = []

    def start_streaming(self):
        self.is_streaming = True
        self.tokens = []

    def push_token(self, token):
        self.tokens.append(token)
        self.buffer.put(token)
        for cb in self._callbacks:
            try: cb(token)
            except: pass

    def finish(self):
        self.is_streaming = False
        return "".join(self.tokens)

    def on_token(self, callback):
        self._callbacks.append(callback)

class ContextManager:
    def __init__(self, max_entries=1000):
        self.entries = deque(maxlen=max_entries)
        self.sessions = {}
        self._lock = threading.Lock()

    def set(self, key, value, session_id="default", ttl=3600.0):
        entry = ContextEntry(key=key, value=value, timestamp=time.time(), session_id=session_id, ttl=ttl)
        with self._lock:
            self.entries.append(entry)
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            self.sessions[session_id].append(entry)

    def get(self, key, session_id="default"):
        with self._lock:
            for entry in reversed(self.entries):
                if entry.key == key and entry.session_id == session_id:
                    if time.time() - entry.timestamp < entry.ttl:
                        return entry.value
                    break
        return None

    def get_session_context(self, session_id):
        result = {}
        with self._lock:
            if session_id in self.sessions:
                for entry in self.sessions[session_id]:
                    if time.time() - entry.timestamp < entry.ttl:
                        result[entry.key] = entry.value
        return result

class ProactiveInteraction:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def check_confidence(self, text, confidence):
        if confidence < self.threshold:
            return {"needs_confirmation": True, "confidence": confidence}
        return {"needs_confirmation": False, "confidence": confidence}

if __name__ == "__main__":
    print("Streaming + Context Module Ready!")
