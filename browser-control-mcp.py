import asyncio, json, os, logging, base64, io
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
log = logging.getLogger("browser-control-mcp")

from mcp.server import FastMCP
server = FastMCP("browser-control", log_level="WARNING")

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

_browser = None
_page = None
_playwright = None

async def ensure_browser():
    global _browser, _page, _playwright
    if _page is not None:
        return _page
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(headless=False)
    _page = await _browser.new_page()
    return _page

@server.tool()
async def browser_open(url: str):
    page = await ensure_browser()
    await page.goto(url, wait_until="domcontentloaded")
    title = await page.title()
    return json.dumps({"status": "ok", "title": title, "url": url})

@server.tool()
async def browser_close():
    global _browser, _page, _playwright
    if _page:
        await _page.close()
        _page = None
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None
    return json.dumps({"status": "ok"})

@server.tool()
async def browser_snapshot():
    page = await ensure_browser()
    content = await page.content()
    return json.dumps({"html_length": len(content)})

@server.tool()
async def browser_title():
    page = await ensure_browser()
    title = await page.title()
    return title

@server.tool()
async def browser_url():
    page = await ensure_browser()
    return page.url

@server.tool()
async def browser_click(selector: str):
    page = await ensure_browser()
    await page.click(selector)
    return json.dumps({"status": "ok", "selector": selector})

@server.tool()
async def browser_type(selector: str, text: str):
    page = await ensure_browser()
    await page.fill(selector, text)
    return json.dumps({"status": "ok", "selector": selector, "chars": len(text)})

@server.tool()
async def browser_type_into(selector: str, text: str):
    page = await ensure_browser()
    await page.click(selector)
    await page.fill(selector, text)
    return json.dumps({"status": "ok", "selector": selector})

@server.tool()
async def browser_press(key: str):
    page = await ensure_browser()
    await page.keyboard.press(key)
    return json.dumps({"status": "ok", "key": key})

@server.tool()
async def browser_scroll(delta_x: int = 0, delta_y: int = 300):
    page = await ensure_browser()
    await page.evaluate(f"window.scrollBy({delta_x}, {delta_y})")
    return json.dumps({"status": "ok", "delta_x": delta_x, "delta_y": delta_y})

@server.tool()
async def browser_wait(ms: int = 1000):
    await asyncio.sleep(ms / 1000)
    return json.dumps({"status": "ok", "waited_ms": ms})

@server.tool()
async def browser_evaluate(js_code: str):
    page = await ensure_browser()
    result = await page.evaluate(js_code)
    return json.dumps({"status": "ok", "result": str(result)[:500]})

@server.tool()
async def browser_screenshot(save_to: Optional[str] = None):
    page = await ensure_browser()
    if save_to:
        await page.screenshot(path=save_to, full_page=False)
        return json.dumps({"status": "ok", "path": save_to})
    data = await page.screenshot(full_page=False)
    return data

@server.tool()
async def browser_get_html():
    page = await ensure_browser()
    html = await page.content()
    return html[:10000]

@server.tool()
async def browser_get_text():
    page = await ensure_browser()
    text = await page.inner_text("body")
    return text[:5000]

@server.tool()
async def browser_get_links():
    page = await ensure_browser()
    links = await page.evaluate("""() => Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href })).filter(l => l.text)""")
    return json.dumps(links[:50])

@server.tool()
async def browser_get_visible_text():
    page = await ensure_browser()
    text = await page.inner_text("body")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines[:100])

@server.tool()
async def browser_navigate_back():
    page = await ensure_browser()
    await page.go_back()
    return json.dumps({"status": "ok", "url": page.url})

@server.tool()
async def browser_navigate_forward():
    page = await ensure_browser()
    await page.go_forward()
    return json.dumps({"status": "ok", "url": page.url})

@server.tool()
async def browser_reload():
    page = await ensure_browser()
    await page.reload()
    return json.dumps({"status": "ok"})

@server.tool()
async def browser_new_tab(url: str = "about:blank"):
    global _page
    page = await ensure_browser()
    new_page = await _browser.new_page()
    if url and url != "about:blank":
        await new_page.goto(url)
    return json.dumps({"status": "ok", "url": url})

@server.tool()
async def browser_list_tabs():
    global _browser
    if not _browser:
        return json.dumps({"tabs": []})
    pages = _browser.contexts[0].pages if _browser.contexts else []
    result = [{"index": i, "title": await p.title(), "url": p.url} for i, p in enumerate(pages)]
    return json.dumps(result)

if __name__ == "__main__":
    log.info("Starting browser-control MCP server (Playwright)...")
    server.run()
