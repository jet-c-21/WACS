# coding: utf-8
import pymysql
from pprint import pprint as pp


class DbTool:
    @staticmethod
    def insert_db(conn: pymysql.connections, cursor: pymysql.cursors, record_list: list):
        for record in record_list:
            table = record.get('type')
            if table == 'r':
                DbTool.insert_reduction_table(cursor, record)

            elif table == 'g':
                DbTool.insert_gps_table(cursor, record)

            elif table == 's':
                DbTool.insert_score_table(cursor, record)

        conn.commit()

    @staticmethod
    def insert_reduction_table(cursor: pymysql.cursors, record: dict):
        sql = 'INSERT INTO `student_reduction_result` ' \
              '(`mark_id`, `student_code`, `score_item_id`, `reduction_item_id`, `times`, `reduct_point`, `info`) ' \
              'VALUES (%(mark_id)s, %(student_code)s, %(score_item_id)s, %(reduction_item_id)s, %(times)s, %(reduct_point)s, %(info)s)'

        cursor.execute(sql, record)

    @staticmethod
    def insert_gps_table(cursor: pymysql.cursors, record: dict):
        sql = 'INSERT INTO `student_gps_result` ' \
              '(`mark_id`, `student_code`, `score_item_id`, ' \
              '`desktop_performance`, `largest_contentful_paint_dt`, ' \
              '`total_blocking_time_dt`, `first_contentful_paint_dt`,' \
              '`interactive_dt`, `speed_index_dt`, `cumulative_layout_shift_dt`,' \
              '`mobile_performance`,`largest_contentful_paint_mob`,' \
              '`total_blocking_time_mob`, `first_contentful_paint_mob`,' \
              '`interactive_mob`, `speed_index_mob`, `cumulative_layout_shift_mob`) ' \
              'VALUES(%(mark_id)s, %(student_code)s, %(score_item_id)s,' \
              '%(desktop_performance)s, %(largest_contentful_paint_dt)s,' \
              '%(total_blocking_time_dt)s, %(first_contentful_paint_dt)s,' \
              '%(interactive_dt)s, %(speed_index_dt)s, %(cumulative_layout_shift_dt)s,' \
              '%(mobile_performance)s, %(largest_contentful_paint_mob)s,' \
              '%(total_blocking_time_mob)s, %(first_contentful_paint_mob)s,' \
              '%(interactive_mob)s, %(speed_index_mob)s, %(cumulative_layout_shift_mob)s)'

        cursor.execute(sql, record)

    @staticmethod
    def insert_score_table(cursor: pymysql.cursors, record: dict):
        sql = 'INSERT INTO `student_score` ' \
              '(`mark_id`, `student_code`, `score_item_id`, ' \
              '`basic_score`, `reduction_score`, ' \
              '`final_score`, `screen_path`, `page_path`, `google_pagespeed_path`) ' \
              'VALUES(%(mark_id)s, %(student_code)s, %(score_item_id)s, ' \
              '%(basic_score)s, %(reduction_score)s, %(final_score)s, ' \
              '%(screen_path)s, %(page_path)s, %(google_pagespeed_path)s)'

        cursor.execute(sql, record)
