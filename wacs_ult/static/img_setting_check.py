# coding: utf-8
import re
import urllib.request
from urllib.parse import urljoin
import pathlib
from configparser import ConfigParser
from PIL import Image
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et


class ImgSettingCheck:
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

    @staticmethod
    def get_img_hwp(url: str):
        image = Image.open(urllib.request.urlopen(url))
        h = image.height
        w = image.width
        if h == 0 or w == 0:
            return 0
        return round(h / w, 2)

    def check(self):
        self.check_img_setting(self.url, self.doc)

    def check_img_setting(self, url: str, doc: BeautifulSoup):
        elements = doc.select('body img')

        for tag in elements:
            path = tag.get('src')
            abs_url = urljoin(url, path)
            height = tag.get('height')
            width = tag.get('width')

            if height is not None and re.match(r'[0-9]+%', str(width)):
                if re.match(r'[0-9]+\s*px', str(height)) and re.match(r'[0-9]+\s*px', str(width)):
                    h = int(height.replace('px', ''))
                    w = int(width.replace('px', ''))
                    hwp = round(h / w, 2)

                    raw_hwp = self.get_img_hwp(abs_url)

                    if hwp != raw_hwp:
                        self.result = False

                        reduct_point = self.POINT * 1
                        self.minus += reduct_point
                        msg = '圖片設定後的寬高比例與原圖比例不同。 tag: {}'.format(tag)
                        error_data = et.get_error_data(18, msg, 1, reduct_point)

                        self.errors.append(error_data)

                else:
                    self.result = False

                    reduct_point = self.POINT * 1
                    self.minus += reduct_point
                    msg = '圖片設定錯誤。 tag: {}'.format(tag)
                    error_data = et.get_error_data(19, msg, 1, reduct_point)

                    self.errors.append(error_data)
