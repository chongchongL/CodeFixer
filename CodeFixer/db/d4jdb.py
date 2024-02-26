from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CodeFixer.config.d4jcfg import D4jCfg


# 使用正确的连接字符串
cfg = D4jCfg.db_config
engine = create_engine(f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}", echo=True)

Session = sessionmaker(bind=engine)

@contextmanager
def getSession(autoCommitByExit=True):
    """使用上下文管理资源关闭"""
    session = Session()
    try:
        yield session
        # 退出时，是否自动提交
        if autoCommitByExit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()