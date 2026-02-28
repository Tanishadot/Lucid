from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
import uuid
from datetime import datetime

from models.conversation import Conversation, Message, MessageRole
from pydantic import BaseModel

class ConversationCreate(BaseModel):
    user_id: str
    title: str

class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    conversation_id: str
    role: MessageRole
    content: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConversationWithMessages(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True

class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_conversations_for_user(self, user_id: str) -> List[ConversationResponse]:
        """Get all conversations for a user, sorted by updated_at DESC"""
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == uuid.UUID(user_id))
            .order_by(desc(Conversation.updated_at))
        )
        conversations = result.scalars().all()
        return [ConversationResponse.from_orm(conv) for conv in conversations]

    async def get_conversation_with_messages(self, conversation_id: str, user_id: str) -> Optional[ConversationWithMessages]:
        """Get a conversation with all its messages"""
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(
                and_(
                    Conversation.id == uuid.UUID(conversation_id),
                    Conversation.user_id == uuid.UUID(user_id)
                )
            )
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            # Sort messages by timestamp
            sorted_messages = sorted(conversation.messages, key=lambda m: m.timestamp)
            message_responses = [MessageResponse.from_orm(msg) for msg in sorted_messages]
            
            return ConversationWithMessages(
                id=str(conversation.id),
                user_id=str(conversation.user_id),
                title=conversation.title,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                messages=message_responses
            )
        return None

    async def create_conversation(self, conversation_data: ConversationCreate) -> ConversationResponse:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=uuid.UUID(conversation_data.user_id),
            title=conversation_data.title
        )
        
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        
        return ConversationResponse.from_orm(conversation)

    async def create_message(self, message_data: MessageCreate) -> MessageResponse:
        """Create a new message and update conversation timestamp"""
        message = Message(
            conversation_id=uuid.UUID(message_data.conversation_id),
            role=message_data.role,
            content=message_data.content
        )
        
        self.db.add(message)
        
        # Update conversation's updated_at timestamp
        conversation_result = await self.db.execute(
            select(Conversation).where(Conversation.id == uuid.UUID(message_data.conversation_id))
        )
        conversation = conversation_result.scalar_one()
        conversation.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(message)
        
        return MessageResponse.from_orm(message)

    async def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Delete a conversation and all its messages"""
        result = await self.db.execute(
            select(Conversation).where(
                and_(
                    Conversation.id == uuid.UUID(conversation_id),
                    Conversation.user_id == uuid.UUID(user_id)
                )
            )
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            await self.db.delete(conversation)
            await self.db.commit()
            return True
        return False

    async def generate_title_from_first_message(self, content: str) -> str:
        """Generate a title from the first user message"""
        # Simple implementation: take first 50 characters
        title = content.strip()[:50]
        if len(content) > 50:
            title += "..."
        return title or "New Conversation"
