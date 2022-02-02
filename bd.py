from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymongo
import redis

from settings import BD_STRING


# PostgreSQL
engine = create_engine(BD_STRING)
Session = sessionmaker(bind=engine)
session = Session()

# Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# mongo db
client = pymongo.MongoClient('localhost', 27017)
mongo_db = client['NextContentDB']
next_collection = mongo_db['next']
