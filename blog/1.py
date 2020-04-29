import ncovdata

yiqingUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
china_data = ncovdata.getChinaData(yiqingUrl)
chinaProvinceRe,chinaProvinceMatchConfirm,chinaProvinceMatchDead,chinaProvinceMatchHeal \
                                                = ncovdata.getChinaProvince(china_data=china_data)
for province,provinceId in chinaProvinceRe.items():
    print(provinceId,province,chinaProvinceMatchConfirm[province],chinaProvinceMatchDead[province],chinaProvinceMatchHeal[province])

print("***********************************************************************")
shandongProvinceId = chinaProvinceRe["山东"]
shandongRe,shandongMatchConfirm,shandongMatchDead,shandongMatchHeal \
                                                = ncovdata.getProvince(china_data=china_data,provinceId=shandongProvinceId)
for city,cityId in shandongRe.items():
    print(cityId,city,shandongMatchConfirm[city],shandongMatchDead[city],shandongMatchHeal[city])
dataChange = ncovdata.getDataChangeList()
