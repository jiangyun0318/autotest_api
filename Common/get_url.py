# coding=utf-8
import os
import sys

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)

from Common import get_excel
from Util.handle_init import handle_ini


def get_url(url_old, path_root):

    excel_name = get_excel.get_excel(path_root.split('/')[-1])

    if '_ao' in excel_name:
        base_url = handle_ini.get_value('host')
    elif '_cms' in excel_name:
        base_url = handle_ini.get_value('host1')
    else:
        base_url = handle_ini.get_value('host')

    url = base_url + url_old

    return url


if __name__ == "__main__":
    a = get_url("/1213444", "1/2/3/excel_ao_1.xlsx")
    print(a)
