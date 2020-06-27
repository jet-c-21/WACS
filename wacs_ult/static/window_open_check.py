# coding: utf-8
from urllib.parse import urljoin
from configparser import ConfigParser
import pathlib
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et
from wacs_ult.public.public_tool import PublicTool


class WindowOpenCheck:
    def __init__(self, url: str, doc: BeautifulSoup):
        self.url = url
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
        self.check_window_open(self.url, self.doc)

    def check_window_open(self, url: str, doc: BeautifulSoup):
        elements = doc.select('body [href]')

        for tag in elements:
            link = tag.get('href')
            if 'tel:' in link and '+' in link:
                continue
            if 'mailto:' in link and '@' in link:
                continue

            abs_url = urljoin(url, link)

            if PublicTool.is_external_domain(url, abs_url) and tag.get('target') != '_blank':
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point

                msg = '連結到外部連結沒有新開視窗。 tag: {}'.format(tag)
                error_data = et.get_error_data(14, msg, 1, reduct_point)
                self.errors.append(error_data)
