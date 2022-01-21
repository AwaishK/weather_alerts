from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.config_parser import configuration_parser

config = configuration_parser()
database_config = config["DATABASE"]
SQLALCHEMY_DATABASE_URL = f"postgresql://{database_config['USER']}:{database_config['PASSWORD']}@localhost/{database_config['NAME']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
