from playwright.sync_api import Page
import datetime

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.kiwi.com/en/"
        self.privacy_popup = page.locator("div[data-test='PrivacyConsent-modal']")
        self.reject_all_button = page.get_by_role("button", name="Reject all")
        self.trip_type_selector_opener = page.get_by_test_id("TripTypeSelector") # The main dropdown button to open options
        self.one_way_option_in_dropdown = page.get_by_test_id("ModePopupOption-oneWay") # The one-way option within the dropdown
        self.departure_airport_input = page.locator("//div[@data-test='PlacePicker-Origin']//input[@data-test='SearchField-input']")
        self.departure_field_container = page.locator("div[data-test='SearchFieldItem-origin']")
        self.departure_airport_clear_button = page.locator("div[data-test='PlacePicker-Origin'] div[data-test='PlacePickerInputPlace-close']")
        self.arrival_airport_input = page.locator("//div[@data-test='PlacePicker-Destination']//input[@data-test='SearchField-input']")
        self.arrival_field_container = page.locator("div[data-test='SearchFieldItem-destination']")
        self.arrival_airport_clear_button = page.locator("div[data-test='PlacePicker-Destination'] div[data-test='PlacePickerInputPlace-close']")
        self.departure_date_input = page.locator("input[data-test='SearchFieldDateInput']")
        self.date_picker_modal = page.locator("div[data-test='NewDatePickerOpen']")
        self.set_dates_button = page.locator("button[data-test='SearchFormDoneButton']")
        self.check_accommodation_checkbox = page.get_by_label("Check accommodation with Kiwi.com Hotels")
        self.search_button = page.locator("a[data-test='LandingSearchButton']")

    def navigate(self):
        self.page.goto(self.url)

    def select_one_way_trip(self):
        self.trip_type_selector_opener.click()
        self.one_way_option_in_dropdown.click()

    def set_departure_airport(self, airport_code):
        self.departure_field_container.click() # Click the container to activate the input
        self.departure_airport_input.fill(airport_code)
        # Click on the suggestion for "Rotterdam, Netherlands" after typing RTM
        self.page.locator(f"div[data-test^='PlacePickerRow-']:has-text(\"Rotterdam, Netherlands\")").click()

    def set_arrival_airport(self, airport_code):
        self.arrival_field_container.click() # Click the container to activate the input
        self.arrival_airport_input.fill(airport_code)
        # Click on the suggestion for "Madrid, Spain" after typing MAD
        self.page.locator(f"div[data-test^='PlacePickerRow-']:has-text(\"Madrid, Spain\")").click()

    def set_departure_date(self, total_days: int):
        self.departure_date_input.click() # Click to open the date picker
        self.date_picker_modal.wait_for(state='visible')

        # Calculate the target date
        target_date = datetime.date.today() + datetime.timedelta(days=total_days)
        target_date_str = target_date.strftime("%Y-%m-%d") # Format to match data-value="YYYY-MM-DD"

        # Find and click the target date
        self.page.locator(f"div[data-test='CalendarDay'][data-value='{target_date_str}']").click()

        # Click the "Set dates" button
        self.set_dates_button.click()
        self.date_picker_modal.wait_for(state='hidden') # Wait for the popup to disappear

    def uncheck_accommodation_option(self):
        if self.check_accommodation_checkbox.is_checked():
            self.check_accommodation_checkbox.click()

    def click_search_button(self):
        self.search_button.click()

    def reject_privacy_consent(self):
        if self.privacy_popup.is_visible():
            self.reject_all_button.click()
            self.privacy_popup.wait_for(state='hidden') # Wait for the popup to disappear

    def clear_departure_airport(self):
        self.departure_airport_clear_button.click()

    def clear_arrival_airport(self):
        self.arrival_airport_clear_button.click()

