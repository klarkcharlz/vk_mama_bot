from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import BD_STRING


engine = create_engine(BD_STRING)
Session = sessionmaker(bind=engine)
session = Session()

