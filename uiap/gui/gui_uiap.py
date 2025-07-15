import os
import re
import logging
from time import sleep
import serial
from pathlib import Path
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QTimer, QMetaObject, QThread
from PySide6.QtWidgets import (
    QComboBox,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QToolButton,
    QPlainTextEdit,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QFont, QIcon
from config.config import UiapConfig, CONFIG_FILE, COMBO_BOX_ITEMS
from core.crypto import *
from utils.log import setup_logging
from gui.Ui_uiap import Ui_Form  # for IntelliSense
from gui.serial_thread import SerialWorker
from gui.serial_rx_tx_item import SerialRxTxItem
from gui.resource_rc import *

logger = logging.getLogger()


# 自定义 Handler 将日志发送到 QPlainTextEdit
class QtLoggerHandler(logging.Handler):
    def __init__(self, text_edit: QtWidgets.QPlainTextEdit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        QtCore.QMetaObject.invokeMethod(
            self.text_edit,
            "appendPlainText",
            QtCore.Qt.ConnectionType.QueuedConnection,
            QtCore.Q_ARG(str, msg),
        )


class UiapWindow(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super().__init__()

        # PyQt6 禁用自动连接
        # QMetaObject.connectSlotsByName = lambda *args: None

        """
        动态加载 .ui 文件

        PyQt6: 
        >>> from PyQt6 import QtWidgets, uic
        >>> uic.loadUi("./ui/uiap.ui", self)

        PySide6: 
        >>> from PySide6.QtUiTools import QUiLoader
        >>> loader = QUiLoader()
        >>> window = loader.load("./ui/uiap.ui", None)
        """
        # uic.load("./ui/uiap.ui", self)
        # 静态加载：编译 -> 静态引入 module
        self.setupUi(self)

        # 配置日志
        setup_logging(log_level=logging.INFO, log_file=".uiap/uiap.log")
        self.log_handler = QtLoggerHandler(self.log_pte)
        self.log_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
            )
        )
        logging.getLogger().addHandler(self.log_handler)

        # 配置默认值
        self.setup_default_value()
        logging.debug("setup default value finish")

        # 加载配置文件中配置
        self.setup_config_value()
        logging.debug("setup config value finish")

        # 绑定信号和槽
        self.connect_signal()
        logging.debug("connect signal finish")

        # 变量初始化
        self.serial_open_status = False
        self.serial_rx_tx_items: list[SerialRxTxItem] = []

        self.serial_thread = QThread()
        self.serial_worker = SerialWorker()
        self.serial_worker.moveToThread(self.serial_thread)
        self.serial_thread.started.connect(
            lambda: logger.info("serial worker thread started")
        )
        self.serial_thread.finished.connect(
            lambda: logger.info("serial worker thread finished")
        )
        self.serial_thread.finished.connect(self.serial_thread.deleteLater)
        self.serial_worker.connect_slots(
            recv_slot=self.on_serial_recv,
            error_slot=self.on_serial_error,
            ftp_done_slot=self.on_serial_ftp_done,
        )
        self.serial_thread.start()

        logger.info("setup uiap window finish")

    def setup_default_value(self):
        for name, items in COMBO_BOX_ITEMS.items():
            if name == "firmware_crypto_cmb":
                for i in range(8):
                    widget = getattr(self, f"{name}_{i}")
                    widget.addItems(items)
            else:
                widget = getattr(self, name)
                widget.addItems(items)
        self.serial_cmb_set_enabled(True)
        self.serial_rts_dtr_chk_set_enabled()

        # 设置等宽字体
        font = QFont("Consolas")
        self.serial_rx_tx_pte.setFont(font)
        self.serial_tx_pte.setFont(font)
        self.log_pte.setFont(font)

    def get_firmware_select_widgets(self):
        self.firmware_select_widgets = []

        firmware_select_widget_info = [
            (QCheckBox, "firmware_selected_chk"),
            (QLineEdit, "firmware_path_le"),
            (QLineEdit, "firmware_address_le"),
            (QComboBox, "firmware_crypto_cmb"),
        ]

        for idx in range(len(self.uiap_config.select_items)):
            firmware_select_widget = []
            for widget_class, widget_name in firmware_select_widget_info:
                widget = self.findChild(widget_class, f"{widget_name}_{idx}")
                if widget is None:
                    logger.warning(f"{widget_name}_{idx} not found")
                firmware_select_widget.append(widget)
            self.firmware_select_widgets.append(firmware_select_widget)

    def setup_config_value(self):
        # load config
        self.uiap_config = UiapConfig.from_json_file(CONFIG_FILE)
        logger.debug(self.uiap_config)

        # setup config
        self.serial_port_cmb.setCurrentText(self.uiap_config.port)
        self.serial_baud_rate_cmb.setCurrentText(self.uiap_config.baud_rate)
        self.serial_data_bits_cmb.setCurrentText(self.uiap_config.data_bits)
        self.serial_stop_bits_cmb.setCurrentText(self.uiap_config.stop_bits)
        self.serial_parity_cmb.setCurrentText(self.uiap_config.parity)
        self.serial_flow_ctrl_cmb.setCurrentText(self.uiap_config.flow_ctrl)
        self.serial_rts_chk.setChecked(self.uiap_config.rts)
        self.serial_dtr_chk.setChecked(self.uiap_config.dtr)

        self.serial_rx_tx_hex_chk.setChecked(self.uiap_config.rx_tx_hex)
        self.serial_tx_hex_chk.setChecked(self.uiap_config.tx_hex)

        self.firmware_fill_byte_le.setText(self.uiap_config.fill_byte)
        self.firmware_transfer_protocol_cmb.setCurrentText(
            self.uiap_config.transfer_protocol
        )
        self.firmware_read_start_address_le.setText(self.uiap_config.read_start_address)
        self.firmware_read_size_le.setText(self.uiap_config.read_size)

        self.get_firmware_select_widgets()
        for idx in range(len(self.uiap_config.select_items)):
            callbacks = [
                lambda widget, idx: widget.setChecked(
                    self.uiap_config.select_items[idx].selected
                ),
                lambda widget, idx: widget.setText(
                    self.uiap_config.select_items[idx].path
                ),
                lambda widget, idx: widget.setText(
                    self.uiap_config.select_items[idx].address
                ),
                lambda widget, idx: widget.setCurrentText(
                    self.uiap_config.select_items[idx].crypto
                ),
            ]

            for widget, callback in zip(self.firmware_select_widgets[idx], callbacks):
                if widget and callback:
                    callback(widget, idx)

    def connect_signal(self):
        # bind all combo box
        for widget in self.findChildren(QComboBox):
            widget.currentTextChanged.connect(
                lambda text, widget=widget: self.on_widget_changed(widget, text)
            )
        self.serial_flow_ctrl_cmb.currentTextChanged.connect(
            self.on_serial_flow_ctrl_cmb_currentTextChanged
        )

        # bind all check box
        for widget in self.findChildren(QCheckBox):
            widget.stateChanged.connect(
                # lambda state, widget=widget: self.on_widget_changed(
                #     widget, state != QtCore.Qt.CheckState,
                # )
                lambda _, widget=widget: self.on_widget_changed(
                    widget, widget.isChecked()
                )
            )
        self.serial_rx_tx_hex_chk.stateChanged.connect(
            self.on_serial_rx_tx_hex_chk_state_changed
        )
        self.serial_tx_hex_chk.stateChanged.connect(
            self.on_serial_tx_hex_chk_state_changed
        )

        # bind all line edit
        for widget in self.findChildren(QLineEdit):
            widget.textChanged.connect(
                lambda text, widget=widget: self.on_widget_changed(widget, text)
            )
            # widget.editingFinished.connect(
            #     lambda widget=widget: self.on_widget_changed(
            #         widget, widget.displayText()
            #     )
            # )

        # bind all tool button
        for widget in self.findChildren(QToolButton):
            widget.clicked.connect(
                lambda _, widget=widget: self.on_tool_button_clicked(widget)
            )

        # 定时扫描串口的端口号
        self.serial_scan_port_timer = QTimer()
        self.serial_scan_port_timer.timeout.connect(
            self.on_serial_scan_port_timer_timeout
        )
        self.serial_scan_port_timer.start(3000)

        # bind push button
        self.serial_open_btn.clicked.connect(self.on_serial_open_btn_clicked)
        self.serial_send_btn.clicked.connect(self.on_serial_send_btn_clicked)
        self.serial_clear_btn.clicked.connect(self.on_serial_clear_btn_clicked)
        self.firmware_combine_btn.clicked.connect(self.on_firmware_combine_btn_clicked)
        self.firmware_update_btn.clicked.connect(self.on_firmware_update_btn_clicked)
        self.firmware_read_btn.clicked.connect(self.on_firmware_read_btn_clicked)

    def parse_widget_name(self, name):
        """
        命名规则: xxx_yyy_zzz[_idx]
        xxx: 前缀 prefix, 例如 serial, firmware
        yyy: 配置名称 config_name, 例如 port, baud_rate
        zzz: 控件名称 widget_abbr, 例如 cmb, le
        idx: 下标索引 idx(可选项), 例如 0, 1

        xxx 可能包含 0-9a-zA-Z
        yyy 可能包含 0-9a-zA-Z_
        zzz 可能包含 a-zA-Z
        idx 可能包含 0-9

        >>> w = UiapWindow()
        >>> w.parse_name("serial_port_cmb")
        {'prefix': 'serial', 'config_name': 'port', 'widget_abbr': 'cmb', 'idx': None}
        >>> w.parse_name("serial_port_cmb_0")
        {'prefix': 'serial', 'config_name': 'port', 'widget_abbr': 'cmb', 'idx': 0}
        >>> w.parse_name("serial_port_cmb_02")
        {'prefix': 'serial', 'config_name': 'port', 'widget_abbr': 'cmb', 'idx': 2}
        >>> w.parse_name("serial_port_cmb_12")
        {'prefix': 'serial', 'config_name': 'port', 'widget_abbr': 'cmb', 'idx': 12}
        >>> w.parse_name("serial_baud_rate_cmb_12")
        {'prefix': 'serial', 'config_name': 'baud_rate', 'widget_abbr': 'cmb', 'idx': 12}
        >>> w.parse_name("serial1_baud_rate_cmb_12")
        {'prefix': 'serial1', 'config_name': 'baud_rate', 'widget_abbr': 'cmb', 'idx': 12}
        """

        pattern = r"^([a-zA-Z0-9]+)_([a-zA-Z0-9_]+)_([a-zA-Z]+)(?:_(\d+))?$"
        match = re.match(pattern, name)
        if match:
            prefix, config_name, widget_abbr, idx = match.groups()
            return {
                "prefix": prefix,
                "config_name": config_name,
                "widget_abbr": widget_abbr,
                "idx": int(idx) if idx else None,
            }
        else:
            logger.error(f"Name '{name}' does not match the pattern.")
            return None

    def on_widget_changed(self, widget, new_value):
        logger.debug(f"-> {widget}, {new_value}")

        widget_name = widget.objectName()
        logger.debug(f"{widget_name}")

        parsed_result = self.parse_widget_name(widget_name)
        if parsed_result is None:
            logger.error(f"{widget_name} parser failed")
            return

        prefix, config_name, widget_abbr, idx = parsed_result.values()
        logger.debug(f"{widget_name}: {prefix}, {config_name}, {widget_abbr}, {idx}")

        config_obj = None
        if idx is None:
            config_obj = self.uiap_config
        else:
            assert idx < len(self.uiap_config.select_items)
            config_obj = self.uiap_config.select_items[idx]

        prev_value = getattr(config_obj, config_name)
        logger.info(f"{widget_name}: {prev_value} -> {new_value}")
        setattr(config_obj, config_name, new_value)

        self.uiap_config.to_json_file(CONFIG_FILE)

    def open_file_dialog(self):
        # 打开文件对话框，只允许选择 .bin 文件
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 BIN 文件", "", "BIN Files (*.bin);;All Files (*)"  # 初始目录
        )

        return file_path

    def on_tool_button_clicked(self, widget):
        widget_name = widget.objectName()
        logger.debug(f"{widget_name}")

        parsed_result = self.parse_widget_name(widget_name)
        if parsed_result is None:
            logger.error(f"{widget_name} parser failed")
            return

        prefix, config_name, widget_abbr, idx = parsed_result.values()
        logger.debug(f"{widget_name}: {prefix}, {config_name}, {widget_abbr}, {idx}")

        file_path = self.open_file_dialog()
        logger.info(f"file_path is {file_path}")
        if file_path is None or file_path == "":
            return

        line_edit_widget = self.firmware_select_widgets[idx][1]
        line_edit_widget.setText(file_path)
        self.uiap_config.to_json_file(CONFIG_FILE)

    def scan_serial_port(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def on_serial_scan_port_timer_timeout(self):

        def get_combo_items(combo: QComboBox):
            return {combo.itemText(i): i for i in range(combo.count())}

        items = get_combo_items(self.serial_port_cmb)
        current_selection = self.serial_port_cmb.currentText()

        available_ports = self.scan_serial_port()

        add_item = []
        remove_item = []
        for port in available_ports:
            if port not in items.keys():
                add_item.append(port)
        current_selection_removed = False
        for port, item_idx in items.items():
            if port not in available_ports:
                if port == current_selection:
                    current_selection_removed = True
                remove_item.append(item_idx)

        for item in remove_item:
            self.serial_port_cmb.removeItem(item)
        for item in add_item:
            self.serial_port_cmb.addItem(item)

        if current_selection_removed:
            if self.serial_open_status:
                self.serial_open_btn.clicked.emit()

    def serial_rts_dtr_chk_set_enabled(self):
        self.serial_rts_chk.setEnabled(
            self.serial_flow_ctrl_cmb.currentText() == "Hardware"
        )
        self.serial_dtr_chk.setEnabled(
            self.serial_flow_ctrl_cmb.currentText() == "Hardware"
        )

    def on_serial_flow_ctrl_cmb_currentTextChanged(self, text):
        self.serial_rts_dtr_chk_set_enabled()

    def serial_cmb_set_enabled(self, enable):
        self.serial_port_cmb.setEnabled(enable)
        self.serial_baud_rate_cmb.setEnabled(enable)
        self.serial_data_bits_cmb.setEnabled(enable)
        self.serial_stop_bits_cmb.setEnabled(enable)
        self.serial_parity_cmb.setEnabled(enable)
        self.serial_flow_ctrl_cmb.setEnabled(enable)
        # self.serial_rts_chk.setEnabled(enable)
        # self.serial_dtr_chk.setEnabled(enable)
        self.serial_rts_dtr_chk_set_enabled()
        self.serial_send_btn.setEnabled(not enable)

    def on_serial_open_btn_clicked(self):
        self.serial_open_status = not self.serial_open_status
        logger.debug(f"serial_open_status is {self.serial_open_status}")

        if self.serial_open_status is True:
            self.serial_open_btn.setText("关闭串口")

            self.serial_worker.open.emit(
                self.uiap_config.port,
                int(self.uiap_config.baud_rate),
                int(self.uiap_config.data_bits),
                int(self.uiap_config.stop_bits),
                self.uiap_config.parity[0],
                self.uiap_config.flow_ctrl == "Software",
                self.uiap_config.flow_ctrl == "Hardware" and self.uiap_config.rts,
                self.uiap_config.flow_ctrl == "Hardware" and self.uiap_config.dtr,
            )
        else:
            self.serial_open_btn.setText("打开串口")
            self.serial_worker.close.emit()

        self.serial_cmb_set_enabled(not self.serial_open_status)

    def to_bytes(self, data_str: str, hex_mode=False):
        if hex_mode:
            cleaned = data_str.replace(" ", "").lower()
            if len(cleaned) % 2 != 0:
                raise ValueError("HEX string length must be even")
            return bytes.fromhex(cleaned)
        else:
            return data_str.encode("ascii")

    def to_str(self, data: bytes, hex_mode=False):
        if hex_mode:
            return " ".join(f"{b:02X}" for b in data)
        else:
            return data.decode("utf-8", errors="replace")

    def on_serial_send_btn_clicked(self, status):
        send_text = self.serial_tx_pte.toPlainText()
        try:
            bytes = self.to_bytes(send_text, self.uiap_config.tx_hex)
            self.serial_worker.send.emit(bytes)
            serial_rx_tx_item = SerialRxTxItem.tx(bytes)
            logger.info(serial_rx_tx_item)
            self.serial_rx_tx_items.append(serial_rx_tx_item)
            self.serial_rx_tx_pte.appendPlainText(
                str(serial_rx_tx_item)
                if self.uiap_config.rx_tx_hex
                else serial_rx_tx_item.decode()
            )
        except Exception as e:
            logger.error(f"{e}")

    def on_serial_recv(self, bytes):
        logger.debug(f"{bytes}")
        serial_rx_tx_item = SerialRxTxItem.rx(bytes)
        logger.info(serial_rx_tx_item)
        self.serial_rx_tx_items.append(serial_rx_tx_item)
        self.serial_rx_tx_pte.appendPlainText(
            str(serial_rx_tx_item)
            if self.uiap_config.rx_tx_hex
            else serial_rx_tx_item.decode()
        )

    def on_serial_error(self, str):
        # logger.error(f"{str}")
        self.serial_open_status = False
        self.serial_worker.close.emit()
        self.serial_cmb_set_enabled(not self.serial_open_status)
        self.show_msg_box(QMessageBox.Icon.Critical, str)

    def on_serial_ftp_done(self, success):
        logger.info(f"on_serial_ftp_done: {success}")
        # self.serial_worker.mode_change.emit("IO")
        self.serial_worker.serial_mode_change("IO")

    def on_serial_rx_tx_hex_chk_state_changed(self, hex_mode: bool = False):
        target_widget = self.serial_rx_tx_pte
        logger.debug(f"{target_widget.objectName()}, {hex_mode}")

        try:
            target_widget.clear()
            for serial_rx_tx_item in self.serial_rx_tx_items:
                target_widget.appendPlainText(
                    str(serial_rx_tx_item)
                    if self.uiap_config.rx_tx_hex
                    else serial_rx_tx_item.decode()
                )
        except Exception as e:
            logger.error(f"{e}")

    def on_serial_tx_hex_chk_state_changed(self, hex_mode: bool = False):
        target_widget = self.serial_tx_pte
        logger.debug(f"{target_widget.objectName()}, {hex_mode}")

        try:
            text = target_widget.toPlainText()
            text_bytes = self.to_bytes(text, not hex_mode)
            text_str = self.to_str(text_bytes, hex_mode)
            target_widget.setPlainText(text_str)
        except Exception as e:
            logger.error(f"{e}")

    def on_serial_clear_btn_clicked(self):
        self.serial_rx_tx_items = []
        self.serial_rx_tx_pte.clear()

    def get_firmware_select_info(self, pred):
        info = []
        for no, (select, path, address, crypto) in enumerate(
            self.firmware_select_widgets
        ):
            if pred(select, path, address, crypto):
                info.append(
                    (
                        no,
                        select.isChecked(),
                        path.text(),
                        address.text(),
                        crypto.currentText(),
                    )
                )
        return info

    def check_firmware_select_info(self, info):
        for no, select, path, address, crypto in info:
            logger.info(f"{no}: {select, path, address, crypto}")

            if not select:
                continue

            # path 是否为可打开的文件路径
            try:
                with open(path, "rb") as f:
                    pass  # 只需尝试打开，不需要读内容
            except IOError as e:
                logger.error(f"{e}")
                self.show_msg_box(QMessageBox.Icon.Critical, str(e))
                return False

            # address 是否为合法的十六进制字符串
            try:
                int(address, 16)
            except ValueError as e:
                logger.error(f"{e}")
                self.show_msg_box(QMessageBox.Icon.Critical, str(e))
                return False
        return True

    def merge_binary_files(self, file_list, output_path, fill_byte=0xFF):
        """
        合并二进制文件到一个输出文件中，并检查重叠与填充空缺。

        :param file_list: 列表，元素为 (file_path, offset)
        :param output_path: 输出文件路径
        """
        # 1. 按照偏移地址排序
        file_list.sort(key=lambda x: x[1])

        # 2. 读取所有文件内容并记录它们的区间范围
        segments = []
        total_size = 0

        for file_path, offset in file_list:
            with open(file_path, "rb") as f:
                content = f.read()
            size = len(content)
            segment = {
                "path": file_path,
                "offset": offset,
                "size": size,
                "data": content,
                "end": offset + size,
            }
            segments.append(segment)

            total_size = max(total_size, segment["end"])

        # 3. 检查重叠区域
        for i in range(1, len(segments)):
            prev = segments[i - 1]
            curr = segments[i]
            if curr["offset"] < prev["end"]:
                msg = str(
                    f"merge overlap\n"
                    f"  {prev['path']} @ {prev['offset']}~{prev['end']}\n"
                    f"  {curr['path']} @ {curr['offset']}~{curr['end']}"
                )
                logger.warning(msg)
                self.show_msg_box(QMessageBox.Icon.Critical, msg)
                return

        # 4. 创建一个初始填充为 fill_byte 的缓冲区
        buffer = bytearray([fill_byte] * total_size)

        # 5. 写入数据到缓冲区
        for seg in segments:
            start = seg["offset"]
            end = seg["end"]
            data = seg["data"]
            buffer[start:end] = data

        # 6. 写出最终文件
        with open(output_path, "wb") as f:
            f.write(buffer)

        msg = f"merge success: {output_path}"
        logger.info(msg)
        self.show_msg_box(QMessageBox.Icon.Information, msg)

    def on_firmware_combine_btn_clicked(self):
        info = self.get_firmware_select_info(
            lambda select, path, address, crypto: select.isChecked()
        )

        if self.check_firmware_select_info(info) is False:
            return

        fill_byte = self.firmware_fill_byte_le.text()
        try:
            fill_byte_hex = int(fill_byte, 16)
            assert 0 <= fill_byte_hex <= 255, "fill_byte must in range [0, 0xFF]"
        except Exception as e:
            logger.error(f"{e}")
            self.show_msg_box(QMessageBox.Icon.Critical, str(e))
            return

        bin_list = []
        for no, select, path, address, crypto in info:
            assert select == True
            bin_list.append((path, int(address, 16)))
        self.merge_binary_files(bin_list, "./merged.bin", fill_byte_hex)

    def on_prev_ftp_send(self):
        pass

    def on_prev_ftp_send(self):
        pass

    def on_firmware_update_btn_clicked(self):
        info = self.get_firmware_select_info(
            lambda select, path, address, crypto: select.isChecked()
        )

        if self.check_firmware_select_info(info) is False:
            return

        if self.serial_open_status == False:
            msg = "please open serial first"
            logger.error(msg)
            self.show_msg_box(QMessageBox.Icon.Critical, msg)
            return

        protocol = self.firmware_transfer_protocol_cmb.currentText()
        self.serial_worker.serial_mode_change(protocol)

        for no, select, path, address, crypto in info:
            assert select == True

            file_path = Path(path)
            filename = file_path.stem
            ext = file_path.suffix

            address_int = int(address, 16)

            crypto_handler = CRYPTO_DICT.get(crypto, None)
            output_path = path
            if crypto_handler is not None:
                output_path = f"{filename}_{crypto}{ext}"
                file_crypto(
                    input_path=path,
                    output_path=output_path,
                    crypto_handler=crypto_handler,
                )
                logger.info(f"{path} -> {output_path}")

            self.serial_worker.ftp_send_file.emit(output_path)
            logger.info(f"send file emit: {output_path}")

    def on_firmware_read_btn_clicked(self):
        start_address = self.firmware_read_start_address_le.text()
        size = self.firmware_read_size_le.text()

        start_address_int = 0
        size_int = 0
        try:
            start_address_int = int(start_address, 16)
            size_int = int(size, 16)
        except ValueError as e:
            logger.error(f"{e}")
            self.show_msg_box(QMessageBox.Icon.Critical, str(e))
            return

        if self.serial_open_status == False:
            msg = "please open serial first"
            logger.error(msg)
            self.show_dialog(QMessageBox.Icon.Critical, msg)
            return

        protocol = self.firmware_transfer_protocol_cmb.currentText()
        self.serial_worker.serial_mode_change(protocol)

        # TODO: 读取固件
        # ret = self.serial_thread.serial_ftp_recv_file(".")
        # logger.info(f"firmware read result: {ret}")
        # self.serial_thread.serial_mode_change("IO")
        self.serial_worker.ftp_recv_file.emit(".")

    def show_msg_box(self, level, msg: str):
        msg_box = QMessageBox()

        msg_box.setWindowTitle("dialog")
        msg_box.setIcon(level)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)

        msg_box.exec()

    def closeEvent(self, event):
        self.serial_thread.quit()
        self.serial_thread.wait()
        super().closeEvent(event)
