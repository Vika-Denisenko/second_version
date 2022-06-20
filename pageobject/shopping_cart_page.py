from decimal import Decimal
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, text_to_be_present_in_element, \
    title_is, text_to_be_present_in_element_attribute, staleness_of, visibility_of, invisibility_of_element, any_of
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage
from pageobject.product_page import extract_decimal_price


class ShoppingCartPage(BasePage):
    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=checkout/cart'

    def get_shopping_table(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, 'table-responsive')

    def get_name_list(self) -> List[str]:
        name_list = [element.text for element in self.get_shopping_table().find_elements(By.TAG_NAME, 'a')]
        return name_list[1::2]

    def total_sum(self) -> str:
        table_with_sum = self.driver.find_elements(By.TAG_NAME, 'tbody')[-1]
        field_sum = table_with_sum.find_elements(By.CLASS_NAME, 'text-right')[-1].text

        return extract_decimal_price(field_sum)

    def get_remove_button(self) -> WebElement:
        remove_button = self.driver.find_element(By.CSS_SELECTOR, '[data-original-title="Remove"]')

        return remove_button

    def remove_cart(self):
        self.get_remove_button().click()
        WebDriverWait(self.driver, timeout=5).until(any_of(invisibility_of_element(self.get_remove_button()),
                                                           text_to_be_present_in_element((By.ID, 'content'),
                                                                                         'Your shopping cart is empty!')
                                                           ))

    def get_content_text(self) -> str:
        content = self.driver.find_element(By.ID, 'content')
        text_empty = content.find_element(By.TAG_NAME, 'p').text

        return text_empty
