# coding=utf-8
import time
import multiprocessing
import requests
import logging


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

SNIFFER = {
    'PROCESS_NUM': 16,
    'THREAD_NUM': 500,
    'PROXY_TYPE': [0, 1, 2, 3],
    'TARGET': 'http://ip.taobao.com/service/getIpInfo2.php?ip=myip',
    'TIMEOUT': 5,
    'OUTPUT': True,
    'BACKEND': 'localhost:6379',
    'KEY_PREFIX': 'ipproxy:',
}


class Validator:
    def __init__(self):
        # 测试代理IP的目标
        self.target = SNIFFER['TARGET']
        # 测试延时
        self.timeout = SNIFFER['TIMEOUT']
        # 开启进程数 默认8进程
        self.process_num = SNIFFER['PROCESS_NUM']
        # gevent线程数 默认500
        self.thread_num = SNIFFER['THREAD_NUM']
        # 要筛选的网站开头
        self.site = 'dazhong_'

    def run_in_multiprocess(self, proxy_list):
        """ 多进程 """
        # 创建quene来交换数据
        result_queue = multiprocessing.Queue()
        # 返回与进程数相同对的列表
        proxy_partitions = self.partite_proxy(proxy_list)
        process = []
        for partition in proxy_partitions:
            p = multiprocessing.Process(target=self.validate_job, args=(result_queue, partition))
            p.start()
            process.append(p)

        for p in process:
            p.join()

        result = {}
        for p in process:
            result.update(result_queue.get())

        return result

    def partite_proxy(self, proxy_list):
        """ 按process_num数对proxy_list进行分块 """
        if len(proxy_list) == 0:
            return []

        result = []
        step = len(proxy_list) / self.process_num + 1
        for i in range(0, len(proxy_list), step):
            result.append(proxy_list[i:i + step])

        return result

    def validate_job(self, result_queue, proxy_list):
        result = {}
        while len(proxy_list) > 0:
            # 取出一个ip信息并且从列表中删除
            ip_port = proxy_list.pop()
            is_valid, speed = self.validate(ip_port)
            if is_valid:
                result[ip_port] = speed
                logging.info("got an valid ip: %s, time:%s", ip_port, speed)

        result_queue.put(result)

    def validate(self, ip_port):
        proxies = {
            "http": "%s" % ip_port,
        }
        phone_header = {
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        }
        try:
            res = requests.get(self.target, proxies=proxies, timeout=self.timeout, headers=phone_header)
            resp = res.json()
            if resp['data']['ip'] != '180.168.56.186':
                start = time.time()
                if self.site == 'kaola_':
                    res_kaola = requests.get(url='http://m.kaola.com/', proxies=proxies, timeout=self.timeout,
                                             headers=phone_header)
                    if res_kaola.status_code == requests.codes.ok:
                        speed = time.time() - start
                        logging.debug('validating %s, success, time:%ss', ip_port, speed)
                        return True, speed
                elif self.site == 'yhd_':
                    res_yhd = requests.get(url='http://m.yhd.com/1', proxies=proxies, timeout=self.timeout,
                                           headers=phone_header)
                    if res_yhd.status_code == requests.codes.ok:
                        speed = time.time() - start
                        logging.debug('validating %s, success, time:%ss', ip_port, speed)
                        return True, speed
                elif self.site == 'jumei_':
                    res_jumei = requests.get(url='http://m.jumei.com/', proxies=proxies, timeout=self.timeout,
                                             headers=phone_header)
                    if res_jumei.status_code == requests.codes.ok:
                        speed = time.time() - start
                        logging.debug('validating %s, success, time:%ss', ip_port, speed)
                        return True, speed
                elif self.site == 'dazhong_':
                    res_dazhong = requests.get(url='http://www.dianping.com/', proxies=proxies, timeout=self.timeout,
                                             headers=phone_header)
                    if res_dazhong.status_code == requests.codes.ok:
                        speed = time.time() - start
                        logging.info('validating %s, success, time:%ss', ip_port, speed)
                        return True, speed
        except Exception as e:
            logging.info("validating %s, fail: %s", ip_port, e)

        return False, 0
