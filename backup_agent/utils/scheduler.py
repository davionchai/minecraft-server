import time
from datetime import datetime, timezone
from croniter import croniter
from typing import Any, Callable


def run_cron_job(cron_expr: str, task: Callable, arguments: Any):
    """Run a task at scheduled intervals using cron expressions.

    Args:
        cron_expr (str): The cron expression defining the schedule.
        task (Callable): The function to be executed.
        arguments (Any): The arguments to be passed to the task function.
    """
    base_time: datetime = datetime.now(timezone.utc)
    cron: croniter = croniter(cron_expr, base_time)
    next_run = cron.get_next(datetime)
    while True:
        now: datetime = datetime.now(timezone.utc)
        if now >= next_run:
            task(arguments)
            next_run = cron.get_next(datetime)
        time.sleep(60)
