from fastapi import FastAPI, Query
import requests
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()
url = "https://raelmorais.github.io/formula/formula1.json"

class Driver(BaseModel):
    name: str
    team: Optional[str] = None
    nationality: Optional[str] = None



@app.get('/api/')
def api_root():
    response = requests.get(url)
    data = response.json()
    return data
@app.get('/api/drivers/')
def get_drivers(
    name: Optional[str] = Query(None, description="Filter by driver name"),
    team: Optional[str] = Query(None, description="Filter by team name"),
    nationality: Optional[str] = Query(None, description="Filter by nationality"),
    limit: Optional[int] = Query(None, description="Limit number of results", ge=1)
) -> List[dict]:
    response = requests.get(url)
    data = response.json()
    
    filtered_data = data
    
    if name:
        filtered_data = [d for d in filtered_data if name.lower() in d.get('name', '').lower()]
    
    if team:
        filtered_data = [d for d in filtered_data if team.lower() in d.get('team', '').lower()]
    
    if nationality:
        filtered_data = [d for d in filtered_data if nationality.lower() in d.get('nationality', '').lower()]
    
    if limit:
        filtered_data = filtered_data[:limit]
    
    return filtered_data


@app.put('/api/drivers/{driver_id}')
def update_driver(driver_id: int, driver: Driver):
    response = requests.get(url)
    data = response.json()

    for i, d in enumerate(data):
        if driver_id in d.get('id', '').lower():
            updated_driver = driver.dict(exclude_unset=True)
            return {
                "message": "Driver updated successfully",
                "driver": updated_driver
            }
    
    return {"message": "Driver not found"}

@app.post('/api/drivers/create/', response_model=Driver)
def create_driver(driver: Driver):
    return driver
@app.get('/api/name/')
def rqp_name(name: str = None):
    response = requests.get(url)
    data = response.json()

    if name is not None:
        filtered_data = [character for character in data 
                        if name.lower() in character.get('name', '').lower()]
        return filtered_data
    return data