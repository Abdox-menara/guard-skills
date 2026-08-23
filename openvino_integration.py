# OpenVINO Integration for RapidOCR - CPU Optimization
# Based on Qwen recommendations for Intel i7-6920HQ

import os
import time
import threading
from typing import List, Tuple, Optional
from pathlib import Path

try:
    from openvino.runtime import Core, CompiledModel
    OPENVINO_AVAILABLE = True
except ImportError:
    OPENVINO_AVAILABLE = False


class OpenVINOOCR:
    """OpenVINO-optimized OCR for Intel CPUs"""
    
    def __init__(self, model_dir: str = None):
        self.core = Core() if OPENVINO_AVAILABLE else None
        self.det_model = None
        self.rec_model = None
        self.model_dir = model_dir or self._find_models()
        self.lock = threading.Lock()
        
        if OPENVINO_AVAILABLE:
            self._load_models()
    
    def _find_models(self) -> str:
        """Find RapidOCR model directory"""
        possible_paths = [
            os.path.join(os.path.expanduser("~"), ".cache", "rapidocr"),
            os.path.join(os.path.dirname(__file__), "models"),
            "C:/Users/Abdox/.cache/rapidocr",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return os.path.join(os.path.dirname(__file__), "models")
    
    def _load_models(self):
        """Load OpenVINO IR models"""
        if not OPENVINO_AVAILABLE:
            print("OpenVINO not available, using fallback")
            return
        
        det_xml = os.path.join(self.model_dir, "det_model.xml")
        rec_xml = os.path.join(self.model_dir, "rec_model.xml")
        
        if os.path.exists(det_xml):
            self.det_model = self.core.compile_model(det_xml, "CPU")
            print(f"Loaded detection model: {det_xml}")
        
        if os.path.exists(rec_xml):
            self.rec_model = self.core.compile_model(rec_xml, "CPU")
            print(f"Loaded recognition model: {rec_xml}")
    
    def ocr(self, image_path: str) -> List[Tuple[str, float]]:
        """Run OCR on image with OpenVINO acceleration"""
        if not OPENVINO_AVAILABLE or not self.det_model:
            return self._fallback_ocr(image_path)
        
        start = time.time()
        
        # Preprocess image
        image = self._preprocess_image(image_path)
        
        # Run detection
        det_result = self.det_model(image)
        
        # Run recognition on detected regions
        results = []
        # ... (full implementation would process detected regions)
        
        elapsed = (time.time() - start) * 1000
        print(f"OpenVINO OCR: {elapsed:.1f}ms")
        
        return results
    
    def _preprocess_image(self, image_path: str):
        """Preprocess image for OpenVINO"""
        try:
            import cv2
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Resize to model input size
            img = cv2.resize(img, (960, 960))
            
            # Convert to NCHW format
            img = img.transpose((2, 0, 1))
            img = img.reshape(1, 3, 960, 960)
            
            # Normalize
            img = img.astype("float32") / 255.0
            
            return img
        except Exception as e:
            print(f"Preprocess error: {e}")
            return None
    
    def _fallback_ocr(self, image_path: str) -> List[Tuple[str, float]]:
        """Fallback to basic OCR"""
        return [("Fallback OCR - OpenVINO not available", 0.0)]


class ThreadedOCR:
    """Thread pool for parallel OCR processing"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.ocr_engine = OpenVINOOCR()
        self.results = {}
        self.lock = threading.Lock()
    
    def process_image(self, image_id: str, image_path: str):
        """Process single image"""
        result = self.ocr_engine.ocr(image_path)
        with self.lock:
            self.results[image_id] = result
    
    def process_batch(self, image_paths: List[str]) -> dict:
        """Process multiple images in parallel"""
        threads = []
        
        for i, path in enumerate(image_paths):
            t = threading.Thread(
                target=self.process_image,
                args=(str(i), path)
            )
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        return self.results


if __name__ == "__main__":
    print("OpenVINO OCR Module")
    print(f"OpenVINO Available: {OPENVINO_AVAILABLE}")
    
    ocr = OpenVINOOCR()
    print(f"Models loaded: det={ocr.det_model is not None}, rec={ocr.rec_model is not None}")

