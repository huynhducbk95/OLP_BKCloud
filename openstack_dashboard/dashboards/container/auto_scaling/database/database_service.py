

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float
from sqlalchemy.orm import sessionmaker, scoped_session
import os.path

Base = declarative_base()
CURRENT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))


class Rule(Base):
    __tablename__ = 'rule'

    id = Column(Integer, primary_key=True)
    metric = Column(String(50))
    upper_threshold = Column(Float)
    lower_threshold = Column(Float)
    node_up = Column(Integer)
    node_down = Column(Integer)

    def __repr__(self):
        return self.id


engine = create_engine(
    'sqlite:///' + CURRENT_FOLDER_PATH + 'rule.sqlite', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.metadata.create_all(engine)


def get_rule_list():
    rule_list = db_session.query(Rule).all()
    return rule_list
