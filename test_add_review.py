import random
import unittest
from random import choice
from string import ascii_letters

from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class AddReviewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = WebDriverFactory.get_driver()
        self.product_url_id = '42'
        self.product_page = ProductPage(self.driver, self.product_url_id)
        self.product_page.open()
        self.product_page.open_review()

    def tearDown(self) -> None:
        self.driver.close()

    def test_reviews_without_rating(self):
        expected_text = 'Warning: Please select a review rating!'
        self.product_page.review()

        self.assertEqual(
            expected_text,
            self.product_page.get_alert_text()
        )

    def test_with_24(self):
        name = 'John'
        rating = random.randrange(5)
        review24_text = ''.join(choice(ascii_letters) for _ in range(24))
        expected_text = 'Warning: Review Text must be between 25 and 1000 characters!'

        self.product_page.rating(rating)
        self.product_page.enter_name(name)
        self.product_page.enter_review(review24_text)
        self.product_page.review()
        self.assertEqual(
            expected_text,
            self.product_page.get_alert_text()

        )

    def test_with_25(self):
        name = 'John'
        rating = random.randrange(5)
        review25 = ''.join(choice(ascii_letters) for _ in range(random.randint(25, 100)))
        expected_text = 'Thank you for your review. It has been submitted to the webmaster for approval.'

        self.product_page.rating(rating)
        self.product_page.enter_name(name)
        self.product_page.enter_review(review25)
        self.product_page.review()
        self.assertEqual(
            expected_text,
            self.product_page.get_alert_text()
        )
