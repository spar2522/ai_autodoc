import os

import httpx


class GithubClient:

    def __init__(self):

        self.token = os.environ["GITHUB_TOKEN"]

        self.base_url = "https://api.github.com"

    def _headers(self):

        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    async def get(
        self,
        path: str,
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.base_url}{path}",
                headers=self._headers(),
            )

            response.raise_for_status()

            return response.json()

    async def post(
        self,
        path: str,
        payload: dict,
    ):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{self.base_url}{path}",
                headers=self._headers(),
                json=payload,
            )

            response.raise_for_status()

            return response.json()
