import threading
import time
import logging
from datetime import datetime, date
from src.models.chat_log import ChatLog

logger = logging.getLogger(__name__)


class LogCleanupScheduler:
    """
    Background scheduler that automatically deletes chat logs older than 7 days.
    Checks once a minute whether a cleanup has run today (UTC); runs at most
    once per day. This is robust to drift and worker restarts.
    """

    CHECK_INTERVAL = 60  # seconds

    def __init__(self, app):
        self.app = app
        self.running = False
        self.thread = None
        self._last_cleanup_date = None

    def start(self):
        """Start the background cleanup scheduler"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            logger.info("Log cleanup scheduler started")

    def stop(self):
        """Stop the background cleanup scheduler"""
        self.running = False

    def _run_scheduler(self):
        while self.running:
            try:
                today = datetime.utcnow().date()
                if self._last_cleanup_date != today:
                    self._run_cleanup()
                    self._last_cleanup_date = today
            except Exception:
                logger.exception("Scheduler error")
            time.sleep(self.CHECK_INTERVAL)

    def _run_cleanup(self):
        try:
            with self.app.app_context():
                deleted_count = ChatLog.delete_old_logs()
                logger.info("Automatic cleanup completed: %d old logs deleted", deleted_count)
        except Exception:
            logger.exception("Cleanup failed")
