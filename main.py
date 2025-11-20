from fastapi import FastAPI
from routers.users import router as router_users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   
                   )

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_users)
