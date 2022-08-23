"""
This file is going to include method that will parse
the specific data that we need from each one of the deal boxes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR,
            'div[class="all-container"]')

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # Pulling the hotel name
            hotel_name = deal_box.find_element(
                By.CLASS_NAME,
                "room-title"
            ).find_element(By.TAG_NAME, "h2").get_attribute('innerHTML').strip().replace('&nbsp;', " ")

            # Pulling the hotel reviews
            room_star_box = deal_box.find_element(
                By.XPATH,
                '/html/body/otk-root/main/otk-search-result/div/div[2]/div/div[2]/otk-indicator/div/div[1]/div['
                '1]/otk-room-box/div/a/div[2]/div[2]')
            first_child = room_star_box.find_elements(By.XPATH, "./* ")[0]
            second_inner_child = first_child.find_elements(By.XPATH, "./* ")[1]
            second_inner_child = second_inner_child.find_elements(By.XPATH, "./* ")
            hotel_score = second_inner_child[1].get_attribute('innerHTML').strip()
            score_count = second_inner_child[2].get_attribute('innerHTML').strip()

            # Pulling the hotel price
            hotel_price = deal_box.find_element(
                By.CLASS_NAME,
                "price"
            ).find_elements(By.TAG_NAME, 'span')[1].get_attribute('innerHTML').strip()

            collection.append(
                [hotel_name, hotel_score, score_count, hotel_price]
            )
        return collection
