# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class LiTagCheck:
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
        self.check_li_tag(self.doc)

    def check_li_tag(self, doc: BeautifulSoup):
        li_list = doc.select('li')
        for li in li_list:
            parent_tag = li.parent.name
            if parent_tag not in ['ul', 'ol']:
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point
                msg = 'li標籤單獨使用, 錯誤元素: {} , 父標籤: {}'.format(str(li).replace('\n', ''), parent_tag)
                error_data = et.get_error_data(26, msg, 1, reduct_point)

                self.errors.append(error_data)
