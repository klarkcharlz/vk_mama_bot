# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Integer, \
    SmallInteger, String, Text, UniqueConstraint, text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()
metadata = Base.metadata


class ContentAboutchildren(Base):
    __tablename__ = 'content_aboutchildren'
    __table_args__ = (
        CheckConstraint('week >= 0'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('content_aboutchildren_id_seq'::regclass)"))
    week = Column(Integer, nullable=False)
    src = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    weigh = Column(Float(53), nullable=False)
    length = Column(Float(53), nullable=False)


class ContentContent(Base):
    __tablename__ = 'content_content'
    __table_args__ = (
        CheckConstraint('day >= 0'),
        CheckConstraint('week >= 0')
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('content_content_id_seq'::regclass)"))
    week = Column(Integer, nullable=False)
    src = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    parent_flag = Column(String(16), nullable=False)
    day = Column(Integer, nullable=False)


class UsersUser(Base):
    __tablename__ = 'users_user'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    user_vk_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    country = Column(String(64))
    city = Column(String(64))
    sex = Column(String(8))
    birth_day = Column(Date)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    last_months = Column(Date)
    due_date = Column(Date)
    subscribe = Column(Boolean, default=False)
