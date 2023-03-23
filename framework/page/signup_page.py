from framework.common.basepage import BasePage
from selenium.webdriver.common.by import By
import time


class SignUpObj(BasePage):
    """注册页面"""
    # 将变量设为类私有变量,变量名前加两个下划线
    # 将无需暴露的方法或变量设为私有
    __usr_input = (By.ID, 'TANGRAM__PSP_4__userName')
    __phone_input = (By.ID, 'TANGRAM__PSP_4__phone')
    __pwd_input = (By.ID, 'TANGRAM__PSP_4__password')
    __code_input = (By.ID, 'TANGRAM__PSP_4__verifyCode')
    __signup_button = (By.ID, 'TANGRAM__PSP_4__submit')
    __ass_text = (By.CLASS_NAME, 'pwd-strength-detail')
    __cancel_button = (By.ID, 'TANGRAM__PSP_30__confirm_cancel')

    def do_signup_fail(self, usr, phone, pwd):
        """
        注册失败操作
        :param usr: 用户名
        :param phone: 手机号
        :param pwd: 密码
        :return: 校验文本
        """
        self.logger.info("【===开始注册操作===】")
        self.wait_eleVisible(self.__usr_input, screenMark='等待用户名输入框')
        self.clean_input(self.__usr_input, screenMark='清空用户名输入框')
        self.input_text(self.__usr_input, usr, screenMark='输入用户名')

        self.wait_eleVisible(self.__phone_input, screenMark='等待手机号输入框')
        self.clean_input(self.__phone_input, screenMark='清空手机号输入框')
        self.input_text(self.__phone_input, phone, screenMark='输入手机号')

        self.wait_eleVisible(self.__pwd_input, screenMark='等待密码输入框')
        self.clean_input(self.__pwd_input, screenMark='清空密码输入框')
        self.input_text(self.__pwd_input, pwd, screenMark='输入密码')

        self.click_element(self.__code_input, screenMark='点击注册输入框')
        msg = self.get_text(self.__ass_text, screenMark='获取断言文本')
        time.sleep(1)
        self.logger.info("【===结束注册操作===】")
        return msg


