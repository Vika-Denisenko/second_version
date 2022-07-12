import unittest

from typing import List

from model import ProductInfo
from pageobject.search_page import SearchPage
from webdriver_factory import WebDriverFactory


class SearchPageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = WebDriverFactory.get_driver()
        self.search_page = SearchPage(self.driver)
        self.search_page.open()

    def tearDown(self) -> None:

        self.driver.close()

    def test_search_apple(self):
        expected_product = ProductInfo(name='Apple Cinema 30"',
                                       price=110.00)

        self.search_page.enter_word('apple')
        self.search_page.search_default()
        self.search_page.clear_search()
        actual_product: List[ProductInfo] = self.search_page.get_search_results()

        self.assertEqual(
            expected_product.name,
            actual_product[0].name

        )

        self.assertEqual(
            expected_product.price,
            actual_product[0].price)

    def test_search_sony(self):
        expected_product = ProductInfo(name='Sony VAIO',
                                       price=1202.00)


        self.search_page.enter_word('sony')
        self.search_page.search_default()
        self.search_page.clear_search()

        actual_product: List[ProductInfo] = self.search_page.get_search_results()

        self.assertEqual(
            expected_product.name,
            actual_product[0].name

        )

        self.assertEqual(
            expected_product.price,
            actual_product[0].price)

    def test_search_nokia(self):
        self.search_page.enter_word('nokia')
        self.search_page.search_default()
        self.search_page.clear_search()
        expected_text = 'There is no product that matches the search criteria.'
        self.assertIn(
            expected_text,
            self.search_page.get_actual_text()
        )

    def test_with_search_criteria(self):
        expected_names_list = ['HP LP3065', 'iMac']
        self.search_page.enter_word_in_field_criteria('stunning')
        self.search_page.click_checkbox()
        self.search_page.search_primary()
        self.search_page.clear_field_criteria()
        actual_names_list = [product.name for product in self.search_page.get_search_results()]
        self.assertEqual(
            expected_names_list,
            actual_names_list

        )
