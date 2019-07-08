import requests
from lxml import html
import re
from tqdm import tqdm
import MySQLdb
from config import DB_INFO
def clean_html(meta_data:str)->str:
    return re.sub(r'<.*?>','',meta_data)
class GeneralSprider:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    def __init__(self,url,table_name,title_parser,news_parser):
        self.url = url
        self.title_parser = title_parser
        self.news_parser = news_parser
        self.table_name = table_name
        self.title_url = []
        self.news = []
        self.conn = MySQLdb.connect(
            **DB_INFO
        )
        self.cur = self.conn.cursor()
        self.run()

    def __del__(self):
        self.conn.close()

    def get_title(self)->list:
        response = requests.get(self.url,headers=self.HEADERS)
        if response.status_code != 200:
            raise Exception(f'{self.url}没有获取到有效的页面')
        tree = html.fromstring(response.text)
        for source_title in tree.xpath(self.title_parser):
            self.title_url.append(source_title.attrib['href'])

    def run(self):
        print(f'开始抓取{self.table_name}', flush=True)
        self.get_title()
        for url in tqdm(self.title_url):
            self.get_news(url)
        self.save()

    def get_news(self,title_url):
        response = requests.get(title_url,headers=self.HEADERS)
        data = {}
        for key in self.news_parser.keys():
            goal = re.findall(self.news_parser[key],response.text)
            data[key] = clean_html(goal[0]) if goal else '' 
        self.news.append(data)

    def insert_db(self,data,pk='title'):
        sql = f'INSERT INTO {self.table_name} \
            ({",".join(data.keys())})\
            VALUES\
            {tuple(data.values())}\
            ON DUPLICATE KEY UPDATE {pk} = "{data.get(pk)}"\
            ;'        
        self.cur.execute(sql)

    def save(self):
        count = 0
        for new in self.news:
            if new['context']:
                count +=1
                self.insert_db(new)
        print(f'插入{count}条新闻', flush=True)
        self.conn.commit()
if __name__ == "__main__":
    linuxsprider = GeneralSprider(
        'https://linux.cn/news/',
        'LinuxNews',
        '//div[@class="block"]//span[@class="title"]/a',
        {
            'title': r'<h1 class="ph" .*?>(.*?)</h1>',
            'author': r'<span class="textcut">(.*?)</span>',
            'datatime': r'\d+-\d+-\d+ \d+:\d+',
            'source': r'<p>来源：(.*?)</p>',
            'cover': r'url\((https://img.linux.net.cn/.*?)\)',
            'context': r'<div id="article_content".*?>([\s\S]*?)<h3>更多资讯</h3>',
        },
    )
    itHome = GeneralSprider(
        'https://it.ithome.com/',
        'ItHomeNews',
        '//div[@class = "block new-list-1"]//a',
        {
            'title': r'<h1>(.*?)</h1>',
            'author': r'作者：<strong>(.*?)</strong>',
            'datatime': r'\d+-\d+-\d+ \d+:\d+:\d+',
            'source': r'来源：<a .*?>(.*?)</a>',
            'cover': r'data-original="(.*?)"',
            'context': r'<div class="post_content" id="paragraph">[\s\S]*?</div>',
        },
    )