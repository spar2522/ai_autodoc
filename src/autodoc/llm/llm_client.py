import httpx


async def generate(
    model: str,
    prompt: str,
) -> str:

    timeout = httpx.Timeout(
        connect=10.0,
        read=600.0,
        write=30.0,
        pool=30.0,
    )

    async with httpx.AsyncClient(timeout=timeout) as client:

        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )

        response.raise_for_status()

        return response.json()["response"]
