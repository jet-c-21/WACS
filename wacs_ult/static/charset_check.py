# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class CharsetCheck:
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
        self.check_charset(self.doc)

    def check_charset(self, doc: BeautifulSoup):
        tag = doc.select('meta[charset]')
        if len(tag) == 0:
            self.result = False


            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'charset 標籤未建立'
            error_data = et.get_error_data(3, msg, 1, reduct_point)

            self.errors.append(error_data)
            return

        charset = tag[0].get('charset')
        if charset not in ['utf-8', 'utf8', 'UTF8', 'UTF-8']:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'charset 標籤錯誤。 tag: {}'.format(charset)
            error_data = et.get_error_data(3, msg, 1, reduct_point)

            self.errors.append(error_data)
