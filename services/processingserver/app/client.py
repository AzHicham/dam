import uuid

import requests

from app.schemas import Format


class ImageServerClient:
    def __init__(self, server_url: str):
        self.session = requests.Session()
        self.server_url = server_url

    def download(self, id: uuid.UUID, format: Format = Format.JPEG, quality: int = 80) -> bytes:
        response = self.session.get(
            f"{self.server_url}/v0/imgsrv/{id}",
            params={"f": format.value, "q": quality}
        )
        response.raise_for_status()
        return response.json()
