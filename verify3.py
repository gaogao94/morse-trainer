from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    # Test with a tall window
    page = browser.new_page(viewport={"width": 900, "height": 1200})
    page.goto("file:///home/admin/coding/morse_trainer/index.html")
    page.wait_for_timeout(500)
    page.screenshot(path="shot_tall.png")

    # Check layout measurements
    layout = page.evaluate("""() => {
        const tw = document.querySelector('.tw');
        const svg = document.querySelector('#tree');
        const app = document.querySelector('.app');
        return {
            appH: app.getBoundingClientRect().height,
            twH: tw.getBoundingClientRect().height,
            svgVB: svg.getAttribute('viewBox'),
            svgPA: svg.getAttribute('preserveAspectRatio'),
            bodyH: document.body.getBoundingClientRect().height,
            viewportH: window.innerHeight
        };
    }""")
    print("Tall window layout:", json.dumps(layout, indent=2))

    # Test with a short window
    page2 = browser.new_page(viewport={"width": 900, "height": 500})
    page2.goto("file:///home/admin/coding/morse_trainer/index.html")
    page2.wait_for_timeout(500)
    layout2 = page2.evaluate("""() => {
        const app = document.querySelector('.app');
        const tw = document.querySelector('.tw');
        return {
            appH: app.getBoundingClientRect().height,
            twH: tw.getBoundingClientRect().height,
            bodyScroll: document.body.scrollHeight,
            viewportH: window.innerHeight
        };
    }""")
    print("Short window layout:", json.dumps(layout2, indent=2))

    browser.close()
