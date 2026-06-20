import os

import httpx


class GithubClient:
    """A client for interacting with the GitHub API."""

    def __init__(self):
        """Initialize the GitHub client with the provided token and configuration."""
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is not set")
        self.base_url = "https://api.github.com"

        timeout = httpx.Timeout(
            connect=30.0,
            read=60.0,
            write=60.0,
            pool=60.0,
        )

        self.client = httpx.AsyncClient(timeout=timeout)

    def _headers(self):
        """Generate the HTTP headers required for GitHub API requests."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    async def get(
        self,
        path: str,
    ):
        """Send a GET request to the GitHub API.

        Args:
            path (str): The API endpoint path.

        Returns:
            dict: The JSON response from the GitHub API.
        """
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
        """Send a POST request to the GitHub API.

        Args:
            path (str): The API endpoint path.
            payload (dict): The data to send in the request body.

        Returns:
            dict: The JSON response from the GitHub API.
        """
        print(f"GitHub POST: {path}")
        response = await self.client.post(
            f"{self.base_url}{path}",
            headers=self._headers(),
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    async def close(self):
        """Close the HTTP client to release resources."""
        await self.client.aclose()