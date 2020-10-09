# coding=utf-8

import json
import os
import sys

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)


def read_json(file_name=None):
    if file_name == None:
        file_path = base_path+"/Config/user_data.json"
    else:
        file_path = base_path+file_name

    with open(file_path,encoding='UTF-8') as f:
        data = json.load(f)
    return data


def get_value(key, file_name=None):
    data = read_json(file_name)
    return data.get(key)
    #return data[key]


def write_value(data, file_name=None):
    data_value  = json.dumps(data)
    if file_name == None:
        path  = base_path+"/Config/cookie.json"
    else:
        path = base_path+file_name
    with open(path, "w") as f:
        f.write(data_value)


# if __name__ == "__main__":
#     data = {
#         "token": '111111'
#     }
#
#     write_value(data, '/Config/header.json')
