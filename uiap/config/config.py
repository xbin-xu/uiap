import os
import json
from dataclasses import asdict, dataclass, field
import logging
import serial.tools.list_ports
from core.crypto import CRYPTO_KEYS

logger = logging.getLogger()

CONFIG_FILE = "./.uiap/settings.json"
SERIAL_PORT_ITEMS = (port.device for port in serial.tools.list_ports.comports())
SERIAL_BAUD_RATE_ITEMS = ("9600", "19200", "38400", "57600", "115200")
SERIAL_DATA_BITS_ITEMS = ("5", "6", "7", "8")
SERIAL_STOP_BITS_ITEMS = ("1", "1.5", "2")
SERIAL_PARITY_ITEMS = ("None", "Even", "Odd", "Mark", "Space")
SERIAL_FLOW_CTRL_ITEMS = ("None", "Hardware", "Software")
FIRMWARE_CRYPTO_ITEMS = CRYPTO_KEYS
FIRMWARE_TRANSFER_PROTOCOL_ITEMS = ("Ymodem",)

COMBO_BOX_ITEMS = {
    "serial_port_cmb": SERIAL_PORT_ITEMS,
    "serial_baud_rate_cmb": SERIAL_BAUD_RATE_ITEMS,
    "serial_data_bits_cmb": SERIAL_DATA_BITS_ITEMS,
    "serial_stop_bits_cmb": SERIAL_STOP_BITS_ITEMS,
    "serial_parity_cmb": SERIAL_PARITY_ITEMS,
    "serial_flow_ctrl_cmb": SERIAL_FLOW_CTRL_ITEMS,
    "firmware_transfer_protocol_cmb": FIRMWARE_TRANSFER_PROTOCOL_ITEMS,
    "firmware_crypto_cmb": FIRMWARE_CRYPTO_ITEMS,
}


@dataclass
class FirmwareSelectItem:
    selected: bool = False
    path: str = ""
    address: str = ""
    crypto: str = "None"


@dataclass
class UiapConfig:
    port: str = ""
    baud_rate: str = "115200"
    data_bits: str = "8"
    stop_bits: str = "1"
    parity: str = "None"
    flow_ctrl: str = "None"
    rts: bool = False
    dtr: bool = False

    rx_tx_hex: bool = False
    tx_hex: bool = False

    fill_byte: str = ""
    transfer_protocol: str = "Raw"
    read_start_address: str = ""
    read_size: str = ""

    select_items: list[FirmwareSelectItem] = field(default_factory=list)

    def __post_init__(self):
        if not self.select_items:
            self.select_items = [FirmwareSelectItem() for _ in range(8)]

    @classmethod
    def from_dict(cls, data):
        # 将字典转换为 UiapConfig 实例，并处理嵌套的 FirmwareSelectItem
        select_items = [
            FirmwareSelectItem(**item) for item in data.pop("select_items", [])
        ]
        return cls(select_items=select_items, **data)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_json_file(cls, file_path):
        if not os.path.exists(file_path):
            logger.warning(f"can not find {file_path}, creating default config...")
            default_config = UiapConfig()
            default_config.to_json_file(file_path)
            return default_config

        logger.debug("loading config...")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return UiapConfig.from_dict(data)

    def to_json_file(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    uiap_config = UiapConfig.from_json_file(CONFIG_FILE)
