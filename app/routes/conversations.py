from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/chat/start")
async def start_conversation(request: Request):
    """
    Retrieve all active sessions.
    """
    body = await request.json()
    session_id = body.get("session_id")
    if not session_id:
        return {"error": "session_id is required"}
    user_input = body.get("input")
    if not user_input:
        return {"error": "input is required"}
    agent = request.app.state.agent
    print(f"Received input: {user_input} for session: {session_id}")
    # result = agent.invoke({"input": user_input, "session_id": session_id})
    result = agent.invoke({"input": user_input, "session_id": session_id})
    
    return JSONResponse(content={"response": result["response"]})