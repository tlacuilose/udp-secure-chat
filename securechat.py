from udpchat import UDPChat, UDPUser
from ciphers import MessageCipher

def start_secure_chat():
    # Both use localhost, but could use other ip.
    # TODO: Enable other ips.
    localhost = "127.0.0.1"

    # Ask for the port to listen and to send to.
    print(f'Opening udp chat on localhost {localhost}')
    myport = int(input("Port you are listening in: "))
    toport = int(input("Port sending to: "))

    # Start and configure the port with the given socket.
    chat = UDPChat(UDPUser(localhost, myport), UDPUser(localhost, toport))

    print("Starting a chat...")

    # Select an encryption method.
    while True:
        ciphertype = input("Select an encryption type (AES, DES, DES3): ").upper()
        if ciphertype in ['AES', 'DES', 'DES3']:
            break

    # Create a  cipher with the selected encryption method.
    cipher = MessageCipher(ciphertype)

    # Manage the keys, create, import, or export.
    while True:
        res_create = input("A key is needed.\nCreate key: c, Import key: i? ")
        if res_create == 'c':
            cipher.createKey()
            exp_ans = input("Want to export the key y/n? ")
            if exp_ans == 'y':
                filename = input("Give me the filename to save the key: ")
                cipher.exportKey(filename)
            else:
                print("Key was not exported.")
            break
        elif res_create == 'i':
            filename = input("Give me the file name of the key: ")
            try :
                cipher.importKey(filename)
                break
            except FileNotFoundError:
                print("Key file not found.")

    # Starting chat.
    while True:
        ans = input("Send: s, Listen: l, exit: x? ")
        if ans == 's':
            chat.enterSend(cipher.encrypt)
        elif ans == 'l':
            chat.enterListen(cipher.decrypt)
        elif ans == 'x':
            break


    print("Closing chat...")

if __name__ == '__main__':
    start_secure_chat()
