import uuid
from typing import Annotated

from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column


class ShortAnnotated():
    _primary_key_pk = True

    intpk = Annotated[int, mapped_column(
        primary_key=_primary_key_pk
    )]
    uuidpk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=_primary_key_pk,
        default=uuid.uuid4
    )]


short_annotate = ShortAnnotated()
