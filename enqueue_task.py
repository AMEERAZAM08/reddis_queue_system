import os
from rq import Queue
from redis import Redis
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access Redis configuration
redis_conn = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME')
)

# Initialize the queue
queue = Queue('simple_task_queue', connection=redis_conn)

def enqueue_task(task_id, additional_data=None):
    """Function to add a task to the queue."""
    task_data = {
        "task_id": task_id,
        "additional_data": additional_data or "No additional data"
    }

    # Enqueue the task
    job = queue.enqueue("worker.simple_task", task_data)
    print(f"Task {task_id} added to queue with job ID: {job.id}")


if __name__ == "__main__":
    # Add a sample task to the queue
    for i in range(1000):
        task_id = f"task_{i:03d}"
        additional_data = {"key": f"value_{i}"}
        enqueue_task(task_id, additional_data)
    # task_id = "task_001"
    # additional_data = {"key": "value"}
    # enqueue_task(task_id, additional_data)
