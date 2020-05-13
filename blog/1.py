import ncovdata
import requests
yiqingUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
china_data = ncovdata.getChinaData(yiqingUrl)
chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal \
                                                = ncovdata.getChinaProvince(china_data=china_data)
for province,provinceId in chinaProvinceRe.items():
    print(provinceId,province,chinaProvinceMatchConfirm[province],chinaProvinceMatchDead[province],chinaProvinceMatchHeal[province])


print("***********************************************************************")
dataChangeListUrl = "https://wuliang.art/ncov/statistics/dataChangeList"
dataChangeList = requests.get(dataChangeListUrl,timeout=3).json()
dataAddChange = dataChangeList["data"]["chinaDayAddList"]
dataAllChange = dataChangeList["data"]["chinaDayList"]
dailyAddConfirm = {}
dailyAddSuspect = {}
dailyAddHeal = {}
dailyAddDead = {}
for i  in range(len(dataAddChange)):
    dailyAddConfirm[dataAddChange[i]["date"]]=dataAddChange[i]["confirm"]
    dailyAddSuspect[dataAddChange[i]["date"]]=dataAddChange[i]["suspect"]
    dailyAddDead[dataAddChange[i]["date"]]=dataAddChange[i]["dead"]
    dailyAddHeal[dataAddChange[i]["date"]]=dataAddChange[i]["heal"]
print(dailyAddConfirm.keys())
print("*******************************Conirm****************************************")
print(dailyAddConfirm.values())
print("********************************Dead***************************************")
print(dailyAddDead.values())
print("**********************************Heal*************************************")
print(dailyAddHeal.values())
# shandongProvinceId = chinaProvinceRe["山东"]
# shandongRe,shandongMatchConfirm,shandongMatchDead,shandongMatchHeal \
#                                                 = ncovdata.getProvince(china_data=china_data,provinceId=shandongProvinceId)
# for city,cityId in shandongRe.items():
#     print(cityId,city,shandongMatchConfirm[city],shandongMatchDead[city],shandongMatchHeal[city])
# dataChange = ncovdata.getDataChangeList()
