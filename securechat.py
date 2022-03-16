from udpchat import UDPChat, UDPUser

# Both use localhost, but could use other ip.
# TODO: Test if other ips work.
localhost = "127.0.0.1"

chat = UDPChat()

myport = int(input("Port you are listening in: "))
toport = int(input("Port sending to: "))
chat.configure(UDPUser(localhost, myport), UDPUser(localhost, toport))

while True:
    ans = input("Send: s, Listen: l, exit: e?")
    if ans == 's':
        chat.enterSend(lambda text : text)
    elif ans == 'l':
        chat.enterListen(lambda text : text)
    else:
        break
