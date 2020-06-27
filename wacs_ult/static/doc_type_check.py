# coding: utf-8
from wacs_ult.error.error_tool import ErrorTool as et
import pathlib
from configparser import ConfigParser


class DocTypeCheck:
    def __init__(self, html):
        self.html = html

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
        self.check_doc_type()

    def check_doc_type(self):
        if '<!DOCTYPE html>' not in self.html:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = '<!DOCTYPE> 標籤錯誤'
            error_data = et.get_error_data(2, msg, 1, reduct_point)

            self.errors.append(error_data)
