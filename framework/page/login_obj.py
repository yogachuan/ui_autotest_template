import time

from framework.common.basepage import BasePage
from selenium.webdriver.common.by import By
from framework.common.driver import Browser
import time


class LoginObj(BasePage):
    """登录页面"""

    search_input = (By.ID, 'kw')

    def do_login(self, keyw):
        self.logger.info("【===开始登录操作===】")
        self.wait_eleVisible(self.search_input, screenMark='等待关键字输入框')
        self.input_text(self.search_input, keyw, screenMark='输入关键字')
        time.sleep(2)

