---
name: dxf-vision
description: Render DXF headlessly to PNG with ezdxf, then review with @vision. Use for electrical_symbols_v1.dxf, SYM_*.dxf, any DXF without AutoCAD open.
---

# DXF → Vision

## Render (headless, no AutoCAD)

```powershell
python -c "
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt
doc = ezdxf.readfile(r'<FILE>.dxf')
msp = doc.modelspace()
fig = plt.figure(figsize=(14,10), dpi=120)
ax = fig.add_axes([0,0,1,1]); ax.set_axis_off()
Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(msp, finalize=True)
fig.savefig(r'<OUT>.png', facecolor='white')
"
```

## Review with @vision

Read the PNG, report: text labels found, block references resolved vs missing,
geometry present vs text-only. Known limit: INSERTs with missing block
definitions render as text only — for full symbols export PNG from AutoCAD.

## Benchmark set

`H:\ai\vision-dwg-batch\outputs\electrical_symbols_v1.png` (12 labels),
`SYM_DIN_RAIL.png` (1 label). October hard set: `benchmark-hard.png` (35 items).

## Log usage

After each real invocation:
\\powershell
python C:/opencodes/guard skills/tools/skill_usage_hook.py dxf-vision use
\