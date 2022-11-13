from framework.page.signup_page import SignUpObj


class LoginTest:
    """登录测试"""
    def __init__(self, dr):
        self.login_obj = SignUpObj(dr)

    def __test_login(self):
        self.login_obj.do_login("yujiachuan")

    def main_test(self):
        self.__test_login()


if __name__ == "__main__":
    login = LoginTest()
    login.test_login()
