# coding: utf-8
import requests
from bs4 import BeautifulSoup

from wacs_ult.error.error_tool import ErrorTool as et


class VitalCheck:
    def __init__(self, url: str):
        # content text count low limit
        self.text_low_limit = 150

        self.url = url
        self.res = None
        self.html = None
        self.doc = None

        self.result = True
        self.minus = 0
        self.errors = list()

    def check(self):
        if not self.check_access():
            return

        if not self.check_response_status():
            return

        if not self.check_html_parse():
            return

        if self.content_is_empty():
            return

    def check_access(self) -> bool:
        try:
            self.res = requests.get(self.url)
            return True

        except Exception as e:
            self.result = False
            self.minus += 100
            msg = '無法讀取作業網頁。 url: {} -> error: {}'.format(self.url, e)
            error_data = et.get_error_data(1, msg, 1, 100)
            self.errors.append(error_data)

            return False

    def check_response_status(self) -> bool:
        status = self.res.status_code
        if status != 200:
            self.result = False
            self.minus += 100
            msg = '網站不存在，或路徑錯誤。 status: {} , url: {}'.format(status, self.url)
            error_data = et.get_error_data(1, msg, 1, 100)
            self.errors.append(error_data)

            return False

        else:
            return True

    def check_html_parse(self) -> bool:
        self.res.encoding = 'utf-8'
        self.html = self.res.text

        try:
            self.doc = BeautifulSoup(self.html, 'html.parser')
            return True

        except Exception as e:
            self.result = False
            self.minus += 100
            msg = '作業網頁無法解析。 url: {} -> error: {}'.format(self.url, e)
            error_data = et.get_error_data(1, msg, 1, 100)
            self.errors.append(error_data)

            return False

    def content_is_empty(self) -> bool:
        text = self.doc.text.strip().replace(' ', '')
        text_count = len(text)

        if text_count < self.text_low_limit:
            self.result = False
            self.minus += 100
            msg = '網頁內容趨近空白 url: {} , 字數: {}'.format(self.url, text_count)
            error_data = et.get_error_data(1, msg, 1, 100)
            self.errors.append(error_data)

            return False

        else:
            return True
