from PySide6.QtCore import Signal, Slot, QTimer
import serial
import logging
from .serial_handler import SerialHandler

logger = logging.getLogger(__name__)


class SerialHandlerIO(SerialHandler):
    def __init__(self, serial_worker=None):
        super().__init__(serial_worker)
        self.timer = QTimer()
        self.timer.timeout.connect(self.recv_data)

    def on_enter(self):
        self.timer.start(100)

    def on_exit(self):
        self.timer.stop()

    def send_file(self, path: str):
        try:
            with open(path, "rb") as f:
                content = f.read()

            self.send_data(content)
            self.serial_worker.ftp_done.emit(True)
        except Exception as e:
            logger.error(f"{e}")
            self.serial_worker.ftp_done.emit(False)

    def recv_file(self, path: str):
        pass
