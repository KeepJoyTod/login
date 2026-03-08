from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional, Generator
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import job as schemas
import time
import asyncio
import json

router = APIRouter(
    tags=["jobs"],
)

# --- AI Generation ---

@router.post("/ai/generations", response_model=schemas.JobIdResponse)
async def create_generation_job(
    request: schemas.GenerateRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # In real implementation, enqueue a Celery task or similar
    job_id = "job_gen_001"
    # background_tasks.add_task(mock_generate_task, job_id)
    return schemas.JobIdResponse(jobId=job_id)

# --- Execution ---

@router.post("/runs", response_model=schemas.JobIdResponse)
async def create_run_job(
    request: schemas.RunRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job_id = "job_run_001"
    # background_tasks.add_task(mock_run_task, job_id)
    return schemas.JobIdResponse(jobId=job_id)

@router.get("/runs/{job_id}/summary", response_model=schemas.JobResultRun)
def get_run_summary(job_id: str, db: Session = Depends(get_db)):
    return schemas.JobResultRun(
        passed=5,
        failed=1,
        failures=[
            {"testcaseId": "tc_1001", "reason": "statusCode expected 200 got 401"}
        ]
    )

# --- Common Job Operations ---

@router.get("/jobs/{job_id}", response_model=schemas.Job)
def get_job(job_id: str, db: Session = Depends(get_db)):
    return schemas.Job(
        id=job_id,
        projectId="p_1",
        type="generate" if "gen" in job_id else "run",
        status="running",
        progress=85,
        steps=[
            schemas.JobStep(name="Prepare Context", status="success"),
            schemas.JobStep(name="Call Model", status="running")
        ]
    )

@router.get("/jobs/{job_id}/results", response_model=schemas.JobResultGenerate)
def get_job_results(job_id: str, db: Session = Depends(get_db)):
    return schemas.JobResultGenerate(
        generatedTestcases=[
            {"testcaseId": "tc_1001", "name": "Create Project - Missing Name", "type": "negative", "priority": "high"}
        ]
    )

@router.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str, db: Session = Depends(get_db)):
    return {"message": "Job cancellation requested"}

# --- Logs ---

@router.get("/jobs/{job_id}/logs", response_model=schemas.RuntimeLogList)
def get_job_logs(
    job_id: str, 
    fromSeq: int = 0, 
    limit: int = 200, 
    db: Session = Depends(get_db)
):
    return schemas.RuntimeLogList(
        nextSeq=201,
        items=[
            schemas.RuntimeLog(seq=1, level="info", message="Start generation...", ts=time.time())
        ]
    )

@router.get("/jobs/{job_id}/logs/stream")
async def stream_job_logs(job_id: str, fromSeq: int = 0):
    async def event_generator():
        # Mock streaming logs
        for i in range(5):
            log_data = {
                "seq": fromSeq + i, 
                "level": "info", 
                "message": f"Step {i} processing...", 
                "ts": time.time()
            }
            yield f"event: log\ndata: {json.dumps(log_data)}\n\n"
            await asyncio.sleep(1)
        
        yield f"event: end\ndata: {json.dumps({'status': 'success'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
