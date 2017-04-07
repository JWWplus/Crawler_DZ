# coding=utf-8
import sys
import urlparse
from base import Base
import logging
import requests
reload(sys)
sys.setdefaultencoding("utf-8")


class fufei_ip:
    def __init__(self):
        pass

    def crawl(self, url):
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        res = requests.get(url, headers=header)
        resp = res.json()
        return resp

    def parse(self, resp):
        result = []
        for i in resp['data']['proxy_list']:
            try:
                ip = {
                    "ip": i.split(':')[0],
                    "port": i.split(':')[1].split(',')[0],
                    "info": "",
                    "type": 3,
                }
                result.append(ip)
            except Exception as e:
                logging.error('fufei_IP parse error: %s', e)
        return result
