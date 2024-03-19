from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
import pyrage as age
from typing import Tuple
import textwrap


def gen_key() -> str:
    """
    Function that generates a key and returns it as a decoded string.
    """
    return Fernet.generate_key().decode()


def encrypt(data: bytes | str, key: str) -> bytes:
    """
    Encrypts the given data using the provided key.

    Args:
        data (bytes | str): The data to be encrypted.
        key (str): The key used for encryption.

    Returns:
        bytes: The encrypted data.
    """
    if not isinstance(key, str):
        key = str(key)
    return age.passphrase.encrypt(data, key)  # type: ignore


def decrypt(encrypted: bytes | str, key: str) -> bytes:
    """
    Decrypts the given encrypted data using the provided key.

    Args:
        encrypted (bytes | str): The data to decrypt.
        key (str): The key to use for decryption.

    Returns:
        bytes: The decrypted data
    """
    if not isinstance(key, str):
        key = str(key)
    if isinstance(encrypted, str):
        encrypted = encrypted.encode()
    return bytes(age.passphrase.decrypt(encrypted, key))  # type: ignore


def encrypt_b64(data: str | bytes, key: str, wrap_width: int = 70) -> str:
    """
    Encrypts the input data using the provided key.
    If the wrap_width is less than 1, the encrypted data is returned
    as a base64 encoded string. Otherwise, the encrypted data is wrapped
    at the specified wrap_width before being returned.

    Args:
        data (str | bytes): The data to be encrypted, either a string or bytes.
        key (str): The key used for encryption.
        wrap_width (int, optional): The width at which to wrap the encrypted data (default is 70).

    Returns:
        str: The encrypted data as a base64 encoded string or wrapped at the specified width.
    """
    if isinstance(data, str):
        data = data.encode()
    encrypted: bytes = encrypt(data, key)
    if wrap_width < 1:
        return b64encode(encrypted).decode("utf-8")
    else:
        b: bytes = b64encode(encrypted)
        return "\n".join(textwrap.wrap(b.decode("utf-8"), wrap_width))
    return


def decrypt_b64(encoded_text: str | bytes, key: str) -> bytes:
    """
    Decrypts a base64 encoded text using the provided key.

    Args:
        encoded_text (str | bytes): The base64 encoded text to be decrypted.
        key (str): The key used for decryption.

    Returns:
        bytes : The decrypted text if successful, None if decryption fails.
    """
    if isinstance(encoded_text, str):
        encoded_text = encoded_text.encode()

    encoded_text = bytes(encoded_text)
    encoded_text = encoded_text.replace(b"\r\n", b"").replace(b"\n", b"")
    b: bytes = decrypt(b64decode(encoded_text), key)
    return b


def age_genkey() -> Tuple[str, str]:
    """
    Function to generate a key pair using x25519 algorithm.

    Returns:
        Tuple[str, str]: Tuple containing the public and private keys.
    """
    ident = age.x25519.Identity.generate()  # type: ignore
    return str(ident.to_public()), str(ident)


def age_encrypt(plaintext: bytes | str, public_key: str, wrap_width: int = 70) -> str:
    """
    Encrypts data using a public key with optional text wrapping.

    Args:
        plaintext (bytes | str): The data to be encrypted, either as bytes or a string.
        public_key (str): The public key used for encryption.
        wrap_width (int, optional): The width at which the encrypted data should be wrapped. Defaults to 70.

    Returns:
        bytes: The encrypted data.
    """
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    recipient = age.x25519.Recipient.from_str(public_key)  # type: ignore
    encrypted: bytes = age.encrypt(plaintext, [recipient])  # type: ignore
    if wrap_width < 1:
        return b64encode(encrypted).decode("utf-8")
    else:
        b: bytes = b64encode(encrypted)
        return "\n".join(textwrap.wrap(b.decode("utf-8"), wrap_width))


def age_decrypt(text_encrypt: bytes | str, private_key: str) -> bytes:
    """
    Decrypts the given encrypted text using the provided private key.

    Args:
        text_encrypt (bytes | str): The encrypted text to be decrypted. It can be either a bytes object or a string.
        private_key (str): The private key used for decryption.

    Returns:
        bytes: The decrypted text as a bytes object.

    Raises:
        None
    """
    if isinstance(text_encrypt, str):
        text_encrypt = text_encrypt.encode(errors="ignore")
    if not isinstance(text_encrypt, bytes):
        text_encrypt = bytes(text_encrypt)
    encrypted: bytes = text_encrypt.replace(b"\r\n", b"").replace(b"\n", b"")
    ident = age.x25519.Identity.from_str(private_key)  # type: ignore
    return age.decrypt(b64decode(encrypted), [ident])  # type: ignore
