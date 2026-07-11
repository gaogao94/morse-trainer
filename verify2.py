from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 900, "height": 1400})
    page.goto("file:///home/admin/coding/morse_trainer/index.html")
    page.wait_for_timeout(500)
    page.screenshot(path="shot_wide.png")
    print("Screenshot saved")

    dims = page.evaluate("""() => {
        const svg = document.getElementById('tree');
        return { w: svg.getAttribute('width'), h: svg.getAttribute('height'), vb: svg.getAttribute('viewBox') };
    }""")
    print("Tree SVG dims:", json.dumps(dims))

    timing = page.evaluate("""() => ({
        tC: document.getElementById('tC').textContent,
        tW: document.getElementById('tW').textContent,
        tU: document.getElementById('tU').textContent,
        tT: document.getElementById('tT').textContent
    })""")
    print("Timing display:", json.dumps(timing))

    browser.close()
