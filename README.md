# NewsSpider
一个可以指定规则的通用新闻爬虫
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
## Docker 使用
### Mac or Windows
默认数据库Host是`host.docker.internal`  
也就是被指向了宿主机的地址
需要在环境变量中指定数据库密码 `passwd`
其他配置信息见`config.py`文件
运行:
```shell
docker build -t tmp .
docker run --rm  -e passwd=passwd tmp 
```
### Linux
由于 `Docker for Linux` 并不支持 `host.docker.internal` 的写法  
如果需要绑定宿主机 可以把网络模式改为`host`   
同时把在环境变量中 `host` 指向 `127.0.0.1` (不要使用localhost)  
```shell
docker build -t tmp. 
docker run --net host --rm  -e host=127.0.0.1 -e passwd=password tmp
```