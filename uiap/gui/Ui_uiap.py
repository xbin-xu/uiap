# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uiap.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QTabWidget, QToolButton, QVBoxLayout, QWidget)
from . import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.NonModal)
        Form.resize(714, 592)
        icon = QIcon()
        icon.addFile(u":/icon/imgs/firmware_update.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.serial_cfg_group_box = QGroupBox(Form)
        self.serial_cfg_group_box.setObjectName(u"serial_cfg_group_box")
        self.gridLayout = QGridLayout(self.serial_cfg_group_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.serial_data_bits_cmb = QComboBox(self.serial_cfg_group_box)
        self.serial_data_bits_cmb.setObjectName(u"serial_data_bits_cmb")

        self.gridLayout.addWidget(self.serial_data_bits_cmb, 2, 1, 1, 2)

        self.serial_baud_rate_cmb = QComboBox(self.serial_cfg_group_box)
        self.serial_baud_rate_cmb.setObjectName(u"serial_baud_rate_cmb")
        self.serial_baud_rate_cmb.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.serial_baud_rate_cmb, 1, 1, 1, 2)

        self.serial_port_lb = QLabel(self.serial_cfg_group_box)
        self.serial_port_lb.setObjectName(u"serial_port_lb")

        self.gridLayout.addWidget(self.serial_port_lb, 0, 0, 1, 1)

        self.serial_stop_bits_cmb = QComboBox(self.serial_cfg_group_box)
        self.serial_stop_bits_cmb.setObjectName(u"serial_stop_bits_cmb")

        self.gridLayout.addWidget(self.serial_stop_bits_cmb, 3, 1, 1, 2)

        self.serial_parity_cmb = QComboBox(self.serial_cfg_group_box)
        self.serial_parity_cmb.setObjectName(u"serial_parity_cmb")

        self.gridLayout.addWidget(self.serial_parity_cmb, 4, 1, 1, 2)

        self.serial_baud_rate_lb = QLabel(self.serial_cfg_group_box)
        self.serial_baud_rate_lb.setObjectName(u"serial_baud_rate_lb")

        self.gridLayout.addWidget(self.serial_baud_rate_lb, 1, 0, 1, 1)

        self.serial_data_bits_lb = QLabel(self.serial_cfg_group_box)
        self.serial_data_bits_lb.setObjectName(u"serial_data_bits_lb")

        self.gridLayout.addWidget(self.serial_data_bits_lb, 2, 0, 1, 1)

        self.serial_port_cmb = QComboBox(self.serial_cfg_group_box)
        self.serial_port_cmb.setObjectName(u"serial_port_cmb")

        self.gridLayout.addWidget(self.serial_port_cmb, 0, 1, 1, 2)

        self.serial_stop_bits_lb = QLabel(self.serial_cfg_group_box)
        self.serial_stop_bits_lb.setObjectName(u"serial_stop_bits_lb")

        self.gridLayout.addWidget(self.serial_stop_bits_lb, 3, 0, 1, 1)

        self.serial_flow_ctrl_lb = QLabel(self.serial_cfg_group_box)
        self.serial_flow_ctrl_lb.setObjectName(u"serial_flow_ctrl_lb")

        self.gridLayout.addWidget(self.serial_flow_ctrl_lb, 5, 0, 1, 1)

        self.serial_parity_lb = QLabel(self.serial_cfg_group_box)
        self.serial_parity_lb.setObjectName(u"serial_parity_lb")

        self.gridLayout.addWidget(self.serial_parity_lb, 4, 0, 1, 1)

        self.serial_flow_ctrl_cmb = QComboBox(self.serial_cfg_group_box)
        self.serial_flow_ctrl_cmb.setObjectName(u"serial_flow_ctrl_cmb")

        self.gridLayout.addWidget(self.serial_flow_ctrl_cmb, 5, 1, 1, 2)

        self.serial_rts_chk = QCheckBox(self.serial_cfg_group_box)
        self.serial_rts_chk.setObjectName(u"serial_rts_chk")

        self.gridLayout.addWidget(self.serial_rts_chk, 6, 0, 1, 1)

        self.serial_open_btn = QPushButton(self.serial_cfg_group_box)
        self.serial_open_btn.setObjectName(u"serial_open_btn")

        self.gridLayout.addWidget(self.serial_open_btn, 8, 0, 1, 3)

        self.serial_dtr_chk = QCheckBox(self.serial_cfg_group_box)
        self.serial_dtr_chk.setObjectName(u"serial_dtr_chk")

        self.gridLayout.addWidget(self.serial_dtr_chk, 6, 1, 1, 1)


        self.horizontalLayout_9.addWidget(self.serial_cfg_group_box)

        self.firmware_cfg_group_box = QGroupBox(Form)
        self.firmware_cfg_group_box.setObjectName(u"firmware_cfg_group_box")
        self.gridLayout_3 = QGridLayout(self.firmware_cfg_group_box)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.firmware_selected_chk_2 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_2.setObjectName(u"firmware_selected_chk_2")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_2, 3, 0, 1, 1)

        self.firmware_crypto_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_crypto_lb.setObjectName(u"firmware_crypto_lb")

        self.gridLayout_2.addWidget(self.firmware_crypto_lb, 0, 5, 1, 1)

        self.firmware_selected_chk_5 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_5.setObjectName(u"firmware_selected_chk_5")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_5, 6, 0, 1, 1)

        self.firmware_crypto_cmb_2 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_2.setObjectName(u"firmware_crypto_cmb_2")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_2, 3, 5, 1, 1)

        self.firmware_open_file_tb_7 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_7.setObjectName(u"firmware_open_file_tb_7")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_7, 9, 3, 1, 1)

        self.firmware_address_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_address_lb.setObjectName(u"firmware_address_lb")

        self.gridLayout_2.addWidget(self.firmware_address_lb, 0, 4, 1, 1)

        self.firmware_path_le_3 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_3.setObjectName(u"firmware_path_le_3")

        self.gridLayout_2.addWidget(self.firmware_path_le_3, 4, 1, 1, 2)

        self.firmware_address_le_6 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_6.setObjectName(u"firmware_address_le_6")

        self.gridLayout_2.addWidget(self.firmware_address_le_6, 7, 4, 1, 1)

        self.firmware_crypto_cmb_1 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_1.setObjectName(u"firmware_crypto_cmb_1")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_1, 2, 5, 1, 1)

        self.firmware_open_file_tb_5 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_5.setObjectName(u"firmware_open_file_tb_5")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_5, 6, 3, 1, 1)

        self.firmware_crypto_cmb_4 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_4.setObjectName(u"firmware_crypto_cmb_4")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_4, 5, 5, 1, 1)

        self.firmware_address_le_4 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_4.setObjectName(u"firmware_address_le_4")

        self.gridLayout_2.addWidget(self.firmware_address_le_4, 5, 4, 1, 1)

        self.firmware_address_le_7 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_7.setObjectName(u"firmware_address_le_7")

        self.gridLayout_2.addWidget(self.firmware_address_le_7, 9, 4, 1, 1)

        self.firmware_crypto_cmb_6 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_6.setObjectName(u"firmware_crypto_cmb_6")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_6, 9, 5, 1, 1)

        self.firmware_open_file_tb_4 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_4.setObjectName(u"firmware_open_file_tb_4")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_4, 5, 3, 1, 1)

        self.firmware_path_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_path_lb.setObjectName(u"firmware_path_lb")

        self.gridLayout_2.addWidget(self.firmware_path_lb, 0, 1, 1, 3)

        self.firmware_selected_chk_1 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_1.setObjectName(u"firmware_selected_chk_1")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_1, 2, 0, 1, 1)

        self.firmware_address_le_5 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_5.setObjectName(u"firmware_address_le_5")

        self.gridLayout_2.addWidget(self.firmware_address_le_5, 6, 4, 1, 1)

        self.firmware_selected_chk_0 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_0.setObjectName(u"firmware_selected_chk_0")
        self.firmware_selected_chk_0.setChecked(False)

        self.gridLayout_2.addWidget(self.firmware_selected_chk_0, 1, 0, 1, 1)

        self.firmware_crypto_cmb_7 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_7.setObjectName(u"firmware_crypto_cmb_7")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_7, 7, 5, 1, 1)

        self.firmware_open_file_tb_3 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_3.setObjectName(u"firmware_open_file_tb_3")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_3, 4, 3, 1, 1)

        self.firmware_path_le_5 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_5.setObjectName(u"firmware_path_le_5")

        self.gridLayout_2.addWidget(self.firmware_path_le_5, 6, 1, 1, 2)

        self.firmware_crypto_cmb_5 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_5.setObjectName(u"firmware_crypto_cmb_5")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_5, 6, 5, 1, 1)

        self.firmware_selected_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_selected_lb.setObjectName(u"firmware_selected_lb")

        self.gridLayout_2.addWidget(self.firmware_selected_lb, 0, 0, 1, 1)

        self.firmware_selected_chk_6 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_6.setObjectName(u"firmware_selected_chk_6")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_6, 7, 0, 1, 1)

        self.firmware_path_le_0 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_0.setObjectName(u"firmware_path_le_0")
        self.firmware_path_le_0.setMinimumSize(QSize(150, 0))

        self.gridLayout_2.addWidget(self.firmware_path_le_0, 1, 1, 1, 2)

        self.firmware_address_le_3 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_3.setObjectName(u"firmware_address_le_3")

        self.gridLayout_2.addWidget(self.firmware_address_le_3, 4, 4, 1, 1)

        self.firmware_crypto_cmb_3 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_3.setObjectName(u"firmware_crypto_cmb_3")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_3, 4, 5, 1, 1)

        self.firmware_open_file_tb_0 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_0.setObjectName(u"firmware_open_file_tb_0")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_0, 1, 3, 1, 1)

        self.firmware_address_le_2 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_2.setObjectName(u"firmware_address_le_2")

        self.gridLayout_2.addWidget(self.firmware_address_le_2, 3, 4, 1, 1)

        self.firmware_selected_chk_7 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_7.setObjectName(u"firmware_selected_chk_7")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_7, 9, 0, 1, 1)

        self.firmware_address_le_0 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_0.setObjectName(u"firmware_address_le_0")
        self.firmware_address_le_0.setMinimumSize(QSize(75, 0))

        self.gridLayout_2.addWidget(self.firmware_address_le_0, 1, 4, 1, 1)

        self.firmware_crypto_cmb_0 = QComboBox(self.firmware_cfg_group_box)
        self.firmware_crypto_cmb_0.setObjectName(u"firmware_crypto_cmb_0")

        self.gridLayout_2.addWidget(self.firmware_crypto_cmb_0, 1, 5, 1, 1)

        self.firmware_address_le_1 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_address_le_1.setObjectName(u"firmware_address_le_1")

        self.gridLayout_2.addWidget(self.firmware_address_le_1, 2, 4, 1, 1)

        self.firmware_selected_chk_3 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_3.setObjectName(u"firmware_selected_chk_3")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_3, 4, 0, 1, 1)

        self.firmware_open_file_tb_2 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_2.setObjectName(u"firmware_open_file_tb_2")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_2, 3, 3, 1, 1)

        self.firmware_path_le_2 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_2.setObjectName(u"firmware_path_le_2")

        self.gridLayout_2.addWidget(self.firmware_path_le_2, 3, 1, 1, 2)

        self.firmware_selected_chk_4 = QCheckBox(self.firmware_cfg_group_box)
        self.firmware_selected_chk_4.setObjectName(u"firmware_selected_chk_4")

        self.gridLayout_2.addWidget(self.firmware_selected_chk_4, 5, 0, 1, 1)

        self.firmware_path_le_4 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_4.setObjectName(u"firmware_path_le_4")

        self.gridLayout_2.addWidget(self.firmware_path_le_4, 5, 1, 1, 2)

        self.firmware_path_le_6 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_6.setObjectName(u"firmware_path_le_6")

        self.gridLayout_2.addWidget(self.firmware_path_le_6, 7, 1, 1, 2)

        self.firmware_open_file_tb_1 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_1.setObjectName(u"firmware_open_file_tb_1")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_1, 2, 3, 1, 1)

        self.firmware_open_file_tb_6 = QToolButton(self.firmware_cfg_group_box)
        self.firmware_open_file_tb_6.setObjectName(u"firmware_open_file_tb_6")

        self.gridLayout_2.addWidget(self.firmware_open_file_tb_6, 7, 3, 1, 1)

        self.firmware_path_le_7 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_7.setObjectName(u"firmware_path_le_7")

        self.gridLayout_2.addWidget(self.firmware_path_le_7, 9, 1, 1, 2)

        self.firmware_path_le_1 = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_path_le_1.setObjectName(u"firmware_path_le_1")

        self.gridLayout_2.addWidget(self.firmware_path_le_1, 2, 1, 1, 2)

        self.gridLayout_2.setColumnStretch(1, 9)
        self.gridLayout_2.setColumnStretch(4, 1)

        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.firmware_read_btn = QPushButton(self.firmware_cfg_group_box)
        self.firmware_read_btn.setObjectName(u"firmware_read_btn")

        self.gridLayout_4.addWidget(self.firmware_read_btn, 6, 0, 1, 3)

        self.firmware_read_size_le = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_read_size_le.setObjectName(u"firmware_read_size_le")

        self.gridLayout_4.addWidget(self.firmware_read_size_le, 5, 2, 1, 1)

        self.firmware_transfer_protocol_cmb = QComboBox(self.firmware_cfg_group_box)
        self.firmware_transfer_protocol_cmb.setObjectName(u"firmware_transfer_protocol_cmb")

        self.gridLayout_4.addWidget(self.firmware_transfer_protocol_cmb, 2, 2, 1, 1)

        self.firmware_update_btn = QPushButton(self.firmware_cfg_group_box)
        self.firmware_update_btn.setObjectName(u"firmware_update_btn")

        self.gridLayout_4.addWidget(self.firmware_update_btn, 3, 0, 1, 3)

        self.firmware_read_start_address_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_read_start_address_lb.setObjectName(u"firmware_read_start_address_lb")

        self.gridLayout_4.addWidget(self.firmware_read_start_address_lb, 4, 0, 1, 2)

        self.firmware_read_start_address_le = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_read_start_address_le.setObjectName(u"firmware_read_start_address_le")
        self.firmware_read_start_address_le.setMinimumSize(QSize(75, 0))

        self.gridLayout_4.addWidget(self.firmware_read_start_address_le, 4, 2, 1, 1)

        self.firmware_read_size_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_read_size_lb.setObjectName(u"firmware_read_size_lb")

        self.gridLayout_4.addWidget(self.firmware_read_size_lb, 5, 0, 1, 2)

        self.firmware_combine_btn = QPushButton(self.firmware_cfg_group_box)
        self.firmware_combine_btn.setObjectName(u"firmware_combine_btn")

        self.gridLayout_4.addWidget(self.firmware_combine_btn, 1, 0, 1, 3)

        self.firmware_fill_byte_le = QLineEdit(self.firmware_cfg_group_box)
        self.firmware_fill_byte_le.setObjectName(u"firmware_fill_byte_le")

        self.gridLayout_4.addWidget(self.firmware_fill_byte_le, 0, 2, 1, 1)

        self.firmware_transfer_protocol_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_transfer_protocol_lb.setObjectName(u"firmware_transfer_protocol_lb")
        self.firmware_transfer_protocol_lb.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout_4.addWidget(self.firmware_transfer_protocol_lb, 2, 0, 1, 2)

        self.firmware_fill_byte_lb = QLabel(self.firmware_cfg_group_box)
        self.firmware_fill_byte_lb.setObjectName(u"firmware_fill_byte_lb")

        self.gridLayout_4.addWidget(self.firmware_fill_byte_lb, 0, 0, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 2, 1, 1)

        self.line = QFrame(self.firmware_cfg_group_box)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line, 0, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 9)
        self.gridLayout_3.setColumnStretch(2, 1)

        self.horizontalLayout_9.addWidget(self.firmware_cfg_group_box)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.serial_tab = QWidget()
        self.serial_tab.setObjectName(u"serial_tab")
        self.verticalLayout_3 = QVBoxLayout(self.serial_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.serial_rx_tx_pte = QPlainTextEdit(self.serial_tab)
        self.serial_rx_tx_pte.setObjectName(u"serial_rx_tx_pte")
        self.serial_rx_tx_pte.setMinimumSize(QSize(0, 0))
        self.serial_rx_tx_pte.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.serial_rx_tx_pte)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serial_tx_pte = QPlainTextEdit(self.serial_tab)
        self.serial_tx_pte.setObjectName(u"serial_tx_pte")

        self.horizontalLayout.addWidget(self.serial_tx_pte)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.serial_rx_tx_hex_chk = QCheckBox(self.serial_tab)
        self.serial_rx_tx_hex_chk.setObjectName(u"serial_rx_tx_hex_chk")

        self.verticalLayout.addWidget(self.serial_rx_tx_hex_chk)

        self.serial_tx_hex_chk = QCheckBox(self.serial_tab)
        self.serial_tx_hex_chk.setObjectName(u"serial_tx_hex_chk")

        self.verticalLayout.addWidget(self.serial_tx_hex_chk)

        self.serial_clear_btn = QPushButton(self.serial_tab)
        self.serial_clear_btn.setObjectName(u"serial_clear_btn")

        self.verticalLayout.addWidget(self.serial_clear_btn)

        self.serial_send_btn = QPushButton(self.serial_tab)
        self.serial_send_btn.setObjectName(u"serial_send_btn")

        self.verticalLayout.addWidget(self.serial_send_btn)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_3.setStretch(0, 9)
        self.verticalLayout_3.setStretch(1, 1)
        self.tabWidget.addTab(self.serial_tab, "")
        self.log_tab = QWidget()
        self.log_tab.setObjectName(u"log_tab")
        self.gridLayout_5 = QGridLayout(self.log_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.log_pte = QPlainTextEdit(self.log_tab)
        self.log_pte.setObjectName(u"log_pte")
        self.log_pte.setMinimumSize(QSize(0, 250))
        self.log_pte.setReadOnly(True)

        self.gridLayout_5.addWidget(self.log_pte, 0, 0, 1, 1)

        self.tabWidget.addTab(self.log_tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"UIAP", None))
        self.serial_cfg_group_box.setTitle(QCoreApplication.translate("Form", u"\u4e32\u53e3\u914d\u7f6e", None))
        self.serial_port_lb.setText(QCoreApplication.translate("Form", u"\u7aef\u53e3\u53f7", None))
        self.serial_baud_rate_lb.setText(QCoreApplication.translate("Form", u"\u6ce2\u7279\u7387", None))
        self.serial_data_bits_lb.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u4f4d", None))
        self.serial_stop_bits_lb.setText(QCoreApplication.translate("Form", u"\u505c\u6b62\u4f4d", None))
        self.serial_flow_ctrl_lb.setText(QCoreApplication.translate("Form", u"\u6d41\u63a7\u5236", None))
        self.serial_parity_lb.setText(QCoreApplication.translate("Form", u"\u6821\u9a8c\u4f4d", None))
        self.serial_rts_chk.setText(QCoreApplication.translate("Form", u"RTS", None))
        self.serial_open_btn.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u4e32\u53e3", None))
        self.serial_dtr_chk.setText(QCoreApplication.translate("Form", u"DTR", None))
        self.firmware_cfg_group_box.setTitle(QCoreApplication.translate("Form", u"\u56fa\u4ef6\u914d\u7f6e", None))
        self.firmware_selected_chk_2.setText(QCoreApplication.translate("Form", u"#2", None))
        self.firmware_crypto_lb.setText(QCoreApplication.translate("Form", u"\u52a0\u5bc6\u7b97\u6cd5", None))
        self.firmware_selected_chk_5.setText(QCoreApplication.translate("Form", u"#5", None))
        self.firmware_open_file_tb_7.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_address_lb.setText(QCoreApplication.translate("Form", u"\u5730\u5740", None))
        self.firmware_open_file_tb_5.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_open_file_tb_4.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_path_lb.setText(QCoreApplication.translate("Form", u"\u8def\u5f84", None))
        self.firmware_selected_chk_1.setText(QCoreApplication.translate("Form", u"#1", None))
        self.firmware_selected_chk_0.setText(QCoreApplication.translate("Form", u"#0", None))
        self.firmware_open_file_tb_3.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_selected_lb.setText(QCoreApplication.translate("Form", u"NO.", None))
        self.firmware_selected_chk_6.setText(QCoreApplication.translate("Form", u"#6", None))
        self.firmware_open_file_tb_0.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_selected_chk_7.setText(QCoreApplication.translate("Form", u"#7", None))
        self.firmware_address_le_0.setText("")
        self.firmware_selected_chk_3.setText(QCoreApplication.translate("Form", u"#3", None))
        self.firmware_open_file_tb_2.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_selected_chk_4.setText(QCoreApplication.translate("Form", u"#4", None))
        self.firmware_open_file_tb_1.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_open_file_tb_6.setText(QCoreApplication.translate("Form", u"...", None))
        self.firmware_read_btn.setText(QCoreApplication.translate("Form", u"\u56fa\u4ef6\u8bfb\u53d6", None))
        self.firmware_update_btn.setText(QCoreApplication.translate("Form", u"\u56fa\u4ef6\u5347\u7ea7", None))
        self.firmware_read_start_address_lb.setText(QCoreApplication.translate("Form", u"\u8d77\u59cb\u5730\u5740", None))
        self.firmware_read_start_address_le.setText("")
        self.firmware_read_size_lb.setText(QCoreApplication.translate("Form", u"\u5927\u5c0f", None))
        self.firmware_combine_btn.setText(QCoreApplication.translate("Form", u"\u56fa\u4ef6\u5408\u5e76", None))
        self.firmware_fill_byte_le.setText("")
        self.firmware_transfer_protocol_lb.setText(QCoreApplication.translate("Form", u"\u4f20\u8f93\u534f\u8bae", None))
        self.firmware_fill_byte_lb.setText(QCoreApplication.translate("Form", u"\u56fa\u4ef6\u586b\u5145", None))
        self.serial_rx_tx_hex_chk.setText(QCoreApplication.translate("Form", u"HEX \u663e\u793a", None))
        self.serial_tx_hex_chk.setText(QCoreApplication.translate("Form", u"HEX \u53d1\u9001", None))
        self.serial_clear_btn.setText(QCoreApplication.translate("Form", u"\u6e05\u7a7a", None))
        self.serial_send_btn.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.serial_tab), QCoreApplication.translate("Form", u"\u4e32\u53e3", None))
#if QT_CONFIG(accessibility)
        self.log_tab.setAccessibleName(QCoreApplication.translate("Form", u"a", None))
#endif // QT_CONFIG(accessibility)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.log_tab), QCoreApplication.translate("Form", u"\u65e5\u5fd7", None))
    # retranslateUi

