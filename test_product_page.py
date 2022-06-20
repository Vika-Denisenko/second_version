import unittest
from decimal import Decimal

from pageobject.product_page import ProductPage, ProductInfo
from webdriver_factory import WebDriverFactory


class ProductPageTest(unittest.TestCase):
    expected_product = ProductInfo(
        name='Apple Cinema 30"',
        brand='Brand: Apple',
        product_code='Product Code: Product 15',
        price=Decimal('110.00'),
        description='The 30-inch Apple Cinema HD Display delivers an amazing 2560 x 1600 pixel resolution',
        url='42'

    )

    def setUp(self) -> None:
        self.driver = WebDriverFactory.get_driver()
        self.product_page = ProductPage(self.driver, self.expected_product.url)
        self.product_page.open()

    def tearDown(self) -> None:
        self.driver.close()

    def test_product(self):
        actual_product = self.product_page.get_product_info()

        self.assertEqual(
            self.expected_product.name,
            actual_product.name
        )

        self.assertEqual(
            self.expected_product.brand,
            actual_product.brand
        )

        self.assertEqual(
            self.expected_product.product_code,
            actual_product.product_code
        )

        self.assertEqual(
            self.expected_product.price,
            actual_product.price
        )

        self.assertIn(
            self.expected_product.description,
            actual_product.description
        )

    '''expected_product2 = ProductInfo(

        name='HP LP3065',
        brand='Brand: Hewlett-Packard',
        product_code='Product Code: Product 21',
        price='122.00',
        description='Stop your co-workers in their tracks with the stunning new 30-inch diagonal HP LP3065',
        url='47'
    )
    expected_product3 = ProductInfo(

        name='Samsung SyncMaster 941BW',
        brand='',
        product_code='Product Code: Product 6',
        price='242.00',
        description='Imagine the advantages of going big without slowing down',
        url='33'
    )'''
