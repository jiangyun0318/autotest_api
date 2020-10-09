# coding=utf-8

import os
import sys


def get_excel(file):
    # 获取并分析case名称

    titles = '接口测试报告'
    descriptions = '相关接口测试用例执行情况'
    path_report = ''

    if 'ao' in file:
        if '1' in file:
            titles = '资运后台接口测试报告!'
            descriptions = '资运相关的接口用例执行情况!'
            path_report = '_ao'

    elif 'bss' in file:
        if '1' in file:
            titles = 'bss接口测试报告!'
            descriptions = 'bss相关的接口用例执行情况!'
            path_report = '_bss'

    elif 'cms' in file:
        if '1' in file:
            titles = 'cms接口测试报告!'
            descriptions = 'cms相关的接口用例执行情况!'
            path_report = '_cms'

    else:
        titles = '调试测试报告~!'
        descriptions = '接口用例执行情况~!'
        path_report = '_ceshi'

    return path_report, titles, descriptions


def get_case_path(env, path):
    if '/ao' in path:
        return path + 'case_ao_1_' + env + '.xlsx'
    elif '/cms' in path:
        return path + 'case_cms_1_' + env + '.xlsx'
    else:
        return path + 'case_bss_1_' + env + '.xlsx'


def get_path_root(path):

    # 默认为test
    env = 'test'
    try:
        env = sys.argv[1]
    except:
        env = 'test'
    finally:
        for root, dirs, files in os.walk(path):
            for file in files:
                if '.DS_Store' in file:
                    continue
                if '_1' in file and  env in file:
                    return get_case_path(env, path)
                else:
                    if 'case_1' in file:
                        return path + 'case_1.xlsx'
            return None
        return None


if __name__ == "__main__":
    a = get_path_root('/Users/jiangyun/Documents/autotest/Case/ao/')
    print(a)
