from sqlalchemy import Column, String, Integer, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.settings.config import config

class BaseMediaModel(config.DBBaseModel):
    __abstract__ = True  # Define que esta classe é abstrata e não será mapeada diretamente como uma tabela
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    original_id = Column(Integer, nullable=False, unique=True, index=True)
    original_language = Column(String, nullable=True)
    overview = Column(Text, nullable=True)
    popularity = Column(Float, nullable=True)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)
    genre_ids = Column(Text, nullable=True) 
    backdrop_path = Column(String, nullable=True)
    poster_path = Column(String, nullable=True)
    is_adult = Column(Boolean, default=False)