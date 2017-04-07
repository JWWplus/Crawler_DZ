# coding=utf-8
import logging
from IP_pubilc import KuaiDaiLi2, XiCiDaiLi
from IP_pay import fufei_ip
import redis
import validate_mult

"""
{1: {}, 2: {}, 3: {u'124.88.67.24:843': 2.685180902481079, u'119.29.35.92:82': 1.9156498908996582 .....
正确的返回结果
1 , 2 ,3代表返回类型  透明  匿名   高匿名
IP地址以及延时
"""
r = redis.StrictRedis.from_url('redis://:@localhost:6379/3')

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# r = redis.StrictRedis(host='localhost', port=6379, db=0)


# 免费ip代理抓取启动函数
def freeip_run():
    proxyip = []
    for source in [KuaiDaiLi2, XiCiDaiLi]:
        instance = source()
        proxyips = instance.crawl()
        proxyip.extend(proxyips)
        logging.info('%s crawl ip: %s', source, len(proxyips))

    validator = validate_mult.Validator()
    result = {}
    proxy_set = classify(proxyip)
    for proxy_type in range(2, 4):
        proxy_list = list(proxy_set.get(proxy_type, set()))
        logging.info('sniffer start, proxy_type: %s, proxy_ip: %s', proxy_type, len(proxy_list))
        result[proxy_type] = validator.run_in_multiprocess(proxy_list)
    save2redis(result)


# 付费代理ip抓取启动函数
# 代理url link请自行购买后加入下方的list中
def payip_run(site_name):
    target_url_list = [
        '',
    ]
    proxyip = []
    instance = fufei_ip()
    for target_url in target_url_list:
        proxyips = instance.crawl(target_url)
        proxyip.extend(instance.parse(proxyips))
        logging.info('%s crawl ip: %s', fufei_ip, len(proxyips))

        validator = validate_mult.Validator()
        validator.site = site_name
        result = {}
        proxy_set = classify(proxyip)
        for proxy_type in range(2, 4):
            proxy_list = list(proxy_set.get(proxy_type, set()))
            logging.info('sniffer start, proxy_type: %s, proxy_ip: %s', proxy_type, len(proxy_list))
            result[proxy_type] = validator.run_in_multiprocess(proxy_list)
        save2redis(result, site_name)
        highusedip = r.zcount(site_name + "ipproxy:3", 0, 1)
        total_ipnum = r.zcard(site_name + "ipproxy:3")
        logging.info(u"%s 抓取到高可用IP%d个" % (site_name, highusedip))
        logging.info(u"%s redis数据库中一共有%d个代理IP" % (site_name, total_ipnum))


def classify(proxyip):
    """ 根据匿名程度对ip进行分类 """
    result = {}
    # 各设置一个set集合
    for i in range(4):
        result.setdefault(i, set())

    for ip in proxyip:
        # 获取IP端口地址
        ip_port = "%(ip)s:%(port)s" % ip
        try:
            # 先转换为set在add
            result[int(ip['type'])].add(ip_port)
        except Exception as e:
            logging.error(e)
            logging.error(ip['ip'], ip['port'], ip['type'])
    # {0: set(), 1: set(), 2: set(), 3: {u'61.137.160.12:8080'}}类似这样的字典，值是一个set区别最后的返回结果
    return result


def save2file(result):
    """ 保存到文件 """
    for types in result:
        txtname = './data/ip_type%s.txt' % types
        with open(txtname, 'wb') as f:
            for ips in result[types]:
                f.write(ips + '\n')


def save2redis(result, site_name):
    """ 保存到redis
        redis 键名 网站名称+ipproxy:3
    """
    global r
    for proxy_type in range(2, 4):
        key = '%s%s%s' % (site_name, validate_mult.SNIFFER['KEY_PREFIX'], proxy_type)
        proxy_list = r.zrange(key, 0, -1)
        # 去除抓取中和redis中重复的元素
        for proxy_ip in (set(result[proxy_type].keys())) - set(proxy_list):
            r.zadd(key, result[proxy_type][proxy_ip], proxy_ip)


if __name__ == "__main__":
    if r.zcard("dazhong_ipproxy:3") < 35:
        payip_run('dazhong_')
