from services.db.app.database import Base
from domain.entities.short_annotated import short_annotate

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, DateTime, text

from datetime import datetime


class BaseAbsModel(Base):
    id: Mapped[short_annotate.uuidpk] # type: ignore
    updated_at: Mapped[datetime] = Column(
        DateTime,
        nullable=True,
        default=None,
        onupdate=datetime.now,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        nullable=False,
    )

    __abstract__ = True

