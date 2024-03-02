import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ex_con


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 1)

    def open(self):
        with allure.step(f"Open {self.page_url} page"):
            self.driver.get(self.page_url)

    def is_opened(self):
        with allure.step(f"Page {self.page_url} is opened."):
            self.wait.until(ex_con.url_to_be(self.page_url))

    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG
        )
