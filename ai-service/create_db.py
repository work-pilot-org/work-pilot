import asyncio
from shared_infrastructure.database.session import engine
from shared_infrastructure.database.base import PublicBase
from shared_infrastructure.database.models.conversation import Conversation, Message

print("Creating database tables...")
PublicBase.metadata.create_all(bind=engine)
print("Database tables created successfully!")
