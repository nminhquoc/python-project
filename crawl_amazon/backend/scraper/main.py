import asyncio


async def my_coroutine():
    print("Start")
    await asyncio.sleep(2)
    print("End")


def main():
    asyncio.run(my_coroutine())


if __name__ == "__main__":
    main()
