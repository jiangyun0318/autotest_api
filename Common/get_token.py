# coding=utf-8
import json
from Base.base_request import request
from Util.handle_json import write_value
from Common.get_url import get_url
from Util.handle_json import get_value
from Util.handle_init import handle_ini


def get_token(path_root):

    token = {}

    type= path_root.split('/')[-1]

    # 默认为资运的用例
    if 'case_1' in type or 'ao' in type or 'cms' in type:
        excel_type = 'ao'
    else:
        excel_type = 'ao'

    # 目前cms与资运均是用的同一个登录接口
    type = get_value(excel_type, "/Config/token.json")

    url_old = type['url']
    data = type['data']
    header = type['header']

    # 目前cms与资运均是用的同一个登录接口
    base_url = handle_ini.get_value('host')

    url = base_url + url_old

    result = request.run_main("post", url, json.dumps(data), None, None, header)

    print(result)

    token["token"] = result["data"]["token"]
    token["Content-Type"] = "application/json"

    write_value(token, '/Config/header.json')

    return token


if __name__ == "__main__":
    a = get_token("1/2/3/excel_crm_1.excel")
    print(a)
