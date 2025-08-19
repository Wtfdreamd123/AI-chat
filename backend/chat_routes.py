from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import uuid
import logging
from typing import List

from models import ChatRequest, ChatResponse, ChatMessage, ChatHistoryResponse, ChatSession
from ai_service import AIService
from database import get_database

logger = logging.getLogger(__name__)

chat_router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize AI service
ai_service = AIService()

async def get_or_create_session(session_id: str = None, db: AsyncIOMotorDatabase = Depends(get_database)) -> str:
    """Get existing session or create new one"""
    if session_id:
        # Check if session exists
        session = await db.chat_sessions.find_one({"id": session_id})
        if session:
            # Update last activity
            await db.chat_sessions.update_one(
                {"id": session_id},
                {"$set": {"updated_at": datetime.utcnow()}}
            )
            return session_id
    
    # Create new session
    new_session_id = str(uuid.uuid4())
    session = ChatSession(id=new_session_id)
    await db.chat_sessions.insert_one(session.dict())
    return new_session_id

@chat_router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Send a message to AI and get response"""
    try:
        # Get or create session
        session_id = await get_or_create_session(request.session_id, db)
        
        # Auto-detect category if not provided or is default
        if request.category == "text" or not request.category:
            detected_category = ai_service.detect_category(request.message)
            category = detected_category
        else:
            category = request.category
        
        # Save user message
        user_message = ChatMessage(
            session_id=session_id,
            type="user",
            content=request.message,
            category=category
        )
        await db.chat_messages.insert_one(user_message.dict())
        
        # Generate AI response
        logger.info(f"Generating AI response for category: {category}")
        ai_response_text = await ai_service.generate_response(
            message=request.message,
            category=category,
            session_id=session_id
        )
        
        # Save AI response
        ai_message = ChatMessage(
            session_id=session_id,
            type="ai",
            content=ai_response_text,
            category=category
        )
        await db.chat_messages.insert_one(ai_message.dict())
        
        # Return response
        return ChatResponse(
            id=ai_message.id,
            response=ai_response_text,
            category=category,
            timestamp=ai_message.timestamp,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@chat_router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    limit: int = 50,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get chat history for a session"""
    try:
        # Verify session exists
        session = await db.chat_sessions.find_one({"id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get messages
        cursor = db.chat_messages.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).limit(limit)
        
        messages = []
        async for message_doc in cursor:
            messages.append(ChatMessage(**message_doc))
        
        return ChatHistoryResponse(messages=messages)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@chat_router.get("/sessions")
async def get_sessions(
    limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get recent chat sessions"""
    try:
        cursor = db.chat_sessions.find().sort("updated_at", -1).limit(limit)
        sessions = []
        async for session_doc in cursor:
            sessions.append(ChatSession(**session_doc))
        
        return {"sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@chat_router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a chat session and all its messages"""
    try:
        # Delete messages
        await db.chat_messages.delete_many({"session_id": session_id})
        
        # Delete session
        result = await db.chat_sessions.delete_one({"id": session_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")