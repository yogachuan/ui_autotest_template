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
            self.logger.exception(f'查找"{screenMark}"元素失败,定位方式:{loc}')
            # 截图
            self.save_webImgs(f"查找元素[{screenMark}]异常")
            raise

    def find_elements(self, loc, screenMark=None):
        """查找多个元素"""
        self.logger.info(f'查找"{screenMark}"元素集,定位方式:{loc}')
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            self.logger.exception(f'查找"{screenMark}"元素集失败,定位方式:{loc}')
            # 截图
            self.save_webImgs(f"查找元素集[{screenMark}]异常")
            raise

    def click_element(self, loc, screenMark=None):
        """点击元素"""
        ele = self.find_element(loc, screenMark)
        self.logger.info(f'点击"{screenMark}",元素定位:{loc}')
        try:
            ele.click()
        except:
            self.logger.exception(f'"{screenMark}"点击失败')
            # 截图
            self.save_webImgs(f"[{screenMark}]点击异常")
            raise

    def input_text(self, loc, text, screenMark=None):
        """输入框输入文本"""
        ele = self.find_element(loc, screenMark)
        self.logger.info(f'在"{screenMark}"输入"{text}",元素定位:{loc}')
        try:
            ele.send_keys(text)
        except:
            self.logger.exception(f'"{screenMark}"输入操作失败!')
            # 截图
            self.save_webImgs(f"[{screenMark}]输入异常")
            raise

    def clean_input(self, loc, screenMark=None):
        """清空输入框"""
        ele = self.find_element(loc, screenMark)
        # 清除操作
        self.logger.info(f'清除"{screenMark}",元素定位:{loc}')
        try:
            ele.clear()
        except:
            self.logger.exception(f'"{screenMark}"清除操作失败')
            # 截图
            self.save_webImgs(f"[{screenMark}]清除异常")
            raise

    def get_text(self, loc, screenMark=None):
        """获取文本内容"""
        # 先查找元素在获取文本内容
        ele = self.find_element(loc, screenMark)
        # 获取文本
        self.logger.info(f'获取"{screenMark}"元素文本内容，元素定位:{loc}')
        try:
            text = ele.text
            self.logger.info(f'获取"{screenMark}"元素文本内容为"{text}",元素定位:{loc}')
            return text
        except:
            self.logger.exception(f'获取"{screenMark}"元素文本内容失败,元素定位:{loc}')
            # 截图
            self.save_webImgs(f"获取[{screenMark}]文本内容异常")
            raise

    def refresh(self, screenMark=None):
        """刷新页面"""
        self.logger.info(f'刷新{screenMark}')
        self.driver.refresh()

    def save_webImgs(self, screenMark=None):
        """
        截图保存目录
        :param screenMark: filepath = 指图片保存目录/screenMark(页面功能名称)_当前时间到秒.png
        :return:
        """
        # 拼接截图文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        screenshot_path = os.path.join(os.path.dirname(cur_path), f'screenshots')
        if not os.path.exists(screenshot_path):
            os.mkdir(screenshot_path)

        # 日期文件夹
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data_screenshot_path = os.path.join(os.path.dirname(cur_path), f'screenshots/{now_date}')
        if not os.path.exists(data_screenshot_path):
            os.mkdir(data_screenshot_path)

        # 当前时间
        dateNow = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        # 路径
        filePath = '{}/{}_{}.png'.format(data_screenshot_path, screenMark, dateNow)
        try:
            self.driver.save_screenshot(filePath)
            self.logger.info(f"截屏成功,图片路径为{filePath}")
        except:
            self.logger.exception('截屏失败!')
