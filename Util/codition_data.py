# coding=utf-8
from Util.handle_excel import excel_data
from jsonpath_rw import parse
import json
import random
import string
from Common.get_sql import mysql


def split_data(data):
    '''
    拆分单元格数据
    pro_001>data.token
    '''
    try:
        case_id = data.split(">")[0]
        rule_data = data.split(">")[1]
        return case_id, rule_data
    except Exception as e:
        print("前置条件未找到>符号！！")


def depend_data(data, excel_type):
    '''
    获取依赖结果集
    '''
    try:
        case_id = split_data(data)[0]
        # print('case_id--->', case_id)
        row_number = excel_data.get_rows_number(case_id, excel_type)
        # print('row_number--->', row_number)
        data = excel_data.get_cell_value(case_id, row_number, 14, excel_type)
        # print('data--->', data)
        return data
    except Exception as e:
        print("获取依赖结果集失败！！")


def get_depend_data(res_data, key):
    '''
    获取依赖字段
    '''
    if not isinstance(res_data, dict):
        try:
            res_data = json.loads(res_data)
        except:
            print('不需要loads')
    json_exe = parse(key)
    madle = json_exe.find(res_data)
    res = [math.value for math in madle][0]
    return res


def get_random_data(type_data, num):
    '''
        获取随机数
    '''
    if '_str'in type_data:
        data = '测试名称'+''.join(random.sample(string.ascii_letters + string.digits, int(num)))

    elif '_int'in type_data:
        str_start = random.choice(['135', '136', '138'])
        str_end = ''.join(random.sample('0123456789', int(num)-3))
        data = str_start + str_end
    else:
        data = ''
        print("get_random_data获取随机数据失败！！")
    return data


def get_data(data, excel_type):
    '''
    获取依赖数据
    '''
    # cus_006 > data[0].dictId
    try:
        type_data = split_data(data)[0]
        print('type_data--->', type_data)

        if '_str' in type_data or '_int' in type_data:
            num = split_data(data)[1]
            data = get_random_data(type_data, num)
            # print('data_str/int--->', data)
        elif '_sql' in type_data:
            sql = split_data(data)[1]
            print(sql)
            result = mysql.getOne(sql)
            # mysql.dispose()
            print(result)
            for res in result:
                return result[res]
        else:
            res_data = depend_data(data, excel_type)
            rule_data = split_data(data)[1]
            # print('res_data-->',res_data, 'rule_data-->', rule_data)
            data = get_depend_data(res_data, rule_data)

        return data

    except Exception as e:
        print("get_data获取依赖数据失败！！")


def write_depend_data(data, target, str1):
    '''
        根据依赖key，写入数据
    '''
    try:
        if len(target) == 0:
            return str1

        if isinstance(data, str):
            need_json = True
            data = json.loads(data)
        else:
            if len(target) == 1:
                need_json = True
            else:
                if isinstance(data, dict) or isinstance(data, list):
                    need_json = True
                else:
                    need_json = False

        if isinstance(data, list):
            target_index = int(target.pop(0))
        else:
            target_index = target.pop(0)

        if need_json:
            data[target_index] = write_depend_data(data[target_index], target, str1)
        else:
            data[target_index] = json.dumps(write_depend_data(data[target_index], target, str1), ensure_ascii=False)
        return data
    except Exception as e:
        print("write_depend_data 写入依赖数据失败！！")


def write_depend_data_url(url, target, str1):

    try:
        return url.replace(target, str1)
    except Exception as e:
        print("write_depend_data_url写入url失败！！")


if __name__ == "__main__":

    # data1 = {"customerAttribuType":2,"customerIdList":[15483]}
    # key1='propertyId'

    data1 = [{"contactsPerson":"江云云","businessContacts":"[{\"label\":\"微信\",\"value\":\"15677777777\",\"id\":208}]","isVisible":1,"officeId":38164,"createdId":297},{"contactsPerson":"小2开关","businessContacts":"[{\"label\":\"手机\",\"value\":\"12345678911\",\"id\":207}]","businessCompany":"招商企业2","contactsType":227,"ownerIdentity":"","isVisible":0,"officeId":38164,"createdId":295},{"contactsPerson":"黄小姐","businessContacts":"[{\"label\":\"手机\",\"value\":\"12345678912\",\"id\":207}]","businessCompany":"我是一个招商企业","contactsType":227,"ownerIdentity":471,"isVisible":0,"officeId":38164,"createdId":295}]
    key1 = '[0].officeId'

    # print(write_depend_data(data1, ['0', 'officeId'], '111111'))

    # s = '2222222,1233444'
    # s1 = '[' + s + ']'
    # print(write_depend_data(data1, ['ccc', '1', 'qq'], eval(s1)))

    # data2 = {'aa':'bbb', 'bb':[{'ee':'ww'}, {'ss':'rr'}]}
    #
    # print(write_depend_data(data1, ['ccc', '0', 'qq'], '111111'))

    # res = write_depend_data_url('/ao/ob-building/buildingID', 'buildingID', s1)
    # print(res)

    k = get_data("pro_sql>select building_id from test_asset_operation.ob_office_info where deleted = 1 ORDER BY building_id desc LIMIT 1", "case_1.xlsx")
    print(k)
