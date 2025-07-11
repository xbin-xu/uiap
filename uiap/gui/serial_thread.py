import logging
from time import sleep
from PySide6.QtCore import QThread, Signal
import serial

logger = logging.getLogger()


class SerialThread(QThread):
    """
    gui_thread          serial_thead
    init -------------->
    open -------------->
    send -------------->
         <-------------- recv
    close ------------->

    init -------------->
    open -------------->
         <-------------- error
    """

    open = Signal(str, int, int, int, str, bool, bool, bool)
    close = Signal()
    recv = Signal(bytes)
    send = Signal(bytes)
    error = Signal(str)

    THREAD_STOP, THREAD_START = (0, 1)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ser = None
        self.thread_running = self.THREAD_STOP
        self.open.connect(self.serial_open)
        self.close.connect(self.serial_close)
        self.send.connect(self.serial_send)
        logger.debug(f"serial thread init")

    def connect_slots(self, recv_slot, error_slot=None):
        if recv_slot:
            self.recv.connect(recv_slot)
        if error_slot:
            self.error.connect(error_slot)

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
                write_timeout=1,  # 防止使用虚拟串口时，由于对端没有打开导致程序堵塞
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

    def thread_quit(self):
        self.thread_running = self.THREAD_STOP

    def run(self):
        self.thread_running = self.THREAD_START
        logger.info(f"serial thread running...")

        try:
            while self.thread_running:
                if not self.serial_is_open():
                    self.sleep(1)
                    continue
                if self.ser.in_waiting > 0:
                    data = self.ser.read_all()
                    self.recv.emit(data)
                self.msleep(100)
        except Exception as e:
            logger.error(f"error: {e}")
            self.error.emit(str(e))
        finally:
            self.serial_close()
            logger.info(f"serial thread exited")
