from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from framework.common.driver import Browser
from framework.common.logger import logger
from datetime import datetime
import os
import time


class BasePage:
    """此类封装所有操作，所有页面继承该类"""

    def __init__(self, dr):
        self.driver = dr
        self.logger = logger

    def wait_eleVisible(self, loc, timeout=30, poll_frequency=0.5, screenMark=None):
        """
        等待元素可见
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param screenMark:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return:None
        """
        self.logger.info(f'等待"{screenMark}"元素,定位方式:{loc}')
        try:
            start = datetime.now()
            WebDriverWait(self.driver, timeout, poll_frequency).until(ec.visibility_of_element_located(loc))
            end = datetime.now()
            self.logger.info(f'等待"{screenMark}"时长:{end - start}')
        except TimeoutException:
            self.logger.exception(f'等待"{screenMark}"元素失败,定位方式:{loc}')
            # 截图
            self.save_webImgs(f"等待元素[{screenMark}]出现异常")
            raise

    def find_element(self, loc, screenMark=None):
        """查找单个元素"""
        self.logger.info(f'查找"{screenMark}"元素，元素定位:{loc}')
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            print('按钮未找到!')

    def find_elements(self):
        """查找多个元素"""
        pass

    def click_ele(self):
        """点击元素"""
        pass

    def input_text(self, loc, text, screenMark=None):
        """输入框输入文本"""
        ele = self.find_element(loc, screenMark)
        self.logger.info(f'在"{screenMark}"输入"{text}",元素定位:{loc}')
        try:
            ele.send_keys(text)
        except:
            print('输入失败')

    def clean_input(self):
        """清空输入框"""
        pass

    def save_webImgs(self, screenMark=None):
        """
        截图保存目录
        :param screenMark: filepath = 指图片保存目录/screenMark(页面功能名称)_当前时间到秒.png
        :return:
        """
        # 拼接日志文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        screenshot_path = os.path.join(os.path.dirname(cur_path), f'Screenshots\\{now_date}')
        if not os.path.exists(screenshot_path):
            os.mkdir(screenshot_path)
        # 当前时间
        dateNow = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        # 路径
        filePath = '{}\\{}_{}.png'.format(screenshot_path, screenMark, dateNow)
        try:
            self.driver.save_screenshot(filePath)
            self.logger.info(f"截屏成功,图片路径为{filePath}")
        except:
            self.logger.exception('截屏失败!')

