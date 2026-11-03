import re

from playwright.sync_api import Page, expect

URL = "https://demo.automationtesting.in/Register.html"

FIRST_NAME = "John"
LAST_NAME = "Doe"
ADDRESS = "123 Main Street, Dhaka"
EMAIL = "john.doe@example.com"
PHONE = "0123456789"
LANGUAGES = ["English", "Hindi"]
SKILL = "Java"
COUNTRY = "India"
YEAR, MONTH, DAY = "1995", "May", "15"
PASSWORD = "Test@1234"


def test_fill_registration_form(page: Page, tmp_path):
    page.goto(URL)
    expect(page).to_have_title("Register")

    # Full name
    first_name = page.locator("input[placeholder='First Name']")
    last_name = page.locator("input[placeholder='Last Name']")
    first_name.fill(FIRST_NAME)
    last_name.fill(LAST_NAME)

    # Address, email and phone
    address = page.locator("textarea[ng-model='Adress']")
    email = page.locator("input[type='email']")
    phone = page.locator("input[type='tel']")
    address.fill(ADDRESS)
    email.fill(EMAIL)
    phone.fill(PHONE)

    # Gender (radio) and hobbies (checkboxes)
    male = page.locator("input[value='Male']")
    cricket = page.locator("#checkbox1")
    movies = page.locator("#checkbox2")
    hockey = page.locator("#checkbox3")
    male.check()
    cricket.check()
    movies.check()

    # Languages: custom multi-select, open it and click each option
    languages = page.locator("#msdd")
    languages.click()
    for language in LANGUAGES:
        page.locator("ul.ui-autocomplete:visible li a", has_text=language).click()
    page.locator("body").click(position={"x": 5, "y": 5})  # close the dropdown

    # Skills: normal <select>
    skills = page.locator("#Skills")
    skills.select_option(SKILL)

    # Select Country: Select2 widget backed by a hidden <select id="country">
    page.locator("span[role='combobox']").click()
    page.locator(".select2-results li", has_text=COUNTRY).click()

    # Date of birth
    year = page.locator("#yearbox")
    month = page.locator("select[placeholder='Month']")
    day = page.locator("#daybox")
    year.select_option(YEAR)
    month.select_option(MONTH)
    day.select_option(DAY)

    # Password and confirm password
    password = page.locator("#firstpassword")
    confirm_password = page.locator("#secondpassword")
    password.fill(PASSWORD)
    confirm_password.fill(PASSWORD)

    # Photo upload
    photo = tmp_path / "photo.png"
    photo.write_bytes(b"\x89PNG\r\n\x1a\n")
    page.locator("#imagesrc").set_input_files(photo)

    # ---- Assertions ----
    expect(first_name).to_have_value(FIRST_NAME)
    expect(last_name).to_have_value(LAST_NAME)
    expect(address).to_have_value(ADDRESS)
    expect(email).to_have_value(EMAIL)
    expect(phone).to_have_value(PHONE)

    expect(male).to_be_checked()
    expect(cricket).to_be_checked()
    expect(movies).to_be_checked()
    expect(hockey).not_to_be_checked()

    for language in LANGUAGES:
        expect(languages).to_contain_text(language)

    expect(skills).to_have_value(SKILL)
    expect(page.locator("#select2-country-container")).to_have_text(COUNTRY)

    expect(year).to_have_value(YEAR)
    expect(month).to_have_value(MONTH)
    expect(day).to_have_value(DAY)

    expect(password).to_have_value(PASSWORD)
    expect(confirm_password).to_have_value(PASSWORD)

    # Submit the form
    submit = page.locator("#submitbtn")
    expect(submit).to_be_enabled()
    submit.click()

    # The demo site has a second required "Country" <select id="countries"> with
    # no options, so browser validation blocks the submit and we stay on the page.
    expect(page).to_have_url(re.compile("Register.html"))
    page.wait_for_timeout(3000)
