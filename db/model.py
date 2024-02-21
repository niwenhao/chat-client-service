from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create an engine
engine = create_engine('mysql://root:password@127.0.0.1/chat_db')
# Create a configured "Session" class
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(128))
    message = Column(String(100))

    def __repr__(self):
        return "<User(id='%s', name='%s', password='%s', message='%s')>" % (
                                self.id, self.name, self.password, self.message)


class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String(50))
    prompt = Column(String(512))

    def __repr__(self):
        return "<ChatSession(id='%s', user_id='%s', name='%s', prompt='%s')>" % (
                                self.id, self.user_id, self.name, self.prompt)
class TalkingHistory(Base):
    __tablename__ = 'talking_histories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    chat_session_id = Column(Integer)
    timestamp = Column(DateTime)
    role = Column(String(50))
    message = Column(String(512))

    def __repr__(self):
        return "<TalkingHistory(user_id='%s', chat_session_id='%s', timestame='%s', role='%s', message='%s')>" % (
                                self.user_id, self.chat_session_id, self.timestame, self.role, self.message)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
def create_tables():
    Base.metadata.create_all(engine)