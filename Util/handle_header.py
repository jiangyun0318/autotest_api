# coding=utf-8
from Util.handle_json import read_json


def get_header():
    data = read_json("/Config/header.json")
    return data


def header_md5():
    pass
