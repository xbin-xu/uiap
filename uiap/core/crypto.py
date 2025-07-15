from typing import Callable
import logging


logger = logging.getLogger(__name__)


def file_crypto(
    input_path: str, output_path: str, crypto_handler: Callable[[bytes], bytes]
):
    try:
        with open(input_path, "rb") as f:
            content = f.read()

        processed = crypto_handler(content)

        with open(output_path, "wb") as f:
            f.write(processed)
    except Exception as e:
        logger.error(f"{e}")


def byte_transform(fn):
    return lambda data: bytes([fn(b) for b in data])


def header_encrypt(header):
    if isinstance(header, str):
        header = header.encode("utf-8")
    assert isinstance(header, bytes)
    return lambda data: header + data


def header_decrypt(header):
    if isinstance(header, bytes):
        header = header.decode("utf-8")
    assert isinstance(header, str)
    return lambda data: data[len(header) :]


def footer_encrypt(footer):
    if isinstance(footer, str):
        footer = footer.encode("utf-8")
    assert isinstance(footer, bytes)
    return lambda data: data + footer


def footer_decrypt(footer):
    if isinstance(footer, bytes):
        footer = footer.decode("utf-8")
    assert isinstance(footer, str)
    footer_length = len(footer)
    return lambda data: data[:-footer_length] if footer_length > 0 else data


def add_n_encrypt(n: int):
    assert 0 < n and n < 256
    return byte_transform(lambda b: (b + n) % 256)


def add_n_decrypt(n: int):
    assert 0 < n and n < 256
    return byte_transform(lambda b: (b - n) % 256)


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend


def aes_128_ecb_encrypt(key: bytes):
    def encrypt(data: bytes) -> bytes:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()

        padder = PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        return encryptor.update(padded_data) + encryptor.finalize()

    return encrypt


def aes_128_ecb_decrypt(key: bytes):
    def decrypt(data: bytes) -> bytes:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(data) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypt


CRYPTO_DICT = {
    "None": None,
    "header_encrypt": header_encrypt("add_header"),
    "header_decrypt": header_decrypt("add_header"),
    "footer_encrypt": footer_encrypt("add_footer"),
    "footer_decrypt": footer_decrypt("add_footer"),
    "add_n_encrypt": add_n_encrypt(1),
    "add_n_decrypt": add_n_decrypt(1),
    "aes_128_ecb_encrypt": aes_128_ecb_encrypt(b"1111111111111111"),
    "aes_128_ecb_decrypt": aes_128_ecb_decrypt(b"1111111111111111"),
}

CRYPTO_KEYS = CRYPTO_DICT.keys()
