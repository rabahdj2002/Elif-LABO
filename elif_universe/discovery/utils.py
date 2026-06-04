import threading
from django.db import connection

def run_threaded_task(task_func, *args, **kwargs):
    """
    Helper to run a synchronous task function in a background thread.
    Used as an emergency fallback to prevent UI blocking when Celery is in Eager mode.
    """
    def wrapper():
        try:
            task_func(*args, **kwargs)
        except Exception as e:
            print(f"BACKGROUND THREAD ERROR: {str(e)}")
        finally:
            # Crucial for Django: connection is thread-local and needs to be closed
            # so it can be returned to the pool, preventing "Too many connections" errors.
            connection.close()

    t = threading.Thread(target=wrapper)
    t.daemon = True
    t.start()
