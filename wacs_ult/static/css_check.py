# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class CssCheck:
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
        self.check_css(self.doc)

    def check_css(self, doc: BeautifulSoup):
        elements = doc.select('link[rel = "stylesheet"][type = "text/css"]')
        for tag in elements:
            path = tag.get('href')
            check_list = path.split('/')
            if 'css' not in check_list:
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point
                msg = 'css未放入css資料夾中。 path: {}'.format(path)
                error_data = et.get_error_data(16, msg, 1, reduct_point)

                self.errors.append(error_data)
