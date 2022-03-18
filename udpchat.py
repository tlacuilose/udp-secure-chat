import socket
from typing import NamedTuple, Callable

class UDPUser(NamedTuple):
    """A UDP user with ip and port

    Args:
        ip (str): The ip of the user.
        port (int): The port of the user.
    """

    ip: str
    port: int

class UDPChat():
    """A chat that sends messages through UDP

    Allows modifying the text when listening or sending

    Args:
        me (UDPUser): This user of the chat with ip and port
        other (UDPUser): The receiving  user of the chat with ip and port

    """
    def __init__(self, me: UDPUser, other: UDPUser):
        self.me = me
        self.other = other

    def enterSend(self, mod_text: Callable[[str], str]):
        """Enter sending mode, send messages through udp.

        Args:
            mod_text (Callable[[str], str]): A modifier for the text before sending it.

        """

        # Start socket on internet with UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        # Start a loop to keep sending messages.
        print(f'Sending to {self.other.ip} on port {self.other.port}, type exit() to finish.')
        while True:
            message = input("Your message: ")

            # Stop the loop when exit() is typed.
            if message == "exit()":
                break

            # Modify text before sending text
            try:
                modded_text = mod_text(message)
            except:
                modded_text = message
            print(f'Sending encrypted: {modded_text}')

            # Send the message to the other ip and port.
            sock.sendto(bytes(modded_text, "utf-8"),  self.other)

        sock.close()

    def enterListen(self, dec_text: Callable[[str], str]):
        """Enter sending mode, send messages through udp.

        Args:
            mod_text (Callable[[str], str]): A modifier for the text before sending it.

        """

        # Start socket on internet with UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        # Start a loop to listen to incoming messages.
        print(f'Listening in {self.me.ip} on port {self.me.port}')
        sock.bind(self.me)

        # Listen on a loop with a 5 second timeout, this allows querying for continuation.
        sock.settimeout(5)
        while True:
            try:
                # Receive messages and modify after receiving them>
                data, _ = sock.recvfrom(1024)
                enc_message = bytes.decode(data)
                print(f'Received encrypted: {enc_message}')
                message = dec_text(enc_message)
                print(f'received message: {message}')
            except socket.timeout:
                # After every timeout, allow stopping the listening loop.
                print("Continue listening for messages? y/n ")
                ans = input()
                if ans == 'n':
                    break
            except ValueError:
                # Alert when the modifier failed.
                print("Failed to decrypt message.")

        sock.close()

