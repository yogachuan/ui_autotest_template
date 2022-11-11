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
        log_path = os.path.join(os.path.dirname(cur_path), f'logs')  # 创建名为logs的文件夹
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # log 日期文件夹
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        phone_log_path = os.path.join(os.path.dirname(cur_path), f'logs//{now_date}')  # 在logs下创建日期文件夹
        if not os.path.exists(phone_log_path):
            os.mkdir(phone_log_path)
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)  # logger设置日志级别,INFO以上级别的信息输出至日志
        # 创建一个handler，用于写入日志文件
        now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        log_name = os.path.join(phone_log_path, f'{now_time}.log')
        fh = logging.FileHandler(log_name)  # 在logs的日期文件夹下创建日志文件
        fh.setLevel(logging.INFO)  # handler设置日志级别,INFO以上级别的信息输出至日志
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s [line:%(lineno)d]: %(message)s')  #  2022-11-05 18:09:45,377 - INFO basepage.py [line:58]: 在"输入关键字"输入"yujiachun",元素定位:('id', 'kw')
        fh.setFormatter(formatter)  # handler写入日志到文件
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getLog(self):
        return self.logger


logger = Logger().logger
