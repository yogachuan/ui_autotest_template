from framework.page.login_obj import LoginObj
import unittest
from framework.common.driver import Browser


class LoginTest(unittest.TestCase):
    """登录测试"""

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.dr = Browser.get_webdriver()
        self.login_obj = LoginObj(self.dr)

    def tearDown(self) -> None:
        self.dr.quit()

    def test_login(self):
        pass
