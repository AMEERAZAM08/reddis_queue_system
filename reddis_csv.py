import csv
from rq import Queue
from redis import Redis
from rq.job import Job
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access Redis configuration
redis_conn = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME')
)

# Connect to the queue
queue = Queue('simple_task_queue', connection=redis_conn)


def export_queue_to_csv(filename="task_queue.csv"):
    """Export all queued, started, and failed tasks to a CSV file."""
    # Open a CSV file for writing
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Job ID", "Task ID", "Status", "Enqueued At", "Started At", "Ended At", "Additional Data"])
        
        # Fetch all jobs in the queue
        jobs = queue.jobs  # Jobs currently in the queue
        for job in jobs:
            task_data = job.kwargs.get("task_data", {})
            writer.writerow([
                job.id,
                task_data.get("task_id", "N/A"),
                "Queued",
                job.enqueued_at,
                job.started_at,
                job.ended_at,
                task_data.get("additional_data", "N/A")
            ])
        
        # Include completed and failed jobs
        for status, registry in [("Finished", queue.finished_job_registry), ("Failed", queue.failed_job_registry)]:
            for job_id in registry.get_job_ids():
                job = Job.fetch(job_id, connection=redis_conn)
                task_data = job.kwargs.get("task_data", {})
                writer.writerow([
                    job.id,
                    task_data.get("task_id", "N/A"),
                    status,
                    job.enqueued_at,
                    job.started_at,
                    job.ended_at,
                    task_data.get("additional_data", "N/A")
                ])
    print(f"Task details exported to {filename}.")


if __name__ == "__main__":
    export_queue_to_csv()
