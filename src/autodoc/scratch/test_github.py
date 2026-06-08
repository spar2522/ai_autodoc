import asyncio
from autodoc.config.environment import *

from autodoc.github.github_client import (
    GithubClient,
)


async def main():

    client = GithubClient()

    user = await client.get("/user")

    print(user["login"])


asyncio.run(main())
