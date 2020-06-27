# coding: utf-8

class ErrorTool:

    @staticmethod
    def get_error_data(ck_id: int, msg: str, times: int, reduct_point: int) -> dict:
        result = dict()
        result['ckId'] = ck_id
        result['info'] = msg
        result['times'] = times
        result['reduct_point'] = reduct_point

        return result
