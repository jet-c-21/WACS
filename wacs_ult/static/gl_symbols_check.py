# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et
from wacs_ult.public.public_tool import PublicTool


class GLSymbolsCheck:
    def __init__(self, html: str, doc: BeautifulSoup):
        self.html = html
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
        self.check_gl_symbols(self.html, self.doc)

    def check_gl_symbols(self, html: str, doc: BeautifulSoup):
        temp_html = PublicTool.escape_content_gls(html, doc)
        ls_count = temp_html.count('<')
        gs_count = temp_html.count('>')

        if ls_count != gs_count:
            dev = abs(ls_count - gs_count)

            self.result = False

            reduct_point = self.POINT * dev
            self.minus += reduct_point
            msg = '<、> 符號數量錯誤。 相差: {}'.format(dev)
            error_data = et.get_error_data(21, msg, 1, reduct_point)

            self.errors.append(error_data)
