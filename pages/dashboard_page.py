import allure
from config.links import Links
from base.base_page import BasePage
from base.base_class import BaseClass


class DashboardPage(BasePage, BaseClass):
    page_url = Links.DASHBOARD_PAGE

    my_info_button = "//span[text()='My Info']"
    admin_button = "//span[text()='Admin']"

    @allure.step("Click on 'My Info' button'")
    def click_my_info_button(self):
        self.is_clickable("xpath", self.my_info_button).click()

    @allure.step("Click on 'Admin' button")
    def click_admin_button(self):
        self.is_clickable("xpath", self.admin_button).click()
