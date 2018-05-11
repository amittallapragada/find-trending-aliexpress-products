from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sqlalchemy.orm import sessionmaker
from sql import *
from aliexpress_crawl import *

app = Flask(__name__)


utils = aliexpress()

@app.route('/')
def index():

	output = utils.return_table()
	return render_template('home.html', dict = output)	

@app.route('/add', methods=['GET','POST'])
def add():
	if request.method == "POST":
		item_type = request.form['type']
		url = request.form['url']
		utils.add_query_to_db(url,item_type)
		return render_template('add_product.html')
	else:
		return render_template('add_product.html')

@app.route('/update')
def update():
	utils.compare_update()
	return "finished updating"


utils.compare_update()