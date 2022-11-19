from framework.page.signup_page import SignUpObj
import unittest
from framework.common.driver import Browser
from ddt import ddt, data, unpack
from framework.common.read_data import read_data
import os
from framework.common.logger import logger


@ddt
class SignUpTest(unittest.TestCase):
    """登录测试"""
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    userdata = read_data.load_excel(os.path.join(base_path, "data", "signup.xlsx"))
    logger.info("signup_data is {}".format(userdata))

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("class setup content")
        cls.dr = Browser.get_webdriver(case='Login')

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("Class teardown content")
        # 不能使用cls.dr.quit(), 需在Browser下封装quit_driver()方法
        # 因为使用cls.dr.quit()后,driver并不等于None,需调用Browser下的quit_driver()方法,重新将driver=None
        Browser.quit_driver()

    def setUp(self) -> None:
        logger.info("function setup content")
        self.signup_obj = SignUpObj(self.dr)

    def tearDown(self) -> None:
        logger.info("function teardown content")

    @data(*userdata)
    @unpack
    def test_signup_fail(self, case, desc, username, phone, pwd, ass):
        logger.info(f'执行测试用例:{case},用例说明:{desc}')
        res = self.signup_obj.do_signup_fail(username, phone, pwd)
        self.assertIn(ass, res)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SignUpTest())
    runner = unittest.TextTestRunner
    test_res = runner.run(suite)
