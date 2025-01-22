from loguru import logger
import datetime

def handle_exception(task_id, error, logger, db_updater):
    logger.error(f"Task {task_id} failed with error: {error}")
    db_updater.update_playground(
        status="Failed",
        end_time=datetime.utcnow(),
        task_id=task_id,
        start_time=None,
        final_result={"error": str(error)}
    )
    return {"status": "failed", "error": str(error)}

def handle_failure(task_id, message):
    logger.error(f"Task {task_id} failed: {message}")
    return {"status": "failed", "message": message}

def publish_status_message(task_id, status, task_name):
    logger.info(f"Task {task_id} - {task_name} status: {status}")
