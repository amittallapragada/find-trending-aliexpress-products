from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy import update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from app_modules.config.db_config import *
Base = declarative_base()

#creates a product
class User(Base):
    """"""
    __tablename__ = "items"

    prod_id = Column('product number', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(1000))
    orders = Column("orders", Integer)
    image = Column('image', String(1000))
    item_type = Column('type', String(1000))
    change = Column('change', Integer)


    def __init__(self, name, orders, image, item_type, change):
        self.name = name
        self.orders = orders
        self.image = image
        self.item_type = item_type
        self.change = change



class types(Base):
    """"""
    __tablename__ = "item_type"
    prod_id = Column('product number', Integer, autoincrement=True, primary_key=True)
    name = Column('item_type', String(1000))
    query = Column('query', String(1000))



    def __init__(self, name, query):
        self.name = name
        self.query = query



#Base.metadata.create_all(engine)


class db_utilities():
	def __init__(self):
		self.engine = create_engine(heroku_engine, pool_size = 20, pool_recycle = 280)

	#add to type table
	def add_type(self, name, url):
		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		#create item
		new_item = types(name,url)
		#add item
		s.add(new_item)
		#commit to db
		s.commit()
		#close session
		s.close()
		#close connection
		conn.close()



	def return_type(self):
		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		output = []
		query = s.query(types)
		for q in query:
			output.append(q)
		#close connections
		s.close()
		conn.close()
		return output




	#adds item
	def add_item(self,name, orders, image, item_type, change):

		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		#create item
		new_item = User(name,orders,image, item_type, change)
		#add item
		s.add(new_item)
		#commit to db
		s.commit()
		#close connections
		s.close()
		conn.close()



	#finds item based on name
	def find_item(self,name):
		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		query = s.query(User).filter(User.name.in_([name]))	
		result = query.first()
		s.close()
		conn.close()
		return result


	#update row
	def update_item(self,name, orders):

		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		change = 0
		curr_item = s.query(User).filter(User.name.in_([name])).first()
		if int(curr_item.orders) < orders:
			change = int(curr_item.change) +  orders - int(curr_item.orders)
			curr_item.orders = orders
			curr_item.change = change
			s.commit()
		
		elif int(curr_item.orders) > orders:
			change = int(curr_item.change) -  (int(curr_item.orders) - orders) 
			curr_item.orders = orders
			curr_item.change = change
			s.commit()
		s.close()
		conn.close()


	#delete item based on name
	def delete_item(self,name):

		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		product = find_item(name)
		s.delete(product)
		s.commit()
		s.close()
		conn.close()

	def drop_table(self):
		User.__table__.drop(self.engine)


	def print_table(self):
		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		query = s.query(User)
		for q in query:
			print(q.name, q.orders, q.image)
		s.close()
		conn.close()



	def return_table(self):

		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		query = s.query(User)
		output = {}
		for q in query:
			if str(q.item_type) not in output:
				output[str(q.item_type)] = [[str(q.item_type), str(q.name), str(q.orders), str(q.change), str(q.image)]]
			else:
				output[str(q.item_type)].append([str(q.item_type), str(q.name), str(q.orders), str(q.change), str(q.image)])
		s.close()
		conn.close()
		return output


	def temp(self):
		conn = self.engine.connect()
		Session = sessionmaker(bind=conn)
		s = Session()
		query = s.query(User)
		for q in query:
			if q.change < 0:
				q.change = 0

		s.commit()
		s.close()
		conn.close()



