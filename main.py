# -*- coding = utf-8 -*-
# @Time : 2020/12/16 15:47
# @Author :董礼
# @File :main.py
# @Software :PyCharm
# 这一部分主要是爬取数据


import urllib.request
import json
from bs4 import BeautifulSoup
import re
import sqlite3
conn = sqlite3.connect("新冠疫情.db")
c = conn.cursor()
# 创建表
# c.execute('''
#     create table city
#     (provinceName char(30) primary key not null,
#     city text)
# ''')
# print("表创建成功")
# conn.commit()
# conn.close()

# 创建每一个省份的表
# c.execute('''
#     create table province
#     (provinceName char(30) primary key not null,
#     confirmed char(20),
#     dead char(20),
#     crued char(20))
# ''')
# print("表创建成功")
# conn.commit()
# conn.close()

# 创建外国的所有数据
# c.execute('''
#     create table otherCountry
#     (countryName char(50) primary key not null,
#     confirmed char(20),
#     dead char(20),
#     crued char(20))
# ''')
# print("表创建成功")
# conn.commit()
# conn.close()

# 创建中国总体趋势表
# c.execute('''
#     create table chinaTrend
#     (date char(20) primary key not null,
#     confirmed char(20),
#     dead char(20),
#     crued char(20))
# ''')
# print("表创建成功")
# conn.commit()
# conn.close()

# 创建外国发展趋势
# c.execute('''
#     create table foreignTrend
#     (date char(20) primary key not null,
#      confirmed char(20),
#     dead char(20),
#     crued char(20))
# ''')
# print("表创建完毕")
# conn.commit()
# conn.close()


# 创建一些重要的国家
# c.execute('''
#     create table ImportantCountryForOther
#     (country char(30) primary key not null,
#     city text)
# ''')
# print("表创建完毕")
# conn.commit()
# conn.close()


# 创建大洲的数据
# c.execute('''
#     create table continentForDate
#     (continentName char(30) primary key not null,
#     confirmed char(20),
#     dead char(20),
#     crued char(20))
# ''')
# print("表创建完毕")
# conn.commit()
# conn.close()

scriptDataRule = re.compile('<script id="captain-config" type="application/json">(.*?)</script>',re.S)
# 如果值为空，将其设置为0
def returnZore(data):
    if data == "":
        return 0
    else:
        return data

def getUrlOne(url):
    headers = {
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.88Safari / 537.36"
    }  #将爬虫伪装成浏览器
    request = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(request)
    bs = BeautifulSoup(response,"html.parser")
    data = bs.find_all("script", id="captain-config")
    # 获得script中的全部数据
    list = re.findall(scriptDataRule, str(data))  #这是一个数组
    province = json.loads(list[0])['component'][0]['caseList']  #这里是中国全部省
    # 首先查找省
    #==============================================================================================这里存放所有省的不同市的所有数据
    for i in range(len(province)):
        data = []     #存放所有市的数据
        provinceName = province[i]['area']   #省份的名字
        ChinaCity = province[i]['subList']   #省份的所有市的集合
        for j in range(len(ChinaCity)):
            if ChinaCity[j]["city"] == '境外输入':
                break
            cityname = ChinaCity[j]["city"]
            cityConfirmedPerson = ChinaCity[j]['confirmed']  #城市确诊人数
            cityDeadPerson = ChinaCity[j]['died']     #城市死亡人数
            cityCruedPerson = ChinaCity[j]['crued']
            #====================将城市数据进行过滤，防止为0的数据
            cityConfirmedPerson = returnZore(cityConfirmedPerson)
            cityDeadPerson = returnZore(cityDeadPerson)
            cityCruedPerson =returnZore(cityCruedPerson)
            cityInfo = (cityname,cityConfirmedPerson,cityDeadPerson,cityCruedPerson)
            # =====================
            data.append(cityInfo)
    #     sql = '''
    #         INSERT INTO city (provinceName,city)
    #         values("%s","%s")
    #     '''%(provinceName,str(data))
    #     c.execute(sql)
    # conn.commit()
    # print("数据插入成功")
    # conn.close()
        # ==============================================================================================
        #下面是爬取一个省的所有数据
    for i in range(len(province)):
        dataForProvince = []   #一个省的所有数据
        provinceName = province[i]['area']
        provinceConfirmedPerson = province[i]['confirmed']
        provinceDiedPerson = province[i]["died"]
        provinceCruedPerson = province[i]['crued']
        dataForProvince.append(provinceName)
        dataForProvince.append(provinceConfirmedPerson)
        dataForProvince.append(provinceDiedPerson)
        dataForProvince.append(provinceCruedPerson)
    #     sql = '''
    #         insert into province
    #         (provinceName,confirmed,dead,crued)
    #         values("%s","%s","%s","%s")
    #     '''%(dataForProvince[0],dataForProvince[1],dataForProvince[2],dataForProvince[3])
    #     c.execute(sql)
    # conn.commit()
    # print('数据库关闭')
    # conn.close()


    # #====================================================================================
    # # 下面爬取外国的全部数据
    caseOutsideList = json.loads(list[0])['component'][0]['caseOutsideList']  #外国全部数据的数组
    outSideCountryForAll = []
    for i in range(len(caseOutsideList)):
        #=========================================================================这里是外国总体数据
        outsideCountryOne = []
        outsideCountryName = caseOutsideList[i]["area"]
        outsideCountryConfirmed = caseOutsideList[i]['confirmed']
        outsideCountryDied = caseOutsideList[i]['died']
        outsideCountryCrued = caseOutsideList[i]['crued']
        outsideCountryOne.append(outsideCountryName)
        outsideCountryOne.append(outsideCountryConfirmed)
        outsideCountryOne.append(outsideCountryDied)
        outsideCountryOne.append(outsideCountryCrued)
        outSideCountryForAll.append(outsideCountryOne)
    #     sql = '''
    #     insert into otherCountry
    #     (countryName,confirmed,dead,crued)
    #     values("%s","%s","%s","%s")
    #     '''%(outsideCountryOne[0],outsideCountryOne[1],outsideCountryOne[2],outsideCountryOne[3])
    #     c.execute(sql)
    # conn.commit()
    # print('数据库关闭')
    # conn.close()

    #     # =========================================================================这里是外国总体数据
    #     # 下面是重点国家的重点城市数据
        if caseOutsideList[i]['subList'] != []:
            outsideCityAll = []
            for j in range(len(caseOutsideList[i]['subList'])):
                caseOutsideCityName = caseOutsideList[i]['subList'][j]['city']  #外国城市名称
                caseOutsideCityConfirmed =caseOutsideList[i]['subList'][j]['confirmed']  #外国城市确诊人数
                caseOutsideCityDied = caseOutsideList[i]['subList'][j]['died']
                caseOutsideCityCrued = caseOutsideList[i]['subList'][j]['crued']
                outsideCity = (caseOutsideCityName,caseOutsideCityConfirmed,caseOutsideCityDied,caseOutsideCityCrued)
                outsideCityAll.append(outsideCity)
    #         sql ='''
    #             insert into ImportantCountryForOther
    #             (country,city)
    #             values("%s","%s")
    #         '''%(outsideCountryName,str(outsideCityAll))
    #         c.execute(sql)
    # conn.commit()
    # print('数据库关闭')
    # conn.close()

    # #查找中国总体情况
    trendForChina = json.loads(list[0])['component'][0]['trend']
    chinaForFDate = trendForChina['updateDate']
    chinaForDataAll = trendForChina['list']
    Confirmed = chinaForDataAll[0]['data']  #中国确诊人数
    Dead = chinaForDataAll[3]['data']
    Crued =chinaForDataAll[2]['data']
    date = chinaForFDate  #爬出所有日期
    # for i in range(len(date)):
    #     sql = '''
    #         insert into chinaTrend
    #         (date,confirmed,dead,crued)
    #         values("%s","%s","%s","%s")
    #     '''%(date[i],str(Confirmed[i]),str(Dead[i]),str(Crued[i]))
    #     c.execute(sql)
    # conn.commit()
    # print("数据插入成功")
    # conn.close()


    # # 外国的疫情趋势
    allForeignTrend = json.loads(list[0])['component'][0]['allForeignTrend']
    dateForOut = allForeignTrend['updateDate']
    confirmedForOut = allForeignTrend['list'][0]['data']     #累计确诊人数
    cruedForOut = allForeignTrend['list'][1]['data']      #治愈人数
    deadForOut = allForeignTrend['list'][2]['data']         #死亡人数
    # for i in range(len(dateForOut)):
    #     sql = '''
    #         insert into foreignTrend
    #         (date,confirmed,dead,crued)
    #         values("%s","%s","%s","%s")
    #     '''%(dateForOut[i],confirmedForOut[i],cruedForOut[i],deadForOut[i])
    #     c.execute(sql)
    # conn.commit()
    # print("数据插入成功")
    # conn.close()


    # 获取各大洲的数据
    continent = json.loads(list[0])['component'][0]['globalList']
    # print(len(continent))
    # for i in range(len(continent)):
        # print(continent[i]['area'])
        # print(continent[i]['confirmed'])
        # print(continent[i]['died'])
        # print(continent[i]['crued'])
        # print("=========")
    #     sql = '''
    #         insert into continentForDate
    #         (continentName,confirmed,dead,crued)
    #         values("%s","%s","%s","%s")
    #     '''%(continent[i]['area'],continent[i]['confirmed'],continent[i]['died'],continent[i]['crued'])
    #     c.execute(sql)
    # conn.commit()
    # print("插入成功")
    # conn.close()

# 每一个城市的数据类型
# {省份:[[城市1,确诊人数,死亡人数,治愈人数]]}
# 每一个省份的全部数据
#[[省份1,确诊人数,死亡人数,治愈人数],[省份2,确诊人数,死亡人数,治愈人数]]
def main():
    getUrlOne("https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner")

if __name__ == "__main__":
    main()