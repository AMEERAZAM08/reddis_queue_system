import os
from rq import Queue, Worker
from redis import Redis
from multiprocessing import Process
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime
import time

# Load environment variables from .env file
load_dotenv()

# Access Redis configuration
redis_conn = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT', 6379)),  # Default to 6379 if not specified
    db=int(os.getenv('REDIS_DB', 0)),         # Default to database 0 if not specified
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME')
)

# Define the Redis queue
queue = Queue('simple_task_queue', connection=redis_conn)

# Define the task
def simple_task(input_request):
    try:
        start_time = datetime.utcnow()
        task_id = input_request.get("task_id", "unknown_task_id")
        logger.info(f"Started task {task_id} with data: {input_request}")

        # Simulate a delay of 10 seconds
        time.sleep(10)

        # Simulate task processing
        result = {"status": "success", "data": input_request}
        logger.info(f"Task {task_id} completed successfully.")
        return result

    except Exception as error:
        logger.error(f"Error processing task: {error}")
        return {"status": "failed", "error": str(error)}

# Function to start a single worker
def start_worker():
    worker = Worker(['simple_task_queue'], connection=redis_conn)
    logger.info("Worker started. Listening for tasks...")
    worker.work()

# Function to start multiple workers
def start_multiple_workers(num_workers=4):
    processes = []
    for i in range(num_workers):
        process = Process(target=start_worker)
        process.start()
        processes.append(process)
        logger.info(f"Started worker {i + 1}")

    # Wait for all workers to complete (they won't complete unless manually stopped)
    for process in processes:
        process.join()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "workers":
        # Start multiple workers if the "workers" argument is provided
        num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        start_multiple_workers(num_workers)
    elif len(sys.argv) > 1 and sys.argv[1] == "enqueue":
        # Enqueue tasks for testing
        num_tasks = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        for i in range(num_tasks):
            input_request = {"task_id": f"task_{i + 1}", "data": f"Sample data for task {i + 1}"}
            queue.enqueue(simple_task, input_request)
            logger.info(f"Task {input_request['task_id']} enqueued.")
    else:
        print("Usage:")
        print("  python script.py workers 4      # Start 4 workers")
        print("  python script.py enqueue 10     # Enqueue 10 tasks")
