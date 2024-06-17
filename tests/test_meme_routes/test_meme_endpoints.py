import uuid
from datetime import datetime
from unittest.mock import AsyncMock, patch
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from domain.entities.meme.schemas.meme_schema import MemeInSchema, MemeOutSchema

meme_id = uuid.uuid4()
meme_data = MemeInSchema(text="Test Meme", photo="http://example.com/photo.jpg")
meme_out = MemeOutSchema(
    id=meme_id,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow(),
    text="Test Meme",
    photo="http://example.com/photo.jpg"
)

@pytest.mark.asyncio
@patch("services.db.repository.meme_repo.MemeRepository.get_meme", new_callable=AsyncMock)
async def test_get_meme(mock_get_meme, client: TestClient):
    mock_get_meme.return_value = meme_out

    response = client.get(f"/memes/{meme_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(meme_out.id),
        "created_at": meme_out.created_at.isoformat(),
        "updated_at": meme_out.updated_at.isoformat() if meme_out.updated_at else None,
        "text": meme_out.text,
        "photo": meme_out.photo,
    }

@pytest.mark.asyncio
@patch("services.db.repository.meme_repo.MemeRepository.delete_meme", new_callable=AsyncMock)
async def test_delete_meme(mock_delete_meme, client: TestClient):
    mock_delete_meme.return_value = {"id": str(meme_id)}

    response = client.delete(f"/memes/{meme_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": str(meme_id)}


@pytest.mark.asyncio
@patch("services.db.repository.meme_repo.MemeRepository.get_memes", new_callable=AsyncMock)
async def test_get_memes(mock_get_memes, client: TestClient):
    mock_get_memes.return_value = [meme_out]

    response = client.get("/memes")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["items"] == [{
        "id": str(meme_out.id),
        "created_at": meme_out.created_at.isoformat(),
        "updated_at": meme_out.updated_at.isoformat() if meme_out.updated_at else None,
        "text": meme_out.text,
        "photo": meme_out.photo,
    }]
    assert response.json()["total"] == 1
    assert response.json()["page"] == 1
    assert response.json()["size"] == 50
