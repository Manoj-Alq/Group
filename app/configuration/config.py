from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "postgresql://postgres:12345@localhost/group"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

router = FastAPI(debug=True, title="Group👨🏾‍🤝‍👨🏻👨🏾‍🤝‍👨🏻")

def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()