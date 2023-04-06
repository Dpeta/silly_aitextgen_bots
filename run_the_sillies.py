#!/usr/bin/env python3
import os
import asyncio

from jasprose_bot import jasprose
from harry_bot import harry
from rust_bot import rust
from awexis_bot import awexis
from tye_bot import tye
from gabriel_bot import gabriel


async def main():
    harry_task = asyncio.create_task(harry.start(os.environ["HARRY_TOKEN"]))
    aweggy_task = asyncio.create_task(awexis.start(os.environ["AWEGGY_TOKEN"]))
    tye_task = asyncio.create_task(tye.start(os.environ["TYE_TOKEN"]))
    rust_task = asyncio.create_task(rust.start(os.environ["RUST_TOKEN"]))
    jasprose_task = asyncio.create_task(jasprose.start(os.environ["JASPROSE_TOKEN"]))
    gabriel_task = asyncio.create_task(gabriel.start(os.environ["GABRIEL_TOKEN"]))
    await aweggy_task
    await tye_task
    await rust_task
    await harry_task
    await jasprose_task
    await gabriel_task


if __name__ == "__main__":
    asyncio.run(main())
    print("Exiting. . .")
