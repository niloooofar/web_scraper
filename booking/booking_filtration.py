"""
This file will include a class with instance methods.
That will be responsible to interact with our website
After we have some results, to apply filtration.
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def choose_accomodation_type(self):
        accomodation_element = self.driver.find_element(
            By.CSS_SELECTOR,
            'otk-selectable-item[placeholder="نوع اقامتگاه"]'
        )
        accomodation_element.click()

        home_element = self.driver.find_element(
            By.CSS_SELECTOR,
            'use[href="/assets/images/Icons/HouseTypes/house.svg#house"]'
        )
        action = ActionChains(self.driver)
        action.move_to_element(home_element).click().perform()

        accept_btn = self.driver.find_element(
            By.CLASS_NAME,
            "action-accept"
        )
        self.driver.execute_script("arguments[0].click();", accept_btn)

    def sort_price_lowest_first(self):
        sort_elements = self.driver.find_element(
            By.CLASS_NAME,
            "sortingType_item"
        ).find_elements(
            By.CSS_SELECTOR,
            "*")
        self.driver.execute_script("arguments[0].click();", sort_elements[3])
