#运行
##准备工作
```shell
pip install django
pip install mysqlclient
pip install request
```
###NCP数据仓库
https://raw.githubusercontent.com/BlankerL/DXY-2019-nCoV-Data/master/csv/DXYArea.csv
```shell
pip install pyecharts -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```
##运行
```shell
python manage.py runserver
python manage.py migrate
```
