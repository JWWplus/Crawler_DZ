# coding: utf-8
import requests
import logging
from lxml import etree
import redis
from pymongo import MongoClient
import re
import json
from celery import Celery
import time

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
r = redis.StrictRedis.from_url('redis://:55f7b56ab5e13921e0935e92@dataTask01:63799/3')
kaola_crawler = MongoClient("localhost:27017").crawler
app = Celery('crawler_kaola', broker='redis://localhost:6379/5')
app.conf.update(
    CELERY_RESULT_BACKEND='mongodb://localhost:27017',
    CELERY_MONGODB_BACKEND_SETTINGS={
        'database': 'celery',
        'taskmeta_collection': 'kaola_crawler',
    }
)
chrome_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
}

error_list = []
base_url = 'http://www.kaola.com'
kaola_url = {
    u'母婴儿童': {
        u'奶粉': 'http://www.kaola.com/category/2620.html?zn=top&amp;zp=category-1-1-1',
        u'纸尿裤/拉拉裤': 'http://www.kaola.com/category/2631.html?zn=top&amp;zp=category-1-1-2',
        u'营养辅食': 'http://www.kaola.com/category/2621.html?zn=top&amp;zp=category-1-1-3',
        u'宝宝用品': 'http://www.kaola.com/category/2664.html?zn=top&amp;zp=category-1-1-4',
        u'童装童鞋': 'http://www.kaola.com/category/2665.html?zn=top&amp;zp=category-1-1-5',
        u'孕妈必备': 'http://www.kaola.com/category/2667.html?zn=top&amp;zp=category-1-1-6',
    },
    u'美容彩妆': {
        u'护肤': 'http://www.kaola.com/category/1472.html?zn=top&zp=category-2-1-1',
        u'彩妆': 'http://www.kaola.com/category/1473.html?zn=top&zp=category-2-1-3',
        u'面膜': 'http://www.kaola.com/category/1471.html?zn=top&zp=category-2-1-2',
        u'防晒修复': 'http://www.kaola.com/category/2881.html?zn=top&zp=category-2-1-4',
        u'香水/香氛': 'http://www.kaola.com/category/6166.html?zn=top&zp=category-2-1-5',
    },
    u'服饰鞋包': {
        u'精选大牌': 'http://www.kaola.com/category/3811.html?zn=top&zp=category-3-1-1',
        u'手表配饰': 'http://www.kaola.com/category/2909.html?zn=top&zp=category-3-1-2',
        u'女士箱包': 'http://www.kaola.com/category/2894.html?zn=top&zp=category-3-1-3',
        u'服饰内衣': 'http://www.kaola.com/category/2895.html?zn=top&zp=category-3-1-4',
        u'男士箱包': 'http://www.kaola.com/category/3494.html?zn=top&zp=category-3-1-5',
        u'鞋': 'http://www.kaola.com/category/2905.html?zn=top&zp=category-3-1-6',
    },
    u'家具个护': {
        u'洗护日用': 'http://www.kaola.com/category/12317.html?zn=top&zp=category-4-1-1',
        u'女性护理': 'http://www.kaola.com/category/12344.html?zn=top&zp=category-4-1-2',
        u'女性护理': 'http://www.kaola.com/category/12344.html?zn=top&zp=category-4-1-2',
        u'其他个护': 'http://www.kaola.com/category/2731.html?zn=top&zp=category-4-1-3',
        u'宠物生活': 'http://www.kaola.com/category/10989.html?zn=top&zp=category-4-1-4',
        u'居家用品': 'http://www.kaola.com/category/2734.html?zn=top&zp=category-4-1-5',
        u'家装家纺': 'http://www.kaola.com/category/2732.html?zn=top&zp=category-4-1-6',
    },
    u'营养保健': {
        u'营养补充': 'http://www.kaola.com/category/2893.html?zn=top&amp;zp=category-5-1-1',
        u'健康养护': 'http://www.kaola.com/category/2916.html?zn=top&amp;zp=category-5-1-2',
        u'女性必备': 'http://www.kaola.com/category/3401.html?zn=top&amp;zp=category-5-1-3',
        u'关爱老年': 'http://www.kaola.com/category/3446.html?zn=top&amp;zp=category-5-1-4',
        u'男性必备': 'http://www.kaola.com/category/3438.html?zn=top&amp;zp=category-5-1-5',
        u'国际汇': 'http://www.kaola.com/category/3013.html?zn=top&amp;zp=category-5-1-6',
    },
    u'海外直邮': {
        u'母婴专区': 'http://www.kaola.com/category/3668.html?zn=top&amp;zp=category-6-1-1',
        u'美容彩妆': 'http://www.kaola.com/category/11778.html?zn=top&amp;zp=category-6-1-2',
        u'电子生活': 'http://www.kaola.com/category/3676.html?zn=top&amp;zp=category-6-1-3',
        u'日用家居': 'http://www.kaola.com/category/3681.html?zn=top&amp;zp=category-6-1-4',
        u'服饰鞋包': 'http://www.kaola.com/category/3692.html?zn=top&amp;zp=category-6-1-5',
        u'美食保健': 'http://www.kaola.com/category/3691.html?zn=top&amp;zp=category-6-1-6',
    },
    u'数码家电': {
        u'手机/配件': 'http://www.kaola.com/category/6782.html?zn=top&amp;zp=category-7-1-1',
        u'数码影音': 'http://www.kaola.com/category/6810.html?zn=top&amp;zp=category-7-1-2',
        u'生活电器': 'http://www.kaola.com/category/6866.html?zn=top&amp;zp=category-7-1-3',
        u'个护健康': 'http://www.kaola.com/category/6839.html?zn=top&amp;zp=category-7-1-4',
        u'厨房电器': 'http://www.kaola.com/category/6826.html?zn=top&amp;zp=category-7-1-5',
        u'办公/外设': 'http://www.kaola.com/category/6867.html?zn=top&amp;zp=category-7-1-6',
    },
    u'环球美食': {
        u'乳品/咖啡/麦片/冲饮': 'http://www.kaola.com/category/5864.html?zn=top&amp;zp=category-8-1-1',
        u'人气热门': 'http://www.kaola.com/category/5924.html?zn=top&amp;zp=category-8-1-2',
        u'茶/酒/饮料': 'http://www.kaola.com/category/5882.html?zn=top&amp;zp=category-8-1-3',
        u'粮油副食': 'http://www.kaola.com/category/6088.html?zn=top&amp;zp=category-8-1-4',
        u'休闲零食': 'http://www.kaola.com/category/5913.html?zn=top&amp;zp=category-8-1-5',
        u'饼干糕点': 'http://www.kaola.com/category/5905.html?zn=top&amp;zp=category-8-1-6',
    },
    u'运动户外': {
        u'运动鞋': 'http://www.kaola.com/category/9694.html?zn=top&amp;zp=category-9-1-1',
        u'运动服装': 'http://www.kaola.com/category/9695.html?zn=top&amp;zp=category-9-1-2',
        u'户外鞋靴': 'http://www.kaola.com/category/9696.html?zn=top&amp;zp=category-9-1-3',
        u'户外服装': 'http://www.kaola.com/category/9697.html?zn=top&amp;zp=category-9-1-4',
        u'户外装备': 'http://www.kaola.com/category/9698.html?zn=top&amp;zp=category-9-1-5',
        u'更多分类': 'http://www.kaola.com/category/9859.html?zn=top&amp;zp=category-9-1-6',
    },
    u'水果生鲜': {
        u'新鲜水果': 'http://www.kaola.com/category/9611.html?zn=top&amp;zp=category-10-1-1',
        u'肉品禽蛋': 'http://www.kaola.com/category/9612.html?zn=top&amp;zp=category-10-1-2',
        u'水产海鲜': 'http://www.kaola.com/category/9613.html?zn=top&amp;zp=category-10-1-3',
        u'速冻特产': 'http://www.kaola.com/category/9614.html?zn=top&amp;zp=category-10-1-4',
        u'蔬菜食材': 'http://www.kaola.com/category/12284.html?zn=top&amp;zp=category-10-1-5',
    },
}


def get_proxy():
    ipproxy = r.zrange('jd_ipproxy:3', 0, 0)
    r.zincrby('jd_ipproxy:3', ipproxy[0], 2)
    return {'http': ipproxy[0]}


def get_url():
    for first_title in kaola_url:
        for second_title in kaola_url[first_title]:
            logging.info("start to crawl the url %s first title is %s, second title is %s" % (kaola_url[first_title][second_title], first_title, second_title))
            try:
                ip_proxy = get_proxy()
                resp = requests.get(url=kaola_url[first_title][second_title], headers=chrome_header, timeout=5, proxies=ip_proxy)
                page = etree.HTML(resp.content)
                div_include_brand = page.xpath('//div[@class="m-classify z-cat3 j-box clearfix"]')
                div_brand = page.xpath('//div[@class="m-classify z-cat3 j-box clearfix" and @id="brandbox"]')
                div_type = [div for div in div_include_brand if div not in div_brand]
                for div in div_type:
                    for a in div.xpath('div//a'):
                        kaola_crawler.kaola_url.insert({
                            'first_title': first_title,
                            'second_title': second_title,
                            'third_title': a.xpath('text()')[0],
                            'url_link': base_url + a.xpath('@href')[0]
                        })
                logging.info("success deal url %s" % kaola_url[first_title][second_title])
            except Exception as e:
                logging.error('error,url is %s first title is %s, second title is %s' % (kaola_url[first_title][second_title], first_title, second_title))
                error_list.append(kaola_url[first_title][second_title])
                continue


@app.task(bind=True, default_retry_delay=1, max_retries=5)
def get_detail(self, url_info):
    type_detail = {}
    try:
        ip_proxy = get_proxy()
        type_detail['url_link'] = url_info['url_link']
        type_detail[u'第一分类'] = url_info['first_title']
        type_detail[u'第二分类'] = url_info['second_title']
        type_detail[u'第三分类'] = url_info['third_title']
        type_detail['selector'] = {}
        resp = requests.get(url_info['url_link'], headers=chrome_header, timeout=5, proxies=ip_proxy)
        page = etree.HTML(resp.content)
        for div_list in page.xpath('//div[@class="m-classify property z-cat3 clearfix j-box"]'):
            if u'其他' in div_list.xpath('div[@class="name"]/text()')[0]:
                for other in div_list.xpath('//div[@class="attr-items all ctag"]/a'):
                    type_detail['selector'][other.xpath('text()')[0]] = div_list.xpath('//div[@class="dropdownlist-content j-tagwrap"]')[div_list.xpath('//div[@class="attr-items all ctag"]/a').index(other)].xpath('div//a/text()')
            else:
                type_detail['selector'][div_list.xpath('div[@class="name"]/text()')[0]] = div_list.xpath('div//a/text()')
        kaola_crawler.kaola_type.insert(type_detail)
        return True
    except Exception as e:
        self.retry(countdown=1, exc=e)


if __name__ == "__main__":
    # get_url()
    for url in list(kaola_crawler.kaola_url.find()):
        logging.info("start to crawl the url %s first title is %s, second title is %s" % (url['url_link'], url['first_title'], url['second_title']))
        result = get_detail.apply_async((url, )).get()
    logging.info("finished! ")
