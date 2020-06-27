# coding: utf-8

from page_marker import PageMarker


class RecordParseTool:
    @staticmethod
    def get_record_list(student_id: str, homework_id, page_marker: PageMarker) -> list:
        RESULT = []
        mark_id = page_marker.mark_id

        RecordParseTool.load_reduct_record(RESULT, mark_id, student_id, homework_id, page_marker)
        RecordParseTool.load_gps_record(RESULT, mark_id, student_id, homework_id, page_marker)
        RecordParseTool.load_score_record(RESULT, mark_id, student_id, homework_id, page_marker)

        return RESULT

    @staticmethod
    def load_reduct_record(result: list, mark_id: str, student_id: str, homework_id, page_marker: PageMarker):
        # create reduct result record
        error_list = page_marker.error_list
        for error in error_list:
            reduct_record = dict()
            reduct_record['type'] = 'r'
            reduct_record['mark_id'] = mark_id
            reduct_record['student_code'] = student_id
            reduct_record['score_item_id'] = homework_id
            reduct_record['reduction_item_id'] = error.get('ckId')
            reduct_record['times'] = error.get('times')
            reduct_record['reduct_point'] = error.get('reduct_point')
            reduct_record['info'] = error.get('info')

            result.append(reduct_record)

    @staticmethod
    def load_gps_record(result: list, mark_id: str, student_id: str, homework_id, page_marker: PageMarker):
        gps_record = dict()
        gps_data = page_marker.gps
        if not page_marker.vital_error and gps_data:
            gps_record['type'] = 'g'
            gps_record['mark_id'] = mark_id
            gps_record['student_code'] = student_id
            gps_record['score_item_id'] = homework_id
            gps_record['desktop_performance'] = gps_data.desktop_perf
            gps_record['largest_contentful_paint_dt'] = gps_data.largest_contentful_paint_dt
            gps_record['total_blocking_time_dt'] = gps_data.total_blocking_time_dt
            gps_record['first_contentful_paint_dt'] = gps_data.first_contentful_paint_dt
            gps_record['interactive_dt'] = gps_data.interactive_dt
            gps_record['speed_index_dt'] = gps_data.speed_index_dt
            gps_record['cumulative_layout_shift_dt'] = gps_data.cumulative_layout_shift_dt
            gps_record['mobile_performance'] = gps_data.mobile_perf
            gps_record['largest_contentful_paint_mob'] = gps_data.largest_contentful_paint_mob
            gps_record['total_blocking_time_mob'] = gps_data.total_blocking_time_mob
            gps_record['first_contentful_paint_mob'] = gps_data.first_contentful_paint_mob
            gps_record['interactive_mob'] = gps_data.interactive_mob
            gps_record['speed_index_mob'] = gps_data.speed_index_mob
            gps_record['cumulative_layout_shift_mob'] = gps_data.cumulative_layout_shift_mob

            result.append(gps_record)

    @staticmethod
    def load_score_record(result: list, mark_id: str, student_id: str, homework_id, page_marker: PageMarker):
        score_record = dict()
        if not page_marker.vital_error:
            score_record['type'] = 's'
            score_record['mark_id'] = mark_id
            score_record['student_code'] = student_id
            score_record['score_item_id'] = homework_id
            score_record['basic_score'] = page_marker.gps_score
            # score_record['add_score'] = 0
            score_record['reduction_score'] = page_marker.reduct_score
            score_record['final_score'] = page_marker.total_score
            score_record['screen_path'] = page_marker.screenshot_save_path
            score_record['page_path'] = page_marker.html_save_path
            score_record['google_pagespeed_path'] = page_marker.gps_json_save_path

        else:
            score_record['type'] = 's'
            score_record['mark_id'] = mark_id
            score_record['student_code'] = student_id
            score_record['score_item_id'] = homework_id
            score_record['basic_score'] = page_marker.gps_score
            # score_record['add_score'] = 0
            score_record['reduction_score'] = page_marker.reduct_score
            score_record['final_score'] = page_marker.total_score
            score_record['screen_path'] = page_marker.screenshot_save_path
            score_record['page_path'] = page_marker.html_save_path
            score_record['google_pagespeed_path'] = ''

        result.append(score_record)
