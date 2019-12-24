import socket
import pickle
from random import randint

def crypt(a1, key):
    a2 = [chr(ord(a1[i]) ^ key) for i in range(len(a1))]
    return ''.join(a2)


def send(conn, msg, K):
    msg = crypt(msg, K)
    conn.send(pickle.dumps(msg))


def receive(conn, K):
    msg = pickle.loads(conn.recv(1024))
    msg = crypt(msg, K)
    return msg


HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = conn.recv(1024)
p, g, A = pickle.loads(msg)
b = randint(10, 250)
B = g ** b % p
conn.send(pickle.dumps(B))
K = A ** b % p


while True:
    try:
        msg = receive(conn, K)
        print(msg)
        send(conn, msg, K)
    except EOFError:
        break




conn.close()