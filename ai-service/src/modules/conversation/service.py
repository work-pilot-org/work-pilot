from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session

from src.modules.conversation.repository import ConversationRepository
from src.modules.conversation.schemas import ConversationResponse, MessageResponse

class ConversationService:
    def __init__(self, db: Session):
        self.repo = ConversationRepository(db)

    def _map_to_response(self, conv) -> ConversationResponse:
        return ConversationResponse(
            id=conv.id,
            title=conv.title,
            date=conv.created_at.strftime("%Y-%m-%d"),
            messages=[
                MessageResponse(
                    id=m.id,
                    role=m.role,
                    content=m.content,
                    created_at=m.created_at
                )
                for m in sorted(conv.messages, key=lambda x: x.created_at)
            ]
        )

    def get_conversations(self, tenant_id: str, auth_user_id: UUID) -> List[ConversationResponse]:
        convs = self.repo.get_user_conversations(tenant_id, auth_user_id)
        return [self._map_to_response(c) for c in convs]

    def get_conversation(self, conversation_id: UUID, tenant_id: str, auth_user_id: UUID) -> Optional[ConversationResponse]:
        conv = self.repo.get_conversation_by_id(conversation_id, tenant_id, auth_user_id)
        if not conv:
            return None
        return self._map_to_response(conv)

    def get_or_create_conversation(self, tenant_id: str, auth_user_id: UUID, message_content: str, conversation_id: Optional[UUID] = None):
        if conversation_id:
            conv = self.repo.get_conversation_by_id(conversation_id, tenant_id, auth_user_id)
            if conv:
                return conv
        
        # Determine title from first message
        title = message_content[:30] + ("..." if len(message_content) > 30 else "")
        return self.repo.create_conversation(tenant_id, auth_user_id, title)

    def add_message(self, conversation_id: UUID, role: str, content: str):
        return self.repo.add_message(conversation_id, role, content)

    def delete_conversation(self, conversation_id: UUID, tenant_id: str, auth_user_id: UUID) -> bool:
        return self.repo.delete_conversation(conversation_id, tenant_id, auth_user_id)
