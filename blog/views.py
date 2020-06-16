import blog.ncovdata as ncovdata
from django.shortcuts import render
from blog.models import Myuser
import blog.charts as dataCharts
# Create your views here.
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate,login as auth_login ,logout
from blog.forms import SignupForm
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
from pyecharts.charts import Pie ,Grid,Bar,Line
from pyecharts.faker import Faker #数据包
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
global jifen

def home(request):
    return render(request,'index.html',locals())


def index(request):
    Url1="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    shuju = requests.post(Url1,timeout=3).json()
    data = json.loads(shuju["data"])
    china_data=data["areaTree"][0]["children"]
    total = data["areaTree"][0]["total"]["confirm"]
    cured = data["areaTree"][0]["total"]["heal"]
    yisi = data["areaTree"][0]["total"]["suspect"]
    dead = data["areaTree"][0]["total"]["dead"]
    lastestUpdateTime = ncovdata.getUpdateTime()
    shandong_total = data["areaTree"][0]["children"][13]["total"]["confirm"]
    shandong_crued = data["areaTree"][0]["children"][13]["total"]["heal"]
    jinan_total = 42#data["areaTree"][0]["children"][13]["children"][3]["total"]["confirm"]

    chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal \
                                                    = ncovdata.getChinaProvince(china_data=china_data)
    province = "山东"
    provinceId = chinaProvinceRe["山东"]
    provinceRe,provinceMatchConfirm,provinceMatchDead,provinceMatchHeal \
                                                    = ncovdata.getProvince(china_data=china_data,provinceId=provinceId)
    dataCharts.createProvincePie(province,provinceMatchConfirm=provinceMatchConfirm)
    rumourUrl ="https://wuliang.art//ncov/rumor/getRumorList?page=1"
    yaoyan = ncovdata.getRumour(rumourUrl=rumourUrl)
    return render(request, 'index.html',locals())
    #logout(request)   # 这个方法，会将存储在用户session的数据全部清空
    #return render(request, 'login.html', {'msg': ''})

def tables(request):
    ########

    #shuju = requests.post("https://service-nxxl1y2s-1252957949.gz.apigw.tencentcs.com/release/newpneumonia")
    #shuju = requests.post("https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5")
    Url1="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    shuju = requests.post(Url1,timeout=3).json()
    data = json.loads(shuju["data"])
    china_data = ncovdata.getChinaData(Url1)
    chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal \
                                                    = ncovdata.getChinaProvince(china_data=china_data)

    provinceId = chinaProvinceRe["山东"]
    provinceRe,provinceMatchConfirm,provinceMatchDead,provinceMatchHeal \
                                                    = ncovdata.getProvince(china_data=china_data,provinceId=provinceId)
    countriesConfirm,countriesCrued,countriesDead,countries =ncovdata.getGlobalData()
    lastestUpdateTime = ncovdata.getUpdateTime()
    return render(request, 'tables.html',locals())

def map1(request):

    return render(request, 'map1.html',locals())

def map2(request):

    return render(request, 'map2.html',locals())

def test(request):

    return render(request, 'test.html',locals())


def charts(request):
    Url1="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    shuju = requests.post(Url1,timeout=3).json()
    data = json.loads(shuju["data"])
    china_data = ncovdata.getChinaData(Url1)
    chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal \
                                                    = ncovdata.getChinaProvince(china_data=china_data)


    dataCharts.createChinaMap(chinaProvinceMatchConfirm=chinaProvinceMatchConfirm)
    lastestUpdateTime = ncovdata.getUpdateTime()


    return render(request, 'charts.html',locals())

def line(request):

    return render(request, 'line.html',locals())

def pie1(request):

    return render(request, 'pie1.html',locals())
def pie2(request):

    return render(request, 'pie2.html',locals())

def map3(request):

    return render(request, 'map3.html',locals())

def forecast(request):
    Url1="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    shuju = requests.post(Url1,timeout=3).json()
    data = json.loads(shuju["data"])
    china_data = ncovdata.getChinaData(Url1)
    chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal \
                                                        = ncovdata.getChinaProvince(china_data=china_data)


    dataCharts.createChinaMap(chinaProvinceMatchConfirm=chinaProvinceMatchConfirm)
    lastestUpdateTime = ncovdata.getUpdateTime()

    return render(request, 'forecast.html',locals())
