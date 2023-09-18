from database import Base
from sqlalchemy import Column,Integer,String,BOOLEAN,TIMESTAMP,text

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(BOOLEAN, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

class User(Base):
    __tablename__="users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
