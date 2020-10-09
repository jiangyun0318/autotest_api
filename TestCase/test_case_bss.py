# coding=utf-8

import os
import sys

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)

import os
from Util.handle_excel import excel_data
import unittest
import ddt
from Base import myddt
from TestCase.public_excel import test_run_main
from Common.get_excel import get_path_root


path_root = get_path_root(base_path + '/Case/crm/')
data = excel_data.get_excel_data(path_root)


@myddt.ddt
class TestCase01(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @myddt.data(*data)
    def test_bss_case001(self, data):
        test_run_main.test_run_case(data, path_root)


if __name__ == "__main__":
    unittest.main()
