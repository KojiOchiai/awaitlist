import asyncio
from datetime import datetime
from typing import AsyncGenerator, List, Tuple


class AwaitList:
    """
    Asynchronous task scheduler that waits for the execution time of tasks.
    Provides a mechanism to process tasks sequentially based on time.
    """

    def __init__(self):
        # Task list [(execution time, task name)]
        self.tasks: List[Tuple[datetime, str]] = []
        # For task notification
        self.condition = asyncio.Condition()

    async def add_task(self, task_time: datetime, task_name: str):
        """
        Add a new task.

        Args:
            task_time (datetime): Scheduled execution time.
            task_name (str): Task name.
        """
        async with self.condition:
            self.tasks.append((task_time, task_name))
            self.tasks.sort(key=lambda x: x[0])  # Sort tasks by time
            self.condition.notify_all()  # Notify waiting processes

    async def wait_for_next_task(self) -> AsyncGenerator[Tuple[datetime, str], None]:
        """
        Wait for the next task and yield it sequentially.

        Yields:
            Tuple[datetime, str]: Execution time and task name.
        """
        while True:
            async with self.condition:
                if self.tasks:
                    now = datetime.now()
                    next_task_time, next_task_name = self.tasks[0]

                    # If the next task is ready to execute
                    if next_task_time <= now:
                        self.tasks.pop(0)  # Remove from the list
                        yield next_task_time, next_task_name
                        continue

                    # Wait until the next task time
                    sleep_time = (next_task_time - now).total_seconds()
                else:
                    # If there are no tasks, wait indefinitely
                    sleep_time = None

            try:
                if sleep_time is not None and sleep_time > 0:
                    await asyncio.wait_for(self.condition.wait(), timeout=sleep_time)
                else:
                    await self.condition.wait()
            except asyncio.TimeoutError:
                pass  # Re-evaluate when sleep ends or new tasks are added
