# coding=utf-8
import logging
import requests
from lxml import etree
import redis

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
r = redis.StrictRedis.from_url('redis://:@localhost:6379/3')
phone_header = {
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
}

chrome_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
}


def get_proxy():
    ipproxy = r.zrange('dazhong_ipproxy:3', 0, 0)
    r.zincrby('dazhong_ipproxy:3', ipproxy[0], 2)
    return {'http': ipproxy[0]}


# 遍历得到所有要抓取的url
def get_meal_type_url(url):
    url_dict = {}
    while 1:
        try:
            ip_proxy = get_proxy()
            resp = requests.get(
                url=url, headers=phone_header, timeout=10, proxies=ip_proxy)
            if resp.status_code == 200:
                break
        except requests.exceptions.Timeout:
            logging.error('timeout!')
            r.zrem('dazhong_ipproxy:3', ip_proxy['http'])
        except:
            logging.error(u'访问失败')
    tree = etree.HTML(resp.content)

    for i in range(1, 30):
        try:
            xpath = '//*[@id="classfy"]/a[%d]' % i
            meal_url = tree.xpath(xpath + '/@href')[0]
            meal_type = tree.xpath(xpath + '/span/text()')[0]
            logging.info(meal_type + u'对应的url为:' + meal_url)
        except:
            continue

        type_url = 'http://www.dianping.com%s' % meal_url
        while 1:
            try:
                ip_proxy = get_proxy()
                resp_type = requests.get(
                    url=type_url, headers=chrome_header, timeout=10, proxies=ip_proxy)
                if resp_type.status_code == 200:
                    break
            except requests.exceptions.Timeout:
                logging.error('timeout!')
                r.zrem('dazhong_ipproxy:3', ip_proxy['http'])
            except:
                logging.error(u'访问失败')

        type_tree = etree.HTML(resp_type.content)
        type_url_dict = {}
        for j in range(2, 15):
            try:
                type_xpath = '//*[@id="classfy-sub"]/a[%d]' % j
                type_url_url = type_tree.xpath(type_xpath + '/@href')[0]
                type_url_type = type_tree.xpath(type_xpath + '/span/text()')[0]
                type_url_dict[type_url_type] = type_url_url
                logging.info(u'%s对应的子菜单 %s url为  %s' %
                             (meal_type, type_url_type, type_url_url))
            except:
                continue

        if not type_url_dict:
            type_url_dict[meal_type] = meal_url

        url_dict[meal_type] = type_url_dict

    return url_dict


if __name__ == "__main__":
    print get_meal_type_url('http://www.dianping.com/search/category/19/10/o3')