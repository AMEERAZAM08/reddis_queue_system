from database.connect_db import get_db_connection

class PlaygroundUpdater:
    def __init__(self, db_params):
        self.db_params = db_params

    def update_start_time(self, start_time, task_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE playground_task_tracker
                    SET start_time = %s, status = 'In Progress'
                    WHERE task_id = %s
                """, (start_time, task_id))
                conn.commit()

    def update_playground(self, status, end_time, task_id, start_time, final_result):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE playground_task_tracker
                    SET status = %s, end_time = %s, start_time = %s, final_result = %s
                    WHERE task_id = %s
                """, (status, end_time, start_time, str(final_result), task_id))
                conn.commit()
