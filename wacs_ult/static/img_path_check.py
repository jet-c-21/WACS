# coding: utf-8
import re
from urllib.parse import urljoin
import pathlib
from configparser import ConfigParser

from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et
from wacs_ult.public.public_tool import PublicTool


class ImgPathCheck:
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
        self.check_img_path(self.url, self.doc)

    def check_img_path(self, url, doc: BeautifulSoup):
        img_list = doc.find_all('img')

        for img in img_list:
            path = img.get('src')
            abs_url = urljoin(url, path)

            if PublicTool.is_external_domain(self.url, abs_url):
                continue
            else:
                check_list = path.split('/')

                # check if img is in img-folder
                if 'images' not in check_list and 'img' not in check_list and 'image' not in check_list:
                    self.result = False

                    reduct_point = self.POINT * 1
                    self.minus += reduct_point
                    msg = '圖片未放在圖片資料夾(images or img or image) 或是路徑設定錯誤。 tag: {}'.format(path)
                    error_data = et.get_error_data(15, msg, 1, reduct_point)

                    self.errors.append(error_data)


                # check img-file-name
                for sub_path in check_list:
                    regex_check = re.findall(r'([\u4E00-\u9FFF]+|[A-Z]+|\s+)', sub_path)
                    if len(regex_check) != 0:
                        self.result = False

                        reduct_point = self.POINT * 1
                        self.minus += reduct_point
                        msg = '圖片檔名或是路徑含有中文/大寫/空白字元。 path_string: {}'.format(sub_path)
                        error_data = et.get_error_data(12, msg, 1, reduct_point)

                        self.errors.append(error_data)
