from httpx import AsyncClient, Timeout
import os


class GithubClient:

    def __init__(self):
        self.token = os.environ["GITHUB_TOKEN"]
        self.base_url = "https://api.github.com"

        timeout = Timeout(
            connect=30.0,
            read=60.0,
            write=60.0,
            pool=60.0,
        )

        self.client = AsyncClient(timeout=timeout)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    async def request(
        self,
        method: str,
        path: str,
        payload: dict = None,
    ):
        print(f"GitHub {method}: {path}")
        response = await self.client.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=self._headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def get(
        self,
        path: str,
    ):
        return await self.request("GET", path)

    async def post(
        self,
        path: str,
        payload: dict,
    ):
        return await self.request("POST", path, payload)

    async def patch(
        self,
        path: str,
        payload: dict,
    ):
        return await self.request("PATCH", path, payload)