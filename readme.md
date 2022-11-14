# python+selenium+unittest+ddt+HTMLTestRunner(以注册百度账号异常为例)

## 一、框架组成

- driver
  放浏览器驱动

- framework

  - common
    公共层放公用的模块

  - config
    配置文件层

  - page
    页面对象层

  - case
    测试用例层

  - data
    测试数据层

  - suite
    测试套件层

  - logs
    输出日志

  - screenshots
    失败截屏

  - report
    输出测试报告

## 二、搭建步骤

### 1、在config层中创建配置文件json格式

setting.json

```json
{

	"host": "https://www.baidu.com",
  "browser_type": "chrome"

}
//浏览器类型chrome、firefox、edge
```

### 2、在common层中写读文件方法

read_data.py

```python
# -*- coding: utf-8 -*-
import yaml
import xlrd
import json
from configparser import ConfigParser
from framework.common.logger import logger


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ReadFileData:
    def __init__(self):
        pass

    @staticmethod
    def load_yaml(file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='gbk') as f:
            data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    @staticmethod
    def load_json(file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='gbk') as f:
            data = json.load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    @staticmethod
    def load_ini(file_path):
        logger.info("加载 {} 文件......".format(file_path))
        config_parser = MyConfigParser()
        config_parser.read(file_path, encoding="UTF-8")
        data = dict(config_parser._sections)
        print("读到数据 ==>>  {} ".format(data))
        return data
      
    @staticmethod
    def load_excel(file_path):
        file = xlrd.open_workbook(file_path)
        sheet = file.sheet_by_index(0)
        data = []
        for row in range(1, sheet.nrows):
            lines = []
            for col in range(1, sheet.ncols):
                value = sheet.cell(row, col).value
                if not isinstance(value, str):
                    # 单元格内容不是字符串类型
                    value = str(int(value))
                lines.append(value)
            data.append(lines)
        return data

read_data = ReadFileData()

if __name__ == '__main__':
    import os

    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    userdata = ReadFileData.load_yaml(os.path.join(base_path, "data", "login_data.yml"))

```

### 3、在common层中写入浏览器方法

单例模式，并创建login的类方法，在浏览器打开后直接登录（根据用例判定，如果是登录测试用例，则不执行login方法）

driver.py

```python
import time
from framework.common.read_data import read_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.common.by import By
from framework.common.logger import logger

base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(base_path, "config", "setting.json")
browser_data = read_data.load_yaml(data_file_path)
browser_type = browser_data['browser_type']
host = browser_data['host']
username = browser_data['username']
pwd = browser_data['pwd']
# print(browser_type)


class Browser:
    """浏览器类,单例模式"""
    driver = None  # 将driver定义为类级变量，则该driver只会保存在类的内存

    def __init__(self):
        pass

    @classmethod  # 将该方法定义为类级方法，则直接调用类名即可，不需要实例化
    def get_webdriver(cls, case='notLogin'):
        if cls.driver is None:
            if browser_type == 'chrome':
                s = Service('../../driver/chromedriver')
                # opt = webdriver.ChromeOptions()
                # opt.add_argument(r"--user-data-dir=C:\Users\1\AppData\Local\Google\Chrome\User Data\Default")  # 使浏览器加载本地缓存
                # cls.driver = webdriver.Chrome(service=s,options=opt)  # 创建浏览器
                cls.driver = webdriver.Chrome(service=s)  # 创建浏览器
                cls.driver.maximize_window()  # 最大化
                cls.driver.implicitly_wait(10)
            elif browser_type == 'firefox':
                pass
            elif browser_type == 'edge':
                pass
            else:
                print('浏览器类型不支持')
                logger.info("浏览器类型不支持")
           
            if case is 'notLogin':
                # 不是登录测试用例则需进行登录操作
                Browser.login()
                time.sleep(3)
            else:
                # 登录测试用例需执行
                cls.driver.get(host)
            logger.info(f"打开链接: {host}...")
            logger.info("WebDriver 初始化完成！")
        return cls.driver

    @classmethod
    def login(cls):
        cls.driver.get(host)
        cls.driver.find_element(By.ID, '').send_keys(username)
        cls.driver.find_element(By.ID, '').send_keys(pwd)
        cls.driver.find_element(By.ID, '').click()
```

### 4、在common层中创建写日志方法

logger.py（细读）

```python
# -*- coding: utf-8 -*-

import logging
import os
import time


class Logger(object):

    def __init__(self, logger_name=None):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        """
        # 日志文件夹，如果不存在则自动创建
        cur_path = os.path.dirname(os.path.realpath(__file__))
        log_path = os.path.join(os.path.dirname(cur_path), f'logs')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # log 日期文件夹
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        phone_log_path = os.path.join(os.path.dirname(cur_path), f'logs\\{now_date}')
        if not os.path.exists(phone_log_path):
            os.mkdir(phone_log_path)
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        log_name = os.path.join(phone_log_path, f'{now_time}.log')
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s [line:%(lineno)d]: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getLog(self):
        return self.logger
logger = Logger().logger
```

### 5、在common层中封装basepage基类

basepage.py（一些基本操作，查找元素、清空输入、输入、点击、截屏等等，可自行添加）

​	*类初始化时需传入driver*

```python
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

    def save_webImgs(self, screenMark=None):
        """
        截图保存目录
        :param screenMark: filepath = 指图片保存目录/screenMark(页面功能名称)_当前时间到秒.png
        :return:
        """
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
        filePath = '{}\\{}_{}.png'.format(screenshot_path, screenMark, dateNow)
        try:
            self.driver.save_screenshot(filePath)
            self.logger.info(f"截屏成功,图片路径为{filePath}")
        except:
            self.logger.exception('截屏失败!')


```

### 6、在page层中创建页面对象

signup_page.py（继承自basepage），所以在实例化该类时需传入driver。

​	*1、页面对象分为三层：元素定位层、操作层、业务层（业务层方法需要以“do”开头，例如do_signup，业务层需要输入的内容以走形参）*

​	*2、获取结果文本用于校验，将结果文本作为方法的返回（代码最后）*

```python
from framework.common.basepage import BasePage
from selenium.webdriver.common.by import By
import time


class SignUpObj(BasePage):
    """注册页面"""

    usr_input = (By.ID, 'TANGRAM__PSP_4__userName')
    phone_input = (By.ID, 'TANGRAM__PSP_4__phone')
    pwd_input = (By.ID, 'TANGRAM__PSP_4__password')
    signup_button = (By.ID, 'TANGRAM__PSP_4__submit')
    ass_text = (By.CLASS_NAME, 'pass-confirmContent-msg')
    cancel_button = (By.ID, 'TANGRAM__PSP_30__confirm_cancel')

    def do_signup(self, usr, phone, pwd):
        self.logger.info("【===开始注册操作===】")
        time.sleep(3)
        self.wait_eleVisible(self.usr_input, screenMark='等待用户名输入框')
        self.clean_input(self.usr_input, screenMark='清空用户名输入框')
        self.input_text(self.usr_input, usr, screenMark='输入用户名')

        self.wait_eleVisible(self.phone_input, screenMark='等待手机号输入框')
        self.clean_input(self.phone_input, screenMark='清空手机号输入框')
        self.input_text(self.phone_input, phone, screenMark='输入手机号')

        self.wait_eleVisible(self.pwd_input, screenMark='等待密码输入框')
        self.clean_input(self.pwd_input, screenMark='清空密码输入框')
        self.input_text(self.pwd_input, pwd, screenMark='输入密码')

        self.click_element(self.signup_button, screenMark='点击注册按钮')
        time.sleep(2)
        msg = self.get_text(self.ass_text,screenMark='提示框文本')
        self.logger.info(f'获取到结果文本{msg}')
        # self.refresh()
        self.click_element(self.cancel_button, screenMark='点击取消按钮')
        time.sleep(2)
        self.logger.info("【===结束注册操作===】")
        return msg
```

### 7、在case层中创建测试用例

在用例中创建浏览器并实例化page层中的页面对象，实例化时需传入driver

test_signup.py（继承自unittest.TestCase）

​	1.*setUpClass、tearDownClass、setUp、tearDown细读*

​	2.*在setup中调用浏览器（调用时需判断用例是不是登录测试用例），并实例化页面对象，实例化时传入该浏览器*

​			登录用例：

​				*Browser.get_driver(case='Login')*

​			非登录用例：

​				*Browser.get_driver()*

​	3.*test_login，真正执行用例的地方，必须以“test_”开头*

​	4.*使用ddt将输入参数传入*

```python
from ddt import ddt, data, unpack
@ddt
class AAA:
  info = []
  //info为数据列表，data方法可将info列表打散并传入test_aaa方法所需参数中
  @data(*info)
  @unpack()
  def test_aaa(self,a,b,c):
    
```



```python
import time
from framework.page.signup_page import SignUpObj
import unittest
from framework.common.driver import Browser
from framework.common.logger import logger
from selenium.webdriver.common.by import By
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

    @data(*userdata)
    @unpack
    def test_signup(self, username, phone, pwd, ass):
      	//将页面对象方法的返回用于校验
        res = self.signup_obj.do_signup(username, phone, pwd)
        self.assertIn(ass, res)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SignUpTest())
    runner = unittest.TextTestRunner
    test_res = runner.run(suite)
```

