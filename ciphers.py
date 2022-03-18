from base64 import b64encode, b64decode
from Crypto.Cipher import DES, AES, DES3
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
from typing import Tuple


class MessageCipher():
    """A Cipher that enabled encrypting messages.

    Allows AES, DES, 3DES methods.

    Args:
        cipher_type (str): Choose between AES, DES or DES3

    """
    def __init__(self, cipher_type: str):
        # Choose the cipher type
        if cipher_type == 'AES':
            self.type = AES
        elif cipher_type == 'DES':
            self.type = DES
        elif cipher_type == 'DES3':
            self.type = DES3
        else:
            print("Error creating cipher type is unidentified.")
            return

        # Begin an initialization vector 
        self.initialization_vector: bytes = ('12345678' * (self.type.block_size//8)).encode('utf-8')

    def createKey(self):
        """Create a key, saved in the cipher state.

        """
        key_size = self.type.key_size if type(self.type.key_size) is not tuple else self.type.key_size[0]
        self.key = Random.new().read(key_size)
        print(f'Key was created using {self.type.__name__}')

    def importKey(self, filename: str):
        """Import a key from a file.

        Args:
            filename (str): The name of the file to import the key.

        """
        with open(filename, 'r') as f:
            self.key = b64decode(f.read().encode('utf-8'))
            print(f'Key was imported using {self.type.__name__}')

    def exportKey(self, filename: str):
        """Export the key being used in the cipher into a file.

        Args:
            filename (str): The name of the file to export the key.

        """
        if self.key == None:
            print("Please create or import a key.")
            return ""

        with open(filename, 'w') as f:
            str_key = b64encode(self.key).decode('utf-8')
            f.write(str_key)
            print(f'Key has been exported to {filename}')

    def encrypt(self, text: str) -> str:
        """Encrypt a message, they key should be imported or created.

        Args:
            text (str): The message to be encrypted.

        Returns:
            The encrypted text.

        """
        if self.key == None:
            print("Please create or import a key.")
            return ""

        self.cipher = self.type.new(self.key, self.type.MODE_CBC, self.initialization_vector)

        encrypted_text =  self.cipher.encrypt(pad(text.encode('utf-8'), self.type.block_size))
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, text: str) -> str:
        """Decrypt a cipher text, they key should be imported or created.

        Args:
            text (str): The cipher text to be encrypted.

        Returns:
            The decrypted plaintext.

        """
        if self.key == None:
            print("Please create or import a key.")
            return ""

        self.cipher = self.type.new(self.key, self.type.MODE_CBC, self.initialization_vector)

        decrypted_text =  unpad(self.cipher.decrypt(b64decode(text.encode('utf-8'))), self.type.block_size)
        return decrypted_text.decode('utf-8')
