from selenium.webdriver.common.by import By
from framework.common.driver import Browser


class MyAssert:
    def __init__(self):
        self.driver = Browser.get_webdriver()

    def element_present(self, locate):
        try:
            self.driver.find_element(By.XPATH, locate).is_displayed()
        except Exception:
            return False
        return True
