import blog.ncovdata as ncovdata
from django.shortcuts import render
from blog.models import Myuser
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
from pyecharts import options as opts
from pyecharts.charts import Page, Pie

yiqingUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"

def createChinaMap(chinaProvinceMatchConfirm):
    chinaProvinces = list(chinaProvinceMatchConfirm.keys())
    provinceConfim = list(chinaProvinceMatchConfirm.values())
    pie1=(
        Pie(init_opts=opts.InitOpts(width="400px", height="260px"))
            .add(
                "",
                [[chinaProvinces[i],provinceConfim[i]] for i in range(len(chinaProvinces))],
                radius=["50%", "75%"],
                center=["50%", "50%"],
                rosetype="area",
                )
            .set_global_opts(
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="10%", pos_left="100%" #图例设置
                    ),
                )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) #设置标签，
            )
    pie1.render('blog/static/pie1.html')

def createProvincePie(province,provinceMatchConfirm):
    provinceCitys = list(provinceMatchConfirm.keys())
    #城市名称标准化
    provinceCitys = [i+'市'  if i !="境外输入" else i for i in provinceCitys]
    citysConfirm = list(provinceMatchConfirm.values())
    # provinceCitys =['济南市', '青岛市', '泰安市', '烟台市', '淄博市', '枣庄市', '潍坊市', '济宁市', '威海市','日照市','临沂市','德州市','聊城市','滨州市','菏泽市','境外输入']
    #citysConfirms=['280','63','35','47','30','24','44','260','38','16','49','37','38','15','11','22']
    list1 = [[provinceCitys[i],citysConfirm[i]] for i in range(len(provinceCitys))] #首先创建数据
    #map_1
    map_1 = Map(init_opts=opts.InitOpts(width="400px", height="460px")) #创建地图，其中括号内可以调整大小，也可以修改主题颜色。
    map_1.add("山东疫情", list1, maptype=province) #添加山东地图
    map_1.set_global_opts( #设置全局配置项
    #title_opts=opts.TitleOpts(title="山东疫情"), 添加标题
    visualmap_opts=opts.VisualMapOpts(max_=300, is_piecewise=True),#最大数据范围 并且使用分段
    legend_opts=opts.LegendOpts(is_show=False), #是否显示图例
    )
    #map_2
    map_2 = (
    Pie(init_opts=opts.InitOpts(width="600px", height="500px")) #创建一个饼图
    .add(
        "", #图名
        [[provinceCitys[i],citysConfirm[i]] for i in range(len(provinceCitys))], #添加数据
        radius=["40%", "75%"], # 调整半径
    )
    .set_global_opts(
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_top="10%", pos_left="88%" #图例设置
        ),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) #设置标签
    )
    map_1.render('blog/static/map1.html')# 地图
    map_2.render('blog/static/map2.html') #饼图  保存到本地
