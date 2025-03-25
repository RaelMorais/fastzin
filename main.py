from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from models import Team, engine, Session, select
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
def get_session():
    with Session(engine) as session:
        yield session
origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",  
    "*",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

@app.post("/teams/", response_model=List[Team])
def create_teams(teams: List[Team], session: Session = Depends(get_session)):
    db_teams = [Team(**team.dict()) for team in teams] 
    session.add_all(db_teams)  
    session.commit()  
    for team in db_teams:
        session.refresh(team)  
    return db_teams 

@app.put('/team/update/{team_id}', response_model=Team)
async def item_update(team_id: int, team: Team, session: Session = Depends(get_session)):
    db_teams = session.get(Team, team_id)
    if not db_teams:
        raise HTTPException(status_code=404, detail='Team not found')
    team_data = team.dict(exclude_unset=True)  # Only update provided fields
    for key, value in team_data.items():
        setattr(db_teams, key, value)
    session.add(db_teams)
    session.commit()
    session.refresh(db_teams)
    
    return db_teams

@app.get("/search/", response_model=List[Team])
def get_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams

@app.get("/team/{team_id}", response_model=Team)
def get_team_by_id(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.get('/search/teams/', response_model=List[Team])
async def search_itens_queryP(
    team_id: Optional[int] = None,
    team_name: Optional[str] = None,
    pilot: Optional[str] = None,
    factory_name: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Team)
    if team_id is not None:
        query = query.where(Team.id == team_id)
    if team_name is not None:
        query = query.where(Team.team_name == team_name)
    if pilot is not None:
        query = query.where(Team.pilot == pilot)
    if factory_name is not None:
        query = query.where(Team.factory_name == factory_name)
    
    results = session.exec(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="Teams not found")
    return results
