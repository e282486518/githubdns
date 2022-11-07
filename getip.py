#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import re
import requests
from bs4 import BeautifulSoup


class Getip:
    def __init__(self):
        self.reg = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) '
                          'Chrome/52.0.2743.82 Safari/537.36',
        }

    def get(self, site):
        ip = self.chinaz(site)
        if ip == '':
            ip = self.ipapi(site)
        if ip == '':
            ip = self.ipaddress(site)
        if ip == '':
            ip = self.whatismyipaddress(site)
        return ip

    def match(self, result: list) -> str:
        trueip = ''
        if not isinstance(result, list):
            return trueip
        for c in result:
            ip = re.findall(self.reg, c.text)
            if len(ip) != 0:
                trueip = ip[0]
                break
        return trueip

    def ipaddress(self, site):
        url = "https://www.ipaddress.com/site/" + site
        trueip = ''
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            result = soup.find_all('ul', class_="comma-separated")
            trueip = self.match(result)
        except Exception as e:
            print("查询" + site + " 时出现错误: " + str(e))
        return trueip

    def chinaz(self, site):
        url = "https://ip.tool.chinaz.com/" + site
        trueip = ''
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            result = soup.find_all('span', class_="Whwtdhalf w15-0 lh45")
            # print(result)
            trueip = self.match(result)
        except Exception as e:
            print("查询" + site + " 时出现错误: " + str(e))
        return trueip

    def whatismyipaddress(self, site):
        url = "https://whatismyipaddress.com//hostname-ip"
        data = {
            "DOMAINNAME": site,
            "Lookup IP Address": "Lookup IP Address"
        }
        trueip = ''
        try:
            res = requests.post(url, headers=self.headers, data=data, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            result = soup.find_all('span', class_="Whwtdhalf w15-0")
            trueip = self.match(result)
        except Exception as e:
            print("查询" + site + " 时出现错误: " + str(e))
        return trueip

    def ipapi(self, site):
        url = "http://ip-api.com/json/%s?lang=zh-CN" % site
        trueip = ''
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            res = json.loads(res.text)
            if res["status"] == "success":
                trueip = res["query"]
        except Exception as e:
            print("查询" + site + " 时出现错误: " + str(e))
        return trueip


if __name__ == "__main__":
    cls = Getip()
    print(cls.get("github.com"))
