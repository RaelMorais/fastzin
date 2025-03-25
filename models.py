from sqlmodel import SQLModel, create_engine, Session, Field, select
from typing import List, Optional

class Team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    team_name: str
    factory_name: str
    pilot: str
    sponsor_master: str

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session