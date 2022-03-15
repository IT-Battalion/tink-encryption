import sys

import tink
from tink import aead, cleartext_keyset_handle

KEYSET= ".key.pem"


def generate_key(path: str):
    key_template = aead.aead_key_templates.AES128_GCM
    keyset_handle = tink.KeysetHandle.generate_new(key_template)

    with open(path, 'wt') as keyset_file:
        cleartext_keyset_handle.write(
            tink.JsonKeysetWriter(keyset_file), keyset_handle)
    return keyset_handle


def encrypt(data: bytes, keyset_file: str):
    keyset_handle = generate_key(keyset_file)

    cipher = keyset_handle.primitive(aead.Aead)

    return cipher.encrypt(data, b'')


def decrypt(data: bytes, keyset_file: str):
    with open(keyset_file, 'rt') as keyset_file:
      text = keyset_file.read()
      keyset_handle = cleartext_keyset_handle.read(tink.JsonKeysetReader(text))

    cipher = keyset_handle.primitive(aead.Aead)

    return cipher.decrypt(data, b'')


def main():
    aead.register()

    if len(sys.argv) <= 2:
        raise Exception('not enough arguments')

    mode = sys.argv[1].lower()
    data = sys.argv[2]

    if mode in ('encrypt', 'enc'):
        print(encrypt(data.encode(), KEYSET).hex())
    elif mode in ('decrypt', 'dec'):
        print(decrypt(bytes.fromhex(data), KEYSET).decode())
    else:
        raise Exception('invalid mode')


if __name__ == '__main__':
    main()
