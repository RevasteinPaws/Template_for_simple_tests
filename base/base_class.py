from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ex_con


class BaseClass:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, 0.2)

    @staticmethod
    def __get_selenium_by(find_by: str) -> str:
        find_by = find_by.lower()
        locating = {'css': By.CSS_SELECTOR,
                    'xpath': By.XPATH,
                    'class_name': By.CLASS_NAME,
                    'id': By.ID,
                    'link_text': By.LINK_TEXT,
                    'name': By.NAME,
                    'partial_link_text': By.PARTIAL_LINK_TEXT,
                    'tag_name': By.TAG_NAME}
        return locating[find_by]

    def is_visible(self, find_by: str, locator: str, error_message: str = None) -> WebElement:
        return self.wait.until(
            ex_con.visibility_of_element_located((self.__get_selenium_by(find_by), locator)),
            error_message)

    def are_visible(self, find_by: str, locator: str, error_message: str = None) -> List[WebElement]:
        return self.wait.until(
            ex_con.visibility_of_all_elements_located((self.__get_selenium_by(find_by), locator)),
            error_message)

    def is_present(self, find_by: str, locator: str, error_message: str = None) -> WebElement:
        return self.wait.until(
            ex_con.presence_of_element_located((self.__get_selenium_by(find_by), locator)),
            error_message)

    def is_not_present(self, find_by: str, locator: str, error_message: str = None) -> WebElement:
        return self.wait.until(
            ex_con.invisibility_of_element_located((self.__get_selenium_by(find_by), locator)),
            error_message)

    def are_present(self, find_by: str, locator: str, error_message: str = None) -> List[WebElement]:
        return self.wait.until(
            ex_con.presence_of_all_elements_located((self.__get_selenium_by(find_by), locator)),
            error_message)

    def is_clickable(self, find_by: str, locator: str, error_message: str = None) -> WebElement:
        return self.wait.until(
            ex_con.element_to_be_clickable((self.__get_selenium_by(find_by), locator)),
            error_message)

    def is_invisible(self, find_by: str, locator: str, error_message: str = None) -> WebElement:
        return self.wait.until(
            ex_con.invisibility_of_element_located((self.__get_selenium_by(find_by), locator)),
            error_message)
