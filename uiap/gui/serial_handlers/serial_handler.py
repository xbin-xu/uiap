from abc import ABC, abstractmethod
import logging

# from gui.serial_thread import SerialWorker


logger = logging.getLogger(__name__)


class SerialHandler(ABC):

    def __init__(self, serial_worker):
        self.serial_worker = serial_worker

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def send_data(self, data: bytes):
        if not self.serial_worker.serial_is_open():
            logger.error("serial is not open")
            return
        assert self.serial_worker.ser

        try:
            self.serial_worker.ser.write(data)
        except Exception as e:
            logger.error(f"{e}")
            self.serial_worker.error.emit(str(e))

    def recv_data(self) -> bytes | None:
        if not self.serial_worker.serial_is_open():
            return None

        try:
            if self.serial_worker.ser.in_waiting > 0:
                data = self.serial_worker.ser.read_all()
                self.serial_worker.recv.emit(data)
                return data
        except Exception as e:
            logger.error(f"{e}")
            self.serial_worker.error.emit(str(e))
        return None

    @abstractmethod
    def send_file(self, path: str):
        pass

    @abstractmethod
    def recv_file(self, path: str):
        pass
