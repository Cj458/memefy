import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Float, ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.base_model import BaseAbsModel


class Meme(BaseAbsModel):
    __tablename__ = 'memes'
    
    text: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(String)
