
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located, any_of, \
    text_to_be_present_in_element
from selenium.webdriver.support.wait import WebDriverWait

from extract_price import extract_decimal_price
from model import ProductInfo
from pageobject.base_page import BasePage



class SearchPage(BasePage):
    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/search'

    def get_search_field(self) -> WebElement:
        '''Получаем input основное поле поиска'''
        search_field: WebElement = self.driver.find_element(By.CLASS_NAME, 'input-lg')
        return search_field

    def get_search_criteria(self) -> WebElement:
        '''Получаем поле search_criteria'''
        return self.driver.find_element(By.ID, 'input-search')

    def get_search_checkbox(self) -> WebElement:
        '''Получаем чекбокс после поля с критерием'''
        return self.driver.find_element(By.ID, 'description')

    def enter_word(self, word: str):
        '''Вводим слово в поле поиска'''
        self.get_search_field().send_keys(word)

    def clear_search(self):
        '''Очищаем поле поиска'''
        self.get_search_field().clear()

    def enter_word_in_field_criteria(self, word: str):
        '''Вводим слово в поле критерия'''
        self.get_search_criteria().send_keys(word)

    def clear_field_criteria(self):
        '''Очищаем поле критерия'''
        self.get_search_criteria().clear()

    def click_checkbox(self):
        '''Кликаем по чекбоксу'''
        self.get_search_checkbox().click()

    def get_search_button(self) -> WebElement:
        '''Находим кнопку поиска с лупой'''
        return self.driver.find_element(By.CLASS_NAME, 'btn-default')

    def get_button_after_criteria(self) -> WebElement:
        '''Находим кнопку поиска Search'''
        return self.driver.find_element(By.ID, 'button-search')

    def search_default(self):
        '''Кликаем по кнопке поиска с лупой'''
        self.get_search_button().click()
        WebDriverWait(self.driver, timeout=3).until(
            any_of(visibility_of_all_elements_located((By.CLASS_NAME, 'product-layout')),
                   text_to_be_present_in_element((By.ID, 'content'), self.get_actual_text()))
        )

    def search_primary(self):
        '''Кликаем по основной кнопке поиска'''
        self.get_button_after_criteria().click()

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
        '''Считываем текст после поиска несуществующего товара'''
        content: WebElement = self.driver.find_element(By.ID, 'content')
        actual_text: str = content.find_elements(By.TAG_NAME, 'p')[-1].text
        return actual_text
