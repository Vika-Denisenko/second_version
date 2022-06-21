import unittest
from typing import List

from pageobject.comparison_page import ComparisonPage
from pageobject.product_page import ProductPage, ProductInfo
from webdriver_factory import WebDriverFactory


class CompareTest(unittest.TestCase):
    expected_product_apple = ProductInfo(
        name='Apple Cinema 30"',
        url='42'
    )
    expected_product_samsung = ProductInfo(
        name='Samsung SyncMaster 941BW',
        url='33'
    )
    expected_product_list: List[ProductInfo] = [expected_product_apple, expected_product_samsung]

    def setUp(self) -> None:
        self.driver = WebDriverFactory.get_driver()

    def tearDown(self) -> None:
        self.driver.close()

    def test_compare(self):
        '''Проверяем успешно ли добавлены продукты к сравнению'''
        for product in self.expected_product_list:
            product_page = ProductPage(self.driver, product.url)
            product_page.open()
            product_page.compare()

            self.assertEqual(
                f'Success: You have added {product.name} to your product comparison!',
                product_page.get_alert_text().split('\n')[0]
            )
        '''Проверяем наличие продуктов на странице сравнения'''
        product_page.open_comparison_page()
        comparison_page = ComparisonPage(self.driver)
        comparison_page.open()
        # comparison_page = product_page.open_comparison_page()
        expected_names: List[str] = [product.name for product in self.expected_product_list]
        actual_names: List[str] = comparison_page.get_name_in_comparison()

        self.assertEqual(
            expected_names,
            actual_names
        )

        '''Проверяем успешно ли удалены продукты из сравнения'''
        for i in range(len(expected_names)):
            comparison_page.remove()

        self.assertEqual(
            'You have not chosen any products to compare.',
            comparison_page.get_alert_text().split('\n×')[0]
        )
