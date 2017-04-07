# coding=utf-8
import logging
import requests
import re
import json
import time
import random
from pymongo import MongoClient
import sys
from lxml import etree


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, filename='detail.log')
logging.getLogger("requests").setLevel(logging.WARNING)

phone_header = {
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
}

chrome_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
}
base_url = 'http://www.dianping.com/shop/'
mongo = MongoClient('localhost:27017').dazhong


def read_shopid_from_file(filname):
    shopid = []
    shopid_json = open(filname, 'r')
    for line in shopid_json.readlines():
        shopid.append(json.loads(line))
    shopid_json.close()

    return shopid


def crawl_detail(shopid_list, part_num):
    total_len = len(shopid_list)
    step = total_len / 2 + 1
    bulk = mongo.detail.initialize_unordered_bulk_op()
    sucess_total = 0

    for id_list in shopid_list[part_num * step: (part_num + 1) * step]:
        for id in id_list['show_id']:
            time.sleep(random.choice([3, 4]))
            target = base_url + str(id)

            if sucess_total != 0 and sucess_total % 150 == 0:
                bulk.execute()
                bulk = mongo.detail.initialize_unordered_bulk_op()
                logging.info(u'成功处理150条记录')

            try:
                resp = requests.get(url=target, headers=chrome_header)
                resp_content = resp.content
                tree = etree.HTML(resp_content)

                name = tree.xpath('//*[@id="basic-info"]/h1/text()')[0].strip().strip('\n')
                province = u'上海'
                city = u'上海'
                address = tree.xpath('//*[@id="basic-info"]/div[2]/span[2]/text()')[0].strip().strip('\n')
                shopping_area = tree.xpath('//*[@id="body"]/div[2]/div[1]/a[2]/text()')[0].strip().strip('\n')
                if tree.xpath('//*[@id="basic-info"]/p[1]/span[2]/text()'):
                    tel = tree.xpath('//*[@id="basic-info"]/p[1]/span[2]/text()')[0].strip().strip('\n')
                else:
                    tel = ''
                coordinates = tree.xpath('//*[@id="aside"]/script[1]/text()')[0].strip().strip('\n')
                coor = re.search(r'.*\(\{lng:(.*)?,lat:(.*)?\}\)', coordinates)
                lng = coor.group(1)
                lat = coor.group(2)
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
            bulk.insert(detail)
            sucess_total += 1
        time.sleep(30)

    bulk.execute()


if __name__ == "__main__":
    try:
        part_num = int(sys.argv[1])

        shopid_list = read_shopid_from_file('shopid.json')
        crawl_detail(shopid_list, part_num)
    except IndexError:
        logging.error(u'请输入正确的参数, 参数选择 0, 1, 2')

