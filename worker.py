import os
from rq import Queue, SimpleWorker
from redis import Redis

from database.connect_db import db_params
from database.update_playground_task_tracker import PlaygroundUpdater
from utils.controlnet_util import handle_exception, handle_failure, publish_status_message
from loguru import logger

from dotenv import load_dotenv
import importlib
import datetime
import time
importlib.reload(datetime)

# Load environment variables from .env file
load_dotenv()

# Access Redis configuration
redis_conn = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),  # This should return a valid integer (e.g., 6379)
    db=int(os.getenv('REDIS_DB', 0)),  # Default to database 0 if not specified
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME')
)

port = int(os.getenv('REDIS_PORT', 6379))

# Define the task
def simple_task(input_request):
    task_id = None  # Initialize task_id to a default value
    db_updater = None  # Initialize db_updater to handle cases where it's not created

    try:
        start_time = datetime.utcnow()
        db_updater = PlaygroundUpdater(db_params=db_params)
        task_id = input_request.get("task_id")  # Extract task_id from input_request

        if not task_id:
            raise ValueError("Task ID is missing in the input_request")

        logger.info(f"Started task with kwargs: {input_request}")
        db_updater.update_start_time(start_time=start_time, task_id=task_id)

        # Simulate a delay of 10 seconds before processing
        time.sleep(10)

        # Simulate task processing
        result = {"status": "success", "data": input_request}
        db_updater.update_playground(
            status="Completed",
            end_time=datetime.utcnow(),
            task_id=task_id,
            start_time=start_time,
            final_result=result
        )
        publish_status_message(task_id, "Completed", "simpleTask")
        return result

    except Exception as error:
        # Handle exceptions gracefully
        if task_id is None:
            task_id = "unknown_task_id"  # Provide a fallback task ID
        if db_updater:
            return handle_exception(task_id, error, logger, db_updater)
        else:
            logger.error(f"Error occurred and db_updater is not initialized: {error}")
            return {"status": "failed", "error": str(error), "task_id": task_id}

# Setup worker
def setup_worker():
    queue = Queue('simple_task_queue', connection=redis_conn)
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.work()

if __name__ == "__main__":
    setup_worker()
