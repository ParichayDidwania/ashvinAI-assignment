from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import sessionmaker
import os
import time

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
table_name = 'classification_files'

DATABASE_URL = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(DATABASE_URL)
Base = declarative_base()
class Document(Base):
    __tablename__ = table_name
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    content = Column(String, nullable=False)

def bootstrap_database():
    connection_successful = False

    while not connection_successful:
        try:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            connection_successful = True
        except Exception as e:
            print("Retrying database connection")
            time.sleep(5)
    

def add_document(content, file_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    new_doc = Document(content=content, file_name=file_name)
    
    session.add(new_doc)
    session.commit()
    session.close()

def useCursorForExecution(fn, client):
    Session = sessionmaker(bind=engine)
    session = Session()

    cursor = session.connection().execution_options(stream_results=True).execute(text(f"SELECT * FROM {table_name}"))
    fn(cursor, client)

    session.commit()
    session.close()
