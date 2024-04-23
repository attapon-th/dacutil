# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from base64 import urlsafe_b64encode, urlsafe_b64decode


def compile_key(key: bytes | str) -> bytes:
    if isinstance(key, str):
        key = key.encode("utf-8", errors="replace")
    return SHA256.new(key).digest()


def pyencrypt(plaintext: str, secret_key: str, header_str: str = "") -> str:
    data: bytes = plaintext.encode("utf-8")
    header: bytes = header_str.encode("utf-8")
    key: bytes = compile_key(secret_key)
    cipher = AES.new(key, AES.MODE_OCB)

    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ".".join([urlsafe_b64encode(x).decode("ascii") for x in (cipher.nonce, header, ciphertext, tag)])


def pydecrypt(ciphertext: str, secret_key: str) -> str:
    s: str = ""
    try:
        key: bytes = compile_key(secret_key)
        jv = [urlsafe_b64decode(x.encode("ascii")) for x in ciphertext.split(".")]
        if len(jv) != 4:
            raise ValueError
        cipher = AES.new(key, AES.MODE_OCB, nonce=jv[0])
        cipher.update(jv[1])
        plaintext: bytes = cipher.decrypt_and_verify(jv[2], jv[3])
        s = plaintext.decode("utf-8", errors="replace")
    except (ValueError, KeyError):
        print("Incorrect decryption")
    return s
