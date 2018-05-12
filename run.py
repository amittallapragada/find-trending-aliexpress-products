from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sqlalchemy.orm import sessionmaker
import os
from app_modules.aliexpress_crawl import aliexpress

#template directory
template_dir = os.getcwd() + "/app_modules/templates/" 

app = Flask(__name__, template_folder=template_dir)

#creates aliexpress object
utils = aliexpress()

#home directory displays current values in the database
@app.route('/')
def index():
	output = utils.return_table()
	return render_template('home.html', dict = output)	

#adds a new type and it's top 10 products to the database
@app.route('/add', methods=['GET','POST'])
def add():
	if request.method == "POST":
		item_type = request.form['type']
		url = request.form['url']
		utils.add_query_to_db(url,item_type)
		return render_template('add_product.html')
	else:
		return render_template('add_product.html')

#calls the compare_update function which will scrape the pages in the types database
@app.route('/update')
def update():
	utils.compare_update()
	return "finished updating"

#uncomment this to run locally
app.run()