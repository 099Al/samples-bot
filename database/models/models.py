import enum
from typing import List

from sqlalchemy import BigInteger, String, Float, Integer, Text, ForeignKey, Date, DateTime, Table, Column, \
    CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import os
import enum
from dotenv import load_dotenv

from database.models.base import Base

load_dotenv()

#engine = create_async_engine(url=os.getenv('SQL_DB'), echo=False)

#async_session = async_sessionmaker(engine)




class T_A(Base):
    __tablename__ = 't_a'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    attr_int: Mapped[int] = mapped_column(Integer, nullable=True)
    attr_date: Mapped[Date] = mapped_column(Date, nullable=True)

    #r_desc = relationship('T_A_DESC', back_populates='r_a', lazy="selectin")
    r_desc: Mapped['T_A_DESC'] = relationship('T_A_DESC', lazy="selectin")

    def __repr__(self):
        return (f'{self.__class__.__name__} ({self.id},{self.name})')

class T_A_DESC(Base):
    __tablename__ = 't_a_desc'

    id: Mapped[str] = mapped_column(ForeignKey('t_a.id'), primary_key=True)
    desc: Mapped[str] = mapped_column(String(100), nullable=True)


    def __repr__(self):
        return (f'{self.__class__.__name__} ({self.id},{self.desc} )')





