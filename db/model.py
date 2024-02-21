from sqlalchemy import create_engine, Column, Integer, String
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
    password = Column(String(12))
    message = Column(String(100))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
def create_tables():
    Base.metadata.create_all(engine)
    Base.metadata.update(engine)