# coding: utf-8
from threading import Thread

from wacs_ult.basic.vital_check import VitalCheck
from wacs_ult.dynamic.driver_tool import DriverTool
from wacs_ult.dynamic.screenshot_helper import ScreenshotHelper
from wacs_ult.dynamic.scroll_bar_check import ScrollBarCheck
from wacs_ult.error.log_tool import LogTool
from wacs_ult.gps_api.gps_api_helper import GPSApiHelper
from wacs_ult.public.save_tool import SaveTool
from wacs_ult.static.all_src_name_check import AllSrcNameCheck
from wacs_ult.static.attr_quote_check import AttrQuoteCheck
from wacs_ult.static.attr_space_check import AttrSpaceCheck
from wacs_ult.static.charset_check import CharsetCheck
from wacs_ult.static.css_check import CssCheck
from wacs_ult.static.doc_type_check import DocTypeCheck
from wacs_ult.static.gl_symbols_check import GLSymbolsCheck
from wacs_ult.static.head_body_check import HeadBodyCheck
from wacs_ult.static.img_display_check import ImgDisplayCheck
from wacs_ult.static.img_setting_check import ImgSettingCheck
from wacs_ult.static.js_check import JsCheck
from wacs_ult.static.lang_check import LangCheck
from wacs_ult.static.li_tag_check import LiTagCheck
from wacs_ult.static.ol_tag_check import OlTagCheck
from wacs_ult.static.page_name_check import PageNameCheck
from wacs_ult.static.tags_check import TagsCheck
from wacs_ult.static.title_check import TitleCheck
from wacs_ult.static.ul_tag_check import UlTagCheck
from wacs_ult.static.window_open_check import WindowOpenCheck

from pprint import pprint as pp

class PageMarker(object):
    def __init__(self, input_url=None, html_save_path=None, screenshot_save_path=None,
                 gps_json_save_path=None, log_path=None, mark_id=None, sheet_path=None):
        self.mark_id = None
        if mark_id:
            self.mark_id = mark_id
        else:
            self.mark_id = LogTool.gen_random_token()

        self.driver = None
        self.sys_log = list()

        self.reduct_score = 0
        self.gps_desktop_perf = 0
        self.gps_mobile_perf = 0
        self.gps_score = 0
        self.total_score = 0
        self.error_list = list()

        self.vital_error = False
        self.url = input_url
        self.res = None
        self.html = None
        self.doc = None

        self.gps = None

        self.log_path = log_path

        if html_save_path:
            self.html_save_path = html_save_path
        else:
            self.html_save_path = 'D:/{}_index.html'.format(self.mark_id)

        if screenshot_save_path:
            self.screenshot_save_path = screenshot_save_path
        else:
            self.screenshot_save_path = 'D:/{}_screen.jpg'.format(self.mark_id)

        if gps_json_save_path:
            self.gps_json_save_path = gps_json_save_path
        else:
            self.gps_json_save_path = 'D:/{}_google_speed_result.json'.format(self.mark_id)

        if sheet_path:
            self.sheet_path = sheet_path
        else:
            self.sheet_path = 'D:/{}_html_error.csv'.format(self.mark_id)

    def mark(self):
        vital_check = VitalCheck(self.url)
        vital_check.check()

        # start basic vital check item
        if not vital_check.result:
            self.reduct_score += vital_check.minus
            self.error_list.extend(vital_check.errors)

            save_html_th = Thread(target=self.save_html)
            dynamic_td = Thread(target=self.dynamic)
            dynamic_td.start()
            save_html_th.start()
            dynamic_td.join()
            save_html_th.join()

            self.vital_error = True

        else:
            # set global variable
            self.res = vital_check.res
            self.html = vital_check.html
            self.doc = vital_check.doc
            # check standard-checking-items
            self.start_standard_checking()

        # calculate final score
        self.calculate_score()

    def start_standard_checking(self):
        static_th = Thread(target=self.static)
        save_html_th = Thread(target=self.save_html)
        gps_td = Thread(target=self.google_page_speed_api_check)
        dynamic_td = Thread(target=self.dynamic)

        gps_td.start()
        dynamic_td.start()
        static_th.start()
        save_html_th.start()

        gps_td.join()
        dynamic_td.join()
        static_th.join()
        save_html_th.join()

    def calculate_score(self):
        if self.gps:
            self.gps_score = self.gps.score
        else:
            self.gps_score = 0

        if self.gps_score != -1:
            score = self.gps_score
            score -= self.reduct_score

            self.total_score = score

            if self.total_score < 0:
                self.total_score = 0

        else:
            self.total_score = -1

    # dynamic part ====================================================================================
    def dynamic(self):
        self.driver = DriverTool.get_driver()
        DriverTool.surf(self.driver, self.url)

        self.do_scroll_bar_check()  # 8
        self.do_screenshot()

        try:
            self.driver.close()
        except Exception as e:
            print(e)

    def do_scroll_bar_check(self):
        scroll_bar_check = ScrollBarCheck(self.driver)
        try:
            scroll_bar_check.check()
            if not scroll_bar_check.result:
                self.reduct_score += scroll_bar_check.minus
                self.error_list.extend(scroll_bar_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_screenshot(self):
        screenshot_helper = ScreenshotHelper(self.driver, self.screenshot_save_path)
        try:
            screenshot_helper.launch()
        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

        if not screenshot_helper.result:
            self.screenshot_save_path = 'failed`'

    # dynamic part ====================================================================================

    def google_page_speed_api_check(self):
        self.gps = GPSApiHelper(self.url, self.gps_json_save_path)
        self.gps.launch()


    def save_html(self):
        status = SaveTool.save_html(self.html_save_path, self.url)
        if not status:
            self.html_save_path = ''

    # static part ====================================================================================
    def static(self):
        self.do_doc_type_check()  # 2
        self.do_charset_check()  # 3
        self.do_lang_check()  # 4
        self.do_title_check()  # 5
        self.do_head_body_check()  # 7
        self.do_img_display_check()  # 10
        self.do_page_name_check()  # 11
        self.do_all_src_name_check()  # 12、13、15
        self.do_window_open_check()  # 14
        self.do_css_check()  # 16
        self.do_js_check()  # 17
        self.do_img_setting_check()  # 18、19
        # self.do_tags_check()  # 20 ***
        # self.do_gl_symbols_check()  # 21
        self.do_attr_space_check()  # 22
        # self.do_attr_quote_check()  # 23
        self.do_ul_tag_check()  # 24
        self.do_ol_tag_check()  # 25
        self.do_li_tag_check()  # 26

    def do_li_tag_check(self):
        # start checking if the usage of ol-tag is correct
        li_tag_check = LiTagCheck(self.doc)
        try:
            li_tag_check.check()
            if not li_tag_check.result:
                self.reduct_score += li_tag_check.minus
                self.error_list.extend(li_tag_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_ol_tag_check(self):
        # start checking if the usage of ol-tag is correct
        ol_tag_check = OlTagCheck(self.doc)
        try:
            ol_tag_check.check()
            if not ol_tag_check.result:
                self.reduct_score += ol_tag_check.minus
                self.error_list.extend(ol_tag_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_ul_tag_check(self):
        # start checking if the usage of ul-tag is correct
        ul_tag_check = UlTagCheck(self.doc)
        try:
            ul_tag_check.check()
            if not ul_tag_check.result:
                self.reduct_score += ul_tag_check.minus
                self.error_list.extend(ul_tag_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_attr_quote_check(self):
        # start checking the " " mark in using attribute elements
        attr_quote_check = AttrQuoteCheck(self.html, self.doc)
        try:
            attr_quote_check.check()
            if not attr_quote_check.result:
                self.reduct_score += attr_quote_check.minus
                self.error_list.extend(attr_quote_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_attr_space_check(self):
        # start checking the space in using attribute elements
        attr_space_check = AttrSpaceCheck(self.html, self.doc)
        try:
            attr_space_check.check()
            if not attr_space_check.result:
                self.reduct_score += attr_space_check.minus
                self.error_list.extend(attr_space_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_gl_symbols_check(self):
        # start checking if the count of "<" and ">" are correct
        gl_symbols_check = GLSymbolsCheck(self.html, self.doc)
        try:
            gl_symbols_check.check()
            if not gl_symbols_check.result:
                self.reduct_score += gl_symbols_check.minus
                self.error_list.extend(gl_symbols_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_tags_check(self):
        # start checking if all tags have its own closed tag
        tags_check = TagsCheck(self.html, self.doc)
        try:
            tags_check.check()
            if not tags_check.result:
                self.reduct_score += tags_check.minus
                self.error_list.extend(tags_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_img_setting_check(self):
        # start checking if the img are set in the correct way
        img_setting_check = ImgSettingCheck(self.url, self.doc)
        try:
            img_setting_check.check()
            if not img_setting_check.result:
                self.reduct_score += img_setting_check.minus
                self.error_list.extend(img_setting_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_js_check(self):
        # start checking if all javascript file is placed in the correct folder
        js_check = JsCheck(self.doc)
        try:
            js_check.check()
            if not js_check.result:
                self.reduct_score += js_check.minus
                self.error_list.extend(js_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_css_check(self):
        # start checking if all css file is placed in the correct folder
        css_check = CssCheck(self.doc)
        try:
            css_check.check()
            if not css_check.result:
                self.reduct_score += css_check.minus
                self.error_list.extend(css_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_window_open_check(self):
        # start checking if correctly using: target="_blank"
        window_open_check = WindowOpenCheck(self.url, self.doc)
        try:
            window_open_check.check()
            if not window_open_check.result:
                self.reduct_score += window_open_check.minus
                self.error_list.extend(window_open_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_all_src_name_check(self):
        # start checking all names of file, folder and img in the html file
        all_src_name_check = AllSrcNameCheck(self.url, self.doc)
        try:
            all_src_name_check.check()
            if not all_src_name_check.result:
                self.reduct_score += all_src_name_check.minus
                self.error_list.extend(all_src_name_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_page_name_check(self):
        # start checking the name of the main html file
        page_name_check = PageNameCheck(self.url)
        try:
            page_name_check.check()
            if not page_name_check.result:
                self.reduct_score += page_name_check.minus
                self.error_list.extend(page_name_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_img_display_check(self):
        # start checking img display
        img_display_check = ImgDisplayCheck(self.url, self.doc)
        try:
            img_display_check.check()
            if not img_display_check.result:
                self.reduct_score += img_display_check.minus
                self.error_list.extend(img_display_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_head_body_check(self):
        # start checking <head> and <body>
        head_body_check = HeadBodyCheck(self.doc)
        try:
            head_body_check.check()
            if not head_body_check.result:
                self.reduct_score += head_body_check.minus
                self.error_list.extend(head_body_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_title_check(self):
        # start checking title
        title_check = TitleCheck(self.doc)
        try:
            title_check.check()
            if not title_check.result:
                self.reduct_score += title_check.minus
                self.error_list.extend(title_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_lang_check(self):
        # start checking lang
        lang_check = LangCheck(self.doc)
        try:
            lang_check.check()
            if not lang_check.result:
                self.reduct_score += lang_check.minus
                self.error_list.extend(lang_check.errors)

        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_charset_check(self):
        # start checking charset
        charset_check = CharsetCheck(self.doc)
        try:
            charset_check.check()
            if not charset_check.result:
                self.reduct_score += charset_check.minus
                self.error_list.extend(charset_check.errors)
        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    def do_doc_type_check(self):
        # start checking document type
        doc_type_check = DocTypeCheck(self.html)
        try:
            doc_type_check.check()
            if not doc_type_check.result:
                self.reduct_score += doc_type_check.minus
                self.error_list.extend(doc_type_check.errors)
        except Exception as e:
            print(LogTool.pp_exception(e))  # 9527

    # static part ====================================================================================

# from pprint import pprint as pp
# y = 'http://myweb.scu.edu.tw/~06170123/mr.puff/'
# # y = 'https://www.acer.com'
# # y = 'http://isee.scu.edu.tw/'
# # y = 'http://myweb.scu.edu.tw/~06170107/'
# x = PageMarker(input_url=y)
# x.mark()
# # pp(x.reduc_score)
# # pp(x.error_list)
