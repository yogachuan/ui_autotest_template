from framework.page.signup_page import SignUpObj
import unittest
from framework.common.driver import Browser
from framework.common.logger import logger
from ddt import ddt, data, unpack
from framework.common.read_data import read_data
import os


@ddt
class SignUpTest(unittest.TestCase):
    """登录测试"""
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    userdata = read_data.load_excel(os.path.join(base_path, "data", "signup.xlsx"))
    logger.info("add_user_data is {}".format(userdata))

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("class setup content")
        cls.dr = Browser.get_webdriver()

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("Class teardown content")
        cls.dr.quit()

    def setUp(self) -> None:
        logger.info("function setup content")
        self.signup_obj = SignUpObj(self.dr)

    def tearDown(self) -> None:
        logger.info("function teardown content")
        # self.dr.quit()

    @data(*userdata)
    @unpack
    def test_signup(self, username, phone, pwd, ass):
        res = self.signup_obj.do_signup(username, phone, pwd)
        self.assertTrue(res)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SignUpTest())
    runner = unittest.TextTestRunner
    test_res = runner.run(suite)
