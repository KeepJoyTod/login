from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import projects, interfaces, testcases, jobs
from .database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Test Platform API",
    description="Backend API for AI-powered Test Case Generation Platform",
    version="1.0.0",
)

# CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(projects.router)
app.include_router(interfaces.router)
app.include_router(interfaces.project_interfaces_router)
app.include_router(testcases.testcases_router)
app.include_router(testcases.project_testcases_router)
app.include_router(jobs.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Test Platform API"}
