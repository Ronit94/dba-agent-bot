from fastapi import APIRouter, Depends, Request

router = APIRouter()

@router.post("/start")
async def start_conversation(request: Request):
    """
    Retrieve all active sessions.
    """
    body = request.json()
    
    
    
    