# coding: utf-8
import json
import os
import urllib.request

from PIL import Image


class SaveTool:
    @staticmethod
    def save_html(html_save_path: str, url: str):
        if not os.path.exists(os.path.dirname(html_save_path)):
            try:
                os.makedirs(os.path.dirname(html_save_path))
                urllib.request.urlretrieve(url, html_save_path)
                return True
            except Exception as e:
                se_list = ['[Inner - save_html] 存取 html 失敗', 'url: ' + url + ' ' + str(e)]
                print(se_list)
                # raise
        else:
            try:
                urllib.request.urlretrieve(url, html_save_path)
                return True

            except Exception as e:
                se_list = ['[Inner - save_html] 存取 html 失敗', 'url: ' + url + ' ' + str(e)]
                print(se_list)
                # raise

    @staticmethod
    def save_json(json_save_path: str, data):
        if not os.path.exists(os.path.dirname(json_save_path)):
            try:
                os.makedirs(os.path.dirname(json_save_path))
                with open(json_save_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            except Exception as e:
                se_list = ['[Inner - save_html] failed to write google speed json to local. ', str(e)]
                print(se_list)
                raise
        else:
            with open(json_save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def save_screenshot(img_save_path: str, img_data: Image):
        if not os.path.exists(os.path.dirname(img_save_path)):
            try:
                os.makedirs(os.path.dirname(img_save_path))
                img_data.save(img_save_path)
            except Exception as e:
                se_list = ['[Inner - save_screen_shot] failed to write screen shot img to local. ', str(e)]
                print(se_list)
        else:
            img_data.save(img_save_path)
