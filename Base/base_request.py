# coding=utf-8

import os
import sys

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)

import requests.packages
import requests
import json

from requests.adapters import HTTPAdapter

s = requests.session()

s.mount('http://', HTTPAdapter(max_retries=3))  # 重试3次
s.mount('https://', HTTPAdapter(max_retries=3))


class BaseRequest:
    # 发送post请求
    def send_post(self, url, data, cookie=None, get_cookie=None, header=None):

        if get_cookie != None:
            pass

        # 忽略https的警告信息
        requests.packages.urllib3.disable_warnings()
        response = s.post(url=url, data=data, cookies=cookie, headers=header, verify=False, timeout=15)
        res = response.text
        return res

    # 发视get请求
    def send_get(self, url, data, cookie=None, get_cookie=None, header=None):

        if get_cookie != None:
            pass

        # 忽略https的警告信息
        requests.packages.urllib3.disable_warnings()
        response = s.get(url=url, params=data, cookies=cookie, headers=header, verify=False, timeout=15)
        res = response.text
        return res

    # 发视put请求
    def send_put(self, url, data, cookie=None, get_cookie=None, header=None):

        if get_cookie != None:
            pass

        # 忽略https的警告信息
        requests.packages.urllib3.disable_warnings()
        response = s.put(url=url, data=data, cookies=cookie, headers=header, verify=False, timeout=15)
        res = response.text
        return res

    # 发视patch请求
    def send_patch(self, url, data, cookie=None, get_cookie=None, header=None):

        if get_cookie != None:
            pass

        # 忽略https的警告信息
        requests.packages.urllib3.disable_warnings()
        response = s.patch(url=url, data=data, cookies=cookie, headers=header, verify=False, timeout=15)
        res = response.text
        return res

    # 发视delete请求
    def send_delete(self, url, data, cookie=None, get_cookie=None, header=None):

        if get_cookie != None:
            pass

        # 忽略https的警告信息
        requests.packages.urllib3.disable_warnings()
        response = s.delete(url=url, data=data, cookies=cookie, headers=header, verify=False, timeout=15)
        res = response.text
        return res

    # 执行方法，传递method、url、data参数
    def run_main(self, method, url, data, cookie=None, get_cookie=None, header=None):

        if method == 'get':
            res = self.send_get(url, data, cookie, get_cookie, header)
        elif method == 'post':
            res = self.send_post(url, data, cookie, get_cookie, header)
        elif method == 'put':
            res = self.send_put(url, data, cookie, get_cookie, header)
        elif method == 'delete':
            res = self.send_delete(url, data, cookie, get_cookie, header)
        else:
            res = self.send_patch(url, data, cookie, get_cookie, header)
        try:
            res = json.loads(res)
        except:
            print("这个结果是一个text")
        return res


request = BaseRequest()

if __name__ == "__main__":
    request = BaseRequest()
    header = {"token": "1f2fc5d3-7720-4e06-8d97-c3693f0e07e7", "Content-Type": "application/json"}
    # header = {"Content-Type": "application/json"}
    res = request.run_main('post', 'https://baoweb.distrii.com/api/ao/jointBrand/queryjointBrandList', '{"page":1,"pageSize":9}', None, None, header)
    print(res)
