from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://demo.automationtesting.in/")
        print("Page title:", page.title())

        # Explicit wait for 3000 ms
        page.wait_for_timeout(3000)

        page.close()
        browser.close()


if __name__ == "__main__":
    main()
