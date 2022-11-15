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
            if case == 'notLogin':
                # 不是登录测试用例则需进行登录操作
                Browser.login()
            else:
                # 登录测试用例需执行
                cls.driver.get(host)
                logger.info(f"打开链接: {host}...")
                logger.info("WebDriver 初始化完成！")
        return cls.driver

    @classmethod
    def login(cls):
        logger.info(f'非登录类测试用例需先进行登录操作')
        cls.driver.get(host)
        logger.info(f"打开链接: {host}...")
        logger.info("WebDriver 初始化完成！")
        cls.driver.find_element(By.ID, '').send_keys(username)
        cls.driver.find_element(By.ID, '').send_keys(pwd)
        cls.driver.find_element(By.ID, '').click()



