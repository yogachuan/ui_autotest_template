import os
import time

# import faker

from framework.common.read_data import read_data
from faker import Faker

def aaa():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    screenshot_path = os.path.join(os.path.dirname(cur_path), f'screenshots')
    if not os.path.exists(screenshot_path):
        os.mkdir(screenshot_path)

    # 日期文件夹
    now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    data_screenshot_path = os.path.join(os.path.dirname(cur_path), f'screenshots/{now_date}')
    if not os.path.exists(data_screenshot_path):
        os.mkdir(data_screenshot_path)


def bbb():
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(base_path)
    userdata = read_data.load_excel(os.path.join(base_path, "data", "signup.xlsx"))
    print(userdata)


if __name__ == '__main__':
    pass
    fake = Faker(locale='zh_CN')

    print(fake.name())
    print(fake.ssn())
    print(fake.phone_number())
    print(fake.province())
    print(fake.city())