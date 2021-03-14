import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import sessionmaker

from .app import WhatsApp as app

Base = declarative_base()


# SQLAlchemy ORM definition for the What app table
class Whatsapp(Base):
	__tablename__ = 'whats_app_messages'
	# Columns
	id = Column(Integer, primary_key=True)
	phone_id = Column(String)
	message_id = Column(String)
	first_message = Column(Boolean)
	latitude = Column(Float)
	longitude = Column(Float)
	title = Column(String)
	owner = Column(String)
	event =  Column(String)
	date_built = Column(String)

class Messagefiles(Base):
	__tablename__ = 'whats_app_files'
	# Columns
	id = Column(Integer, primary_key=True)
	message_id = Column(String)
	path = Column(String)
	

def add_new_image(message_id, path):
	new_message = Messagefiles(
		message_id = message_id,
		path = path
	)
	# Get connection/session to database
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()

	# Add the new messages record to the session
	session.add(new_message)

	# Commit the session and close the connection
	session.commit()
	session.close()

def get_images(m_id):
	# Get connection/session to database
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()
	# Query for all images records
	images = session.query(Messagefiles).filter_by(message_id = m_id).all()
	session.close()
	return images

def add_new_message(phone_id, first, m_id, lat, longit, title, owner, event, date_built):
	# Create new Whatsapp message record
	new_message = Whatsapp(
		phone_id= phone_id,
		message_id= m_id,
		first_message = first,
		latitude= lat,
		longitude=longit,
		title=title,
		owner=owner,
		event=event,
		date_built=date_built
	)
	# Get connection/session to database
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()

	# Add the new message record to the session
	session.add(new_message)

	# Commit the session and close the connection
	session.commit()
	session.close()

def current_message_exist(p_id, title, event, owner):
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()
	incomplete = session.query(Whatsapp).filter_by(phone_id= p_id, first_message = True).first()
	# Check if it is incomplete or new messages 
	if incomplete == None:
		session.close()
		return incomplete, title, event, owner
	else:
		session.close()
		return incomplete.message_id, incomplete.title, incomplete.event, incomplete.owner
	session.close()
	return None, "", "", ""

def update_message(phone_id, m_id, first, lat, longit, title, owner, event):
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()
	# Check the parameters to update in the database
	t_query = {}
	if (lat or longit) and lat != 1:
		t_query["latitude"] = lat 
		t_query["longitude"] = longit
	if not first:
		t_query["first_message"] = first
	if event:
		t_query["event"] =  event
	if title:
		t_query["title"] = title
	if owner:
		t_query["owner"] = owner
	records = session.query(Whatsapp).filter_by(phone_id = phone_id, message_id = m_id, first_message = True).update(t_query , synchronize_session = False)
	session.commit()
	session.close()

def get_messages(stype, term):
	# Get connection/session to database
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()
	#get type and value
	messages = None
	if stype == 'name':
		messages = session.query(Whatsapp).filter(Whatsapp.owner.like(term)).all()
	else:
		messages = session.query(Whatsapp).filter(Whatsapp.title.like(term)).all()

	session.close()
	return messages

def get_all_messages():
	# Get connection/session to database
	Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
	session = Session()
	# Query for message records
	messages = session.query(Whatsapp).filter_by(first_message = False).all()
	session.close()
	return messages

def init_primary_db(engine, first_time):
	# Create all the tables
	Base.metadata.create_all(engine)
	# Add data
	if first_time:
		# Make session
		Session = sessionmaker(bind=engine)
		session = Session()
		# Initialize database with one message
		message1 = Whatsapp(
			phone_id="0000000000",
			message_id = '1',
			first_message = False,
			latitude=40.406624,
			longitude=-111.529133,
			title="Random Message",
			owner="Daniel De La O",
			event='Worst Event Ever',
			date_built="April 12, 1993"
		)
		message2 = Messagefiles(
			message_id = '1',
			path = '/home'
		)
		# Add the dams to the session, commit, and close
		session.add(message1)
		session.add(message2)
		session.commit()
		session.close()