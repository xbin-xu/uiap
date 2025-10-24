from dataclasses import dataclass
from datetime import datetime


def now_str():
    """返回当前时间戳字符串，格式为 HH:MM:SS.sss"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]  # 取前3位毫秒


@dataclass
class SerialRxTxItem:
    timestamp: str = ""
    rx_tx: bool = False
    data: bytes = b""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = now_str()

    def __str__(self):
        return f"[{self.timestamp}] {'TX<-' if self.rx_tx else 'RX->'} {self.data}"

    def decode(self, encoding="utf-8"):
        return f"[{self.timestamp}] {'TX<-' if self.rx_tx else 'RX->'} {self.data.decode(encoding, errors='replace')}"

    @classmethod
    def rx(cls, data: bytes, timestamp: str = ""):
        return cls(timestamp=timestamp, rx_tx=False, data=data)

    @classmethod
    def tx(cls, data: bytes, timestamp: str = ""):
        return cls(timestamp=timestamp, rx_tx=True, data=data)
