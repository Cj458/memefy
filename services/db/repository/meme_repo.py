import uuid
from typing import List, Optional


from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    delete,
    select,
    update,
)

from common.exceptions import CustomExceptionError
from common.utils import extract_path_from_nextcloud
from domain.entities.meme.models.meme_model import Meme
from domain.entities.meme.schemas.meme_schema import MemeInSchema
from external_interfaces.next_cloud_client import get_nextcloud_client


class MemeRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    
    async def create_meme(self, data: MemeInSchema, photo: UploadFile) -> Meme:
        data.photo = photo

        meme = data.model_dump()
        new_meme = Meme(**meme)
        self.session.add(new_meme)

        await self.session.commit()

        await self.session.refresh(new_meme)

        return new_meme
    

    async def get_meme(self, meme_id: uuid.UUID) -> Meme:
        stmt = select(Meme).where(Meme.id == meme_id)

        db_meme = await self.session.execute(stmt)
        meme = db_meme.scalars().first()

        if not db_meme:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CustomExceptionError.MEME_NOT_FOUND
            )

        return meme
    

    async def delete_meme(self, meme_id: uuid.UUID) -> Meme:
        
        db_meme = await self.session.get(Meme, meme_id)
        nextcloud_client = await get_nextcloud_client()
   
        if not db_meme:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CustomExceptionError.MEME_NOT_FOUND
            )

        stmt = delete(Meme).where(Meme.id == meme_id)
        await self.session.execute(stmt)
        await self.session.commit()

        await nextcloud_client.delete_file(url=db_meme.photo)

        return db_meme


    async def update_meme(self, meme_id: uuid.UUID, data: MemeInSchema, photo: Optional[UploadFile]) -> Meme:

        nextcloud_client = await get_nextcloud_client()

        db_meme = await self.session.execute(
            select(Meme).where(Meme.id == meme_id))
        
        meme = db_meme.scalars().first()

        if photo and meme.photo:
            await nextcloud_client.delete_file(url=meme.photo)

        if photo:

            file_data = [photo, ]
            responses = await nextcloud_client.upload_file(
                user_id='123', files=file_data, folder_name='meme_galery'
            )       

            data.photo = str(responses[0].url if responses[0] else meme.photo)
        else:
            data.photo = str(meme.photo)

        updata_data = data.model_dump(exclude_unset=True)

        stmt = update(Meme).where(Meme.id == meme_id).values(updata_data)
        await self.session.execute(stmt)
        await self.session.commit()
        await self.session.refresh(meme)

        return meme


    async def get_memes(self) -> List[Meme]:

        stmt = select(Meme)
        db_meme = await self.session.execute(stmt)
        memes = db_meme.scalars().all()

        return memes




