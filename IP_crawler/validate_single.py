# coding=utf-8
import time
import requests
import logging

SNIFFER = {
    'PROCESS_NUM': 4,
    'THREAD_NUM': 500,
    'PROXY_TYPE': [0, 1, 2, 3],
    'TARGET': 'http://ip.taobao.com/service/getIpInfo2.php?ip=myip',
    'TIMEOUT': 2,
    'OUTPUT': True,
    'BACKEND': 'localhost:6379',
    'KEY_PREFIX': 'ipproxy:',
}

LOGGER = {
    "PATH": './ipproxy.log'
}


class Validator:
    def __init__(self):
        # 测试代理IP的目标
        self.target = SNIFFER['TARGET']
        # 测试延时
        self.timeout = SNIFFER['TIMEOUT']
        # 开启进程数 默认4进程
        self.process_num = SNIFFER['PROCESS_NUM']
        # gevent线程数 默认500
        self.thread_num = SNIFFER['THREAD_NUM']

    def run_in_multiprocess(self, proxy_list):
        return self.validate_job(proxy_list)

    def validate_job(self, proxy_list):
        result = {}
        while len(proxy_list) > 0:
            # 取出一个ip信息并且从列表中删除
            ip_port = proxy_list.pop()
            is_valid, speed = self.validate(ip_port)
            if is_valid:
                result[ip_port] = speed
                logging.info("got an valid ip: %s, time:%s", ip_port, speed)

        return result

    def validate(self, ip_port):
        proxies = {
            "http": "%s" % ip_port,
        }
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        try:
            start = time.time()
            res = requests.get(self.target, proxies=proxies, timeout=self.timeout, headers=header)
            resp = res.json()
            if res.status_code == requests.codes.ok and resp['data']['ip'] != '180.168.56.186':
                speed = time.time() - start
                logging.debug('validating %s, success, time:%ss', ip_port, speed)
                return True, speed

        except Exception as e:
            logging.debug("validating %s, fail: %s", ip_port, e)

        return False, 0
