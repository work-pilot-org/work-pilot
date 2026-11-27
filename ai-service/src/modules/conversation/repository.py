from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from shared_infrastructure.database.models.conversation import Conversation, Message

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, tenant_id: str, auth_user_id: UUID, title: str) -> Conversation:
        conv = Conversation(tenant_id=tenant_id, auth_user_id=auth_user_id, title=title)
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def get_user_conversations(self, tenant_id: str, auth_user_id: UUID) -> List[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(Conversation.tenant_id == tenant_id, Conversation.auth_user_id == auth_user_id)
            .order_by(desc(Conversation.updated_at))
            .all()
        )

    def get_conversation_by_id(self, conversation_id: UUID, tenant_id: str, auth_user_id: UUID) -> Optional[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.tenant_id == tenant_id,
                Conversation.auth_user_id == auth_user_id,
            )
            .first()
        )

    def delete_conversation(self, conversation_id: UUID, tenant_id: str, auth_user_id: UUID) -> bool:
        conv = self.get_conversation_by_id(conversation_id, tenant_id, auth_user_id)
        if conv:
            self.db.delete(conv)
            self.db.commit()
            return True
        return False

    def add_message(self, conversation_id: UUID, role: str, content: str) -> Message:
        msg = Message(conversation_id=conversation_id, role=role, content=content)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg
