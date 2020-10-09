# coding=utf-8

import os
import sys
import re

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)

from Util.handle_excel import excel_data
import unittest
import requests
import json
import urllib.request
from Util.handle_header import get_header
from Util.handle_result import handle_result_json,handle_result_json_section, handle_result_sql
from Base.base_request import request
from Common.get_url import get_url
from Util.codition_data import get_data, write_depend_data_url, write_depend_data, get_depend_data
from Util.handle_json import write_value


@unittest.skip('执行标识为no，跳过不执行')
def skip():
    pass


class TestRunMain(unittest.TestCase):

    def test_run_case(self, data, excel_type):

        cookie = None
        get_cookie = None
        header = None
        data_token = {}

        is_run = data[2]

        if is_run == 'no':
            skip()
        else:
            case_id = data[0]
            i = excel_data.get_rows_number(case_id, excel_type)
            method = data[6]
            url_old = data[5]
            url = get_url(url_old, excel_type)

            # 针对URL中的中文进行URL编码
            regex = re.compile("[\u4e00-\u9fa5]+")
            convert = str(regex.findall(url))
            url = url.replace(convert, urllib.request.quote(convert))

            if data[7]:
                data1 = json.loads(data[7])
            else:
                data1 = ''

            is_header = data[9]
            excepect_method = data[10]
            excepect_result = data[11]
            is_depend = data[3]
            data_depend = data[4]

            try:

                if is_depend and data_depend:
                    '''
                    获取依赖数据，并赋值到目标接口data或者url中
                    '''
                    # 多个依赖，兼容中英文符号，过滤末尾换行
                    depend = (is_depend.replace("；", ";")).split(';', -1)
                    depend_key = (data_depend.replace("；", ";")).split(';', -1)

                    depend = [x.strip() for x in depend if x.strip() != '']
                    depend_key = [x.strip() for x in depend_key if x.strip() != '']

                    # print('depend--->', depend)

                    j = 0
                    depend_data = ''

                    for depend1 in depend:
                        depend2 = (depend1.replace("，", ",")).split(',', -1)
                        # print('depend2---->', depend2)
                        n = 0
                        # 处理一个字段多值的情况
                        for depend3 in depend2:
                            if n == 0:
                                depend_data = str(get_data(depend3, excel_type))
                                print('depend_data--->', depend_data)
                            else:
                                # print('depend3--->', depend3)
                                depend_data = depend_data + ',' + str(get_data(depend3, excel_type))
                            n += 1

                        # print(data1)
                        # print(depend_key[j])

                        # 根据data字段值，是字符串还是列表，赋值的时候相应的处理
                        if data1 != '' and isinstance(get_depend_data(data1, depend_key[j]), list):
                            s1 = '[' + depend_data + ']'
                            # print('依赖是list类型-------->', s1)
                            depend_data = eval(s1)
                        else:
                            depend_data = str(depend_data)
                            # print('依赖是str类型-------->', depend_data)

                        # 根据依赖key，赋值到相应的字段中（仅支持处理get的数据）
                        if data1 == '':
                            url = write_depend_data_url(url, depend_key[j], str(depend_data))
                        else:
                            tmp = depend_key[j].replace('[', '.').replace(']', '')
                            depend_key2 = tmp.split('.', -1)
                            data1 = write_depend_data(data1, depend_key2, depend_data)

                        j += 1

                    # print('depend_key-->',depend_key)
                    # print('depend_data-->', depend_data)
                    # print('data1-->', data1)

                if is_header == 'yes_token':
                    header = get_header()
                else:
                    header = {"Content-Type": "application/json"}

                # 针对URL中的中文进行URL编码,赋依赖值后也存在中文情况
                regex = re.compile("[\u4e00-\u9fa5]+")
                convert = str(regex.findall(url))
                url = url.replace(convert, urllib.request.quote(convert))

                if method == 'get':
                    res = request.run_main(method, url, data1, cookie, get_cookie, header)
                else:
                    res = request.run_main(method, url, json.dumps(data1), cookie, get_cookie, header)

                # 若有登录接口，获取其中的token
                if 'userLogin' in url:
                    if res['code'] == 0:
                        data_token["token"] = res['data']["token"]
                        data_token["Content-Type"] = "application/json"
                        write_value(data_token, '/Config/header.json')

                try:
                    code = res['code']
                    message = res['msg']
                except Exception as e:
                    code = -1
                    message = '接口错误'
                    print('入参格式错误！请检查！！status-->', res['status'])
                    raise e

                if excepect_method == 'json':
                    result = handle_result_json(res, json.loads(excepect_result))
                    try:
                        self.assertTrue(result)
                        excel_data.excel_write_data(case_id, i, 13, "通过", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res), excel_type)
                    except Exception as e:
                        excel_data.excel_write_data(case_id, i, 13, "失败", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res).encode('latin-1').decode('unicode_escape'), excel_type)
                        raise e

                elif excepect_method == 'json_section':
                    result_depend_data, re_json_data = handle_result_json_section(res, excepect_result)
                    try:
                        self.assertEqual(str(result_depend_data), str(re_json_data))
                        excel_data.excel_write_data(case_id, i, 13, "通过", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res), excel_type)
                    except Exception as e:
                        excel_data.excel_write_data(case_id, i, 13, "失败", excel_type)
                        excel_data.excel_write_data(case_id, i, 14,'result_res==%s,result_json==%s' % (result_depend_data, re_json_data),excel_type)
                        raise e

                elif excepect_method == 'msg':
                    try:
                        self.assertEqual(message, excepect_result)
                        excel_data.excel_write_data(case_id, i, 13, "通过", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res), excel_type)
                    except Exception as e:
                        excel_data.excel_write_data(case_id, i, 13, "失败", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res).encode('latin-1').decode('unicode_escape'), excel_type)
                        raise e

                elif excepect_method == 'code':
                    try:
                        self.assertEqual(code, excepect_result)
                        excel_data.excel_write_data(case_id, i, 13, "通过", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res), excel_type)
                    except Exception as e:
                        excel_data.excel_write_data(case_id, i, 13, "失败", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res).encode('latin-1').decode('unicode_escape'), excel_type)
                        raise e

                elif excepect_method == 'sql':
                    result_depend_data, re_sql_data = handle_result_sql(res, excepect_result)
                    try:
                        self.assertEqual(str(result_depend_data), str(re_sql_data))
                        excel_data.excel_write_data(case_id, i, 13, "通过", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, json.dumps(res), excel_type)
                    except Exception as e:
                        excel_data.excel_write_data(case_id, i, 13, "失败", excel_type)
                        excel_data.excel_write_data(case_id, i, 14, 'result_res==%s,result_sql==%s'%(result_depend_data,re_sql_data), excel_type)
                        raise e

                else:
                    print("期望结果方式错误，目前只支持json/msg/code/sql比较！")
                    excel_data.excel_write_data(case_id, i, 13, "不通过，预期结果方式目前只支持json/msg/code!", excel_type)

            except requests.exceptions.ConnectionError:
                requests.status_code = "Connection refused"

            except Exception as e:
                excel_data.excel_write_data(case_id, i, 13, "失败", excel_type)
                raise e


test_run_main = TestRunMain()
