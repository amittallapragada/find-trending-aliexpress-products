import urllib
from bs4 import BeautifulSoup
import re
from sql import *
#request = urllib.urlopen("https://www.aliexpress.com/w/wholesale-necklace.html?initiative_id=SB_20180508171940&site=glo&groupsort=1&SortType=total_tranpro_desc&g=y&SearchText=necklace")
output = file('output.html').read()
#soup = BeautifulSoup(output, 'html.parser')

def add_top_ten(soup, item_type):
	items = soup.findAll("div", {"class": "item"})
	items = items[:10]
	for item in items:
		#gets name and image of product
		name = item.find(class_="info").find("a").get("title")
		image = item.find(class_="pic").find("a").find(class_="picCore").get('src')
		if image is None:
			image = item.find(class_="pic").find("a").find(class_="picCore").get('image-src')
		print image

		regex = re.compile(r'((\d)+)')
		orders = regex.search(item.find(class_="order-num-a ").find("em").text)
		orders = int(orders.group())
		#add to db
		add_item(name, orders, image, item_type, 0)



def add_query_to_db(query_url, item_type):
	request = urllib.urlopen(query_url)
	soup = BeautifulSoup(request.read(), 'html.parser')	#chnge back request.read()
	add_type(item_type, query_url)
	add_top_ten(soup, item_type)

#tries to find the product and finds difference in sales
def compare_update():
	types = return_type()

	for t in types:
		request = urllib.urlopen(t.query)
		soup = BeautifulSoup(request.read(), 'html.parser')	
		items = soup.findAll("div", {"class": "item"})
		items = items[:10]
		for item in items:
			#gets name and image of product
			name = item.find(class_="info").find("a").get("title")
			image = item.find(class_="pic").find("a").get("href")
			regex = re.compile(r'((\d)+)')
			orders = regex.search(item.find(class_="order-num-a ").find("em").text)
			orders = int(orders.group())
			if find_item(name) == None:
				add_item(name, orders, image, t.name)
			else:
				update_item(name,orders)




#add_query_to_db("https://www.aliexpress.com/w/wholesale-necklace.html?initiative_id=SB_20180508171940&site=glo&groupsort=1&SortType=total_tranpro_desc&g=y&SearchText=necklace")

#watches
#https://www.aliexpress.com/premium/watch.html?spm=2114.search0204.0.0.2fac57a3E0T9Ua&site=glo&groupsort=1&SearchText=watch&g=y&SortType=total_tranpro_desc&tc=ppc&initiative_id=SB_20180508225242&filterCat=200214036,200214007,200214011









# for div in mydivs:
# 	test = div.find("div", {"class": "info"})
# 	print test
# 	print "\n\n\n"
# 	print len(test)
# 	#test = test.find("h3", {"class": "icon-hotproduct "})
	
# 	#test = test.find("a", {"class": "history-item product "})
# 	print test


