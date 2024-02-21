# include all the fastapi routes here
from fastapi import FastAPI
from api.logon import router as logon_router

app = FastAPI()
app.include_router(logon_router)