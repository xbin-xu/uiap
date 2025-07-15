from abc import ABC, abstractmethod
import serial
import logging

logger = logging.getLogger(__name__)


class SerialHandler(ABC):
    def __init__(self, serial_worker=None):
        self.serial_worker = serial_worker

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def send_data(self, data: bytes):
        if not self.serial_worker.serial_is_open():
            logger.error(f"serial is not open")

        try:
            self.serial_worker.ser.write(data)
        except Exception as e:
            logger.error(f"{e}")
            self.serial_worker.error.emit(str(e))

    def recv_data(self) -> bytes:
        # if not self.serial_worker.serial_is_open():
        #     logger.error(f"serial is not open")

        try:
            if (
                self.serial_worker.serial_is_open()
                and self.serial_worker.ser.in_waiting > 0
            ):
                data = self.serial_worker.ser.read_all()
                self.serial_worker.recv.emit(data)
        except Exception as e:
            logger.error(f"{e}")
            self.serial_worker.error.emit(str(e))

    @abstractmethod
    def send_file(self, path: str):
        pass

    @abstractmethod
    def recv_file(self, path: str):
        pass
