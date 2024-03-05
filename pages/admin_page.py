import allure
from config.links import Links
from base.base_page import BasePage
from base.base_class import BaseClass


class AdminPage(BasePage, BaseClass):

    page_url = Links.ADMIN_PAGE
