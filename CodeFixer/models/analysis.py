from sqlalchemy import Column, Integer, String, Text
from .base import Base  # 导入共享的 Base 实例


class Analysis(Base):
    __tablename__ = 'analysis'
    
    id = Column(Integer, primary_key=True)
    bug = Column(String(50), unique=False, nullable=False)
    epoch = Column(Integer, nullable=False)
    step = Column(Integer, nullable=False)
    analysis = Column(Text, unique=False)


        
    


    