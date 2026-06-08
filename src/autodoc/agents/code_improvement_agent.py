# This is a dummy agent. The actual improvement agent can be built later.
# Usually agents can be used for more open ended tasks like finding technical debts.
# so autodoc is a hybrid, where deterministic flows are handled by github hooks to
# redis event queue to asynwworker dequeue to local LLM to generating the PR
# generate_improvement is a simple wrapper around LLM calls, but in future it can be extended
# to include more complex logic and prompting and probably become an agent to find related code,
# generate tests etc.

from autodoc.llm.improvement_generator import (
    generate_improvement,
)


class CodeImprovementAgent:

    async def run(
        self,
        task,
        model,
    ):

        return await generate_improvement(
            task,
            model,
        )
