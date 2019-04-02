import pymongo
import time
import pprint
import logging
from logging.config import fileConfig
import requests
import re
from bs4 import BeautifulSoup
 	
fileConfig("logging_config.conf")

logger = logging.getLogger('root')

def get_database():
	host = "127.0.0.1"
	port = 27017

	conn = pymongo.MongoClient(host=host, port=port)
	db = conn.get_database("hitokoto")
	
	return db


def get_time():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def save_categories(db, collection_name):
	"""存储分类, 暂时一次性插入

	db: 数据库对象 hitokoto
	collection_name: 集合名称 categories
	"""
	categories = db.get_collection(collection_name)
	cate_list = [
		{
			"created_time": get_time(),
			"initial": "a",
			"name": "Anime",
			"chinese": "动画",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "c",
			"name": "Comic",
			"chinese": "动漫",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "g",
			"name": "Game",
			"chinese": "游戏",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "n",
			"name": "Novel",
			"chinese": "小说",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "m",
			"name": "Myself",
			"chinese": "原创",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "I",
			"name": "Internet",
			"chinese": "网络",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "o",
			"name": "Other",
			"chinese": "其他",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "p",
			"name": "Poetry",
			"chinese": "古诗",
			"modiflied_time": get_time()
		},
		{
			"created_time": get_time(),
			"initial": "v",
			"name": "Verse",
			"chinese": "宋词",
			"modiflied_time": get_time()
		}
	]

	categories.insert_many(cate_list)

	# for cate in cate_list:
	# 	# 存在时则更新修改时间，不存在时则插入

	# 	categories.update(
	# 			{"initial": cate["initial"]}, 
	# 			{"$set":{"modiflied_time": get_time()}},
	# 			True
	# 		)


def get_categories(db, collection_name):
	categories = db.get_collection(collection_name)
	for cate in categories.find():
		pprint.pprint(cate)


class JuZiMi:

	def __init__(self):
		self.headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
		}

		self.db = get_database()
		self.hitokoto = self.db.get_collection("hitokoto")


	def anime_pages(self):
		base_url = "https://www.juzimi.com"
		start_url = "https://www.juzimi.com/allarticle/dongmantaici?page={0}"

		resp = requests.get(start_url.format(0), headers=self.headers)
		soup = BeautifulSoup(resp.text, 'lxml')

		last_page = soup.select(".pager-item")[-1].text


		for page in range(int(last_page)):
		#for page in range(int("1")):
			logger.info("爬取第{0}页动漫页".format(page))
			resp = requests.get(start_url.format(page), headers=self.headers)
			

			# 请求不成功则跳过
			if resp.status_code != 200:
				logger.warn("请求不成功，状态码为{0}".format(resp.status_code))
				continue

			soup = BeautifulSoup(resp.text, 'lxml')

			for view in soup.select(".views-field-phpcode"):
				a_label = view.select(".xqallarticletilelink")[0]
				come_from = "《{0}》".format(a_label.text)
				url = base_url + a_label['href'] + "?page={0}"

				# 获取默认作者，无则""
				if len(view.select("a"))==4:
					author = view.select("a")[1].text
				else:
					author = ""

				self.anima_detail_pages(come_from, url, author)

	def anima_detail_pages(self, come_from, url, author):
		logger.info("开始爬取{0}语录".format(come_from))

		start_url = url.format(0)

		resp = requests.get(start_url, headers=self.headers)
		soup = BeautifulSoup(resp.text, 'lxml')

		if soup.select(".pager-last"):
			last_page = soup.select(".pager-last")[0].text
		else:
			last_page = "1"

		for page in range(int(last_page)):
		#for page in range(int("1")):
			logger.info("开始爬取{0}语录第{1}页".format(come_from, page))
			resp = requests.get(url.format(page), headers=self.headers)
			
			if resp.status_code != 200:
				logger.warn("请求不成功，状态码为{0}".format(resp.status_code))
				continue

			soup = BeautifulSoup(resp.text, 'lxml')

			for view in soup.select(".views-row"):
				if view.select(".xlistju"):
					body = view.select(".xlistju")[0].text
				else:
					continue
				category = 'a'
				if view.select(".views-field-field-oriwriter-value"):
					authors = view.select(".views-field-field-oriwriter-value")[0].text
				else:
					authors = author

				info = {
					"hitokoto": body,
					"category": category,
					"from": come_from,
					"creator": authors,
					"created_time": get_time()
				}

				self.hitokoto.insert(info)

			time.sleep(3)


				# logger.info("{0} -- {1}".format(body, authors))
		logger.info("结束爬取{0}语录".format(come_from))




"""
id, body, category, from, author, created_time
"""

# db = get_database()
# save_categories(db, "categories")
# get_categories(db, "categories")
juzimi = JuZiMi()
juzimi.anime_pages()
