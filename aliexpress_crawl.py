from bs4 import BeautifulSoup
import re
from sql import *
import sys

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen



#request = urllib.urlopen("https://www.aliexpress.com/w/wholesale-necklace.html?initiative_id=SB_20180508171940&site=glo&groupsort=1&SortType=total_tranpro_desc&g=y&SearchText=necklace")
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

		regex = re.compile(r'((\d)+)')
		orders = regex.search(item.find(class_="order-num-a ").find("em").text)
		orders = int(orders.group())
		#add to db
		add_item(name, orders, image, item_type, 0)



def add_query_to_db(query_url, item_type):
	request = urlopen(query_url)
	soup = BeautifulSoup(request, 'html.parser')	#chnge back request.read()
	add_type(item_type, query_url)
	add_top_ten(soup, item_type)

#tries to find the product and finds difference in sales
def compare_update():
	types = return_type()
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
			if find_item(name) == None:
				add_item(name, orders, image, t.name, 0)
			else:
				update_item(name,orders)


#add_query_to_db("https://www.aliexpress.com/w/wholesale-necklace.html?initiative_id=SB_20180508171940&site=glo&groupsort=1&SortType=total_tranpro_desc&g=y&SearchText=necklace")
#https://www.aliexpress.com/premium/watch.html?spm=2114.search0204.0.0.2fac57a3E0T9Ua&site=glo&groupsort=1&SearchText=watch&g=y&SortType=total_tranpro_desc&tc=ppc&initiative_id=SB_20180508225242&filterCat=200214036,200214007,200214011









# for div in mydivs:
# 	test = div.find("div", {"class": "info"})
# 	print test
# 	print "\n\n\n"
# 	print len(test)
# 	#test = test.find("h3", {"class": "icon-hotproduct "})
	
# 	#test = test.find("a", {"class": "history-item product "})
# 	print test


