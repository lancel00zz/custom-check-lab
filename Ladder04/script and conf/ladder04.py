from datadog_checks.base import AgentCheck
import platform
import os
import datetime
import json
import time
import socket

class LadderCheck(AgentCheck):
    # ===============================================
    # Section 1: Determine the Desktop Path (Common)
    # ===============================================
    def get_desktop_path(self):
        r"""
        Determines the desktop folder path based on the current OS.
        For macOS: assumes ~/Desktop.
        For Windows: uses %USERPROFILE%\Desktop.
        For other OS (e.g., Linux): assumes ~/Desktop.

        Returns the desktop path if it exists; otherwise returns "Oups! No Desktop on this system!".
        """
        current_os = platform.system()
        if current_os == "Darwin":
            desktop = os.path.expanduser("~/Desktop")
        elif current_os == "Windows":
            desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
        else:
            desktop = os.path.expanduser("~/Desktop")

        return desktop if os.path.isdir(desktop) else "Oups! No Desktop on this system!"

    # =======================================================
    # Section 2: OS-Specific Routines for Counting Desktop Items
    # =======================================================
    def count_desktop_files_mac(self, desktop):
        """
        macOS-specific routine: Count visible files/folders on the Desktop.
        Hidden items (names starting with '.') are ignored.
        Additionally, the file "Thumbs.db" (case-insensitive) is ignored.
        Returns the count, or -1 if the Desktop is not accessible.
        """
        if desktop == "Oups! No Desktop on this system!":
            return -1
        try:
            items = os.listdir(desktop)
        except Exception:
            return -1
        visible_items = [item for item in items if not item.startswith('.') and item.lower() != "thumbs.db"]
        return len(visible_items)

    def count_desktop_files_windows(self, desktop):
        """
        Windows-specific routine: Count visible files/folders on the Desktop.
        Hidden items (names starting with '.') are ignored.
        Returns the count, or -1 if the Desktop is not accessible.
        """
        if desktop == "Oups! No Desktop on this system!":
            return -1
        try:
            items = os.listdir(desktop)
        except Exception:
            return -1
        visible_items = [item for item in items if not item.startswith('.')]
        return len(visible_items)

    def count_desktop_files_other(self, desktop):
        """
        Linux/Other OS routine: Count visible files/folders on the Desktop.
        Hidden items (names starting with '.') are ignored.
        Returns the count, or -1 if the Desktop is not accessible.
        """
        if desktop == "Oups! No Desktop on this system!":
            return -1
        try:
            items = os.listdir(desktop)
        except Exception:
            return -1
        visible_items = [item for item in items if not item.startswith('.')]
        return len(visible_items)

    # =======================================================
    # Section 3: Helper to Read the Last Log Entry for Delta Calculation
    # =======================================================
    def get_previous_log_record(self, log_file):
        """
        Reads the last log entry from log_file (if available) and returns the full JSON record.
        If no log entry is found or an error occurs, returns None.
        """
        try:
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = [line for line in f.read().splitlines() if line.strip()]
                    if lines:
                        last_line = lines[-1]
                        record = json.loads(last_line)
                        return record
        except Exception:
            return None
        return None

    # =======================================================
    # Section 4: The Check Method (Entry Point for the Agent)
    # =======================================================
    def check(self, instance):
        # Dynamically determine the script's filename
        script_name = os.path.basename(__file__)

        # Determine OS and select the appropriate desktop path and counting function
        current_os = platform.system()
        if current_os == "Darwin":
            friendly_os = "MacOS"
            desktop_path = self.get_desktop_path()
            file_count = self.count_desktop_files_mac(desktop_path)
        elif current_os == "Windows":
            friendly_os = "Windows"
            desktop_path = self.get_desktop_path()
            file_count = self.count_desktop_files_windows(desktop_path)
        else:
            friendly_os = current_os  # e.g., "Linux"
            desktop_path = self.get_desktop_path()
            file_count = self.count_desktop_files_other(desktop_path)

        # Get computer name
        comp_name = socket.gethostname()

        # Get current date and time (a single consistent reference)
        now = datetime.datetime.now()
        current_dt = now.strftime('%Y-%m-%d %H:%M:%S')
        now_ts = int(time.time())

        # Determine status based on file count
        if file_count < 10 and file_count != -1:
            status = "INFO"
        elif 10 <= file_count < 15:
            status = "WARNING"
        elif file_count >= 15:
            status = "ALERT"
        else:
            status = "UNKNOWN"

        # Determine log file path (store the custom log file in the same directory as this check)
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ladder.log")
        
        # Get the previous log record (if any)
        prev_record = self.get_previous_log_record(log_file)
        if prev_record is not None:
            prev_count = prev_record.get("file_count")
            prev_dt_str = prev_record.get("datetime")
            try:
                prev_dt = datetime.datetime.strptime(prev_dt_str, '%Y-%m-%d %H:%M:%S')
                prev_ts = int(time.mktime(prev_dt.timetuple()))
            except Exception:
                prev_ts = 0
        else:
            prev_count = None
            prev_ts = 0

        # Timer logic: 
        # A) If file count has changed since last log, log the event.
        # B) Otherwise, if no log was recorded for more than 12 hours (43200 seconds), log an "alive" message.
        log_this_run = False
        if file_count != prev_count:
            log_this_run = True
            log_reason = f"File count changed: {prev_count} → {file_count} on {comp_name}"
        elif now_ts - prev_ts > 43200:
            log_this_run = True
            log_reason = f"No change, but 12h passed since last log. {comp_name} was alive."

        # Create the log record as a JSON object
        log_record = {
            "comp_name": comp_name,
            "datetime": current_dt,
            "os": friendly_os,
            "script": script_name,
            "file_count": file_count,
            "desktop_path": desktop_path,
            "status": status,
            "file_count_change": file_count - (prev_count if prev_count is not None else file_count)
        }
        log_json = json.dumps(log_record)

        # Set up logger (this part remains unchanged)
        import logging  # local import
        logger = logging.getLogger("ladder")
        logger.setLevel(logging.INFO)
        if not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        logger.propagate = False

        # Write the log only if conditions are met
        if log_this_run:
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_json + "\n")
            except Exception as e:
                self.log.error("Error writing log: %s", e)
            # Also use the Agent's logging mechanism for debugging
            self.log.info(log_json)
        else:
            self.log.debug("No logging required this run.")

        # Report the desktop file count as a gauge metric to Datadog, including useful tags.
        self.gauge("ladder.desktop.file_count", file_count,
                   tags=[f"os:{friendly_os}", f"status:{status}", f"script:{script_name}"])
