import unittest
from decimal import Decimal
from typing import List

from model import ProductInfo
from pageobject.product_page import ProductPage
from pageobject.shopping_cart_page import ShoppingCartPage
from webdriver_factory import WebDriverFactory


class ShoppingCartTest(unittest.TestCase):
    expected_product_samsung = ProductInfo(
        name='Samsung SyncMaster 941BW',
        price='242.00',
        url='33',
        qty=2
    )
    expected_product_HP = ProductInfo(
        name='HP LP3065',
        price='122.00',
        url='47',
        qty=1
    )
    expected_products_list: List[ProductInfo] = [expected_product_samsung, expected_product_HP]

    def setUp(self) -> None:
        self.driver = WebDriverFactory.get_driver()

    def tearDown(self) -> None:
        self.driver.close()

    def test_shopping_cart(self):
        '''Проверяем успешное добавление товара в корзину'''
        for i in range(len(self.expected_products_list)):
            product_page = ProductPage(self.driver, self.expected_products_list[i].url)
            product_page.open()
            product_page.send_qty(self.expected_products_list[i].qty)
            product_page.cart()
            self.assertEqual(
                f'Success: You have added {self.expected_products_list[i].name} to your shopping cart!',
                product_page.get_alert_text().split('\n×')[0]
            )
        '''Проверяем наличие добавленных товаров в корзине и сумму'''
        shopping_cart_page = ShoppingCartPage(self.driver)
        shopping_cart_page.open()

        expected_name_list: List[str] = [product.name for product in self.expected_products_list]
        actual_name_list: List[str] = shopping_cart_page.get_name_list()
        self.assertEqual(
            expected_name_list,
            actual_name_list

        )

        expected_total_sum: Decimal = Decimal(606.00)
        actual_total_sum = shopping_cart_page.total_sum()

        self.assertEqual(
            expected_total_sum,
            actual_total_sum
        )

        for _ in range(len(self.expected_products_list)):
            shopping_cart_page.remove_cart()

        self.assertEqual(
            'Your shopping cart is empty!',
            shopping_cart_page.get_content_text()
        )
