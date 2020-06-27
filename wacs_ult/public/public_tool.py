# coding: utf-8
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup


class PublicTool:
    @staticmethod
    def is_external_domain(base_url, url: str) -> bool:
        self_domain = urlparse(base_url).netloc
        check_domain = urlparse(url).netloc
        if check_domain != self_domain:
            return True
        else:
            return False

    @staticmethod
    def escape_content_gls(html: str, doc: BeautifulSoup):
        result = html
        remove_list = doc.find_all(text=re.compile("(<|>)"))
        for replace_str in remove_list:
            result = result.replace(replace_str, '')

        return result
