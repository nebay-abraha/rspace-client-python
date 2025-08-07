import os
import re
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv

load_dotenv()

RSPACE_URL = os.getenv("RSPACE_URL")
RSPACE_USERNAME = os.getenv("RSPACE_USERNAME")
RSPACE_PASSWORD = os.getenv("RSPACE_PASSWORD")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(RSPACE_URL)

        # Step 1: Login
        page.get_by_role("textbox", name="User").fill(RSPACE_USERNAME)
        page.get_by_role("textbox", name="Password").fill(RSPACE_PASSWORD)
        page.get_by_role("button", name="Log in").click()

        # Step 2: Navigate to Profile → Manage API Key
        page.get_by_role("link", name="My RSpace").click()
        page.wait_for_selector("text=Generate key")
        page.click("text=Generate key")
        expect(page.get_by_role("dialog", name="Confirm Password")).to_be_visible()
        page.get_by_role("textbox", name="Please confirm your password").fill(RSPACE_PASSWORD)
        page.get_by_role("button", name="OK").click()
        expect(page.get_by_role("link", name="Regenerate key")).to_be_visible()
        expect(page.locator("#apiKeyInfo")).to_contain_text("Key:")

        # Step 4: Wait for key to appear and extract it
        page.wait_for_selector("text=Key:")
        full_text = page.locator("div.api-menu__key").inner_text()
        api_key = re.search(r'Key:\s*([A-Za-z0-9]+)', full_text).group(1).strip()

        with open("api_key.txt", "w") as f:
            f.write(api_key)
            
        browser.close()



if __name__ == "__main__":
    main()