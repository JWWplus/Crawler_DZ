# coding: utf-8
from jindong_url import total_link
import requests
import logging
from lxml import etree
import redis
from pymongo import MongoClient
import re
import json


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
r = redis.StrictRedis.from_url('redis://:55f7b56ab5e13921e0935e92@dataTask01:63799/3')
jd_crawler = MongoClient("localhost:27017").crawler

chrome_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
}
base_url = "https://list.jd.com"
error_list = []
name_map = {
    'jiaoyongdianqi': u'家用电器',
    'shouji': u'手机',
    'shuma': u'数码',
    'diannao_bangong': u'电脑办公',
    'jiaju_jiazhuang': u'家居家装',
    'chuju': u'厨具',
    'jiaju': u'家具',
    'fushi_neiyi': u'服饰内衣',
    'meizhuang_gehu': u'美妆个护',
    'chongwushenghuo': u'宠物生活',
    'xiexue': u'鞋靴',
    'liping_xiangbao': u'礼品箱包',
    'zhongbiao': u'钟表',
    'yundonghuwai': u'运动户外',
    'qicheyongping': u'汽车用品',
    'wanjuyueqi': u'玩具乐器',
    'muyin': u'母婴',
    'jiulei': u'酒类',
    'shipingyinliao': u'食品饮料',
    'shengxian': u'生鲜',
    'yiyaobaojian': u'医药保健',
}


def get_proxy():
    ipproxy = r.zrange('jd_ipproxy:3', 0, 0)
    r.zincrby('jd_ipproxy:3', ipproxy[0], 2)
    return {'http': ipproxy[0]}


def get_all_url():
    for first_title in total_link:
        for second_title in total_link[first_title]:
            logging.info("start to crawl the url %s first title is %s, second title is %s" % (total_link[first_title][second_title], first_title, second_title))
            try:
                ip_proxy = get_proxy()
                resp = requests.get(url=total_link[first_title][second_title], headers=chrome_header, timeout=5, proxies=ip_proxy)
                page = etree.HTML(resp.content)
                if page.xpath('//*[@id="J_crumbsBar"]/div/div/div/div[3]/div/div[2]/ul/li'):
                    for li in page.xpath('//*[@id="J_crumbsBar"]/div/div/div/div[3]/div/div[2]/ul/li'):
                        for li_info in li:
                            jd_crawler.jd_url.insert({
                                'fisrt_title': first_title,
                                'second_title': second_title,
                                'third_title': li_info.xpath('@title')[0],
                                'third_title_url': base_url + li_info.xpath('@href')[0],
                            })
            except Exception as e:
                logging.error('error,url is %s first title is %s, second title is %s' % (total_link[first_title][second_title], first_title, second_title))
                error_list.append(total_link[first_title][second_title])
                continue


def get_tab_detail():
    third_title_url_list = list(jd_crawler.jd_url.find())
    for url in third_title_url_list:
        try:
            url_dict = {}
            url_dict['selector'] = {}
            fourth_title_url = {}
            logging.info("start to crawle url %s,first title is %s, second title is %s, third title is %s" % (url['third_title_url'], name_map[url['fisrt_title']], url['second_title'], url['third_title']))
            ip_proxy = get_proxy()
            resp = requests.get(url=url['third_title_url'], headers=chrome_header, timeout=5, proxies=ip_proxy)

            page = etree.HTML(resp.content)
            url_dict[u'第一分类'] = name_map[url['fisrt_title']]
            url_dict[u'第二分类'] = url['second_title']
            url_dict[u'第三分类'] = url['third_title']
            url_dict[u'第四分类'] = ''
            if re.search(r'other_exts =(.*)?;', resp.content):
                result = re.search(r'other_exts =(.*)?;', resp.content)
                other_exts = result.group(1)
                exts = json.loads(other_exts)
                for kind in exts:
                    if u'大家说' in kind['name']:
                        continue
                    url_dict['selector'][kind['name']] = [i.strip() for i in kind['value_name'].split(';')]
                    if u'分类' in kind['name']:
                        name_id = kind['id']
                        value_id = [i.strip() for i in kind['value_id'].split(';')]
                        for ids in value_id:
                            fourth_title_url[[i.strip() for i in kind['value_name'].split(';')][value_id.index(ids)]] = (url['third_title_url'] + u'&ev={0}_{1}&sort=sort_totalsales15_desc&trans=1&JL=3_分类_{2}#J_crumbsBar'.format(name_id, ids, [i.strip() for i in kind['value_name'].split(';')][value_id.index(ids)]))
            if page.xpath('//*[@id="J_selector"]/div[@class="J_selectorLine s-line J_selectorFold"]'):
                for tab in page.xpath('//*[@id="J_selector"]/div[@class="J_selectorLine s-line J_selectorFold"]'):
                    if u'价格' in tab.xpath('div/div[@class="sl-key"]/span/text()')[0] or u'大家说' in tab.xpath('div/div[@class="sl-key"]/span/text()')[0]:
                        continue
                    else:
                        kind = tab.xpath('div/div[@class="sl-key"]/span/text()')[0]
                        kind_type = tab.xpath('div/div[@class="sl-value"]/div/ul/li/a/text()')
                        url_dict['selector'][kind] = kind_type
                        if u'分类' in kind:
                            text_list = tab.xpath('div/div[@class="sl-value"]/div/ul/li/a/text()')    
                            fourth_title = [u'https://list.jd.com' + i for i in tab.xpath('div/div[@class="sl-value"]/div/ul/li/a/@href')]
                            for text in text_list:
                                fourth_title_url[text] = fourth_title[text_list.index(text)]
            url_dict['url_link'] = url['third_title_url']
            jd_crawler.jd_type.insert(url_dict)
            logging.info("success deal url %s" % url['third_title_url'])
            for fouth_url in fourth_title_url:
                get_fourth_detail(name_map[url['fisrt_title']], url['second_title'], url['third_title'], fouth_url, fourth_title_url[fouth_url])
        except Exception as E:
            logging.error('error,url is %s first title is %s, second title is %s' % (url['third_title_url'], name_map[url['fisrt_title']], url['second_title']))


def get_fourth_detail(first, second, third, fouth, url):
    try:
        url_dict = {}
        url_dict['selector'] = {}
        logging.info("start to crawle url %s,first title is %s, second title is %s, third title is %s, fouth title is %s" % (url, first, second, third, fouth))
        ip_proxy = get_proxy()
        resp = requests.get(url=url, headers=chrome_header, timeout=5, proxies=ip_proxy)

        page = etree.HTML(resp.content)
        url_dict[u'第一分类'] = first
        url_dict[u'第二分类'] = second
        url_dict[u'第三分类'] = third
        url_dict[u'第四分类'] = fouth
        if re.search(r'other_exts =(.*)?;', resp.content):
            result = re.search(r'other_exts =(.*)?;', resp.content)
            other_exts = result.group(1)
            exts = json.loads(other_exts)
            for kind in exts:
                if u'大家说' in kind['name']:
                    continue
                url_dict['selector'][kind['name']] = [i.strip() for i in kind['value_name'].split(';')]

        if page.xpath('//*[@id="J_selector"]/div[@class="J_selectorLine s-line J_selectorFold"]'):
            for tab in page.xpath('//*[@id="J_selector"]/div[@class="J_selectorLine s-line J_selectorFold"]'):
                if u'价格' in tab.xpath('div/div[@class="sl-key"]/span/text()')[0] or u'大家说' in tab.xpath('div/div[@class="sl-key"]/span/text()')[0]:
                    continue
                else:
                    kind = tab.xpath('div/div[@class="sl-key"]/span/text()')[0]
                    kind_type = tab.xpath('div/div[@class="sl-value"]/div/ul/li/a/text()')
                    url_dict['selector'][kind] = kind_type

        url_dict['url_link'] = url
        jd_crawler.jd_type.insert(url_dict)
        logging.info("success deal url %s" % url)
    except Exception as E:
        logging.info("error! url %s,first title is %s, second title is %s, third title is %s, fouth title is %s" % (url, first, second, third, fouth))


if __name__ == "__main__":
    # get_all_url()
    get_tab_detail()
