import asyncio
from services import *


async def main():
    tasks = [
        await asyncio.create_task(kuban.main()),
        await asyncio.create_task(moi_biznes.main()),
        await asyncio.create_task(msp.main())
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
