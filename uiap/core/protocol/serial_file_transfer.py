import os
from time import sleep
import serial
import logging
from typing import Callable, Optional
from typing import *
from abc import ABC, abstractmethod
from ymodem.Socket import ModemSocket

logger = logging.getLogger()


class SerialFtp:
    def __init__(self, ser: serial.Serial):
        self.ser = ser

    def transfer(self, file_path: str, is_send: bool = True) -> bool:
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.ser.write(content)
            return True
        except Exception as e:
            logger.error(f"error: {e}")
            return False

    def read(self, size, timeout):
        if self.ser and self.ser.write_timeout != timeout:
            self.ser.write_timeout = timeout

        return self.ser.read(size)

    def write(self, data, timeout):
        if self.ser and self.ser.write_timeout != timeout:
            self.ser.write_timeout = timeout
        return self.ser.write(data)


class SerialFtpYmodem(SerialFtp):

    def __init__(self, ser: serial.Serial):
        super().__init__(ser)
        self.ftp = ModemSocket(super().read, self.write)
        # self.ftp._protocol_features = 0

    def transfer(self, file_path: str | List[str], is_send: bool = True) -> bool:
        assert self.ser and self.ftp
        if is_send:
            if isinstance(file_path, str):
                ret = self.ftp.send([file_path])
            else:
                ret = self.ftp.send(file_path)
        else:
            assert isinstance(file_path, str)
            ret = self.ftp.recv(file_path)
        return ret


# ---


class SerialFileTransfer(ABC):
    RECV, SEND = (False, True)

    def __init__(
        self,
        ser: serial.Serial,
        file_transfer_protocol: SerialFtp,
    ):
        self.ser = ser
        self.file_transfer_protocol = file_transfer_protocol

    @abstractmethod
    def prev_transfer(self, is_send: bool = True) -> bool:
        pass

    @abstractmethod
    def post_transfer(self, is_send: bool = True) -> bool:
        pass

    def transfer(self, file_path: str | List[str], is_send: bool = True) -> bool:
        if self.ser is None:
            logger.error("serial is None")
            return False

        if self.ser.is_open == False:
            try:
                self.ser.open()
            except Exception as e:
                logger.error(f"{e}")
                return False

        if not self.prev_transfer(is_send):
            logger.error("prev_transfer failed")
            return False

        if not self.file_transfer_protocol.transfer(file_path, is_send):
            logger.info(f"send ret False")
            return False

        if not self.post_transfer(is_send):
            logger.error("post_transfer failed")
            return False

        return True

    def send(self, file_path: str | list[str]) -> bool:
        return self.transfer(file_path, self.SEND)

    def recv(self, file_path: str) -> bool:
        return self.transfer(file_path, self.RECV)


class SerialFileTransferCustom(SerialFileTransfer):
    def prev_transfer(self, is_send: bool = True) -> bool:
        if is_send:
            self.ser.write(b"1")
        else:
            self.ser.write(b"2")
        sleep(0.2)
        return True

    def post_transfer(self, is_send: bool = True) -> bool:
        return True
