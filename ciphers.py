from base64 import b64encode, b64decode
from Crypto.Cipher import DES, AES, DES3
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
from typing import Tuple


class MessageCipher():
    def __init__(self, cipher_type: str):
        if cipher_type == 'AES':
            self.type = AES
        elif cipher_type == 'DES':
            self.type = DES
        elif cipher_type == 'DES3':
            self.type = DES3
        else:
            print("Error creating cipher type is unidentified.")
            return

        self.initialization_vector: bytes = ('12345678' * (self.type.block_size//8)).encode('utf-8')

    def createKey(self):
        key_size = self.type.key_size if type(self.type.key_size) is not tuple else self.type.key_size[0]
        self.key = Random.new().read(key_size)
        print(f'Key was created using {self.type.__name__}')

    def importKey(self, filename: str):
        with open(filename, 'r') as f:
            self.key = b64decode(f.read().encode('utf-8'))
            print(f'Key was imported using {self.type.__name__}')

    def exportKey(self, filename: str):
        if self.key == None:
            print("Please create or import a key.")
            return ""

        with open(filename, 'w') as f:
            str_key = b64encode(self.key).decode('utf-8')
            f.write(str_key)
            print(f'Key has been exported to {filename}')

    def encrypt(self, text: str) -> str:
        if self.key == None:
            print("Please create or import a key.")
            return ""

        self.cipher = self.type.new(self.key, self.type.MODE_CBC, self.initialization_vector)

        encrypted_text =  self.cipher.encrypt(pad(text.encode('utf-8'), self.type.block_size))
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, text: str) -> str:
        if self.key == None:
            print("Please create or import a key.")
            return ""

        self.cipher = self.type.new(self.key, self.type.MODE_CBC, self.initialization_vector)

        decrypted_text =  unpad(self.cipher.decrypt(b64decode(text.encode('utf-8'))), self.type.block_size)
        return decrypted_text.decode('utf-8')
