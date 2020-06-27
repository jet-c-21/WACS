# coding: utf-8
import os
import sys
import traceback
import random


class LogTool:
    bar = '==============================================================================='

    @staticmethod
    def gen_random_token():
        random_token = ''
        for i in range(4):
            j = random.randrange(0, 3)
            if j == 1:
                a = random.randrange(0, 10)
                random_token += str(a)
            elif j == 2:
                a = chr(random.randrange(65, 91))
                random_token += a
            else:
                a = chr(random.randrange(97, 123))
                random_token += a

        return random_token

    @staticmethod
    def generate_log_file_name(date_str) -> str:
        return '{}-{}.txt'.format(date_str, LogTool.gen_random_token())

    @staticmethod
    def update_slog(path=None, msg=None, purpose=None):
        if purpose == 'a':
            # print(msg)
            if os.path.exists(path):
                with open(path, 'a') as f:
                    f.write(msg + '\n')
            else:
                LogTool.init_file(path)
                with open(path, 'a') as f:
                    f.write(msg + '\n')

        elif purpose == 'm':
            with open(path, 'r') as old_file:
                lines = old_file.readlines()
                with open(path, 'r+') as new_file:
                    if len(lines) == 0:
                        lines.append(msg)
                        new_file.writelines(lines)
                    else:
                        lines[-1] = msg
                        new_file.writelines(lines)

    @staticmethod
    def update_browser_log(path=None, worker_name=None, msg=None, purpose=None):
        log_path = '{}/browser/log-{}.txt'.format(path, worker_name)
        if not os.path.exists(log_path):
            with open(log_path, 'w') as f:
                pass

        if purpose == 'a':
            with open(log_path, 'a') as f:
                f.write(msg + '\n')
        elif purpose == 'm':
            with open(log_path, 'r') as old_file:
                lines = old_file.readlines()
                with open(log_path, 'r+') as new_file:
                    lines[-1] = msg
                    new_file.writelines(lines)
        elif purpose == 'ab':
            with open(log_path, 'a') as f:
                f.write(LogTool.bar + '\n')

    @staticmethod
    def add_bar(path):
        with open(path, 'a') as f:
            f.write(LogTool.bar + '\n')

    @staticmethod
    def init_file(path):
        with open(path, 'w') as _:
            return

    @staticmethod
    def pp_exception(e):
        try:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            err_msg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            return err_msg
        except:
            return str(e)
