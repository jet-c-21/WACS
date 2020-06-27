# coding: utf-8
from urllib.parse import urljoin

import pathlib
from configparser import ConfigParser

import bs4
import requests
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et


class ImgDisplayCheck:
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
        self.check_img_display(self.url, self.doc)

    def check_img_display(self, url: str, doc: bs4.BeautifulSoup):
        img_list = doc.find_all('img')
        for img in img_list:
            path = img.get('src')
            # path = path.replace('data:', '')  # $$ FIND-AT: 2020/06/19
            abs_url = urljoin(url, path)

            try:
                res = requests.get(abs_url)
            except Exception as e:
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point
                msg = '圖片完全無法讀取。 img_path: {}'.format(path)
                error_data = et.get_error_data(10, msg, 1, reduct_point)

                self.errors.append(error_data)
                continue

            status = res.status_code
            if status != 200 and status != 403:
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point
                msg = '圖片顯示狀態錯誤。 status: {} , img-path: {}'.format(status, path)
                error_data = et.get_error_data(10, msg, 1, reduct_point)

                self.errors.append(error_data)
