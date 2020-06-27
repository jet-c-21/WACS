# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class TitleCheck:
    def __init__(self, doc: BeautifulSoup):
        self.doc = doc

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
        self.check_title(self.doc)

    def check_title(self, doc: BeautifulSoup):
        tag = doc.select('head title')

        if len(tag) == 0:
            self.result = False
            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'title 標籤未建立'
            error_data = et.get_error_data(5, msg, 1, reduct_point)
            self.errors.append(error_data)
            return

        title = tag[0].text
        if len(title) == 0 or title is None:
            self.result = False
            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'title 標籤錯誤'
            error_data = et.get_error_data(5, msg, 1, reduct_point)
            self.errors.append(error_data)
