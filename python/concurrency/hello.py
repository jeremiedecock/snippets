import asyncio

async def say_hello():
    await asyncio.sleep(3)  # Simulates a long task (waiting for 1 second)
    print("Hello!")

async def say_goodbye():
    await asyncio.sleep(1)  # Simulates a long task (waiting for 1 second)
    print("Goodbye!")

async def main():
    print("Start")
    # await say_hello()
    # await say_goodbye()
    await asyncio.gather(say_hello(), say_goodbye())
    print("End")

# To run the main asynchronous function
asyncio.run(main())