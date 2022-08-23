import os

from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By

from booking import constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport


class Booking(webdriver.Chrome):

    def __init__(self, driver_path="C:\Program Files (x86)", tear_down=False):
        self.driver_path = driver_path
        self.tear_down = tear_down
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(30)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tear_down:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, "CityNameBoxSearch")
        search_field.clear()
        search_field.send_keys(place_to_go)
        first_result = self.find_element(By.ID, "0")
        first_result.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(By.CLASS_NAME, "gtm_home_search_personcount")
        selection_element.click()

        increase_person_element = self.find_element(By.CSS_SELECTOR, 'img[src="/assets/images/plus-icon.svg"]')
        for _ in range(count):
            increase_person_element.click()

    def click_search(self):
        search_button = self.find_element(
            By.CLASS_NAME,
            "gtm_home_search_button"
        )
        search_button.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.choose_accomodation_type()
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element(
            By.XPATH,
            '/html/body/otk-root/main/otk-search-result/div/div[2]/div/div[2]/otk-indicator/div/div[1]'
        )
        report = BookingReport(hotel_boxes)
        table = PrettyTable(field_names=["عنوان", "امتیاز", "تعداد امتیاز دهندگان", "قیمت"])
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
