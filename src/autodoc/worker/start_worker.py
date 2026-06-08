# start_worker.py

import asyncio
from autodoc.config.config_loader import load_config
from autodoc.constants import CONFIG_DIR
from autodoc.config.environment import *
from autodoc.worker import pr_worker, review_worker

config = load_config(CONFIG_DIR / "registered_configs.yaml")


async def main():

    review_task = asyncio.create_task(review_worker.worker(config))

    pr_task = asyncio.create_task(pr_worker.worker(config))

    # every worker runs in the same process currently, to be moved to separate processes in the future
    await asyncio.gather(
        review_task,
        pr_task,
    )


if __name__ == "__main__":

    asyncio.run(main())
