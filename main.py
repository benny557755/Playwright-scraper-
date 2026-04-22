from playwright.sync_api import sync_playwright
from utils import export_csv, export_json
import time


def block_resources(route):
    if route.request.resource_type in ["image", "font"]:
        route.abort()
    else:
        route.continue_()


def main():
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.route("**/*", block_resources)
        page.goto("https://sandbox.oxylabs.io/products", wait_until="domcontentloaded")

        while True:
            page.wait_for_selector(".product-card")
            products = page.query_selector_all(".product-card")

            for product in products:
                name = product.query_selector(".title").inner_text()
                price = product.query_selector(".price-wrapper").inner_text()

                data.append({
                    "name": name,
                    "price": price
                })

            next_button = page.locator(".next a")

            if next_button.count() > 0:
                is_disabled = next_button.first.get_attribute("aria-disabled")

                if is_disabled != "true":
                    print("Clicking next page...")
                    next_button.first.click()
                    page.wait_for_selector(".product-card")
                else:
                    print("Last page reached")
                    break
            else:
                break

        browser.close()

    export_csv(data)
    export_json(data)

    print(f"Done. Total items: {len(data)}")


if __name__ == "__main__":
    main()
