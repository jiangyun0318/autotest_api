# coding=utf-8

import unittest
import os
import sys

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)

import datetime
import xlwt
from Base import HTMLTestRunner
from Common.get_excel import get_excel
from Util.handle_mail import handle_mail


def remove_contents(contents, targets):
    """删除targets列表中与contents列表共有的元素"""
    for content in contents:
        while content in targets:
            targets.remove(content)
    return targets


def find_contents(keys, targets):
    """找出targets列表中包含关键字的元素"""
    results = []
    for target in targets:
        if keys in target:
            results.append(target)
    return results


def rmv_by_keys(keys, targets):
    """删除列表中包含关键字的元素"""
    return remove_contents(find_contents(keys, targets), targets)


def add_case(file):
    case_path = os.path.join(base_path, "TestCase")

    if '_ao_1' in file:
        discover = unittest.defaultTestLoader.discover(case_path, pattern='test_case_ao.py')
    elif '_bss_1' in file:
        discover = unittest.defaultTestLoader.discover(case_path, pattern='test_case_bss.py')
    elif '_cms_1' in file:
        discover = unittest.defaultTestLoader.discover(case_path, pattern='test_case_cms.py')
    else:
        discover = unittest.defaultTestLoader.discover(case_path, pattern='excel_case.py')
    return discover


if __name__ == "__main__":

    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    case_path = base_path + "/Case"

    f2 = []
    f = []

    for root, dirs, files in os.walk(case_path):
        f = f + files
        f = list(set(f))
    if '.DS_Store' in f:
        f.remove('.DS_Store')
    if 'case_0.xlsx' in f:
        f.remove('case_0.xlsx')

    # 默认为test
    env = 'test'

    try:
        env = sys.argv[1]
    except:
        # 获取外部参数错误，默认赋值test
        env = 'test'
    finally:
        if env == 'test':
            files1 = rmv_by_keys('beta', f)
            f2 = rmv_by_keys('prod', files1)

        elif env == 'beta':
            files1 = rmv_by_keys('test', f)
            f2 = rmv_by_keys('prod', files1)

        elif env == 'prod':
            files1 = rmv_by_keys('test', f)
            f2 = rmv_by_keys('beta', files1)
        else:
            print('命令执行错误！！')

        for file in f2:

            if ('xls' or 'xlsx' or 'csv') and '_1' in file:
                path_report, titles, descriptions = get_excel(file)
                file_path = base_path + '/Report/' + now + path_report + '_report.html'
                with open(file_path, 'wb') as f:
                    runner = HTMLTestRunner.HTMLTestRunner(stream=f, title=titles,
                                                           description=descriptions)
                    runner.run(add_case(file))
                f.close()

        # new_report_mail = handle_mail.new_file(base_path + '/Report/')
        # # log.info(new_report_mail)
        # handle_mail.send_mail(new_report_mail)
