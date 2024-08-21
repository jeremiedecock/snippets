import asyncio

async def async_task(name, time):
    print(f"{name} starts...")
    await asyncio.sleep(time)  # Simulates a blocking operation (non-blocking wait)
    print(f"{name} ends after {time} seconds.")

async def main():
    # Create multiple asynchronous tasks
    task1 = asyncio.create_task(async_task("Task 1", 2))
    task2 = asyncio.create_task(async_task("Task 2", 3))

    print("Tasks have been started.")
    
    # Wait for all tasks to complete
    await task1
    await task2

    print("All tasks are completed.")

# Start the event loop and execute the main function
asyncio.run(main())