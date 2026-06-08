from autodoc.llm.prompt_builder import (
    build_prompt,
)

from autodoc.llm.llm_client import (
    generate,
)


async def generate_improvement(
    task,
    model: str,
) -> str:

    prompt = build_prompt(task)

    return await generate(
        model=model,
        prompt=prompt,
    )
