# coding: utf-8
from selenium import webdriver


class DriverTool:
    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # not show browser
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--test-type')
        browser = webdriver.Chrome(options=options)
        return browser

    @staticmethod
    def surf(browser: webdriver, url: str):
        try:
            browser.get(url)
        except Exception as e:
            print(e)
