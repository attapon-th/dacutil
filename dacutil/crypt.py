from cryptography.fernet import Fernet
from base64 import b64encode, b64decode


def gen_key() -> bytes:
    """
    Generate a key and return it as bytes.
    """
    return Fernet.generate_key()


def encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypts the given data using the provided key and returns the encrypted text.

    Args:
        data (bytes): The data to be encrypted.
        key (bytes): The key used for encryption.

    Returns:
        bytes: The encrypted text.
    """
    cipher_suite = Fernet(key)
    encoded_text = cipher_suite.encrypt(data)
    return encoded_text


def decrypt(encoded_text: bytes | str, key: bytes | str) -> bytes | None:
    """
    Decrypts the encoded text using the provided key.

    Args:
        encoded_text (bytes | str): The text to be decrypted.
        key (bytes | str): The key to be used for decryption.

    Returns:
        bytes | None: The decrypted text if successful, None if an exception occurs.
    """
    cipher_suite = Fernet(key)
    if isinstance(encoded_text, str):
        encoded_text = encoded_text.encode()
    try:
        return cipher_suite.decrypt(encoded_text)
    except Exception:
        return None


def encrypt_b64(data: str | bytes, key: bytes, wrap: int | None = None) -> str:
    """
    Encrypts the input data using the provided key and returns the result as a base64 encoded string.

    Args:
        data (str | bytes): The data to be encrypted, either as a string or bytes.
        key (bytes): The key used for encryption.
        wrap (int | None, optional): wrap encoded lines after COLS character if None is no wrapping. Defaults to None.

    Returns:
        str: The base64 encoded encrypted data.
    """
    if isinstance(data, str):
        data = data.encode()
    return b64encode(encrypt(data, key)).decode()


def decrypt_b64(encoded_text: str | bytes, key: bytes) -> str | None:
    """
    Decrypts a base64 encoded text using a given key.

    Args:
        encoded_text (str | bytes): The base64 encoded text to be decrypted.
        key (bytes): The key used for decryption.

    Returns:
        str | None: The decrypted text, or None if decryption fails.
    """
    if isinstance(encoded_text, str):
        encoded_text = encoded_text.encode()

    try:
        encoded_text = bytes(encoded_text)
        encoded_text = encoded_text.replace(b"\r\n", b"").replace(b"\n", b"")
        b: bytes | None = decrypt(b64decode(encoded_text), key)
        if b is None:
            return None
        return b.decode()
    except Exception:
        return None
