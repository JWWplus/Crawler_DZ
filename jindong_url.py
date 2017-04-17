# coding: utf-8
total_link = {
    # 家用电器
    'jiaoyongdianqi': {
        u'大家电': 'https://list.jd.com/list.html?cat=737,794,798',
        u'厨卫大电': 'https://list.jd.com/list.html?cat=737,13297,1300',
        u'厨房小电': 'https://list.jd.com/list.html?cat=737,752,13702',
        u'生活电器': 'https://list.jd.com/list.html?cat=737,738,747',
        u'个护健康': 'https://list.jd.com/list.html?cat=737,1276,739',
    },
    # 手机
    'shouji': {
        u'手机通讯': 'https://list.jd.com/list.html?cat=9987,653,655',
        u'手机配件': 'https://list.jd.com/list.html?cat=9987,830,13658',
    },
    # 数码
    'shuma': {
        u'数码配件': 'https://list.jd.com/list.html?cat=652,829,845',
        u'摄影摄像': 'https://list.jd.com/list.html?cat=652,654,831',
        u'智能设备': 'https://list.jd.com/list.html?cat=652,12345,12347',
        u'影音娱乐': 'https://list.jd.com/list.html?cat=652,828,837',
        u'电子教育': 'https://list.jd.com/list.html?cat=652,12346,12357',
    },
    # 电脑办公
    'diannao_bangong': {
        u'电脑整机': 'https://list.jd.com/list.html?cat=670,671,1105',
        u'电脑配件': 'https://list.jd.com/list.html?cat=670,677,678',
        u'外设产品': 'https://list.jd.com/list.html?cat=670,686,693',
        u'游戏设备': 'https://list.jd.com/list.html?cat=670,12800,12801',
        u'网络产品': 'https://list.jd.com/list.html?cat=670,699,700',
        u'办公设备': 'https://list.jd.com/list.html?cat=670,716,722',
        u'文具/耗材': 'https://list.jd.com/list.html?cat=670,729,730',
        u'服务产品': 'https://list.jd.com/list.html?cat=670,703,10011',
    },
    # 家居家装
    'jiaju_jiazhuang': {
        u'家纺': 'https://list.jd.com/list.html?cat=1620,1621,1626',
        u'收纳用品': 'https://list.jd.com/list.html?cat=1620,13780,13781',
        u'灯具': 'https://list.jd.com/list.html?cat=1620,1623,1648',
        u'生活日用': 'https://list.jd.com/list.html?cat=1620,1624,11167',
        u'家装软饰': 'https://list.jd.com/list.html?cat=1620,11158,11162',
    },
    # 厨具
    'chuju': {
        u'烹饪锅具': 'https://list.jd.com/list.html?cat=6196,6197,6199',
        u'刀剪菜板': 'https://list.jd.com/list.html?cat=6196,6198,6209',
        u'厨房配件': 'https://list.jd.com/list.html?cat=6196,6214,6215',
        u'水具酒具': 'https://list.jd.com/list.html?cat=6196,6219,6223',
        u'餐具': 'https://list.jd.com/list.html?cat=6196,6227,6228',
        u'酒店用品': 'https://list.jd.com/list.html?cat=6196,9182,9183',
        u'茶具/咖啡具': 'https://list.jd.com/list.html?cat=6196,11143,11148',
    },
    # 家具
    'jiaju': {
        u'卧室家具': 'https://list.jd.com/list.html?cat=9847,9848,9863',
        u'客厅家具': 'https://list.jd.com/list.html?cat=9847,9849,9870',
        u'餐厅家具': 'https://list.jd.com/list.html?cat=9847,9850,9877',
        u'书房家具': 'https://list.jd.com/list.html?cat=9847,9851,9881',
        u'储物家具': 'https://list.jd.com/list.html?cat=9847,9852,9885',
        u'阳台/户外': 'https://list.jd.com/list.html?cat=9847,9853,9889',
        u'办公家具': 'https://list.jd.com/list.html?cat=9847,9854,9893',
        u'儿童家具': 'https://list.jd.com/list.html?cat=9847,13533,13534',
    },
    # 服饰内衣
    'fushi_neiyi': {
        u'女装': 'https://list.jd.com/list.html?cat=1315,1343,9714',
        u'男装': 'https://list.jd.com/list.html?cat=1315,1342,1348',
        u'内衣': 'https://list.jd.com/list.html?cat=1315,1345,1364',
        u'服饰配件': 'https://list.jd.com/list.html?cat=1315,1346,9790',
    },
    # 美装个护
    'meizhuang_gehu': {
        u'清洁用品': 'https://list.jd.com/list.html?cat=1316,1625,1671',
        u'面部护肤': 'https://list.jd.com/list.html?cat=1316,1381,1391',
        u'身体护理': 'https://list.jd.com/list.html?cat=1316,1383,1401',
        u'口腔护理': 'https://list.jd.com/list.html?cat=1316,1384,1405',
        u'女性护理': 'https://list.jd.com/list.html?cat=1316,1385,1408',
        u'洗发护发': 'https://list.jd.com/list.html?cat=1316,1386,11922',
        u'香水彩妆': 'https://list.jd.com/list.html?cat=1316,1387,11932',
    },
    # 宠物生活
    'chongwushenghuo': {
        u'宠物主粮': 'https://list.jd.com/list.html?cat=6994,6995,7002',
        u'小宠用品': 'https://list.jd.com/list.html?cat=6994,13963,13964',
        u'宠物零食': 'https://list.jd.com/list.html?cat=6994,6996,7006',
        u'医疗保健': 'https://list.jd.com/list.html?cat=6994,6997,7011',
        u'家居日用': 'https://list.jd.com/list.html?cat=6994,6998,7017',
        u'水族': 'https://list.jd.com/list.html?cat=6994,13968,13969',
        u'宠物玩具': 'https://list.jd.com/list.html?cat=6994,6999,7024',
        u'出行装备': 'https://list.jd.com/list.html?cat=6994,7000,7028',
        u'洗护美容': 'https://list.jd.com/list.html?cat=6994,7001,7035',
        u'狗狗': 'https://list.jd.com/list.html?tid=1001668',
    },
    # 鞋靴
    'xiexue': {
        u'流行男鞋': 'https://list.jd.com/list.html?cat=11729,11730,6907',
        u'时尚女鞋': 'https://list.jd.com/list.html?cat=11729,11731,6920',
    },
    # 礼品箱包
    'liping_xiangbao': {
        u'潮流女包': 'https://list.jd.com/list.html?cat=1672,2575,5259',
        u'精品男包': 'https://list.jd.com/list.html?cat=1672,2576,2584',
        u'功能箱包': 'https://list.jd.com/list.html?cat=1672,2577,3997',
        u'礼品': 'https://list.jd.com/list.html?cat=1672,2599,1440',
        u'奢侈品': 'https://list.jd.com/list.html?cat=1672,2615,9187',
        u'婚庆': 'https://list.jd.com/list.html?cat=1672,12059,7067',
    },
    # 钟表
    'zhongbiao': {
        u'钟表': 'https://list.jd.com/list.html?cat=5025,5026,13673',
    },
    # 珠宝首饰
    # 运动户外
    'yundonghuwai': {
        u'运动鞋包': 'https://list.jd.com/list.html?cat=1318,12099,9756',
        u'运动服饰': 'https://list.jd.com/list.html?cat=1318,12102,12104',
        u'骑行运动': 'https://list.jd.com/list.html?cat=1318,12115,12116',
        u'垂钓用品': 'https://list.jd.com/list.html?cat=1318,12147,12148',
        u'游泳用品': 'https://list.jd.com/list.html?cat=1318,12154,12155',
        u'户外鞋服': 'https://list.jd.com/list.html?cat=1318,2628,12123',
        u'户外装备': 'https://list.jd.com/list.html?cat=1318,1462,1473',
        u'健身训练': 'https://list.jd.com/list.html?cat=1318,1463,12109',
        u'体育用品': 'https://list.jd.com/list.html?cat=1318,1466,13804',
    },
    # 汽车用品
    'qicheyongping': {
        u'维修保养': 'https://list.jd.com/list.html?cat=6728,6742,11849',
        u'车载电器': 'https://list.jd.com/list.html?cat=6728,6740,13983',
        u'美容清洗': 'https://list.jd.com/list.html?cat=6728,6743,13979',
        u'汽车装饰': 'https://list.jd.com/list.html?cat=6728,6745,13984',
        u'安全自驾': 'https://list.jd.com/list.html?cat=6728,6747,6792',
        u'汽车服务': 'https://list.jd.com/list.html?cat=6728,12402,12403',
        u'赛事改装': 'https://list.jd.com/list.html?cat=6728,13256,13981',
    },
    # 玩具乐器
    'wanjuyueqi': {
        u'适用年龄': 'https://list.jd.com/list.html?cat=6233,6234,6239',
        u'遥控/电动': 'https://list.jd.com/list.html?cat=6233,6235,6245',
        u'毛绒布艺': 'https://list.jd.com/list.html?cat=6233,6236,6254',
        u'娃娃玩具': 'https://list.jd.com/list.html?cat=6233,6237,6257',
        u'模型玩具': 'https://list.jd.com/list.html?cat=6233,6253,6261',
        u'健身玩具': 'https://list.jd.com/list.html?cat=6233,6260,6265',
        u'动漫玩具': 'https://list.jd.com/list.html?cat=6233,6264,6272',
        u'益智玩具': 'https://list.jd.com/list.html?cat=6233,6271,6276',
        u'积木拼插': 'https://list.jd.com/list.html?cat=6233,6275,6280',
        u'DIY玩具': 'https://list.jd.com/list.html?cat=6233,6279,6281',
        u'创意减压': 'https://list.jd.com/list.html?cat=6233,6289,6292',
        u'乐器': 'https://list.jd.com/list.html?cat=6233,6291,6294',
    },
    # 母婴
    'muyin': {
        u'奶粉': 'https://list.jd.com/list.html?cat=1319,1523,7052',
        u'营养辅食': 'https://list.jd.com/list.html?cat=1319,1524,12191',
        u'尿裤湿巾': 'https://list.jd.com/list.html?cat=1319,1525,7057',
        u'喂养用品': 'https://list.jd.com/list.html?cat=1319,1526,7060',
        u'洗护用品': 'https://list.jd.com/list.html?cat=1319,1527,1556',
        u'童车童床': 'https://list.jd.com/list.html?cat=1319,1528,1563',
        u'寝居服饰': 'https://list.jd.com/list.html?cat=1319,6313,6314',
        u'妈妈专区': 'https://list.jd.com/list.html?cat=1319,4997,5002',
        u'童装童鞋': 'https://list.jd.com/list.html?cat=1319,11842,11222',
        u'安全座椅': 'https://list.jd.com/list.html?cat=1319,12193,12194',
    },

    # 酒类
    'jiulei': {
        u'中外名酒': 'https://list.jd.com/list.html?cat=12259,12260,9438',
    },
    # 食品饮料
    'shipingyinliao': {
        u'进口食品': 'https://list.jd.com/list.html?cat=1320,5019,5020',
        u'地方特产': 'https://list.jd.com/list.html?cat=1320,1581,12217',
        u'休闲食品': 'https://list.jd.com/list.html?cat=1320,1583,13757',
        u'粮油调味': 'https://list.jd.com/list.html?cat=1320,1584,13789',
        u'饮料冲调': 'https://list.jd.com/list.html?cat=1320,1585,10975',
        u'食品礼券': 'https://list.jd.com/list.html?cat=1320,2641,2642',
        u'茗茶': 'https://list.jd.com/list.html?cat=1320,12202,12203',
    },
    # 生鲜
    'shengxian': {
        u'蔬菜': 'https://list.jd.com/list.html?cat=12218,13553,13573',
        u'禽肉蛋品': 'https://list.jd.com/list.html?cat=12218,13586,13587',
        u'水果': 'https://list.jd.com/list.html?cat=12218,12221,13563',
        u'猪牛羊肉': 'https://list.jd.com/list.html?cat=12218,13581,12247',
        u'海鲜水产': 'https://list.jd.com/list.html?cat=12218,12222,12241',
        u'冷冻食品': 'https://list.jd.com/list.html?cat=12218,13591,13592',
        u'饮品甜品': 'https://list.jd.com/list.html?cat=12218,13598,13603',
    },
    # 医药保健
    'yiyaobaojian': {
        u'营养健康': 'https://list.jd.com/list.html?cat=9192,9193,9200',
        u'营养成分': 'https://list.jd.com/list.html?cat=9192,9194,9214',
        u'传统滋补': 'https://list.jd.com/list.html?cat=9192,9195,9229',
        u'计生情趣': 'https://list.jd.com/list.html?cat=9192,9196,12609',
        u'保健器械': 'https://list.jd.com/list.html?cat=9192,9197,13787',
        u'护理护具': 'https://list.jd.com/list.html?cat=9192,12190,12599',
        u'中西药品': 'https://list.jd.com/list.html?cat=9192,12632,12641',
    },
}
