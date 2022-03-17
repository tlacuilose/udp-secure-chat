import socket
from typing import NamedTuple, Callable

# A socket with ip and port.
class UDPUser(NamedTuple):
    ip: str
    port: int

# A chat that listens and sends modified messages.
class UDPChat():
    def _hasConfig(self) -> bool:
        return self.me != None and self.other != None

    # Configure chat before sending or listening
    def configure(self, me: UDPUser, other: UDPUser):
        self.me = me
        self.other = other

    # Start a send loop, enc_text encrypting the message being sent.
    def enterSend(self, enc_text: Callable[[str], str]):
        if not self._hasConfig:
            print('Please configure the chat')
            return 

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        print(f'Sending to {self.other.ip} on port {self.other.port}, type exit() to finish.')
        while True:
            message = input("Your message: ")
            if message == "exit()":
                break
            enc_message = enc_text(message)
            print(f'Sending encrypted: {enc_message}')
            sock.sendto(bytes(enc_message, "utf-8"),  self.other)

        sock.close()

    # Start a listen loop, dec_text decrypts the message being received.
    def enterListen(self, dec_text: Callable[[str], str]):
        if not self._hasConfig:
            print('Please configure the chat')
            return 

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        print(f'Listening in {self.me.ip} on port {self.me.port}')
        sock.bind(self.me)
        sock.settimeout(3)
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                enc_message = bytes.decode(data)
                print(f'Received encrypted: {enc_message}')
                message = dec_text(enc_message)
                print(f'received message: {message}')
            except socket.timeout:
                print("Continue waiting? y/n ")
                ans = input()
                if ans == 'n':
                    break

        sock.close()



