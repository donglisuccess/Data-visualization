# # -*- coding = utf-8 -*-
# # @Time : 2020/12/15 21:22
# # @Author :董礼
# # @File :app.py.py
# # @Software :PyCharm
#
# # 引入包
from flask import Flask,render_template,request,jsonify
# render_template作用是模板引擎渲染
import sqlite3
# 引入数据库
app = Flask(__name__)
#
@app.route("/")    #后盾接口
def index():
# 模块6
    datalist = []
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    print("数据库连接成功")
    sql = '''
        select city from city
        '''
    cursor = c.execute(sql)
    for data in cursor:
        if eval(data[0]):
            datalist.append(eval(data[0]))
    conn.commit()
    print("数据库关闭")
    conn.close()
    # 查找世界确诊人数
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    sql = '''
            select continentName,confirmed,dead,crued from continentForDate
        '''
    cursor = c.execute(sql)
    continentData = []
    for item in cursor:
        if item[0] != '热门':
            continentData.append(item)
        else:
            otherData = item
    conn.commit()
    print("数据库关闭")
    conn.close()
    # 中国疫情人数
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    sql = '''
                select confirmed from chinaTrend
            '''
    cursor = c.execute(sql)
    for item in cursor:
        ChinaNum = item[0]
    conn.commit()
    print("数据库关闭")
    conn.close()
    continentNameData = []
    continentConfiredData = []
    for item in continentData:
        if item[0] != '其他':
            continentNameData.append(item[0])
            continentConfiredData.append(item[1])
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    print("数据库连接成功")
    sql = '''
        select continentName,confirmed,dead,crued from continentForDate
    '''
    cursor = c.execute(sql)
    continentList = []
    for item in cursor:
        temp = {}
        temp['value'] = item[1]
        temp['name'] = item[0]
        continentList.append(temp)
    conn.commit()
    conn.close()
    # 在这里设置地图的数据
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    sql = '''
        select provinceName,confirmed from province
    '''
    cursor = c.execute(sql)
    provinceData = []
    for item in cursor:
        temp = {}
        temp['name']=item[0]
        temp['value']= item[1]
        provinceData.append(temp)
    return render_template("index.html",number=otherData,datalist = datalist,
                           ChinaNum=ChinaNum,
                           continentNameData=continentNameData,
                           continentConfiredData=continentConfiredData,
                           continentList=continentList,
                           provinceData=provinceData)
# 查找城市
@app.route("/city",methods = ["get",'post'])
def city():
    Province = request.args['ProVince']
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    print('数据库连接成功')
    sql = '''
        select provinceName,city from city
    '''
    cursor = c.execute(sql)
    cityName = []
    cityConfirmed = []
    for data in cursor:
        length = len(Province)
        if Province[length-1:] == "省":
            if data[0] == Province[0:length-1]:
                provinceName1= data[0]
                cityAllInfo = []
                citys = eval(data[1])
                for city in citys:
                    cityInfo = {}
                    cityInfo['city'] = city[0]
                    cityInfo['确诊'] = city[1]
                    cityInfo['死亡'] = city[2]
                    cityInfo['治愈'] = city[3]
                    cityAllInfo.append(cityInfo)
        elif data[0] == Province:
            provinceName1 = data[0]
            cityAllInfo = []
            citys = eval(data[1])
            for city in citys:
                cityInfo = {}
                cityInfo['city']= city[0]
                cityInfo['确诊'] = city[1]
                cityInfo['死亡'] = city[2]
                cityInfo['治愈'] = city[3]
                cityAllInfo.append(cityInfo)
    conn.commit()
    conn.close()
    return render_template("city.html",provinceName1= provinceName1 ,cityAllInfo = cityAllInfo)

@app.route("/country",methods = ["post","get"])
def country():
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    print("数据库已打开")
    sql = '''
           select date,confirmed,dead from foreignTrend
       '''
    cursor = c.execute(sql)
    n = 2
    deadForForeign = []
    confirmedForForeign = []
    for row in cursor:
        if eval(row[0]) == n + 0.15:
            deadForForeign.append(row[2])
            confirmedForForeign.append(row[1])
            n += 1
    # print(deadForForeign)
    # print(confirmedForForeign)
    return render_template('country.html',deadForForeign=deadForForeign,confirmedForForeign=confirmedForForeign)


@app.route("/foreign",methods= ['post','get'])
def foreign():
    requestCountry = request.args['foreign']
    dataItem = ['日本','美国','韩国','意大利']
    for item in dataItem:
        if requestCountry == item:
            conn = sqlite3.connect("新冠疫情.db")
            c = conn.cursor()
            print("数据库已打开")
            sql = '''
                      select country,city from ImportantCountryForOther
                  '''
            cursor = c.execute(sql)
            for item in cursor:
                if requestCountry == item[0]:
                    cityName = []
                    cityConfirmed = []
                    cityDead = []
                    for it in eval(item[1]):
                        cityName.append(it[0])
                        cityConfirmed.append(it[1])
                        cityDead.append(it[2])
            conn.commit()
            conn.close()
            return render_template("foreign.html",requestCountry=requestCountry,cityName=cityName,cityConfirmed=cityConfirmed,cityDead=cityDead)
    conn = sqlite3.connect("新冠疫情.db")
    c = conn.cursor()
    print("数据库已打开")
    sql = '''
               select countryName,confirmed,dead,crued from otherCountry
           '''
    cursor = c.execute(sql)
    for item in cursor:
        number = []
        if requestCountry == item[0]:
            number.append(item[1])
            number.append(item[2])
            number.append(item[3])
            return render_template("test.html",number = number,requestCountry = requestCountry)


if __name__ == "__main__":
    app.run(debug = True)
