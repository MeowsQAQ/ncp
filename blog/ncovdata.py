from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests, json
from pyecharts.charts import Pie ,Grid,Bar,Line
from pyecharts.faker import Faker
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import time, datetime

yiqingUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
dataChangeListUrl = "https://wuliang.art/ncov/statistics/dataChangeList"
globalData = "https://lab.isaaclin.cn/nCoV/api/area?lastest=1"

def getGlobalData():
    globalData = "https://lab.isaaclin.cn/nCoV/api/area?lastest=1"
    globalList = requests.get(globalData,timeout=3,verify =False).json()
    globalList = globalList["results"]
    countriesConfirm = {}
    countriesCrued = {}
    countriesDead = {}
    countries = {}
    for i in range(len(globalList)):
        if(globalList[i]["countryName"]!="中国"):
            countries[i] = globalList[i]["countryName"]
            countriesConfirm[globalList[i]["countryName"]]=globalList[i]["confirmedCount"]
            countriesCrued[globalList[i]["countryName"]]=globalList[i]["curedCount"]
            countriesDead[globalList[i]["countryName"]]=globalList[i]["deadCount"]
    return countriesConfirm,countriesCrued,countriesDead,countries

def getDataChangeList():
    #获取api返回的json，并进行格式化
    dataChangeListUrl = "https://wuliang.art/ncov/statistics/dataChangeList"
    dataChangeList = requests.get(dataChangeListUrl,timeout=3).json()
    #将每日新增，以及每日情况分别命名dataAddChange和dataAllChange，并新建每日新增确诊，疑似，死亡病例的字典
    dataAddChange = dataChangeList["data"]["chinaDayAddList"]
    dataAllChange = dataChangeList["data"]["chinaDayList"]
    dailyAddConfirm = {}
    dailyAddSuspect = {}
    dailyAddDead = {}
    #遍历dataAddChange,并对每日新增确诊、疑似、死亡字典进行填充,key为日期，value为人数
    for i  in range(len(dataAddChange)):
        dailyAddConfirm[dataAddChange[i]["date"]]=dataAddChange[i]["confirm"]
        dailyAddSuspect[dataAddChange[i]["date"]]=dataAddChange[i]["suspect"]
        dailyAddDead[dataAddChange[i]["date"]]=dataAddChange[i]["dead"]
    print(dailyAddConfirm.keys())
    print(dailyAddConfirm.values())
    print(sum(dailyAddDead.values()))
    print("*********************")
    #将湖北确诊数据命名为dataHubeiAddConfirm,同上方法得到湖北确诊和非湖北确诊
    dataHubeiAddConfirm  = dataChangeList["data"]["dailyNewAddHistory"]
    dailyHubeiAddConfirm = {}
    dailyNotHubeiAddConfirm = {}
    for i in range(len(dataHubeiAddConfirm)):
        dailyHubeiAddConfirm[dataHubeiAddConfirm[i]["date"]] = dataHubeiAddConfirm[i]["hubei"]
        dailyNotHubeiAddConfirm[dataHubeiAddConfirm[i]["date"]] = dataHubeiAddConfirm[i]["notHubei"]
    print("HUBEICONFIRM")
    print(dailyHubeiAddConfirm.keys())
    print(dailyHubeiAddConfirm.values())
    print("WUHANCONFIRM")
    #同理得到武汉确诊情况
    dataWuhanAddConfirm  = dataChangeList["data"]["wuhanDayList"]
    dailyWuhanAddConfirm = {}
    for i in range(len(dataWuhanAddConfirm)):
        dailyWuhanAddConfirm[dataWuhanAddConfirm[i]["date"]] = dataWuhanAddConfirm[i]["wuhan"]["confirmAdd"]
    print(dailyWuhanAddConfirm.keys())
    print(dailyWuhanAddConfirm.values())
    return dataAddChange,dataAllChange

def getUpdateTime():
    yiqingUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    yiqingShuju = requests.post(yiqingUrl,timeout=3).json()
    data = json.loads(yiqingShuju["data"])
    lastUpdateTime = data["lastUpdateTime"]
    return lastUpdateTime

def getChinaData(yiqingUrl):
        yiqingShuju = requests.post(yiqingUrl,timeout=3).json()
        data = json.loads(yiqingShuju["data"])
        china_data=data["areaTree"][0]["children"]
        return china_data

def getChinaProvince(china_data):
    chinaProvinceMatchConfirm = {}
    chinaProvinceMatchDead = {}
    chinaProvinceMatchHeal = {}
    chinaProvinceRe = {}
    for i in range(len(china_data)):
        chinaProvinceRe[china_data[i]["name"]]=i
        chinaProvinceMatchConfirm[china_data[i]["name"]] = china_data[i]["total"]["confirm"]
        chinaProvinceMatchDead[china_data[i]["name"]] = china_data[i]["total"]["dead"]
        chinaProvinceMatchHeal[china_data[i]["name"]] = china_data[i]["total"]["heal"]
    return chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal

def getProvince(china_data,provinceId):
    province_data = china_data[provinceId]["children"]
    print(provinceId)
    provinceMatchConfirm = {}
    provinceMatchDead = {}
    provinceMatchHeal = {}
    provinceRe = {}
    for i in range(len(province_data)):
        provinceRe[province_data[i]["name"]]=i
        provinceMatchConfirm[province_data[i]["name"]] = province_data[i]["total"]["confirm"]
        provinceMatchDead[province_data[i]["name"]] = province_data[i]["total"]["dead"]
        provinceMatchHeal[province_data[i]["name"]] = province_data[i]["total"]["heal"]
    return provinceRe,provinceMatchConfirm,provinceMatchDead,provinceMatchHeal

def getRumour(rumourUrl):
    response = requests.get(rumourUrl,timeout=3).json()
    yaoyan=response["data"]
    rumours = {}
    rumours_date = {}
    rumours_author = {}
    rumours_title = {}
    rumoursNum=5
    for i in range(1,rumoursNum):
        rumours[i] = yaoyan[i]
        rumours_date= yaoyan[i]["date"]
        rumours_author= yaoyan[i]["author"]
        rumours_title= yaoyan[i]["title"]
    return rumours
