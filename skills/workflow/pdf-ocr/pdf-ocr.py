#!/usr/bin/env python3
import sys, os, io, tempfile, shutil, json, time, urllib.request
from pathlib import Path
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from PIL import Image, ImageEnhance, ImageFilter
import fitz, pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
CONFIG_DIR = Path.home() / ".config" / "pdf-ocr"
CONFIG_FILE = CONFIG_DIR / "config.json"
LANG_CACHE = {}
SUPPORTED_IMAGES = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp"}
SUPPORTED_INPUT = {".pdf"} | SUPPORTED_IMAGES
QUALITY_PRESETS = {
    "draft":   {"dpi": 150, "contrast": 1.3, "sharpen": False},
    "standard":{"dpi": 300, "contrast": 1.5, "sharpen": True},
    "high":    {"dpi": 400, "contrast": 1.5, "sharpen": True},
    "ultra":   {"dpi": 600, "contrast": 1.5, "sharpen": True},
}
DEFAULT_CONFIG = {"lang": "eng+fra", "quality": "high", "output_dir": "", "overwrite": False}

def log(msg): print(msg, flush=True)

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f: return {**DEFAULT_CONFIG, **json.load(f)}
        except: pass
    return dict(DEFAULT_CONFIG)

def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f: json.dump(cfg, f, indent=2)

def get_available_langs():
    if LANG_CACHE: return LANG_CACHE
    try:
        r = os.popen('"' + pytesseract.pytesseract.tesseract_cmd + '" --list-langs 2>&1').read()
        langs = [l.strip() for l in r.splitlines() if l.strip() and not l.startswith("List")]
        LANG_CACHE.update({l: True for l in langs})
        return LANG_CACHE
    except: return {}

def has_text(path):
    try:
        reader = __import__("pypdf").PdfReader(str(path))
        total = sum(len(p.extract_text() or "") for p in reader.pages)
        return total / max(len(reader.pages), 1) >= 20
    except: return False

def ocr_page(page, quality, lang):
    q = QUALITY_PRESETS.get(quality, QUALITY_PRESETS["high"])
    dpi = q["dpi"]
    ow, oh = page.rect.width, page.rect.height
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    img = ImageEnhance.Contrast(img).enhance(q["contrast"])
    if q["sharpen"]: img = img.filter(ImageFilter.SHARPEN)
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, lang=lang, extension="pdf", config="--psm 3 --oem 3")
    tess_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    tess_page = tess_doc[0]
    tw, th = tess_page.rect.width, tess_page.rect.height
    sx, sy = ow/tw, oh/th
    xrefs = tess_page.get_contents()
    if xrefs:
        raw = tess_doc.xref_stream(xrefs[0])
        new = ("q\n{:.6f} 0 0 {:.6f} 0 0 cm\n".format(sx, sy)).encode() + raw + b"\nQ\n"
        tess_doc.update_stream(xrefs[0], new)
    tess_page.set_mediabox(fitz.Rect(0, 0, ow, oh))
    return tess_doc

def process_single(input_path, cfg, pages=None):
    path = Path(input_path)
    if not path.exists(): return "File not found: " + str(path)
    ext = path.suffix.lower()
    if ext not in SUPPORTED_INPUT: return "Unsupported format: " + ext
    lang = cfg["lang"]; quality = cfg["quality"]
    t_start = time.time()

    if ext in SUPPORTED_IMAGES:
        q = QUALITY_PRESETS.get(quality, QUALITY_PRESETS["high"])
        img = Image.open(str(path))
        w, h = img.size
        orig_dpi = img.info.get("dpi", (72,72))[0]
        if orig_dpi < q["dpi"]:
            scale = q["dpi"] / orig_dpi
            img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
        img_gray = img.convert("L")
        img_gray = ImageEnhance.Contrast(img_gray).enhance(q["contrast"])
        if q["sharpen"]: img_gray = img_gray.filter(ImageFilter.SHARPEN)
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img_gray, lang=lang, extension="pdf", config="--psm 3 --oem 3")
        tess_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        tess_page = tess_doc[0]
        tw, th = tess_page.rect.width, tess_page.rect.height
        sx, sy = 595/tw, 842/th
        xrefs = tess_page.get_contents()
        if xrefs:
            raw = tess_doc.xref_stream(xrefs[0])
            new = ("q\n{:.6f} 0 0 {:.6f} 0 0 cm\n".format(sx, sy)).encode() + raw + b"\nQ\n"
            tess_doc.update_stream(xrefs[0], new)
        tess_page.set_mediabox(fitz.Rect(0, 0, 595, 842))
        out = tess_doc
        method = "ocr"; total = 1
    elif has_text(str(path)):
        doc = fitz.open(str(path))
        out = fitz.open(); out.insert_pdf(doc)
        total = len(doc); doc.close(); method = "copy"
    else:
        doc = fitz.open(str(path)); total = len(doc)
        ocr_set = set(range(total))
        if pages: ocr_set = {i for i in range(total) if i+1 in pages}
        log("  OCR {} of {} pages ({} quality, {}dpi)...".format(len(ocr_set), total, quality, QUALITY_PRESETS[quality]["dpi"]))
        out = fitz.open()
        done = 0
        for i in range(total):
            if i in ocr_set:
                pg_doc = ocr_page(doc[i], quality, lang)
                out.insert_pdf(pg_doc)
                pg_doc.close()
                done += 1
                elapsed = time.time() - t_start
                rate = done / elapsed if elapsed > 0 else 0
                remaining = len(ocr_set) - done
                eta = remaining / rate if rate > 0 else 0
                log("  [{}/{}] pg {:.0f} OK  {:.1f} pg/s eta {:.0f}s".format(done, len(ocr_set), i+1, rate, eta))
            else:
                out.insert_pdf(doc, from_page=i, to_page=i)
        doc.close(); method = "ocr"

    stem = path.stem
    out_name = stem + " [OCR].pdf"
    out_path = (Path(cfg["output_dir"]) / out_name if cfg["output_dir"] else path.parent / out_name)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf"); tmp.close()
    out.save(tmp.name, deflate=True, garbage=4); out.close()
    n = 1
    while True:
        try:
            if out_path.exists():
                if cfg.get("overwrite"):
                    os.remove(str(out_path))
                else:
                    out_name = stem + " [OCR] ({}).pdf".format(n)
                    out_path = (Path(cfg["output_dir"]) / out_name if cfg["output_dir"] else path.parent / out_name)
                    n += 1; continue
            shutil.move(tmp.name, str(out_path)); break
        except (PermissionError, OSError):
            out_name = stem + " [OCR] ({}).pdf".format(n)
            out_path = (Path(cfg["output_dir"]) / out_name if cfg["output_dir"] else path.parent / out_name)
            n += 1
    elapsed = time.time() - t_start
    size_mb = os.path.getsize(str(out_path)) / (1024*1024)
    speed = total/elapsed if elapsed>0 else 0
    return "Done [{}] {} pg, {:.1f} pg/s, {:.0f}s, {:.1f} MB: {}".format(method, total, speed, elapsed, size_mb, out_name)

def batch_process(paths, cfg):
    results = []
    for p in paths:
        po = Path(p)
        if po.is_dir():
            cnt = 0
            for ext in SUPPORTED_INPUT:
                for f in sorted(po.glob("*" + ext)):
                    results.append(process_single(str(f), cfg)); cnt += 1
            if cnt == 0: results.append("No supported files in: " + p)
        else: results.append(process_single(p, cfg))
    return results

def list_langs():
    langs = get_available_langs()
    if not langs: log("No languages found."); return
    installed = sorted(langs.keys())
    log("Installed OCR languages:")
    for l in installed: log("  " + l)
    log(""); log("Total: " + str(len(installed)) + " languages")
    log('Tip: Install more with: pdf-ocr.py --install-lang <code>')

def install_lang(lang_code):
    url = "https://github.com/tesseract-ocr/tessdata/raw/main/" + lang_code + ".traineddata"
    dest = r"C:\Program Files\Tesseract-OCR\tessdata" + "\\" + lang_code + ".traineddata"
    try:
        log("Downloading " + lang_code + "...")
        urllib.request.urlretrieve(url, dest)
        log("Installed " + lang_code)
        LANG_CACHE.clear()
    except Exception as e: log("Failed: " + str(e))

def main():
    parser = ArgumentParser(prog="pdf-ocr", description="PDF OCR v7 - Searchable PDF via content stream scaling")
    parser.add_argument("input", nargs="*")
    parser.add_argument("-q", "--quality", choices=list(QUALITY_PRESETS.keys()))
    parser.add_argument("-l", "--lang")
    parser.add_argument("-p", "--pages")
    parser.add_argument("-o", "--output")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--list-langs", action="store_true")
    parser.add_argument("--install-lang", metavar="CODE")
    parser.add_argument("--config", action="store_true")
    args = parser.parse_args()
    cfg = load_config()
    if args.config:
        for k,v in cfg.items(): log("  {}: {}".format(k, v)); return
    if args.list_langs: list_langs(); return
    if args.install_lang: install_lang(args.install_lang); return
    if args.quality: cfg["quality"] = args.quality
    if args.lang: cfg["lang"] = args.lang
    if args.output: cfg["output_dir"] = args.output
    if args.overwrite: cfg["overwrite"] = True
    save_config(cfg)
    pages = None
    if args.pages:
        pages = set()
        for part in args.pages.split(","):
            part = part.strip()
            if "-" in part:
                a,b = part.split("-",1)
                pages.update(range(int(a.strip()), int(b.strip())+1))
            else: pages.add(int(part))
    if not args.input: parser.print_help(); return
    try:
        batch = args.batch or all(Path(p).is_dir() for p in args.input if Path(p).exists())
        if batch: results = batch_process(args.input, cfg)
        else: results = [process_single(p, cfg, pages) for p in args.input]
        for r in results: log(r)
    except KeyboardInterrupt: log("Cancelled.")

if __name__ == "__main__": main()
