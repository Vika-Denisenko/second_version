from dataclasses import dataclass
from decimal import Decimal

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage


def extract_decimal_price(text: str) -> Decimal:
    """Функция, которая извлекает из строки цену"""
    '''Считываем цену без знака доллара'''
    price_with_sign = text[1:]
    '''Если есть разделяющая запятая в цифре, убираем ее'''
    price_without_punctuation = price_with_sign.replace(",", "")

    return Decimal(price_without_punctuation)


@dataclass
class ProductInfo:
    name: str
    brand: str = ''
    product_code: str = ''
    price: Decimal = 0
    description: str = ''
    '''Убрать url and qty'''
    url: str = ''
    qty: int = 0


class ProductPage(BasePage):
    def __init__(self, driver: WebDriver, product_id: str):
        super().__init__(driver)
        self.product_id = product_id

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/product&product_id=' + self.product_id

    def get_name(self) -> str:
        '''Получаем название продукта'''
        name: WebElement = self.driver.find_element(By.TAG_NAME, 'h1')
        return name.text

    def get_brand_and_product_code(self) -> WebElement:
        '''Получаем вебэлемент с  брэндом и продукт кодом'''
        return self.driver.find_elements(By.CLASS_NAME, 'col-sm-4')[1]

    def get_brand(self) -> str:
        '''Получаем текс бренда'''
        brand: WebElement = self.get_brand_and_product_code().find_elements(By.TAG_NAME, 'li')[0]
        return brand.text

    def get_product_code(self) -> str:
        '''Получаем текст с продукт кодом'''
        product_code: WebElement = self.get_brand_and_product_code().find_elements(By.TAG_NAME, 'li')[1]
        return product_code.text

    def get_price(self) -> str:
        '''Получаем строку с ценой'''
        price_with_punctuation: str = self.driver.find_elements(By.TAG_NAME, 'h2')[1].text
        return price_with_punctuation

    def get_description(self) -> str:
        '''Получаем строку описание продукта'''
        text_description: WebElement = self.driver.find_element(By.ID, 'tab-description')
        return text_description.text

    def get_product_info(self):
        '''Собираем все данные о продукте'''
        product = ProductInfo(
            name=self.get_name(),
            brand=self.get_brand(),
            product_code=self.get_product_code(),
            price=extract_decimal_price(self.get_price()),
            description=self.get_description()
        )

        return product

    def get_tab_review(self) -> WebElement:
        '''Находим вкладку отзывов'''
        return self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Reviews')

    def open_review(self):
        '''Открываем вкладку отзывов'''
        self.get_tab_review().click()
        '''WebDriverWait(self.driver, timeout=5).until(
            text_to_be_present_in_element((By.ID, 'review'), 'There are no reviews for this product.')
        )'''

    def get_button_review(self) -> WebElement:
        '''Находим кнопку Continue'''
        return self.driver.find_element(By.ID, 'button-review')

    def review(self):
        '''Нажимаем на кнопку Continue'''
        self.get_button_review().click()
        WebDriverWait(self.driver, timeout=5).until(
            visibility_of_element_located((By.CLASS_NAME, 'alert-dismissible'))
        )

    def get_alert_text(self) -> str:
        '''Читаем текст предупреждения'''
        warning_text: WebElement = self.driver.find_element(By.CLASS_NAME, 'alert-dismissible')
        return warning_text.text

    def get_name_field(self) -> WebElement:
        '''Находим поле имя во вкладке отзывов'''
        return self.driver.find_element(By.ID, 'input-name')

    def get_review_field(self) -> WebElement:
        '''Находим поле с Your Review'''
        return self.driver.find_element(By.ID, 'input-review')

    def get_radio_button(self) -> WebElement:
        '''Находим радиокнопки с рейтингом'''
        return self.driver.find_elements(By.NAME, 'rating')

    def rating(self, rating):
        '''Выбираем любой рейтинг'''
        self.get_radio_button()[rating].click()

    def enter_name(self, name: str):
        '''На вкладке отзывов вводим имя'''
        self.get_name_field().send_keys(name)

    def enter_review(self, review: str):
        '''В поле отзывов вводим отзыв'''
        self.get_review_field().send_keys(review)

    def compare_but(self)-> WebElement:
        '''Находим добавить в сравнение '''
        return self.driver.find_element(By.CSS_SELECTOR, '[data-original-title="Compare this Product"]')

    def compare(self):
        '''Кликаем по кнопке добавить в сравнение'''
        self.compare_but().click()
        WebDriverWait(self.driver, timeout=5).until(
            visibility_of_element_located((By.CLASS_NAME, 'alert-dismissible'))
        )

    def open_comparison_page(self):
        '''Открываем страницу сравнения'''
        '''я тут не разобралась как это сделать лучше'''
        self.driver.find_element(By.LINK_TEXT, 'product comparison').click()

    def get_field_quantity(self) -> WebElement:
        '''Находим поле с количеством'''
        return self.driver.find_element(By.ID, 'input-quantity')

    def clear_qty(self):
        '''Очищаем поле количество'''
        self.get_field_quantity().clear()

    def send_qty(self, quantity):
        '''Отправляем нужное нам количество'''
        self.clear_qty()
        self.get_field_quantity().send_keys(quantity)

    def get_button_card(self) -> WebElement:
        '''Находим кнопку добавить в корзину'''
        return self.driver.find_element(By.ID, 'button-cart')

    def cart(self):
        '''Кликаем по кнопке добавить в корзину'''
        self.get_button_card().click()
        WebDriverWait(self.driver, timeout=5).until(
            visibility_of_element_located((By.CLASS_NAME, 'alert-dismissible')))
