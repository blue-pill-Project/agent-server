from ..state import GraphState
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def collect_images(state: GraphState) -> GraphState:
    image_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(state["pinterest_url"])
        page.wait_for_timeout(2000)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        soup = BeautifulSoup(page.content(), "html.parser")
        for item in soup.select("div.V3gVHw.TfR6nu.v65fHc"):
            img = item.find("img")
            if img:
                link = (
                    img.get("srcset").split(",")[-1].strip().split(" ")[0]
                    if img.get("srcset")
                    else img.get("src")
                )
                if link and link.startswith("http"):
                    image_urls.append(link)

        browser.close()

        return {"image_urls": image_urls}
