from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage


class ComparisonPage(BasePage):
    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/compare'

    def get_name_in_comparison(self) -> List[str]:
        '''Получаем список продуктов на странице сравнения'''
        table_body: WebElement = self.driver.find_element(By.TAG_NAME, 'tbody')
        search_names_el: List[WebElement] = table_body.find_elements(By.TAG_NAME, 'a')
        actual_name_in_comparison: List[str] = [el.text for el in search_names_el]
        return actual_name_in_comparison

    def get_button_remove(self) -> WebElement:
        '''Находим кнопку удалить'''
        button_remove: WebElement = self.driver.find_element(By.CLASS_NAME, 'btn-danger')
        return button_remove

    def remove(self):
        '''Кликаем по кнопке удалить, ждем чтобы '''
        WebDriverWait(self.driver, timeout=5).until(
            element_to_be_clickable(self.get_button_remove()))
        self.get_button_remove().click()

    def get_alert_text(self) -> str:
        '''Считываем текст после удаления из сравнения'''
        content: WebElement = self.driver.find_element(By.ID, 'content')
        warning_text: WebElement = content.find_element(By.TAG_NAME, 'p')
        return warning_text.text
