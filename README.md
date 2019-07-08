# NewsSpider
一个可以指定规则的新闻爬虫
## 设计思路
采集新闻网站的首页 
在首页得到每篇新闻的`URL`
然后再去抓取每篇新闻的内容 
按照写好的`页面解析`规则进行解析
最后把按照规则解析的数据保存到数据库中
## 使用
```
pip install -r requester
env passwd=password host=host python3 main.py  
```
## Docker使用
默认数据库Host是宿主机的3306端口
需要在环境变量中指定数据库密码 `passwd`
其他配置信息见`config.py`文件
运行:
```shell
docker build -t tmp .
docker run --rm  -e passwd=dreamst@2019 tmp 
```