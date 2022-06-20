from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:

    '''Родительский класс PageObject'''

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_url(self) -> str:
        '''Обязательно реализовать в дочерних классах'''
        raise NotImplementedError

    def open(self):
        '''Открыть страницу логина'''
        self.driver.get(self.get_url())
