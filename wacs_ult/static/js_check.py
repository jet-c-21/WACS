# coding: utf-8
import re
import pathlib
from configparser import ConfigParser
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et


class JsCheck:
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
        self.check_js(self.doc)

    def check_js(self, doc: BeautifulSoup):
        elements = doc.select('script')
        for tag in elements:
            path = tag.get('src')
            if path is None:
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point
                msg = 'script 標籤內沒有設定 src  tag: {}'.format(tag)
                error_data = et.get_error_data(17, msg, 1, reduct_point)

                self.errors.append(error_data)
                continue

            else:
                regex_check = re.findall(
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                    path)
                if regex_check != 0:
                    continue
                else:
                    check_list = path.split('/')
                    if 'js' not in check_list:
                        self.result = False

                        reduct_point = self.POINT * 1
                        self.minus += reduct_point
                        msg = 'javascript 未寫在 js 資料夾中。 path: {}'.format(path)
                        error_data = et.get_error_data(17, msg, 1, reduct_point)

                        self.errors.append(error_data)
