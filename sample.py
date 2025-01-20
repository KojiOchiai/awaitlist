import asyncio
from datetime import datetime, timedelta

from awaitlist import AwaitList


async def process_tasks(await_list: AwaitList):
    """Fetch tasks from the list and process them sequentially."""
    async for task_time, task_name in await_list.wait_for_next_task():
        print(f"[Processor] Executing: {task_name} at {datetime.now()}")


async def add_tasks(await_list: AwaitList):
    """Example of dynamically adding tasks."""
    # Add a task scheduled 5 second later
    task_time_5min = datetime.now() + timedelta(seconds=5)
    await await_list.add_task(task_time_5min, "Task 5 second later")
    print(f"[AddTasks] Added: Task 5 second later for {task_time_5min}")

    # Add a task scheduled 1 second later
    await asyncio.sleep(1)  # Wait 1 second
    task_time_1sec = datetime.now() + timedelta(seconds=1)
    await await_list.add_task(task_time_1sec, "Task 1 second later")
    print(f"[AddTasks] Added: Task 1 second later for {task_time_1sec}")


async def main():
    await_list = AwaitList()
    await asyncio.gather(process_tasks(await_list), add_tasks(await_list))


# Execute
if __name__ == "__main__":
    asyncio.run(main())
