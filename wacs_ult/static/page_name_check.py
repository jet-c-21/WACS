# coding: utf-8
import re
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class PageNameCheck:
    def __init__(self, url: str):
        self.url = url

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
        self.check_file_path(self.url)

    def check_file_path(self, url):
        check_list = url.split('/')
        if len(check_list) == 0:
            return

        file_name = check_list[-1]
        regex_check = re.findall(r'([\u4E00-\u9FFF]+|[A-Z]+|\s+)', file_name)
        if len(regex_check) != 0:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = '網頁檔名或是含有 "中文" 或 "大寫字母" 或 "空白字元" 。 path_string: {}'.format(file_name)
            error_data = et.get_error_data(11, msg, 1, reduct_point)

            self.errors.append(error_data)
