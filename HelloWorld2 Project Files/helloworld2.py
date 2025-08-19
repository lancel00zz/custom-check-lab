import os
import json
import time
import logging
import socket
import platform
from datadog_checks.base import AgentCheck

class Helloworld2Check(AgentCheck):
    def check(self, instance):
        # Resolve Desktop path based on OS
        if platform.system().lower() == 'windows':
            desktop_path = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
        else:
            desktop_path = os.path.expanduser("~/Desktop")

        # Count visible files and folders
        try:
            file_count = len([
                f for f in os.listdir(desktop_path)
                if not f.startswith('.') and os.path.exists(os.path.join(desktop_path, f))
            ])
        except Exception as e:
            self.log.warning(f"Could not access Desktop: {e}")
            file_count = -1

        # Submit metric
        self.gauge('helloworld2.desktop_file_count', file_count)

        # Set log directory based on OS
        if platform.system().lower() == 'windows':
            log_dir = os.environ.get("TEMP", "C:\\Temp")
        else:
            log_dir = '/opt/datadog-agent/logs'

        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, 'helloworld2.log')
        state_file = os.path.join(log_dir, 'helloworld2_state.json')
        host = socket.gethostname()

        # Set up logger
        logger = logging.getLogger('helloworld2')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Load previous state
        last_count = None
        last_logged = 0
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
            last_count = state.get("last_count")
            last_logged = state.get("last_logged", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        now = int(time.time())
        log_this_run = False

        # Decide whether to log
        if file_count != last_count:
            log_this_run = True
            log_reason = f"File count changed: {last_count} → {file_count} on {host}"
        elif now - last_logged > 43200:
            log_this_run = True
            log_reason = f"No change, but 12h passed since last log. {host} was alive."

        # Log using correct level and emoji
        if log_this_run:
            if file_count > 18:
                logger.warning(f"⚠️ {log_reason}")
            else:
                logger.info(f"✅ {log_reason}")

            # Save new state
            try:
                with open(state_file, 'w') as f:
                    json.dump({
                        "last_count": file_count,
                        "last_logged": now
                    }, f)
            except Exception as e:
                self.log.warning(f"Could not write state file: {e}")