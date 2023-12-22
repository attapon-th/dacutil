from multiprocessing.pool import ThreadPool
from typing import Callable, Iterable, Mapping, Any


# initialize a worker in the thread pool
def __initialize_worker():
    # from threading import current_thread
    # thread = current_thread()

    # report a message
    # print(f"Initializing worker, thread={thread.name}")
    pass


def worker(
    processes: int,
    task: Callable,
    values: Iterable[Mapping[str, Any]] = (),
    initializer=__initialize_worker,
) -> None:
    """
    Executes a given task in parallel using a thread pool.

    Args:
        processes (int): The number of worker processes in the thread pool.
        task (Callable): The task to be executed by each worker process.
        values (Iterable[Mapping[str, Any]], optional): The values to be passed as arguments to the task function. task number == len(values) Defaults to () no task.
        initializer (Callable, optional): The initializer function to be called when a worker process is created. Defaults to __initialize_worker.

    Returns:
        None: This function does not return any value.
    """
    # create and configure the thread pool
    with ThreadPool(processes, initializer=initializer) as pool:
        for kwargs in values:
            _ = pool.apply_async(task, kwds=kwargs)

        pool.close()
        pool.join()
