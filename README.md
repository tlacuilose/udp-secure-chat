# Python UDP Secure Chat

Command line encrypted chat through udp sockets.

- Choose ports to communicate in localhost.
- Choose encryption method AES, DES, DES3.
- Import, export, create a key.
- Send and receive encrypted messages.

# How to install

Clone the repository

```bash
git clone https://github.com/tlacuilose/udp-secure-chat
```

Start and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Start chat

```bash
python securechat.py
```

# Chat user guide

1. The chat asks the port where messages will be received.
    - Write an integer number.
2. The chat asks the port where messages will be sent.
    - Write an integer number.
3. The chat asks the encryption method.
    - Write "AES", "DES", "DES3" only.
4. A key should be created, choose to create or import a key.
    - Type 'c' to create a key. A key will be created and choose to export it or not.
        - Type 'y' to export a key.
            - Type the file name where the key will be exported to.
        - Type 'n' to not export a key.
    - Type 'i' to import a key. The file name where the key is located should be entered.
        - Enter the file name of the key to import.
5. Choose between 's' to send messages or 'l' to listen for messages.
    - Type 's' and start sending messages.
        - Type message and hit enter to send a message to the selected port.
        - Type 'exit()' to return to the previous menu.
    - Type 'l' and start listening for messages.
        - Messages received will be shown.
        - The chat will ask to continue listening for messages.
            - Type 'y' to continue listening for messages and to show hold back messages.
            - Type 'n' to stop listening and to return to the previous message.
    - Type 'x' to close the chat.
