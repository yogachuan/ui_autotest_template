from framework.common.basepage import BasePage
from selenium.webdriver.common.by import By
import time


class SignUpObj(BasePage):
    """注册页面"""

    usr_input = (By.ID, 'TANGRAM__PSP_4__userName')
    phone_input = (By.ID, 'TANGRAM__PSP_4__phone')
    pwd_input = (By.ID, 'TANGRAM__PSP_4__password')
    code_input = (By.ID, 'TANGRAM__PSP_4__verifyCode')
    signup_button = (By.ID, 'TANGRAM__PSP_4__submit')
    ass_text = (By.CLASS_NAME, 'pwd-strength-detail')
    cancel_button = (By.ID, 'TANGRAM__PSP_30__confirm_cancel')

    def do_signup_fail(self, usr, phone, pwd):
        self.logger.info("【===开始注册操作===】")
        self.wait_eleVisible(self.usr_input, screenMark='等待用户名输入框')
        self.clean_input(self.usr_input, screenMark='清空用户名输入框')
        self.input_text(self.usr_input, usr, screenMark='输入用户名')

        self.wait_eleVisible(self.phone_input, screenMark='等待手机号输入框')
        self.clean_input(self.phone_input, screenMark='清空手机号输入框')
        self.input_text(self.phone_input, phone, screenMark='输入手机号')

        self.wait_eleVisible(self.pwd_input, screenMark='等待密码输入框')
        self.clean_input(self.pwd_input, screenMark='清空密码输入框')
        self.input_text(self.pwd_input, pwd, screenMark='输入密码')

        self.click_element(self.code_input, screenMark='点击注册输入框')
        msg = self.get_text(self.ass_text, screenMark='获取断言文本')
        time.sleep(1)
        self.logger.info("【===结束注册操作===】")
        return msg


