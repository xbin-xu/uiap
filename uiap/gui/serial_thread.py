import logging
from PySide6.QtCore import QObject, Signal, Slot
import serial
from .serial_handlers.serial_handler import SerialHandler
from .serial_handlers.serial_handler_io import SerialHandlerIO
from .serial_handlers.serial_handler_ymodem import SerialHandlerYmodem

logger = logging.getLogger()


class SerialWorker(QObject):
    """
    ui_thread          serial_thead
    start ------------->

    open -------------->
    send -------------->
    recv_request ------>
         <-------------- recv
    close ------------->

    open -------------->
         <-------------- error
    """

    # signals
    open = Signal(str, int, int, int, str, bool, bool, bool)
    close = Signal()
    send = Signal(bytes)
    recv_request = Signal()
    recv = Signal(bytes)
    error = Signal(str)
    mode_change = Signal(str)
    ftp_send_file = Signal(str)
    ftp_recv_file = Signal(str)
    ftp_done = Signal(int)

    SERIAL_MODE_IO, SERIAL_MODE_YMODEM = ("IO", "Ymodem")
    SERIAL_MODE = (SERIAL_MODE_IO, SERIAL_MODE_YMODEM)
    SERIAL_HANDLERS = {
        SERIAL_MODE_IO: SerialHandlerIO,
        SERIAL_MODE_YMODEM: SerialHandlerYmodem,
    }

    def __init__(self):
        super().__init__()

        self.ser: serial.Serial | None = serial.Serial()
        self.serial_mode = self.SERIAL_MODE_IO
        self.serial_handler: SerialHandler = self.SERIAL_HANDLERS[self.serial_mode](
            self
        )
        if self.serial_handler:
            self.serial_handler.on_enter()

        self.open.connect(self.serial_open)
        self.close.connect(self.serial_close)
        self.send.connect(self.serial_send)
        self.recv_request.connect(self.serial_recv_request)
        self.mode_change.connect(self.serial_mode_change)
        self.ftp_send_file.connect(self.serial_ftp_send_file)
        self.ftp_recv_file.connect(self.serial_ftp_recv_file)

    def connect_slots(self, recv_slot, error_slot=None, ftp_done_slot=None):
        if recv_slot:
            self.recv.connect(recv_slot)
        if error_slot:
            self.error.connect(error_slot)
        if ftp_done_slot:
            self.ftp_done.connect(ftp_done_slot)

    def serial_is_open(self):
        return self.ser and self.ser.is_open

    @Slot(str, int, int, int, str, bool, bool, bool)
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
        timeout=1,
        write_timeout=1,
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
                timeout=timeout,
                write_timeout=write_timeout,
            )
            logger.info("serial open success")
        except Exception as e:
            logger.error(f"{e}")
            self.error.emit(str(e))

    @Slot()
    def serial_close(self):
        if self.serial_is_open():
            assert self.ser is not None
            self.ser.close()
            self.ser = None
            logger.info("serial close success")

    @Slot(bytes)
    def serial_send(self, data: bytes):
        if not self.serial_handler:
            logger.warning("serial handler not ready")
            return

        self.serial_handler.send_data(data)

    @Slot()
    def serial_recv_request(self):
        if not self.serial_handler:
            logger.warning("serial handler not ready")
            return

        self.serial_handler.recv_data()

    @Slot(str)
    def serial_mode_change(self, mode: str):
        assert mode in self.SERIAL_MODE

        if mode == self.serial_mode:
            return

        if self.serial_handler:
            self.serial_handler.on_exit()

        self.serial_mode = mode
        serial_handler_class: SerialHandler | None = self.SERIAL_HANDLERS.get(
            self.serial_mode
        )
        if serial_handler_class:
            self.serial_handler = serial_handler_class(self)
            self.serial_handler.on_enter()

    @Slot(str)
    def serial_ftp_send_file(self, file_path: str):
        self.serial_handler.send_file(file_path)

    @Slot(str)
    def serial_ftp_recv_file(self, file_path: str):
        self.serial_handler.recv_file(file_path)
