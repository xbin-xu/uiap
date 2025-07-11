import os
import logging
from logging.handlers import RotatingFileHandler


# 定义 ANSI 颜色代码
class LogColors:
    DEBUG = "\033[94m"  # 蓝色
    INFO = "\033[92m"  # 绿色
    WARNING = "\033[93m"  # 黄色
    ERROR = "\033[91m"  # 红色
    CRITICAL = "\033[41m"  # 红底白字
    RESET = "\033[0m"  # 重置颜色


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: LogColors.DEBUG,
        logging.INFO: LogColors.INFO,
        logging.WARNING: LogColors.WARNING,
        logging.ERROR: LogColors.ERROR,
        logging.CRITICAL: LogColors.CRITICAL,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, LogColors.RESET)
        self._style._fmt = f"{color}[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s{LogColors.RESET}"
        return super().format(record)


def setup_logging(log_level=logging.INFO, log_file="logs/app.log"):
    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 创建 logger 并设置级别
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # 移除已有的 handlers（防止重复添加）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 日志格式（用于文件和控制台）
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台处理器（带颜色）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    # 文件处理器（带滚动）
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
