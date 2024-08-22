import asyncio

async def C():
    print("Exécution de C")

async def B():
    await C()

async def A():
    await B()

# Start the event loop and execute the main function
asyncio.run(A())