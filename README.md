# Redis Queue Task Processing with Multiprocessing

This project demonstrates how to use Python's `rq` (Redis Queue) for task processing with support for multiprocessing. It includes a worker system to process tasks asynchronously and enqueues tasks using Redis.

---

## Features

- Queue system powered by `rq` and Redis.
- Multiprocessing support for parallel task processing.
- Simulated task processing with a delay.
- Command-line interface for starting workers and enqueuing tasks.
- Monitoring of tasks with `rq-dashboard`.

---

## Requirements

- Python 3.8 or later
- Redis server
- Required Python packages (see below)

---

## Installation

Clone the Repository:
   ```bash
   git clone https://github.com/AMEERAZAM08/reddis_queue_system.git
   cd reddis_queue_system
   ```
Install Dependencies: Install the required Python packages from requirements.txt:
bash
```
pip install -r requirements.txt
```
Set Up Redis:

Install and start a Redis server on your local machine or a remote server.
Default Redis port: 6379
Set Up Environment Variables: Create a .env file in the project root with the following content:

```
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_USERNAME=
REDIS_PASSWORD=
# Database Configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```
## Usage
Start the Redis Server
Ensure the Redis server is running. If Redis is installed locally:

1. Enqueue Tasks
Run the following command to enqueue tasks into the simple_task_queue:
```
python script.py enqueue <num_tasks>
Replace <num_tasks> with the number of tasks to enqueue. For example:
python script.py enqueue 10

```
2. Start Workers
```
Start multiple worker processes to process tasks concurrently:

python script.py workers <num_workers>
Replace <num_workers> with the number of worker processes. For example:

python script.py workers 4
```
3. Monitor Tasks
```

Use rq-dashboard to monitor task states (queued, started, finished, failed):


rq-dashboard

```
Open the dashboard in your browser at http://localhost:9181.

Project Structure
```
.
├── script.py                     # Main script for enqueuing tasks and starting workers
├── database/
│   ├── connect_db.py             # Database connection module
│   ├── update_playground_task_tracker.py  # Module for task database updates
├── utils/
│   ├── controlnet_util.py        # Utility functions for exception handling and messaging
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── .env                          # Environment 
```

# How It Works

## Task Definition

- Tasks are defined as functions (e.g., `simple_task`) that accept input and perform some processing.
- A simulated delay of 10 seconds is added to mimic long-running tasks.

## Queueing

- Tasks are enqueued into `simple_task_queue` using `rq.Queue.enqueue()`.

## Workers

- Workers listen to the `simple_task_queue` and process tasks asynchronously.
- Multiprocessing is used to start multiple worker processes, enabling parallel task execution.

## Monitoring

- `rq-dashboard` provides a web-based UI to monitor task states in real-time.

---

# Commands Summary

## 1. Enqueue Tasks

Enqueue a specified number of tasks into the queue:

```bash
python worker_multiprocessing.py enqueue <num_tasks>
```




# Contributing
Feel free to submit issues or pull requests to improve this project.
