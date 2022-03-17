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
        self.cipher = self.type.new(self.key, self.type.MODE_CBC, self.initialization_vector)

    def importKey(self, filename: str):
        with open(filename, 'r') as f:
            self.key = b64decode(f.read().encode('utf-8'))
            print(f'Key was imported using {self.type.__name__}')
            self.cipher = self.type.new(self.key, self.type.MODE_CBC, self.initialization_vector)

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
        
        if self.cipher == None:
            print("Configuration failed, import or create key.")
            return ""

        encrypted_text =  self.cipher.encrypt(pad(text.encode('utf-8'), self.type.block_size))
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, text: str) -> str:
        if self.key == None:
            print("Please create or import a key.")
            return ""

        if self.cipher == None:
            print("Configuration failed, import or create key.")
            return ""

        decrypted_text =  unpad(self.cipher.decrypt(b64decode(text.encode('utf-8'))), self.type.block_size)
        return decrypted_text.decode('utf-8')


def des_or_aes_encryption(text_to_enc: str, cipher_type: str) -> Tuple[str, str]:
  """ Encrypts a message with DES or AES cipher

  Parameters:
    text_to_enc (str): Text that is going to be encrypted
    cipher_type (str): Cipher algorithm to be used

  Returns:
    (str, str): Encrypted text with DES or AES cipher & encryption key
  """

  # Check if cipher is DES or AES
  cipher_is_aes: bool = cipher_type == 'AES'

  # Define values for corresponding cipher
  block_size: int = (DES.block_size, AES.block_size)[cipher_is_aes]
  key_size: int = (DES.key_size, AES.key_size[0])[cipher_is_aes]
  cipher_mode: int = (DES.MODE_CBC, AES.MODE_CBC)[cipher_is_aes]

  # Generates random key with corresponding size
  key: bytes = Random.new().read(key_size)
  # Generates iv with corresponding size
  initialization_vector: bytes = (
      '12345678' * (block_size//8)).encode('utf-8')
  # Instantiates cipher algorithm
  cipher = ((DES, AES)[cipher_is_aes]).new(
      key, cipher_mode, initialization_vector)
  # Encrypt message
  encrypted_text: bytes = cipher.encrypt(
      pad(text_to_enc.encode('utf-8'), block_size))

  return (b64encode(encrypted_text).decode('utf-8'), b64encode(key).decode('utf-8'))


def des_or_aes_decryption(text_to_dec: str, key: str, cipher_type: str) -> str:
  """ Decrypts a message with DES or AES encryption

  Parameters:
    text_to_dec (str): Text that is going to be decrypted
    key (int): key for DES or AES cipher
    cipher_type (str): Cipher algorithm to be used

  Returns:
    str: Decrypted text with DES or AES cipher
  """

  # Check if cipher is DES or AES
  cipher_is_aes: bool = cipher_type == 'AES'

  # Define values for corresponding cipher
  block_size: int = (DES.block_size, AES.block_size)[cipher_is_aes]
  cipher_mode: int = (DES.MODE_CBC, AES.MODE_CBC)[cipher_is_aes]

  # Generates iv with corresponding size
  initialization_vector: bytes = (
      '12345678' * (block_size//8)).encode('utf-8')
  # Instantiates cipher algorithm
  cipher = ((DES, AES)[cipher_is_aes]).new(
      b64decode(key.encode('utf-8')), cipher_mode, initialization_vector)
  # Decrypt message
  decrypted_text: bytes = unpad(cipher.decrypt(
      b64decode(text_to_dec.encode('utf-8'))), block_size)

  return decrypted_text.decode('utf-8')


def main():
  """ Main method for program execution & option selection """

  continue_execution = True
  while continue_execution:
    # Print available options
    print(('\nChoose an option: \n'
           '1) DES Encryption\n'
           '2) DES Decryption\n'
           '3) AES Encryption\n'
           '4) AES Decryption\n'
           '5) Exit\n'))

    input_option = input()
    print()

    # Execute method for encryption
    if input_option in ['1', '2']:
      cipher_type = 'DES' if input_option == '3' else 'AES'
      print('Enter text to encrypt:')
      text_input: str = input()
      print('\n*** {0} Encryption ***\nEncrypted text:\n{1[0]}\nKey:\n{1[1]}\n'.format(
          cipher_type, des_or_aes_encryption(text_input, cipher_type)))

    # Execute method for decryption
    elif input_option in ['3', '4']:
      cipher_type = 'DES' if input_option == '4' else 'AES'
      print('Enter text to decrypt:')
      text_input: str = input()
      print('Enter key:')
      key: str = input()
      print('\n*** {} Decryption ***\nDecrypted text:\n{}\n'.format(cipher_type,
            des_or_aes_decryption(text_input, key, cipher_type)))

    else:
      continue_execution = False

    print('----------------------------')

if __name__ == '__main__':
    main()
