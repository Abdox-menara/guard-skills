---
name: pdf-ocr
version: 7.0.0
author: Abdox
description: |
  ULTRA-ADVANCED PDF OCR Skill — Content stream scaling approach that produces
  the smallest possible searchable PDFs with perfect text selectability.
  Uses Tesseract's native PDF output and scales it to match original page
  dimensions via PDF content stream transforms.

  PDF-OCR: Complete document digitization system that converts scanned PDFs
  and images into fully searchable, selectable-text PDFs with maximum quality.

  FEATURES:
  - Content stream scaling (smallest files, best selectability)
  - Tesseract OCR with auto language detection
  - Batch processing: entire folders in one command
  - Quality presets: Draft / Standard / High / Ultra
  - Page range selection: specific pages or ranges
  - Multiple input formats: PDF, PNG, JPG, TIFF, BMP
  - Smart image preprocessing: contrast, sharpen
  - Auto-detect text PDFs (no OCR needed, just copy)
  - Real-time progress with ETA tracking
  - Config file for persistent settings
  - Right-click context menu integration
  - Drag-and-drop batch file support

  TRIGGER PHRASES: "OCR PDF", "searchable PDF", "extract text from PDF",
  "make PDF searchable", "batch OCR", "scanned to text", "PDF OCR tool",
  "digitize document", "OCR this PDF", "convert scanned PDF".

  TRAINED ON: Tesseract OCR, image preprocessing, PDF content stream manipulation,
  PyMuPDF, batch workflows, document digitization.

  ENVIRONMENT: Windows 11, Python 3.11+, Tesseract OCR, PyMuPDF, pytesseract,
  pypdf, Pillow.

  SECURITY: All processing is local — no data leaves the machine.
---

# PDF OCR Pro — v7.0.0

## Architecture

Content stream scaling approach:
1. **Render** — PDF pages are rendered as high-resolution images (up to 600 DPI)
2. **Preprocess** — Images are contrast-enhanced and sharpened
3. **OCR** — Tesseract generates a native PDF with invisible text (`3 Tr` render mode)
4. **Scale** — Content stream is wrapped in a scale transform to match original page dimensions
5. **Set MediaBox** — Page geometry is corrected to match the original

**Why this approach wins**: Tesseract's native PDF uses `3 Tr` (invisible text) with CID font encoding. When this raw content stream is preserved and scaled via a PDF transform (`q sx 0 0 sy 0 0 cm ... Q`), the text remains selectable in all PDF viewers including PDFelement. No form XObjects, no re-encoding — smallest file size and perfect selectability.

### Comparison of tested approaches

| Approach | File Size | Selectable | Notes |
|----------|-----------|------------|-------|
| Content stream scaling (v7) | 1.7 MB/page | Yes | Winner: smallest files, raw text ops |
| show_pdf_page() | 1.8 MB/page | Yes | Similar but adds form XObject overhead |
| insert_text(render_mode=3) | 2.8 MB/page | Yes | Larger, PyMuPDF re-encodes fonts |
| OCRmyPDF | 27 MB/page | Yes | 16x larger due to image re-encoding |
| Tesseract raw | 1.8 MB/page | Yes | Wrong page size (3401x4812) |
| Tesseract+MediaBox only | 1.8 MB/page | No | Text drawn off-page |

### Critical implementation detail

```python
# WRONG: tp.set_contents(new) → ValueError: bad xref
# RIGHT: use update_stream()
td.update_stream(xrefs[0], new_bytes)
```

## Available Commands

| Action | Command |
|--------|---------|
| Basic OCR | `pdf-ocr.py document.pdf` |
| High quality | `pdf-ocr.py -q ultra document.pdf` |
| Page range | `pdf-ocr.py -p 1-10,15,20-25 document.pdf` |
| Batch folder | `pdf-ocr.py --batch ./scans/` |
| Custom language | `pdf-ocr.py -l ara+eng document.pdf` |
| Text output | `pdf-ocr.py -f txt document.pdf` |
| Specific output dir | `pdf-ocr.py -o ./output/ document.pdf` |
| List languages | `pdf-ocr.py --list-langs` |
| Install language | `pdf-ocr.py --install-lang ara` |
| Show config | `pdf-ocr.py --config` |
| Set config | `pdf-ocr.py --set threads 8` |

## Quality Presets

| Preset | DPI | Use Case |
|--------|-----|----------|
| `draft` | 150 | Quick preview, large batches, low priority |
| `standard` | 300 | General purpose, good balance |
| `high` | 400 | Important documents, small text |
| `ultra` | 600 | Archival quality, maximum accuracy |

## Language Support

Default: `eng+fra` (English + French)

Install additional languages:
```
pdf-ocr.py --install-lang ara    # Arabic
pdf-ocr.py --install-lang deu    # German
pdf-ocr.py --install-lang spa    # Spanish
pdf-ocr.py --install-lang chi_sim  # Chinese Simplified
pdf-ocr.py --install-lang rus    # Russian
```

## Workflow

1. Place script in `Desktop\PDF OCR Tool\` or run from anywhere
2. Right-click any PDF/PNG/JPG → "Create Searchable PDF (OCR)"
3. Or drag-drop onto `OCR PDF.cmd`
4. Or use CLI for advanced options

## Troubleshooting

- **"File not found"** — Check path contains no special characters, use quotes
- **"Tesseract not found"** — Verify Tesseract installed at `C:\Program Files\Tesseract-OCR\`
- **Permission denied** — Close the output PDF if it's open in a viewer
- **Poor OCR quality** — Try `-q ultra` for higher DPI, or install the correct language
- **Slow processing** — Increase threads with `--set threads 8` or use `-q standard`
- **Cross-drive error** — Use `-o` to specify output on the same drive as input

## Files

- `pdf-ocr.py` — Main script (put on Desktop for easy access)
- `OCR PDF.cmd` — Drag-and-drop batch file
- `Install Context Menu.reg` — Right-click context menu installer
- `~/.config/pdf-ocr/config.json` — Persistent settings
