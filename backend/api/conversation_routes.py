from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from config.database import get_db
from services.conversation_service import (
    ConversationService,
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages,
    MessageCreate,
    MessageResponse
)
from models.conversation import MessageRole

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

# Mock user authentication - in production, get from JWT token
def get_current_user_id() -> str:
    """Mock authentication - returns a fixed user ID for demo"""
    return "550e8400-e29b-41d4-a716-446655440000"

@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Get all conversations for the logged-in user"""
    service = ConversationService(db)
    conversations = await service.get_conversations_for_user(user_id)
    return conversations

@router.get("/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific conversation with all its messages"""
    service = ConversationService(db)
    conversation = await service.get_conversation_with_messages(conversation_id, user_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Create a new conversation"""
    # Ensure the conversation is created for the current user
    conversation_data.user_id = user_id
    
    service = ConversationService(db)
    conversation = await service.create_conversation(conversation_data)
    return conversation

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def add_message(
    conversation_id: str,
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Add a new message to a conversation"""
    # Verify the conversation belongs to the user
    service = ConversationService(db)
    conversation = await service.get_conversation_with_messages(conversation_id, user_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Ensure message is added to the correct conversation
    message_data.conversation_id = conversation_id
    
    message = await service.create_message(message_data)
    return message

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Delete a conversation and all its messages"""
    service = ConversationService(db)
    success = await service.delete_conversation(conversation_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return {"message": "Conversation deleted successfully"}

@router.post("/start", response_model=ConversationWithMessages)
async def start_new_conversation(
    first_message: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Start a new conversation with the first message"""
    service = ConversationService(db)
    
    # Generate title from first message
    title = await service.generate_title_from_first_message(first_message)
    
    # Create conversation
    conversation_data = ConversationCreate(user_id=user_id, title=title)
    conversation = await service.create_conversation(conversation_data)
    
    # Add the first message
    message_data = MessageCreate(
        conversation_id=str(conversation.id),
        role=MessageRole.USER,
        content=first_message
    )
    message = await service.create_message(message_data)
    
    # Return conversation with the first message
    return ConversationWithMessages(
        id=str(conversation.id),
        user_id=str(conversation.user_id),
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[MessageResponse.from_orm(message)]
    )
