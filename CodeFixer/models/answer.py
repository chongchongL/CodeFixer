from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from .base import Base  # 导入共享的 Base 实例
from datetime import datetime


class Answer(Base):
    __tablename__ = 'answer'
    
    id = Column(Integer, primary_key=True)
    bug = Column(String(50), unique=False, nullable=False, comment="bug的标识")
    epoch = Column(Integer, nullable=False)
    step = Column(Integer, nullable=True)
    answer = Column(Text)
    analysis_epoch = Column(Integer, nullable=True)
    time = Column(DateTime, default=func.now())
