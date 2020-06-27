# coding: utf-8
import datetime
import os
from configparser import ConfigParser
from urllib.parse import urljoin

import pymysql
import requests
from bs4 import BeautifulSoup
import pandas as pd

from page_marker import PageMarker
from wacs_ult.db.db_tool import DbTool
from wacs_ult.error.homepage_error_tool import HomepageErrorTool
from wacs_ult.error.log_tool import LogTool
from wacs_ult.public.record_parse_tool import RecordParseTool
from wacs_ult.public.sheet_tool import SheetTool
from pprint import pprint as pp


class WACS:
    def __init__(self):
        self.db_connection = None
        self.db_user = None
        self.db_password = None
        self.db_name = None
        self.manual_check_date = None
        self.root_save_dir = None
        self.config_path = None
        self.config = None
        self.load_config()

        self.conn = None
        self.cursor = None
        self.homepage_list = list()

        self.target_date = ''
        self.target_date_dash = ''

        self.homework_id = None

        self.log_path = None

    # pre-work 0
    def load_config(self):
        self.config_path = 'setting.ini'
        self.config = ConfigParser()
        self.config.read(self.config_path)
        self.db_connection = self.config['db']['connection']
        self.db_user = self.config['db']['user']
        self.db_password = self.config['db']['password']
        self.db_name = self.config['db']['name']

        if self.config['manual']['date'] != 'null':
            self.manual_check_date = self.config['manual']['date']

        self.root_save_dir = self.config['save']['dir']

    # pre-work 1
    def set_target_date(self):
        if self.manual_check_date:
            for t in self.manual_check_date.split('-'):
                self.target_date += t
            self.target_date_dash = self.manual_check_date

        else:
            curr_time = datetime.datetime.now()
            year, month, day = str(curr_time.year), str(curr_time.month), str(curr_time.day)

            if len(month) == 1:
                month = '0' + month

            if len(day) == 1:
                day = '0' + day

            self.target_date = '{}{}{}'.format(year, month, day)
            self.target_date_dash = '{}-{}-{}'.format(year, month, day)

    # pre-work 2
    def init_log(self):
        if not os.path.exists('log'):
            os.mkdir('log')

        fn = LogTool.generate_log_file_name(self.target_date_dash)
        self.log_path = 'log/{}'.format(fn)
        LogTool.init_file(self.log_path)

    # pre-work 3
    def connect_db(self) -> bool:
        try:
            self.conn = pymysql.connect(self.db_connection, self.db_user, self.db_password, self.db_name)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            msg = '{} - [{}] Failed to connect mysql database. error: {}'.format(datetime.datetime.now(), __name__,
                                                                                 LogTool.pp_exception(e))
            LogTool.update_slog(self.log_path, msg, 'a')
            return False

    def launch(self):
        self.set_target_date()
        # self.init_log()
        if not self.connect_db():
            return

        self.set_homework_id()
        if not self.homework_id:
            msg = '{} - [{}] Cannot find homework id.'.format(datetime.datetime.now(), __name__)
            LogTool.update_slog(self.log_path, msg, 'a')
            return

        if not self.get_homepage_list():
            return

        self.filt_homepage()

        self.checking()

        self.conn.close()

    def filt_homepage(self):
        temp = []
        for record in self.homepage_list:
            status = int(record[4])
            if status <= int(self.config['status_filt']['level']):
                temp.append(record)

        self.homepage_list = temp

    def set_homework_id(self):
        query = 'SELECT * FROM class.student_score_item;'
        try:
            self.cursor.execute(query)
            data = list(self.cursor.fetchall())
        except Exception as e:
            msg = '{} - [{}] Failed to set homework id. error: {}'.format(datetime.datetime.now(), __name__,
                                                                          LogTool.pp_exception(e))
            LogTool.update_slog(self.log_path, msg, 'a')
            return False

        for d in data:
            date_str = str(d[5])
            if self.target_date_dash == date_str:
                self.homework_id = d[0]

    def get_homepage_list(self) -> bool:
        query = '''SELECT * FROM class.student_website;'''
        try:
            self.cursor.execute(query)
            self.homepage_list = list(self.cursor.fetchall())
            return True
        except Exception as e:
            msg = '{} - [{}] Failed to get homepage data from database. error: {}'.format(datetime.datetime.now(),
                                                                                          __name__,
                                                                                          LogTool.pp_exception(e))
            LogTool.update_slog(self.log_path, msg, 'a')
            return False

    def get_target_url(self, url: str, res: requests.request) -> str:
        res.encoding = 'utf-8'
        html = res.text
        doc = BeautifulSoup(html, 'html.parser')
        css_q = 'a[href*="' + self.target_date + '"]'
        element = doc.select(css_q)
        if len(element):
            link = element[0].get('href')
            target_url = urljoin(url, link)
            return target_url

    # entry-point function
    def checking(self):
        for index, data in enumerate(self.homepage_list):
            # xx = 108
            # if index <= xx:  # skipppppp
            #     continue

            student_id = data[0]
            url = data[2]

            # if student_id != '08170219':
            #     continue

            print('{} - START - {} > {}'.format(index, student_id, url))
            mark_result = self.do_marking(student_id, url)
            DbTool.insert_db(self.conn, self.cursor, mark_result)

            print('FINISH\n')

            # if index == xx + 1:
            #     break

            # break

    def do_marking(self, student_id: str, url: str) -> list:
        html_save_path = '{}/{}/{}/{}/index.html'.format(self.root_save_dir, self.target_date[0:4],
                                                         student_id, self.target_date)
        screenshot_save_path = '{}/{}/{}/{}/screen.jpg'.format(self.root_save_dir, self.target_date[0:4],
                                                               student_id, self.target_date)
        gps_json_save_path = '{}/{}/{}/{}/google_speed_result.json'.format(self.root_save_dir, self.target_date[0:4],
                                                                           student_id, self.target_date)

        sheet_path = '{}/{}/{}/{}/html_error.csv'.format(self.root_save_dir, self.target_date[0:4],
                                                               student_id, self.target_date)

        error_mark_id = LogTool.gen_random_token()

        try:
            res = requests.get(url)
        except Exception as e:
            msg = '{} - [{}] Failed to access the homepage. url: {} , error: {}'.format(datetime.datetime.now(),
                                                                                        __name__, url,
                                                                                        LogTool.pp_exception(e))
            LogTool.update_slog(self.log_path, msg, 'a')

            msg = '無法存取首頁'
            return HomepageErrorTool.get_error_record(error_mark_id, student_id, self.homework_id, msg)

        if res.status_code != 200:
            msg = '無法成功讀取網頁, http status: {}'.format(res.status_code)
            return HomepageErrorTool.get_error_record(error_mark_id, student_id, self.homework_id, msg)

        target_url = self.get_target_url(url, res)
        if not target_url:
            msg = '無法獲得該次作業網址 - {}'.format(self.target_date_dash)
            return HomepageErrorTool.get_error_record(error_mark_id, student_id, self.homework_id, msg)

        # mark_id = '{}-{}-{}'.format(student_id, self.homework_id, self.target_date)

        print('CHECKING - {}'.format(target_url))
        page_marker = PageMarker(input_url=target_url,
                                 html_save_path=html_save_path,
                                 screenshot_save_path=screenshot_save_path,
                                 gps_json_save_path=gps_json_save_path,
                                 log_path=self.log_path,
                                 sheet_path=sheet_path)
        page_marker.mark()
        self.create_sheet(student_id, self.homework_id, page_marker)

        return RecordParseTool.get_record_list(student_id, self.homework_id, page_marker)

    def create_sheet(self, student_id: str, homework_id: str, page_marker: PageMarker):
        reduct_result = page_marker.error_list
        df = pd.DataFrame(columns=['student_id', 'score_item_id', 'reduction_item_id', 'times', 'reduct_point', 'info'])
        for rd in reduct_result:
            df.loc[len(df)] = [student_id, homework_id, rd['ckId'], rd['times'], rd['reduct_point'], rd['info']]

        df.to_csv(page_marker.sheet_path, encoding='utf-8', index=False)


# qqq = WACS()
# qqq.launch()
