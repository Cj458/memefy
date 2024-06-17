import httpx
from fastapi import HTTPException
from common.enums import ErrorMessage, NextCloudConfig


class NextcloudClient:
    SERVICE_UNAVAILABLE_ERROR = ErrorMessage.SERVICE_UNAVAILABLE_ERROR.value

    def __init__(self, username, password, nextcloud_url):
        self.username = username
        self.password = password
        self.nextcloud_url = nextcloud_url
        self.base_url = (
            f'{self.nextcloud_url}/'
            f'{self.username}'
        )
        self.client = httpx.AsyncClient(auth=(self.username, self.password))

    async def _request(self, method, url, **kwargs):
        async with httpx.AsyncClient(
                auth=(self.username, self.password)
        ) as client:
            try:
                response = await client.request(method=method, url=url, **kwargs)
                return response
            except httpx.ConnectError as exc:
                error_message = self.SERVICE_UNAVAILABLE_ERROR.format(exc)
                raise HTTPException(status_code=503, detail=error_message)

    async def create_folder(self, user_id, folder_name):
        url_path_user = f'{self.base_url}/{user_id}'
        url_path_folder = f'{url_path_user}/{folder_name}'
        try:
            await self._request('MKCOL', url_path_user)
            await self._request('MKCOL', url_path_folder)
            return 201
        except Exception as ex:
            raise HTTPException(status_code=503, detail=f'Ошибка при создании файла! Error: {ex}')

    async def upload_file(self, user_id, files, folder_name):
        await self.create_folder(user_id, folder_name)

        final_files = []
        for file in files:
            if not file:
                final_files.append(None)
                continue

            read_file = await file.read()
            file_data = {
                'name': file.filename,
                'file_code': read_file,
                'content_type': file.content_type,
            }
            final_files.append(file_data)

        response = []
        for file_data in final_files:
            if not file_data:
                response.append(None)
                continue

            url = f"{self.base_url}/{user_id}/{folder_name}/{file_data.get('name')}"
            res = await self._request(
                method='PUT',
                url=url,
                data=file_data.get('file_code'),
            )
            response.append(res)

        return response if response else [None, None]

    async def download_file(self, url):
        response = await self._request('GET', url)
        return response

    async def delete_file(self, url):
        response = await self._request(method='DELETE', url=url)
        return response


async def get_nextcloud_client():
    username = NextCloudConfig.NEXT_CLOUD_USERNAME.value
    password = NextCloudConfig.NEXT_CLOUD_PASSWORD.value
    nextcloud_url = NextCloudConfig.NEXT_CLOUD_URL.value
    return NextcloudClient(username=username, password=password, nextcloud_url=nextcloud_url)
