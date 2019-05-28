# _*_coding:utf-8_*_
# Editor  : SHEEHAN YUAN
# Date    : 2019/5/20 18:31
# File    : mylog.py
# IDE     : PyCharm

# -*- coding:utf-8 -*-

import logging
import getpass
import sys


class MyLog(object):
    def __init__(self):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)
        self.logFile = sys.argv[0][0:-3] + '.log'
        self.formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name) -10s %(message)-12s\r\n')
        self.logHand = logging.FileHandler(self.logFile, encoding='utf8')
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.DEBUG)
        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.DEBUG)
        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    mylog = MyLog()
    mylog.debug(u"I'm debug 测试中文")
    mylog.info("I'm info")
    mylog.warn("I'm info")
    mylog.error(u"I'm error 测试中文")
    mylog.critical("I'm critical")
