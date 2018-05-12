from bs4 import BeautifulSoup
import re
#from sql import *
from app_modules.sql import db_utilities
import sys
#still liek python 2 :(
if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

class aliexpress():
	def __init__(self):
		self.utils = db_utilities()


	def add_top_ten(self, soup, item_type):
		items = soup.findAll("div", {"class": "item"})
		items = items[:10]
		for item in items:
			#gets name and image of product
			name = item.find(class_="info").find("a").get("title")
			image = item.find(class_="pic").find("a").find(class_="picCore").get('src')
			if image is None:
				image = item.find(class_="pic").find("a").find(class_="picCore").get('image-src')

			regex = re.compile(r'((\d)+)')
			orders = regex.search(item.find(class_="order-num-a ").find("em").text)
			orders = int(orders.group())
			#add to db
			self.utils.add_item(name, orders, image, item_type, 0)



	def add_query_to_db(self, query_url, item_type):
		request = urlopen(query_url)
		soup = BeautifulSoup(request, 'html.parser')	#chnge back request.read()
		self.utils.add_type(item_type, query_url)
		self.utils.add_top_ten(soup, item_type)

	#tries to find the product and finds difference in sales
	def compare_update(self):
		types = self.utils.return_type()
		for t in types:
			request = urlopen(t.query)
			soup = BeautifulSoup(request, 'html.parser')	
			items = soup.findAll("div", {"class": "item"})
			items = items[:10]
			for item in items:
				#gets name and image of product
				name = item.find(class_="info").find("a").get("title")
				image = item.find(class_="pic").find("a").get("href")
				regex = re.compile(r'((\d)+)')
				orders = regex.search(item.find(class_="order-num-a ").find("em").text)
				orders = int(orders.group())
				if self.utils.find_item(name) == None:
					self.utils.add_item(name, orders, image, t.name, 0)
				else:
					self.utils.update_item(name,orders)

	def return_table(self):
		return self.utils.return_table()



test = aliexpress()
test.compare_update()




##tests##
#add_query_to_db("https://www.aliexpress.com/premium/earrings.html?site=glo&groupsort=1&SearchText=earrings&g=y&SortType=total_tranpro_desc&tc=ppc&initiative_id=SB_20180510001905&filterCat=200000144,200000141,200190014", 'earrings')
#https://www.aliexpress.com/premium/watch.html?spm=2114.search0204.0.0.2fac57a3E0T9Ua&site=glo&groupsort=1&SearchText=watch&g=y&SortType=total_tranpro_desc&tc=ppc&initiative_id=SB_20180508225242&filterCat=200214036,200214007,200214011


#add_query_to_db("https://www.aliexpress.com/premium/survival.html?spm=2114.search0204.0.0.2bfc3e2azzTv6D&site=glo&groupsort=1&SearchText=survival&g=y&SortType=total_tranpro_desc&tc=ppc&initiative_id=AS_20180509135956&filterCat=200215442,200215579,200215441", 'survival')
