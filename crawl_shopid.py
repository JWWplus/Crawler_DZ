# coding=utf-8
import logging
import requests
import re
import json
import random
from get_type_url import get_meal_type_url
from pymongo import MongoClient
from lxml import etree
import sys
import redis
r = redis.StrictRedis.from_url('redis://:@localhost:6379/3')

"""
ssh -i xingin_xhs_crawler.pem ec2-user@ec2-54-222-224-200.cn-north-1.compute.amazonaws.com.cn -o serveraliveinterval=60
ssh -i xingin_xhs_crawler.pem ec2-user@ec2-54-223-28-44.cn-north-1.compute.amazonaws.com.cn -o serveraliveinterval=60
ssh -i xingin_xhs_crawler.pem ec2-user@ec2-54-223-147-222.cn-north-1.compute.amazonaws.com.cn -o serveraliveinterval=60
"""
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.basicConfig(filename='error.log', level=logging.ERROR)
logging.getLogger("requests").setLevel(logging.WARNING)

phone_header = {
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
}

chrome_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
}
base_url = 'http://www.dianping.com'
base_shop_url = 'http://www.dianping.com/shop/'
mongo = MongoClient('localhost:27017').dazhong
all_url_dict = {
    u'西安': 'http://www.dianping.com/search/category/17/10/o3',
    u'大连': 'http://www.dianping.com/search/category/19/10/o3',
    u'沈阳': 'http://www.dianping.com/search/category/18/10/o3',
    u'厦门': 'http://www.dianping.com/search/category/15/10/o3',
    u'常熟': 'http://www.dianping.com/search/category/417/10/o3'
}


def get_proxy():
    ipproxy = r.zrange('dazhong_ipproxy:3', 0, 0)
    r.zincrby('dazhong_ipproxy:3', ipproxy[0], 2)
    return {'http': ipproxy[0]}


def get_shop_id(url, num):
    url_dict = get_meal_type_url(url)
    if url_dict == -1:
        return -1
    else:
        for type in url_dict:
            for sub_type in url_dict[type]:
                info = []
                sub_type_url = base_url + url_dict[type][sub_type]
                for i in range(1, 51):
                    target = sub_type_url + 'p' + str(i)
                    try:
                        logging.info(u'start to crawl url %s' % target)
                        while 1:
                            try:
                                ip_proxy = get_proxy()
                                resp = requests.get(
                                    url=target, headers=chrome_header, timeout=10, proxies=ip_proxy)
                                if resp.status_code == requests.codes.ok:
                                    break
                                elif resp.status_code == 404:
                                    logging.error(u'无第%d页' % i)
                                    break
                                else:
                                    logging.error(u'代理被拒绝!')
                                    r.zrem('dazhong_ipproxy:3', ip_proxy['http'])
                            except:
                                logging.error(u'timeout ! 或者代理被拒绝!')
                                r.zrem('dazhong_ipproxy:3', ip_proxy['http'])

                        shop_id_by_re = re.search(
                            r".*,shops:'(.*?)',note:", resp.content)
                        total_id = shop_id_by_re.group(1)
                        shop_id = json.loads(total_id)

                        for j in range(len(shop_id)):
                            info.append(shop_id[j]['s'])

                    except AttributeError:
                        logging.error(u'url无第%d页' % i)
                        break
                    except requests.exceptions.Timeout:
                        logging.error(u'抓取timeout!')
                        r.zrem('dazhong_ipproxy:3', ip_proxy['http'])

                    except:
                        logging.error(u'页面抓取失败,失败url为%s' % target)

                crawl_detail(info, num)


def crawl_detail(shopid_list, num):
    sucess_total = 0
    insert_list = []
    for id in shopid_list:
        target = base_shop_url + str(id)

        if sucess_total != 0 and sucess_total % 150 == 0 and insert_list:
            mongo.shopdetail.insert_many(insert_list)
            insert_list = []
            logging.info(u'成功处理150条记录')

        try:
            while 1:
                try:
                    logging.info('start to crawl url %s' % target)
                    ip_proxy = get_proxy()
                    resp = requests.get(url=target, headers=chrome_header, proxies=ip_proxy, timeout=5)
                    if resp.status_code == requests.codes.ok:
                        break
                    else:
                        r.zrem('dazhong_ipproxy:3', ip_proxy['http'])
                except:
                    logging.error(u'代理被拒绝!')
                    r.zrem('dazhong_ipproxy:3', ip_proxy['http'])

            resp_content = resp.content
            tree = etree.HTML(resp_content)

            name = tree.xpath('//*[@id="basic-info"]/h1/text()')[0].strip().strip('\n')
            province = ''
            city = all_url_dict.keys()[num - 1]

            address = tree.xpath('//*[@id="basic-info"]/div[2]/span[2]/text()')[0].strip().strip('\n')
            shopping_area = tree.xpath('//*[@id="body"]/div[2]/div[1]/a[2]/text()')[0].strip().strip('\n')
            if tree.xpath('//*[@id="basic-info"]/p[1]/span[2]/text()'):
                tel = tree.xpath('//*[@id="basic-info"]/p[1]/span[2]/text()')[0].strip().strip('\n')
            else:
                tel = ''
            coordinates = tree.xpath('//*[@id="top"]/script[2]/text()')[0].strip().strip('\n')
            coor_lng = re.search(r'.*shopGlng:"(.*)?".*', coordinates)
            coor_lat = re.search(r'.*shopGlat: "(.*)?".*', coordinates)
            lng = coor_lng.group(1)
            lat = coor_lat.group(1)
            shop_type = tree.xpath('//*[@id="body"]/div[2]/div[1]/a[3]/text()')[0].strip().strip('\n')
            pic_list = []

            for i in range(1, 5):
                if tree.xpath('//*[@id="aside"]/div[1]/div/div[2]/div/ul/li[%d]/a/img/@src' % i):
                    pic_list.append(tree.xpath('//*[@id="aside"]/div[1]/div/div[2]/div/ul/li[%d]/a/img/@src' % i)[0])

            if not pic_list:
                pic_list.append(tree.xpath('//*[@id="aside"]/div[1]/div/a/img/@src')[0])

        except IndexError:
            logging.error(u'解析未成功,xpath/re 在该页面提取失败 url=%s' % target)
            continue

        except:
            logging.error(u'解析未成功,url=%s' % target)
            continue

        detail = {
            'name': name,
            'province': province,
            'city': city,
            'address': address,
            'shopping_area': shopping_area,
            'tel': tel,
            'lng': lng,
            'lat': lat,
            'shop_type': shop_type,
            'pic': pic_list,
            'source': 'dz',
        }
        insert_list.append(detail)
        sucess_total += 1

    if insert_list:
        mongo.shopdetail.insert_many(insert_list)


if __name__ == "__main__":
    num = int(sys.argv[1])
    url = all_url_dict.values()[num - 1]
    get_shop_id(url, num)
