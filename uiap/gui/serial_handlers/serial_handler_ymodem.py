import logging
from gui.serial_handlers.serial_handler import SerialHandler
from core.serial_file_transfer import SerialFileTransferCustom, SerialFtpYmodem

# from gui.serial_thread import SerialWorker

logger = logging.getLogger(__name__)


class SerialHandlerYmodem(SerialHandler):
    def __init__(self, serial_worker):
        super().__init__(serial_worker)
        self.ftp = SerialFileTransferCustom(
            self.serial_worker.ser, SerialFtpYmodem(self.serial_worker.ser)
        )

    def send_file(self, path: str):
        ret = self.ftp.transfer(path, self.ftp.SEND)
        self.serial_worker.ftp_done.emit(ret)

    def recv_file(self, path: str):
        ret = self.ftp.transfer(path, self.ftp.RECV)
        self.serial_worker.ftp_done.emit(ret)
