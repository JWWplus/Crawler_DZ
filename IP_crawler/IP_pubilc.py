# coding=utf-8
import sys
import urlparse
from base import Base
import logging
reload(sys)
sys.setdefaultencoding("utf-8")

"""实时获取"""


class KuaiDaiLi2(Base):
    """ www.kuaidaili.com """

    def crawl(self):
        base = "http://www.kuaidaili.com/proxylist/"
        proxyip = []
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        for i in range(1, 11):
            proxyip.extend(self.get(urlparse.urljoin(base, str(i)), headers=headers))

        return proxyip

    def parse(self, soup):
        result = []
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[0].string,
                    "port": d[1].string,
                    "info": d[5].string,
                    "type": 0,
                }
                if d[2].string == "透明":
                    ip["type"] = 1
                elif d[2].string == "匿名":
                    ip["type"] = 2
                    result.append(ip)
                elif d[2].string == "高匿名":
                    ip["type"] = 3
                    result.append(ip)

            except Exception as e:
                logging.error('KuaiDaiLi2 parse error: %s', e)

        return result


class XiCiDaiLi(Base):
    """ www.xicidaili.com """

    def crawl(self):
        base = "http://www.xicidaili.com"
        proxyip = []
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        # 现在只抓取国内匿名代理,不考虑国外匿名代理
        for u in ["nn"]:
            proxyip.extend(self.get(urlparse.urljoin(base, u), headers=headers))

        return proxyip

    def parse(self, soup):
        result = []
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[1].string,
                    "port": d[2].string,
                    "info": "",
                    "type": 0,
                }
                info = d[4].find("a")
                if info:
                    ip["info"] = info.string

                if d[4].string == "透明":
                    ip["type"] = 1
                elif d[4].string == "匿名":
                    ip["type"] = 2
                    result.append(ip)
                elif d[4].string == "高匿":
                    ip["type"] = 3
                    result.append(ip)

            except Exception as e:
                logging.error('XiCiDaiLi parse error: %s', e)

        return result


class IP66API(Base):
    """ http://www.66ip.cn/nm.html """

    def crawl(self):
        proxyip = []
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        for c in range(3):
            # 超级匿名
            nm = "http://www.66ip.cn/nmtq.php?getnum=800&anonymoustype=4&proxytype=2&api=66ip"
            proxyip.extend(self.set_type(self.get(nm, headers=headers), 3))
            for i in range(2, 4):
                # 透明，普匿，高匿
                nm = "http://www.66ip.cn/nmtq.php?getnum=800&anonymoustype=%s&proxytype=2&api=66ip" % i
                proxyip.extend(self.set_type(self.get(nm, headers=headers), i))

        return proxyip

    def parse(self, soup):
        result = []
        for d in soup.find('body').contents:
            try:
                d = str(d).strip()
                if d != '' and d[0].isdigit():
                    ip = {
                        "ip": d.split(':')[0],
                        "port": d.split(':')[1],
                        "info": "",
                        "type": 0,
                    }
                    result.append(ip)
            except Exception as e:
                logging.error('IP66API parse error: %s', e)

        return result

    def set_type(self, proxyip=[], iptype=0):
        result = []
        for ip in proxyip:
            ip['type'] = iptype
            result.append(ip)

        return result
