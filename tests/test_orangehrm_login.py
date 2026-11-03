import re

from playwright.sync_api import Page, expect

URL = "https://opensource-demo.orangehrmlive.com/"
USERNAME = "Admin"
PASSWORD = "admin123"


def test_login_with_xpath(page: Page):
    page.goto(URL)

    # Select the fields and button using XPath locators
    username_field = page.locator("//input[@name='username']")
    password_field = page.locator("//input[@name='password']")
    login_button = page.locator("//button[@type='submit']")

    username_field.fill(USERNAME)
    expect(username_field).to_have_value(USERNAME)

    password_field.fill(PASSWORD)
    expect(password_field).to_have_value(PASSWORD)

    login_button.click()

    # A successful login lands on the dashboard
    expect(page).to_have_url(re.compile("dashboard"))
    expect(page.locator("//h6[normalize-space()='Dashboard']")).to_be_visible()
    page.wait_for_timeout(3000)


def test_forgot_password_with_text_locator(page: Page):
    page.goto(URL)

    # Select the "Forgot your password?" link by its visible text
    forgot_password = page.get_by_text("Forgot your password?")
    expect(forgot_password).to_be_visible()

    forgot_password.click()

    # Clicking it should open the Reset Password page
    expect(page).to_have_url(re.compile("requestPasswordResetCode"))
    expect(page.get_by_role("heading", name="Reset Password")).to_be_visible()
    page.wait_for_timeout(3000)
