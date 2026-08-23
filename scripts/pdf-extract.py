import sys, os, io, tempfile
from pathlib import Path

from PIL import Image
import fitz
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
OCR_LANG = 'eng+fra'

from pypdf import PdfReader


def has_text(path):
    reader = PdfReader(str(path))
    total = 0
    for page in reader.pages:
        t = page.extract_text()
        if t:
            total += len(t.strip())
    return total / max(len(reader.pages), 1) >= 20


def ocr_page(img):
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, lang=OCR_LANG, extension='pdf')
    return fitz.open(stream=pdf_bytes, filetype='pdf')


def make_searchable(path):
    doc = fitz.open(str(path))
    out = fitz.open()

    for i in range(len(doc)):
        page = doc[i]
        imgs = page.get_images(full=True)
        best = None
        if imgs:
            for xref, _, w, h, _, _, _, _, _, _ in imgs:
                if best is None or (w * h) > (best[1] * best[2]):
                    best = (xref, w, h)
        if best and best[1] >= 1500 and best[2] >= 1500:
            base = doc.extract_image(best[0])
            img = Image.open(io.BytesIO(base["image"]))
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))

        page_pdf = ocr_page(img)
        out.insert_pdf(page_pdf)
        page_pdf.close()

    doc.close()
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: pdf-extract.py <pdf_path>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print("File not found")
        sys.exit(1)

    if has_text(str(pdf_path)):
        doc = fitz.open(str(pdf_path))
        out = fitz.open()
        out.insert_pdf(doc)
        doc.close()
    else:
        out = make_searchable(str(pdf_path))

    base_name = f"{pdf_path.stem} [OCR]"
    out_name = base_name + ".pdf"
    out_path = pdf_path.parent / out_name

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    out.save(tmp.name)
    out.close()

    n = 1
    while True:
        try:
            if out_path.exists():
                os.remove(str(out_path))
            os.rename(tmp.name, str(out_path))
            break
        except (PermissionError, OSError):
            out_name = f"{base_name} ({n}).pdf"
            out_path = pdf_path.parent / out_name
            n += 1

    print(f"Done: {out_name}")


if __name__ == "__main__":
    main()
