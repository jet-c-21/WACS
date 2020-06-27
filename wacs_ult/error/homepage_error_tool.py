# coding: utf-8

class HomepageErrorTool:
    @staticmethod
    def get_error_record(error_mark_id: str, student_id: str, homework_id: str, error_info: str) -> list:
        output = list()

        # reduct result
        reduct_record = dict()
        reduct_record['type'] = 'r'
        reduct_record['mark_id'] = error_mark_id
        reduct_record['student_code'] = student_id
        reduct_record['score_item_id'] = homework_id
        reduct_record['reduction_item_id'] = 1
        reduct_record['times'] = 1
        reduct_record['reduct_point'] = 100
        reduct_record['info'] = error_info

        output.append(reduct_record)

        # score
        score_record = dict()
        score_record['type'] = 's'
        score_record['mark_id'] = error_mark_id
        score_record['student_code'] = student_id
        score_record['score_item_id'] = homework_id
        score_record['basic_score'] = 0
        score_record['reduction_score'] = 100
        score_record['final_score'] = 0
        score_record['screen_path'] = ''
        score_record['page_path'] = ''
        score_record['google_pagespeed_path'] = ''

        output.append(score_record)

        return output
