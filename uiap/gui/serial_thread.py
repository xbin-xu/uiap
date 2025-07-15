import logging
from time import sleep
from PySide6.QtCore import QThread, Signal
import serial
from core.protocol.serial_file_transfer import *

logger = logging.getLogger()


class SerialThread(QThread):
    """
    gui_thread          serial_thead
    start ------------->

    open -------------->
    send -------------->
         <-------------- recv
    close ------------->

    open -------------->
         <-------------- error
    """

    open = Signal(str, int, int, int, str, bool, bool, bool)
    close = Signal()
    recv = Signal(bytes)
    send = Signal(bytes)
    error = Signal(str)
    mode_change = Signal(str)
    ftp_recv_file = Signal(str)
    ftp_send_file = Signal(str)
    ftp_done = Signal(int)

    THREAD_STOP, THREAD_START = (0, 1)

    SERIAL_MODE_IO, SERIAL_MODE_RAW, SERIAL_MODE_YMODEM = ("IO", "Raw", "Ymodem")
    SERIAL_MODE = (SERIAL_MODE_IO, SERIAL_MODE_RAW, SERIAL_MODE_YMODEM)
    SERIAL_MODE_DICT = {
        "IO": SERIAL_MODE_IO,
        "Raw": SERIAL_MODE_RAW,
        "Ymodem": SERIAL_MODE_YMODEM,
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ser = None
        self.thread_running = self.THREAD_STOP
        self.serial_mode = self.SERIAL_MODE_IO
        self.serial_file_transfer: SerialFileTransfer = None
        self.open.connect(self.serial_open)
        self.close.connect(self.serial_close)
        self.send.connect(self.serial_send)
        self.mode_change.connect(self.serial_mode_change)
        self.ftp_recv_file.connect(self.serial_ftp_recv_file)
        self.ftp_send_file.connect(self.serial_ftp_send_file)
        logger.debug(f"serial thread init")

    def connect_slots(self, recv_slot, error_slot=None, ftp_done_slot=None):
        if recv_slot:
            self.recv.connect(recv_slot)
        if error_slot:
            self.error.connect(error_slot)
        if ftp_done_slot:
            self.ftp_done.connect(ftp_done_slot)

    def serial_is_open(self):
        return self.ser and self.ser.is_open

    def serial_open(
        self,
        port=None,
        baudrate=9600,
        bytesize=8,
        stopbits=1,
        parity="N",
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
    ):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                xonxoff=xonxoff,
                rtscts=rtscts,
                stopbits=stopbits,
                dsrdtr=dsrdtr,
                timeout=1,  # 防止文件传输时，程序阻塞
                write_timeout=1,  # 防止使用虚拟串口时，由于对端没有打开导致程序阻塞
            )
            logger.info(f"serial open success")
        except Exception as e:
            logger.error(f"error: {e}")
            self.error.emit(str(e))

    def serial_close(self):
        if self.serial_is_open():
            self.ser.close()
            self.ser = None
            logger.info(f"serial close success")

    def serial_send(self, data: bytes):
        if not self.serial_is_open():
            logger.error(f"serial is not open")

        try:
            self.ser.write(data)
        except serial.SerialTimeoutException as e:
            logger.warning(f"error: {e}")
            self.error.emit(str(e))
        except Exception as e:
            logger.error(f"error: {e}")
            self.error.emit(str(e))

    def serial_mode_change(self, mode: str):
        assert mode in self.SERIAL_MODE

        if self.ser is None:
            return False

        if mode == self.serial_mode:
            return True

        self.serial_mode = mode
        # self.ser.flush()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        if not self.ser.is_open:
            self.ser.open()

        if self.serial_mode == self.SERIAL_MODE_IO:
            pass
        elif self.serial_mode == self.SERIAL_MODE_RAW:
            self.serial_file_transfer = SerialFileTransferCustom(
                self.ser, SerialFtp(self.ser)
            )
            pass
        elif self.serial_mode == self.SERIAL_MODE_YMODEM:
            self.serial_file_transfer = SerialFileTransferCustom(
                self.ser, SerialFtpYmodem(self.ser)
            )
        return True

    def serial_ftp_recv_file(self, file_path: str) -> bool:
        ret = self.serial_file_transfer.transfer(
            file_path, self.serial_file_transfer.RECV
        )
        self.ftp_done.emit(ret)

    def serial_ftp_send_file(self, file_path: str | list[str]) -> bool:
        ret = self.serial_file_transfer.transfer(
            file_path, self.serial_file_transfer.SEND
        )
        self.ftp_done.emit(ret)

    def thread_quit(self):
        self.thread_running = self.THREAD_STOP

    def run(self):
        self.thread_running = self.THREAD_START
        logger.info(f"serial thread running...")

        try:
            while self.thread_running:
                if self.serial_mode == self.SERIAL_MODE_IO and self.serial_is_open():
                    if self.ser.in_waiting > 0:
                        data = self.ser.read_all()
                        self.recv.emit(data)
                    self.msleep(100)
                else:
                    self.msleep(1000)
        except Exception as e:
            logger.error(f"error: {e}")
            self.error.emit(str(e))
        finally:
            self.serial_close()
            logger.info(f"serial thread exited")
