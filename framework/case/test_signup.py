import time
from framework.page.signup_page import SignUpObj
import unittest
from framework.common.driver import Browser
from framework.common.logger import logger
from selenium.webdriver.common.by import By


class SignUpTest(unittest.TestCase):
    """登录测试"""

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("class setup content")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("Class teardown content")

    def setUp(self) -> None:
        logger.info("function setup content")
        self.dr = Browser.get_webdriver()
        self.signup_obj = SignUpObj(self.dr)

    def tearDown(self) -> None:
        logger.info("function teardown content")
        self.dr.quit()

    def test_login(self):
        self.signup_obj.do_signup('yoga', '13292679672', 'y2571682')
        time.sleep(3)
        loc = (By.CLASS_NAME, 'pass-confirmContent-msg')
        res = self.signup_obj.get_text(loc)
        print(res)
        self.assertIn('手机已sdfsdjh注册', res)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SignUpTest())
    runner = unittest.TextTestRunner
    test_res = runner.run(suite)


