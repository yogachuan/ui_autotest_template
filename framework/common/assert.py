from selenium.webdriver.common.by import By
from framework.common.driver import Browser
from framework.common.basepage import BasePage


class MyAssert(BasePage):
    def __init__(self, dr):
        super().__init__(dr)
