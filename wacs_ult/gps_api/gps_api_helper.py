# coding: utf-8
import json
import pathlib
import threading
from configparser import ConfigParser
import requests
import datetime
from pprint import pprint as pp
from wacs_ult.public.save_tool import SaveTool
from wacs_ult.error.log_tool import LogTool


class GPSApiHelper:
    def __init__(self, url: str, gps_json_save_path: str):
        self.config_path = None
        self.config = None
        self.load_config()
        self.api_domain = self.config['apiVersion']['domain']
        self.api_key = self.config['apiKey']['token']
        self.result = False

        # METRICS
        self.metrics_path = None
        self.metrics = None
        self.load_metrics()

        # performance
        self.desktop_weight = float(self.metrics['desktop_performance']['weight'])
        self.desktop_perf = 0
        self.mobile_weight = float(self.metrics['mobile_performance']['weight'])
        self.mobile_perf = 0
        self.score = 0

        # largest_contentful_paint
        self.largest_contentful_paint_dt_weight = float(self.metrics['largest_contentful_paint']['dt_weight'])
        self.largest_contentful_paint_mob_weight = float(self.metrics['largest_contentful_paint']['mob_weight'])
        self.largest_contentful_paint_dt = 0
        self.largest_contentful_paint_mob = 0

        # total_blocking_time
        self.total_blocking_time_dt_weight = float(self.metrics['total_blocking_time']['dt_weight'])
        self.total_blocking_time_mob_weight = float(self.metrics['total_blocking_time']['mob_weight'])
        self.total_blocking_time_dt = 0
        self.total_blocking_time_mob = 0

        # first_contentful_paint
        self.first_contentful_paint_dt_weight = float(self.metrics['first_contentful_paint']['dt_weight'])
        self.first_contentful_paint_mob_weight = float(self.metrics['first_contentful_paint']['mob_weight'])
        self.first_contentful_paint_dt = 0
        self.first_contentful_paint_mob = 0

        # interactive
        self.interactive_dt_weight = float(self.metrics['interactive']['dt_weight'])
        self.interactive_mob_weight = float(self.metrics['interactive']['mob_weight'])
        self.interactive_dt = 0
        self.interactive_mob = 0

        # speed_index
        self.speed_index_dt_weight = float(self.metrics['speed_index']['dt_weight'])
        self.speed_index_mob_weight = float(self.metrics['speed_index']['mob_weight'])
        self.speed_index_dt = 0
        self.speed_index_mob = 0

        # cumulative_layout_shift
        self.cumulative_layout_shift_dt_weight = int(self.metrics['cumulative_layout_shift']['dt_weight'])
        self.cumulative_layout_shift_mob_weight = int(self.metrics['cumulative_layout_shift']['mob_weight'])
        self.cumulative_layout_shift_dt = 0
        self.cumulative_layout_shift_mob = 0

        self.access_timeout = 180
        self.re_access_time = 3

        self.url = url
        self.gps_json_save_path = gps_json_save_path
        self.check_url_desktop = '{}{}&strategy={}&key={}'.format(self.api_domain, self.url, 'DESKTOP', self.api_key)
        self.check_url_mobile = '{}{}&strategy={}&key={}'.format(self.api_domain, self.url, 'MOBILE', self.api_key)
        self.desktop_result = dict()
        self.mobile_result = dict()

    def load_config(self):
        self.config_path = '{}/config.ini'.format(pathlib.Path(__file__).parent.absolute())
        self.config = ConfigParser()
        self.config.read(self.config_path)

    def load_metrics(self):
        self.metrics_path = '{}/metrics.ini'.format(pathlib.Path(__file__).parent.absolute())
        self.metrics = ConfigParser()
        self.metrics.read(self.metrics_path)

    def launch(self):
        self.get_gps_result()
        if not self.check_api_response():
            self.api_error_handler()
            return

        self.get_score()
        self.save_json()

    def api_error_handler(self):
        self.mobile_perf = -1
        self.desktop_perf = -1
        self.score = -1

        msg = '{} - API ERROR: {}'.format(datetime.datetime.now(), self.url)
        LogTool.update_slog(self.config['gpsLog']['path'], msg, 'a')


    def save_json(self):
        data = dict()
        data['desktop'] = self.desktop_result
        data['mobile'] = self.mobile_result
        SaveTool.save_json(self.gps_json_save_path, data)

    # --------------------------------- Get Json ---------------------------------
    def get_gps_result(self):
        desktop = threading.Thread(target=self.access_desktop)
        mobile = threading.Thread(target=self.access_mobile)
        desktop.start()
        mobile.start()
        desktop.join()
        mobile.join()

    def access_desktop(self):
        res = requests.get(self.check_url_desktop)
        res.encoding = 'utf-8'
        self.desktop_result = json.loads(res.text)

    def access_mobile(self):
        res = requests.get(self.check_url_mobile)
        res.encoding = 'utf-8'
        self.mobile_result = json.loads(res.text)

    def check_api_response(self):
        if self.desktop_result.get('error'):
            error_code = self.desktop_result.get('error').get('code')
            return False

        if self.mobile_result.get('error'):
            error_code = self.mobile_result.get('error').get('code')
            return False

        return True

    # --------------------------------- Get Score ---------------------------------
    def get_score(self):
        self.get_largest_contentful_paint()
        self.get_total_blocking_time()
        self.get_first_contentful_paint()
        self.get_interactive()
        self.get_speed_index()
        self.get_cumulative_layout_shift()

        self.desktop_perf = round(self.desktop_perf * self.desktop_weight, 2)
        self.mobile_perf = round(self.mobile_perf * self.mobile_weight, 2)

        self.score = round((self.desktop_perf + self.mobile_perf) / 2, 2)

    def get_largest_contentful_paint(self):
        key_name = self.metrics['largest_contentful_paint']['api_key']

        # Desktop Score
        dt_rs = self.desktop_result.get('lighthouseResult').get('audits').get(key_name).get('score')

        self.largest_contentful_paint_dt = dt_rs * self.largest_contentful_paint_dt_weight
        self.largest_contentful_paint_dt = round(self.largest_contentful_paint_dt, 2)

        # Mobile Score
        mob_rs = self.mobile_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.largest_contentful_paint_mob = mob_rs * self.largest_contentful_paint_mob_weight
        self.largest_contentful_paint_mob = round(self.largest_contentful_paint_mob, 2)

        # add to performance
        self.desktop_perf += self.largest_contentful_paint_dt
        self.mobile_perf += self.largest_contentful_paint_mob

    def get_total_blocking_time(self):
        key_name = self.metrics['total_blocking_time']['api_key']

        # Desktop Score
        dt_rs = self.desktop_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.total_blocking_time_dt = dt_rs * self.total_blocking_time_dt_weight
        self.total_blocking_time_dt = round(self.total_blocking_time_dt, 2)

        # Mobile Score
        mob_rs = self.mobile_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.total_blocking_time_mob = mob_rs * self.total_blocking_time_mob_weight
        self.total_blocking_time_mob = round(self.total_blocking_time_mob, 2)

        # add to performance
        self.desktop_perf += self.total_blocking_time_dt
        self.mobile_perf += self.total_blocking_time_mob

    def get_first_contentful_paint(self):
        key_name = self.metrics['first_contentful_paint']['api_key']

        # Desktop Score
        dt_rs = self.desktop_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.first_contentful_paint_dt = dt_rs * self.first_contentful_paint_dt_weight
        self.first_contentful_paint_dt = round(self.first_contentful_paint_dt, 2)

        # Mobile Score
        mob_rs = self.mobile_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.first_contentful_paint_mob = mob_rs * self.first_contentful_paint_mob_weight
        self.first_contentful_paint_mob = round(self.first_contentful_paint_mob, 2)

        # add to performance
        self.desktop_perf += self.first_contentful_paint_dt
        self.mobile_perf += self.first_contentful_paint_mob

    def get_interactive(self):
        key_name = self.metrics['interactive']['api_key']

        # Desktop Score
        dt_rs = self.desktop_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.interactive_dt = dt_rs * self.interactive_dt_weight
        self.interactive_dt = round(self.interactive_dt, 2)

        # Mobile Score
        mob_rs = self.mobile_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.interactive_mob = mob_rs * self.interactive_mob_weight
        self.interactive_mob = round(self.interactive_mob, 2)

        # add to performance
        self.desktop_perf += self.interactive_dt
        self.mobile_perf += self.interactive_mob

    def get_speed_index(self):
        key_name = self.metrics['speed_index']['api_key']

        # Desktop Score
        dt_rs = self.desktop_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.speed_index_dt = dt_rs * self.speed_index_dt_weight
        self.speed_index_dt = round(self.speed_index_dt, 2)

        # Mobile Score
        mob_rs = self.mobile_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.speed_index_mob = mob_rs * self.speed_index_mob_weight
        self.speed_index_mob = round(self.speed_index_mob, 2)

        # add to performance
        self.desktop_perf += self.speed_index_dt
        self.mobile_perf += self.speed_index_mob

    def get_cumulative_layout_shift(self):
        key_name = self.metrics['cumulative_layout_shift']['api_key']

        # Desktop Score
        dt_rs = self.desktop_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.cumulative_layout_shift_dt = dt_rs * self.cumulative_layout_shift_dt_weight
        self.cumulative_layout_shift_dt = round(self.cumulative_layout_shift_dt, 2)

        # Mobile Score
        mob_rs = self.mobile_result.get('lighthouseResult').get('audits').get(key_name).get('score')
        self.cumulative_layout_shift_mob = mob_rs * self.cumulative_layout_shift_mob_weight
        self.cumulative_layout_shift_mob = round(self.cumulative_layout_shift_mob, 2)

        # add to performance
        self.desktop_perf += self.cumulative_layout_shift_dt
        self.mobile_perf += self.cumulative_layout_shift_mob
