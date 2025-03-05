from uuid import UUID
from datetime import datetime

class Comment:
    def __init__(self, id: UUID, user_id: UUID, media_id: int, media_type: str, content: str, created_at: datetime):
        self.id = id
        self.user_id = user_id
        self.media_id = media_id
        self.media_type = media_type
        self.content = content
        self.created_at = created_at
