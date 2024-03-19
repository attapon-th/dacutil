from dacutil import crypt, __version__
import pytest


class TestGetConfig:
    # Retrieves configuration from a file URI with no authentication or headers
    def test_age_encrypt_and_decrypt(self):
        plaintext = b"bob can't be trusted"
        pubkey, prikey = crypt.age_genkey()
        e = crypt.age_encrypt(plaintext, pubkey)
        d: bytes = crypt.age_decrypt(e, prikey)

        # Assert
        assert isinstance(e, str)
        assert isinstance(d, bytes)
        assert d == plaintext

        print(crypt.age_decrypt(e, prikey))

    def test_b64_encrypte_and_decrypt(self):
        key = crypt.gen_key()
        plaintext = b"bob can't be trusted"
        e = crypt.encrypt_b64(plaintext, key)
        d = crypt.decrypt_b64(e, key)
        assert isinstance(e, str)
        assert isinstance(d, bytes)
        assert d == plaintext
