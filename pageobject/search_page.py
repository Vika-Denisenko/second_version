from dataclasses import dataclass
from decimal import Decimal
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, \
    visibility_of_all_elements_located, any_of, text_to_be_present_in_element
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage


def extract_decimal_price(text: str) -> Decimal:
    """Функция, которая извлекает из строки цену"""

    # text == "$110.00 $122.00\nEx Tax: $90.00"
    split_by_lines: List[str] = text.split("\n")
    # split_by_lines == ["$110.00 $122.00", "Ex Tax: $90.00"]

    first_price_lines = split_by_lines[0].split(' ')
    # first_price == ["$110.00", "$122.00"]

    # Удаляем первый символ (доллар)
    first_price = first_price_lines[0][1:]
    # В случае 1,202.00 нужно убрать запятую.
    first_price_without_punctuation = first_price.replace(",", "")

    return Decimal(first_price_without_punctuation)


@dataclass
class ProductInfo:
    name: str
    price: Decimal


class SearchPage(BasePage):
    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/search'

    def get_search_field(self) -> WebElement:
        '''Получаем основное поле поиска'''
        search_field = self.driver.find_element(By.CLASS_NAME, 'input-lg')
        return search_field

    def get_search_criteria(self) -> WebElement:
        return self.driver.find_element(By.ID, 'input-search')

    def get_search_checkbox(self) -> WebElement:
        return self.driver.find_element(By.ID, 'description')

    def enter_word(self, word: str):
        '''Вводим слово в поле поиска'''
        search_field = self.get_search_field()
        search_field.send_keys(word)

    def clear_search(self):
        '''Очищаем поле поиска'''
        search_field = self.get_search_field()
        search_field.clear()

    def enter_word_in_field_criteria(self, word: str):
        criteria_field = self.get_search_criteria()
        criteria_field.send_keys(word)

    def clear_field_criteria(self):
        self.get_search_criteria().clear()

    def click_checkbox(self):
        self.get_search_checkbox().click()

    def get_search_button(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, 'btn-default')

    def get_button_after_criteria(self) -> WebElement:
        return self.driver.find_element(By.ID, 'button-search')

    def search_basic(self):
        self.get_search_button().click()
        WebDriverWait(self.driver, timeout=3).until(
            any_of(visibility_of_all_elements_located((By.CLASS_NAME, 'product-layout')),
                   text_to_be_present_in_element((By.ID, 'content'), self.get_actual_text()))
            )

    def search_advanced(self):
        self.get_button_after_criteria().click()

    def get_search_description(self) -> WebElement:
        return self.driver.find_element(By.ID, 'description')

    def get_search_results(self) -> List[ProductInfo]:
        """Метод, который возвращает список моделей ProductInfo,
        в том порядке, в како они встречаются на странице."""

        # Получаем все теги <div class="product-layout ...">...</div>
        # со всем содержимым.
        products_tags = self.driver.find_elements(By.CLASS_NAME, 'product-layout')

        # Заводим пустой массив, куда будем накапливать информацию о продуктах.
        products: List[ProductInfo] = []

        # Перебираем все найденные теги с классом product-layout
        for product_div_tag in products_tags:
            # Внутри тега ищем тег <H4> — внутри него будет название продукта.
            name: str = product_div_tag.find_element(By.TAG_NAME, 'h4').text

            # Внутри тега ищем тег с классом price, внутри него будет информация о ценах.
            price_text: str = product_div_tag.find_element(By.CLASS_NAME, 'price').text

            # Создаем объект по модели продукта.
            product = ProductInfo(
                name=name,

                # Корректно выбираем первую цену из строки.
                price=extract_decimal_price(price_text)
            )

            # Добавляем объект продукта в общий массив с продуктами.
            products.append(product)

        return products

    def get_actual_text(self) -> str:
        actual_text = self.driver.find_element(By.ID, 'content').text
        return actual_text
