# coding: utf-8
import pathlib
from selenium import webdriver
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class ScrollBarCheck:
    def __init__(self, browser: webdriver):
        self.browser = browser

        self.config_path = None
        self.config = None
        self.POINT = None
        self.load_point()

        self.result = True
        self.minus = 0
        self.errors = list()

    def load_point(self):
        self.config_path = '{}/reduct.ini'.format(pathlib.Path(__file__).parent.parent.absolute())
        self.config = ConfigParser()
        self.config.read(self.config_path)
        self.POINT = int(self.config[self.__class__.__name__]['POINT'])

    def check(self):
        self.check_scroll_bar(self.browser)

    def check_scroll_bar(self, browser: webdriver):
        width = browser.execute_script("return document.body.scrollWidth")
        if width > 1280:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = '網頁出現橫向卷軸。 網頁寬度: {}'.format(width)
            error_data = et.get_error_data(8, msg, 1, reduct_point)

            self.errors.append(error_data)
