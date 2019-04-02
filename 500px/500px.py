import requests
import re
from bs4 import BeautifulSoup
import time
import os
import logging
 
logging.basicConfig(
	level=logging.INFO, 
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class PixabaySpider():
	"""爬取 500px 对应尺寸的图片

	"""
	def __init__(self):
		self.prefix_url = "https://pixabay.com"
		self.min_height = 1080
		self.min_width = 1920
		self.start_page = 1
		self.end_page = 5
		self.headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
			'cookie': 'is_human=1; _ga=GA1.2.1850162889.1547365538; __cfduid=dcfa99483b3f8b942dca5e9ea04313e2a1552194897; _gid=GA1.2.291527365.1552194900; lang=zh; sessionid=".eJxVjEsOwiAUAO_C2hA-LSlehrxHnwWF1vDZaLy7tQuTbicz82Yuwbp0WIhd2SuwC3PQW3C9UnEBatgxDkriSCTIozZGo0WjpVCTma2aEMQgb1pJdY4R_IPWee-fZbuTb7y3mCr3vbYtHyKPh7pCJrcVRxli-nenWfx9rLKDGEf2-QJ3wT0t:1h2tAi:Fk5STARN9jvc7EJxT8_bPclP24U"; csrftoken=EIIEKQ526F3PZz4VOOFfw8ENFgmQo9UVDzXwRN2BN7NHUo0vt3LLnwqrzTFxA7GK; client_width=1399',
		}

	def parse(self):
		"""获取每个搜索页面的图片链接

		"""

		url = "https://pixabay.com/images/search/?min_height={0}&min_width={1}&pagi={2}"
		
		for page in range(self.start_page, self.end_page+1):
			logger.info("获取第{0}页结果".format(page))
			request_url = url.format(self.min_height, self.min_width, page)
			resp = requests.get(request_url)
			pattern = re.compile('<a.+?href="(/photos/(?!search).+?-\d*/)">', re.S)
			items = re.findall(pattern, resp.text)

			for rear_url in items:
				try:
					self.parse_detail(self.prefix_url+rear_url)
				except:
					continue

	def parse_detail(self, url):
		"""在对应图片页面获取下载链接

		"""
		try:
			resp = requests.get(url)
		except:
			logger.error("进入图片链接{0}失败".format(url))

		soup = BeautifulSoup(resp.text, 'lxml')
		file_name = soup.select("[data-perm='check']")[-1]['value']
		download_url = "https://pixabay.com/zh/images/download/{0}?attachment".format(file_name)
		
		try:
			image = requests.get(download_url, headers=self.headers).content
		except:
			logger.error("下载图片{0}失败".format(file_name))

		self.save_image(file_name, image)

	def save_image(self, file_name, image):
		"""保存图片
		"""
		if os.path.exists(file_name):
			logger.info("图片{0}已存在".file_name)
		else:
			logger.info("开始保存 {0}".format(file_name))
			with open(file_name, 'wb') as f:
				f.write(image)
			logger.info("保存完成 {0}".format(file_name))
			time.sleep(5)

pixabay = PixabaySpider()
pixabay.parse()
