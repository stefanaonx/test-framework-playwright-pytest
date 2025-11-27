from playwright.sync_api import Page, expect
import datetime
import re

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.kiwi.com/en/"

        # Privacy Pop-up
        self.privacy_accept_button = page.locator("[data-test='CookiesPopup-Accept']")

        # Mapping for airport codes to full names as they appear in suggestions
        self.airport_code_to_full_name = {
            "RTM": "Rotterdam, Netherlands",
            "MAD": "Madrid, Spain"
        }

        # Trip Type Selector
        # This will click the currently displayed trip type to open the dropdown
        self.trip_type_selector_opener = page.get_by_role("button", name=re.compile(r"Return|One-way"))
        self.one_way_option_in_dropdown = page.locator("[data-test='ModePopupOption-oneWay']")

        # Airport Inputs
        self.departure_airport_input = page.locator("[data-test='PlacePickerInput-origin'] [data-test='SearchField-input']")
        self.departure_field_container = page.locator("div[data-test='SearchFieldItem-origin']") # still useful for initial click
        self.departure_airport_clear_button = page.locator("div[data-test='PlacePicker-Origin'] div[data-test='PlacePickerInputPlace-close']")

        self.arrival_airport_input = page.locator("[data-test='PlacePickerInput-destination'] [data-test='SearchField-input']")
        self.arrival_field_container = page.locator("div[data-test='SearchFieldItem-destination']") # still useful for initial click
        self.arrival_airport_clear_button = page.locator("div[data-test='PlacePicker-Destination'] div[data-test='PlacePickerInputPlace-close']")


        # Date Picker
        self.departure_date_input = page.locator("[data-test='SearchFieldDateInput']")
        self.set_dates_button = page.locator("[data-test='SearchFormDoneButton']")
        # Locator for individual date cells will be dynamic in set_departure_date

        # Accommodation Checkbox
        self.check_accommodation_checkbox_icon = page.locator(".orbit-checkbox-icon-container > .orbit-icon").first

        # Search Button
        self.search_button = page.locator("[data-test='LandingSearchButton']")

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state('networkidle') # Wait for network to be idle
        self.dismiss_privacy_consent()

    def dismiss_privacy_consent(self):
        try:
            # Using the direct codegen locator
            self.privacy_accept_button.click(timeout=15000) # Removed force=True, not needed with direct locator
        except Exception as e:
            print(f"Privacy consent popup not found or could not be dismissed: {e}")

    def select_one_way_trip(self):
        self.trip_type_selector_opener.click() # Click to open dropdown
        self.one_way_option_in_dropdown.click() # Click one-way option

    def set_departure_airport(self, airport_code):
        # Clear existing if any (codegen didn't show this but it's a good practice)
        if self.departure_airport_clear_button.is_visible():
             self.departure_airport_clear_button.click()
        self.departure_airport_input.click() # Click to activate input
        self.departure_airport_input.fill(airport_code) # Removed slowly=True
        # Codegen used get_by_role("button", name="Rotterdam, Netherlands Add")
        # We need to generalize this. The has-text approach is still good for suggestions.
        full_airport_name = self.airport_code_to_full_name.get(airport_code, airport_code)
        self.page.get_by_role("button", name=f"{full_airport_name} Add").click() # Corrected locator

    def set_arrival_airport(self, airport_code):
        # Clear existing if any
        if self.arrival_airport_clear_button.is_visible():
             self.arrival_airport_clear_button.click()
        self.arrival_airport_input.click() # Click to activate input
        self.arrival_airport_input.fill(airport_code) # Removed slowly=True
        # Codegen used page.locator("[data-test="PlacePickerRow-city"]").click()
        # This might be too generic if there are multiple city rows.
        # Sticking with has-text for now, but keeping an eye on it.
        full_airport_name = self.airport_code_to_full_name.get(airport_code, airport_code)
        self.page.get_by_role("button", name=f"{full_airport_name} Add").click() # Corrected locator

    def set_departure_date(self, total_days: int):
        self.departure_date_input.click() # Click to open the date picker

        target_date = datetime.date.today() + datetime.timedelta(days=total_days)
        target_date_str = target_date.strftime("%Y-%m-%d") # Format to match data-value="YYYY-MM-DD"

        # The codegen shows clicking a navigation button, but we want to click the specific date.
        # We will keep our original logic for clicking the specific date, as it's more direct.
        self.page.locator(f"div[data-test='CalendarDay'][data-value='{target_date_str}']").click()

        self.set_dates_button.click() # Click the "Set dates" button

    def uncheck_accommodation_option(self):
        # Use the codegen's direct locator for the checkbox icon
        # We still check if it's checked to avoid unnecessary clicks
        if self.page.get_by_label("Check accommodation with Kiwi.com Hotels").is_checked():
            self.check_accommodation_checkbox_icon.click()

    def click_search_button(self):
        self.search_button.click()

