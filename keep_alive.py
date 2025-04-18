import logging
import subprocess
import time
import threading
from pwnagotchi.plugins import Plugin

class KeepAlivePlugin(Plugin):
    __author__ = 'cashflowmarcin'
    __version__ = '1.0'
    __license__ = 'MIT'
    __description__ = 'Keeps the tether connection alive by pinging a host every N minutes.'

    def __init__(self):
        self._thread = None
        self.running = False

    def _ping_loop(self, interval, host):
        while self.running:
            try:
                logging.info(f"[keep-alive] Pinging {host}")
                subprocess.run(['ping', '-c', '1', '-W', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logging.error(f"[keep-alive] Ping failed: {e}")
            time.sleep(interval)

    def on_loaded(self):
        interval = int(self.options.get("interval", 120))  # seconds
        host = self.options.get("host", "google.com")

        self.running = True
        self._thread = threading.Thread(target=self._ping_loop, args=(interval, host))
        self._thread.daemon = True
        self._thread.start()
        logging.info(f"[keep-alive] Plugin loaded. Pinging {host} every {interval} seconds.")

    def on_unload(self, ui):
        self.running = False
        if self._thread:
            self._thread.join()
        logging.info("[keep-alive] Plugin unloaded.")
