from http import client
import os

import httpx


class GithubClient:

    def __init__(self):

        self.token = os.environ["GITHUB_TOKEN"]

        self.base_url = "https://api.github.com"

        timeout = httpx.Timeout(
            connect=30.0,
            read=60.0,
            write=60.0,
            pool=60.0,
        )

        self.client = httpx.AsyncClient(timeout=timeout)

    def _headers(self):

        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    async def get(
        self,
        path: str,
    ):
        print(f"GitHub GET: {path}")
        response = await self.client.get(
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
        print(f"GitHub POST: {path}")
        response = await self.client.post(
            f"{self.base_url}{path}",
            headers=self._headers(),
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    async def patch(
        self,
        path: str,
        payload: dict,
    ):
        print(f"GitHub PATCH: {path}")

        response = await self.client.patch(
            f"{self.base_url}{path}",
            headers=self._headers(),
            json=payload,
        )

        response.raise_for_status()

        return response.json()
