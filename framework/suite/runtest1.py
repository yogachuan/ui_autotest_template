from framework.common.driver import Browser
from framework.case.test_login1 import LoginTest


class Run:
    def __prepare(self):
        self.dr = Browser.get_webdriver()

    def run_test(self):
        LoginTest(self.dr).main_test()

    def __finish(self):
        self.dr.quit()

    def main_test(self):
        self.__prepare()
        
        self.run_test()
        self.__finish()


if __name__ == '__main__':
    run = Run()
    run.main_test()

