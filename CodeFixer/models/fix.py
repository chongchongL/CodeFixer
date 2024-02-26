from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from .base import Base  # 导入共享的 Base 实例
from datetime import datetime

class Fix(Base):
    __tablename__ = 'fix'
    
    id = Column(Integer, primary_key=True)
    bug = Column(String(50), unique=False, nullable=False, comment="bug的标识")
    epoch1 = Column(Integer, nullable=False, comment="解释的epoch")
    epoch2 = Column(Integer, nullable=False, comment="补丁的epoch")
    step = Column(Integer, nullable=True)
    answer = Column(Text)
    analysis = Column(Text, nullable=True)
    type = Column(Integer, nullable=True, comment="0: 未修复 1: 与人工补丁一致 2: 与人工补丁不一致")