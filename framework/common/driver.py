import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Browser:
    """浏览器类,单例模式"""
    driver = None  # 将driver定义为类级变量，则该driver只会保存在类的内存

    def __init__(self):
        pass

    @classmethod  # 将该方法定义为类级方法，则直接调用类名即可，不需要实例化
    def get_webdriver(cls):
        if cls.driver is None:
            s = Service('../../driver/chromedriver')
            # opt = webdriver.ChromeOptions()
            # opt.add_argument(r"--user-data-dir=C:\Users\1\AppData\Local\Google\Chrome\User Data\Default")  # 使浏览器加载本地缓存
            # cls.driver = webdriver.Chrome(service=s,options=opt)  # 创建浏览器
            cls.driver = webdriver.Chrome(service=s)  # 创建浏览器
            cls.driver.maximize_window()  # 最大化
            # cls.driver.get("192.168.1.212:8081/secmail/")  # 打开链接
            cls.driver.get("https://www.baidu.com/")  # 打开链接
            time.sleep(3)
        return cls.driver
