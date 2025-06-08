from fastapi import APIRouter, Depends, HTTPException, Request
from app.services import db_utils
from fastapi.responses import JSONResponse
from app.middlewares.logger import logger
router = APIRouter()

@router.get("/get-session/{email}")
async def get_db_sessions(email: str):
    """
    Retrieve all active sessions.
    """
    try:
        sessions = await db_utils.get_saved_session(email)
        if sessions:
            return JSONResponse(status_code=200, content={"message": "fetch user Session data", "data": sessions})
        else:
            logger.error(sessions)
            return HTTPException(status_code=404, detail="no session found for this user")
        
    except Exception as e:
        logger.error(f"Error fetching sessions for {email}: {str(e)}")
        return HTTPException(status_code=500, detail=f"An error occurred while fetching sessions: {str(e)}")
    
    


@router.post("/save-session")
async def save_db_session(request: Request):
    """
    Save a session for a user.
    """
    try:
        body = await request.json()
        email = body.get("email")
        token = body.get("token")
        user_info = body.get("user_info")
        logger.info(f"Saving session for user: {body.get('email')}")
        if not email or not token or not user_info:
            logger.error("Missing required parameters: email, token, or user_info")
            return HTTPException(status_code=400, detail="Missing required parameters: email, token, or user_info")
        
        if not isinstance(token, dict) or not isinstance(user_info, dict):
            logger.error("Invalid data types for token or user_info")
            return HTTPException(status_code=400, detail="Invalid data types for token or user_info")
        # Save the session using the utility function
        logger.info(f"Saving session for user: {email} with token: {token} and user_info: {user_info}")
        
        await db_utils.save_session(email, token, user_info)
        logger.info(f"Session saved for user: {email}")
        return JSONResponse(status_code=200, content={"message": "Session saved successfully"})
    except Exception as e:
        logger.error(f"Error saving session for {email}: {str(e)}")
        return HTTPException(status_code=500, detail=f"An error occurred while saving the session: {str(e)}")
    
    
@router.post("/add-conversation-session")
async def add_conversation_session(request: Request):
    """
    Add a conversation session for a user.
    """
    try:
        body = await request.json()
        email = body.get("email")
        chat_context = body.get("chat_context")
        logger.info(f"Adding conversation session for user: {email}")
        
        if not email or not chat_context:
            logger.error("Missing required parameters: email or chat_context")
            return HTTPException(status_code=400, detail="Missing required parameters: email or chat_context")
        
        if not isinstance(chat_context, dict):
            logger.error("Invalid data type for chat_context")
            return HTTPException(status_code=400, detail="Invalid data type for chat_context")
        
        await db_utils.add_conversation_session(email, chat_context)
        logger.info(f"Conversation session added for user: {email}")
        return JSONResponse(status_code=200, content={"message": "Conversation session added successfully"})
    
    except Exception as e:
        logger.error(f"Error adding conversation session for {email}: {str(e)}")
        return HTTPException(status_code=500, detail=f"An error occurred while adding the conversation session: {str(e)}")