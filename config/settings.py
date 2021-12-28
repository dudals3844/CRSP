import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
DB_CONNECT = os.environ.get('DB_CONNECT')
DB_PREPROCESSING_CONNECT = os.environ.get('DB_PREPROCESSING_CONNECT')
ENGINE = create_engine(DB_CONNECT, echo=False)
ENGINE_PREPROCESSING = create_engine(DB_PREPROCESSING_CONNECT, echo=False)
META = MetaData()
BASE = declarative_base()

