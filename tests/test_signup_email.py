import re

from playwright.sync_api import Page, expect

URL = "https://demo.automationtesting.in/"
EMAIL = "test.user@example.com"


def test_signup_with_email(page: Page):
    page.goto(URL)

    # Select the "Email id for Sign Up" text field
    email_field = page.locator("#email")
    expect(email_field).to_be_visible()

    # fill() sets the whole value at once
    email_field.fill(EMAIL)
    expect(email_field).to_have_value(EMAIL)

    # type the email key by key (type() is deprecated; press_sequentially() replaces it)
    email_field.clear()
    email_field.press_sequentially(EMAIL, delay=100)
    expect(email_field).to_have_value(EMAIL)

    # Select the enter/arrow button next to the field and click it
    enter_button = page.locator("#enterimg")
    enter_button.click()

    # Clicking it should take us to the Register page
    expect(page).to_have_url(re.compile("Register.html"))
    page.wait_for_timeout(3000)
