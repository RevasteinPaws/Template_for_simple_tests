import allure
from config.links import Links
from base.base_page import BasePage
from base.base_class import BaseClass


class PersonalPage(BasePage, BaseClass):
    page_url = Links.PERSONAL_PAGE

    first_name_filed = "//input[@placeholder='First Name']"
    save_personal_fields_button = "(//button[@type='submit'])[1]"

    @allure.step("Change name'")
    def change_name(self, new_name):
        with allure.step(f"Change name on '{new_name}'"):
            first_name_field = self.is_clickable("xpath", self.first_name_filed)
            first_name_field.clear()
            first_name_field.send_keys(new_name)

    @allure.step("Save changes")
    def save_changes(self):
        self.is_clickable("xpath", self.save_personal_fields_button).click()
