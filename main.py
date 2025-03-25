from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Team(BaseModel): #Base de dados
    id: int 
    name: str
    team_name: str 
    factory_name: str
    pilot: str 
    sponsor_master : str 
teams_db = []


@app.get("/search/", response_model=List[Team])#Listagem de todos os dados. 
def get_teams():
    return teams_db

@app.get("/team/{team_id}", response_model=Team) #Filtro por ID 
def get_team_by_id(team_id: int): 
    for team in teams_db:
        if team.id == team_id: 
            return team
    raise HTTPException(status_code=404, detail="Team not found")

@app.post("/teams/") #Post
def create_teams(teams: List[Team]):
    for team in teams:
        teams_db.append(team)
    return {"message": "Teams created successfully", "teams": teams}

@app.get('/search/teams/')
async def search_itens_queryP(team_id: Optional[int] = None, team_name: Optional[str] = None, pilot: Optional[str] = None, factory_name: Optional[str] = None):
    results = teams_db

    if team_id is not None:
        results = [team for team in results if team.id == team_id]

    if team_name is not None:
        results = [team for team in results if team.team_name == team_name]

    if pilot is not None:
        results = [team for team in results if team.pilot == pilot]

    if factory_name is not None:
        results = [team for team in results if team.factory_name == factory_name]

    if not results:
        raise HTTPException(status_code=404, detail="Teams not found")
    
    return results