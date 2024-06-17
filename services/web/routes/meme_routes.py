import uuid
from fastapi import (APIRouter, 
                     UploadFile,
                     status, 
                     File, 
                     Body, 
                     Depends,
                     Header)

from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from sqlalchemy.ext.asyncio import AsyncSession

# internal module imports
from domain.entities.meme.schemas.meme_schema import MemeDeleteMethodSchema, MemeInSchema, MemeOutSchema
from services.db.app.database import get_async_session
from external_interfaces.next_cloud_client import get_nextcloud_client
from common.utils import extract_path_from_nextcloud
from services.db.repository.meme_repo import MemeRepository

router = APIRouter(
    prefix="/memes",
    tags=["Meme"],
)

@router.post('',
             response_model=MemeOutSchema,
             status_code=status.HTTP_201_CREATED)
async def create_meme(
    meme: MemeInSchema = Body(...),
    photo: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session)):

    file_data = [photo, ]
    nextcloud_client = await get_nextcloud_client()

    responses = await nextcloud_client.upload_file(
       user_id='123', files=file_data, folder_name='meme_galery'
    )

    return await MemeRepository(session=session).\
        create_meme(data=meme, photo=str(responses[0].url if responses[0] else None))


@router.get('/{meme_id}',
            response_model=MemeOutSchema,
            status_code=status.HTTP_200_OK)
async def get_meme(
    meme_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)):


    return await MemeRepository(session=session).\
        get_meme(meme_id=meme_id)


@router.delete('/{meme_id}', 
               response_model=MemeDeleteMethodSchema)
async def delete_meme(
    meme_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)):


    return await MemeRepository(session=session).\
        delete_meme(meme_id=meme_id)


@router.patch('/{meme_id}', response_model=MemeOutSchema)
async def update_meme(
    meme_id: uuid.UUID,
    update_meme_data: MemeInSchema = Body(...),
    photo: UploadFile = File(None),
    session: AsyncSession = Depends(get_async_session)):


    return await MemeRepository(session=session).\
        update_meme(meme_id=meme_id, data=update_meme_data, photo=photo)


@router.get('',
            status_code=status.HTTP_200_OK, 
            response_model=Page[MemeOutSchema],)
async def get_memes(
    params: Params = Depends(),
    session: AsyncSession = Depends(get_async_session)):

    disable_installed_extensions_check()

    memes = await MemeRepository(session=session).\
        get_memes()
    
    return paginate(memes, params=params)