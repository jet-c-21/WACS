# coding: utf-8
import re
from urllib.parse import urljoin
import pathlib
from configparser import ConfigParser
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et
from wacs_ult.public.public_tool import PublicTool


class AllSrcNameCheck:
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
        self.check_all_src_name(self.url, self.doc)

    def check_all_src_name(self, url: str, doc: BeautifulSoup):
        # file part
        elements = doc.select('[href]')
        for tag in elements:
            link = tag.get('href')
            if 'tel:' in link and '+' in link:
                continue
            if 'mailto:' in link and '@' in link:
                continue

            abs_url = urljoin(url, link)
            if not PublicTool.is_external_domain(url, abs_url):
                # file
                path_list = link.split('/')
                file = path_list.pop()
                file_check = re.findall(r'([\u4E00-\u9FFF]+|[A-Z]+|\s+)', file)
                if len(file_check) != 0:
                    self.result = False

                    reduct_point = self.POINT * 1
                    self.minus += reduct_point
                    msg = '上傳的檔案中，有的名稱含有 中文 或 大寫 或 空白字元。 file name: {}'.format(file)
                    error_data = et.get_error_data(13, msg, 1, reduct_point)

                    self.errors.append(error_data)

                # folder
                for folder in path_list:
                    folder_check = re.findall(r'([\u4E00-\u9FFF]+|[A-Z]+|\s+)', folder)
                    if len(folder_check) != 0:
                        self.result = False

                        reduct_point = self.POINT * 1
                        self.minus += reduct_point
                        msg = '上傳的資料夾中，有的名稱含有 中文 or 大寫 or 空白字元。 folder name: {}'.format(folder)
                        error_data = et.get_error_data(13, msg, 1, reduct_point)

                        self.errors.append(error_data)

        # img part
        img_list = doc.find_all('img')

        for img in img_list:
            path = img.get('src')
            abs_url = urljoin(self.url, path)
            if PublicTool.is_external_domain(url, abs_url):
                continue
            else:
                check_list = path.split('/')
                # 是否在圖片資料夾
                if 'images' not in check_list and 'img' not in check_list and 'image' not in check_list:
                    self.result = False

                    reduct_point = self.POINT * 1
                    self.minus += reduct_point
                    msg = '圖片未放在圖片資料夾(images or img or image) 或是路徑設定錯誤。 tag: {}'.format(path)
                    error_data = et.get_error_data(15, msg, 1, reduct_point)

                    self.errors.append(error_data)

                # 查看檔名
                for sub_path in check_list:
                    regex_check = re.findall(r'([\u4E00-\u9FFF]+|[A-Z]+|\s+)', sub_path)
                    if len(regex_check) != 0:
                        self.result = False

                        reduct_point = self.POINT * 1
                        self.minus += reduct_point
                        msg = '圖片檔名或是路徑含有中文/大寫/空白字元。 path_string: {}'.format(sub_path)
                        error_data = et.get_error_data(12, msg, 1, reduct_point)

                        self.errors.append(error_data)
