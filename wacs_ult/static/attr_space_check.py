# coding: utf-8
import re
import pathlib
from configparser import ConfigParser
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et


class AttrSpaceCheck:
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
        self.check_attr_space(self.html, self.doc)

    def check_attr_space(self, html: str, doc: BeautifulSoup):
        tag_list = [tag.name for tag in doc.find_all()]
        tag_list = list(set(tag_list))
        hp = r'href=\"([^"]*)\"'
        srcp = r'src=\"([^"]*)\"'

        for tag in tag_list:
            pattern = r'<{1}' + tag + ' [^<,>]*>{1}'
            find_list = re.findall(pattern, html)

            for check_tag in find_list:
                temp_tag = check_tag
                if bool(re.findall(hp, temp_tag)):
                    replace_p = r' href=\"([^"]*)\"'
                    temp_tag = re.sub(replace_p, '', temp_tag)

                if bool(re.findall(srcp, temp_tag)):
                    replace_p = r' src=\"([^"]*)\"'
                    temp_tag = re.sub(replace_p, '', temp_tag)

                req_p = r'\"([^"]*)\"'
                re_list = re.findall(req_p, temp_tag)

                for re_str in re_list:
                    re_str = re_str.replace('"', '')
                    temp_tag = temp_tag.replace(re_str, '')

                class_num = temp_tag.count('=')
                space_num = temp_tag.count(' ')

                if space_num < class_num:
                    self.result = False

                    reduct_point = self.POINT * 1
                    self.minus += reduct_point
                    msg = '元素屬性之間沒有用空白隔開 tag: {}'.format(check_tag)
                    error_data = et.get_error_data(22, msg, 1, reduct_point)

                    self.errors.append(error_data)
