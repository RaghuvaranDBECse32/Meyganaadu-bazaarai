from fastapi import FastAPI
from demand_model import demand_forecast

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Meyganaadu BazaarAI API Running"}

@app.get("/forecast")
def forecast():

    data = demand_forecast()

    return {"forecast":data}
