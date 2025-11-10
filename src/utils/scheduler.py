import threading
import time
from datetime import datetime
from src.models.chat_log import ChatLog

class LogCleanupScheduler:
    """
    Background scheduler that automatically deletes chat logs older than 7 days.
    Runs cleanup once per day at midnight UTC.
    """
    
    def __init__(self, app):
        self.app = app
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the background cleanup scheduler"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            print("[SCHEDULER] Log cleanup scheduler started")
    
    def stop(self):
        """Stop the background cleanup scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
            print("[SCHEDULER] Log cleanup scheduler stopped")
    
    def _run_scheduler(self):
        """Background thread that runs the cleanup task"""
        while self.running:
            try:
                # Calculate seconds until next midnight UTC
                now = datetime.utcnow()
                next_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                
                # If we're past midnight today, schedule for tomorrow
                if now >= next_midnight:
                    from datetime import timedelta
                    next_midnight += timedelta(days=1)
                
                seconds_until_midnight = (next_midnight - now).total_seconds()
                
                print(f"[SCHEDULER] Next cleanup scheduled in {seconds_until_midnight/3600:.1f} hours")
                
                # Sleep until midnight (check every minute to allow for graceful shutdown)
                sleep_time = min(60, seconds_until_midnight)
                for _ in range(int(seconds_until_midnight / sleep_time)):
                    if not self.running:
                        break
                    time.sleep(sleep_time)
                
                # Run cleanup at midnight
                if self.running:
                    self._run_cleanup()
                
            except Exception as e:
                print(f"[SCHEDULER ERROR] {e}")
                # Sleep for an hour before retrying
                time.sleep(3600)
    
    def _run_cleanup(self):
        """Execute the log cleanup task"""
        try:
            with self.app.app_context():
                deleted_count = ChatLog.delete_old_logs()
                print(f"[SCHEDULER] Automatic cleanup completed: {deleted_count} old logs deleted")
        except Exception as e:
            print(f"[SCHEDULER ERROR] Cleanup failed: {e}")
