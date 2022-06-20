import unittest
from typing import List

from pageobject.compare_page import ComparePage
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
        '''Проверяем успешно ли добавлен продукт к сравнению'''
        for product in self.expected_product_list:
            product_page = ProductPage(self.driver, product.url)
            product_page.open()
            product_page.compare()

            self.assertEqual(
                f'Success: You have added {product.name} to your product comparison!',
                product_page.get_alert_text().split('\n')[0]
            )

        compare_page = ComparePage(self.driver)
        compare_page.open()
        expected_names:List[str]=[product.name for product in self.expected_product_list]
        actual_names:List[str]=compare_page.get_name_in_comparison()

        self.assertEqual(
                    expected_names,
                    actual_names
                )

        '''Проверяем успешно ли удалены продукты из сравнения'''
        for i in range(len(expected_names)):
            compare_page.remove()

        self.assertEqual(
            'You have not chosen any products to compare.',
            compare_page.get_alert_text().split('\n×')[0]
        )
