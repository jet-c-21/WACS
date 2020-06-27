# coding: utf-8
import re
import pathlib
from configparser import ConfigParser
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et
from wacs_ult.public.public_tool import PublicTool


class TagsCheck:
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
        self.check_tags(self.html, self.doc)

    def check_tags(self, html: str, doc: BeautifulSoup):
        self_closing = ['area', 'base', 'br', 'embed', 'hr', 'iframe', 'img',
                        'input', 'link', 'meta', 'param', 'source', 'track',
                        'address', 'aside']
        tag_list = [tag.name for tag in doc.find_all()]
        tag_list = list(set(tag_list))

        temp_html = PublicTool.escape_content_gls(html, doc)

        for tag in tag_list:
            if tag in self_closing:
                continue
            # pattern = r'<{1}' + tag + ' ' + '[^<,>]*>{1}'
            # pattern = r'^(<{1}' + tag + ' ' + ')(.*)(>{1})$'
            pattern = r'<' + tag + ' '
            normal_start = '<' + tag + '>'
            normal_end = '</' + tag + '>'
            sp_case_list = re.findall(pattern, temp_html)
            start_count = len(sp_case_list) + temp_html.count(normal_start)
            end_count = temp_html.count(normal_end)

            if start_count != end_count:

                # print(tag, start_count, end_count)

                dev = abs(start_count - end_count)

                if start_count > end_count:
                    info = normal_start + ' 多於 ' + normal_end
                else:
                    info = normal_end + ' 多於 ' + normal_start

                self.result = False

                reduct_point = self.POINT * dev
                self.minus += reduct_point
                msg = 'tag 的開始與結束有錯誤。 {} 相差數: {}'.format(info, dev)
                error_data = et.get_error_data(20, msg, dev, reduct_point)

                self.errors.append(error_data)
