import allure
from config.links import Links
from base.base_page import BasePage
from base.base_class import BaseClass


class LoginPage(BasePage, BaseClass):
    page_url = Links.LOGIN_PAGE

    username_field = "//input[@name='username']"
    password_field = "//input[@name='password']"
    submit_button = "//button[@type='submit']"

    @allure.step("Enter login")
    def enter_login(self, login):
        self.is_clickable("xpath", self.username_field).send_keys(login)

    @allure.step("Enter password")
    def enter_password(self, password):
        self.is_clickable("xpath", self.password_field).send_keys(password)

    @allure.step("Click submit button")
    def click_submit_button(self):
        self.is_clickable("xpath", self.submit_button).click()
