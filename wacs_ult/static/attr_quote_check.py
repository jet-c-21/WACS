# coding: utf-8
import re

from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et
from wacs_ult.public.public_tool import PublicTool


class AttrQuoteCheck:
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

    @staticmethod
    def get_tags_with_attr(clean_html: str, doc: BeautifulSoup) -> list:
        result = []
        tag_list = [tag.name for tag in doc.find_all()]
        tag_list = list(set(tag_list))

        for tag in tag_list:
            pattern = r'<{1}' + tag + ' [^<,>]*>{1}'
            temp = re.findall(pattern, clean_html)
            for check_tag in temp:
                result.append(check_tag)

        return result

    def check(self):
        self.check_attr_quote(self.html, self.doc)

    def check_attr_quote(self, html: str, doc: BeautifulSoup):
        temp_html = PublicTool.escape_content_gls(html, doc)
        tags_with_attr = AttrQuoteCheck.get_tags_with_attr(temp_html, doc)

        for raw_str in tags_with_attr:
            soup = BeautifulSoup(raw_str, 'html.parser')
            for el in soup():
                all_attrs = list(el.attrs.keys())
                equal_symbol_count = 0

                for attr_name in all_attrs:
                    equal_symbol_count += raw_str.count('{}'.format(attr_name))  # edit at 2020/06/23

                quote_count = raw_str.count('"')

                if quote_count != equal_symbol_count * 2:
                    self.result = False

                    reduct_point = self.POINT * 1
                    self.minus += reduct_point
                    msg = '屬性的 " " 符號沒有正確使用。 錯誤元素: {}'.format(raw_str)
                    error_data = et.get_error_data(23, msg, 1, reduct_point)

                    self.errors.append(error_data)
