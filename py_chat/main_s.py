import socket
import threading
import configparser
import time
import logging

# ログ設定
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config = configparser.ConfigParser()
config.read('net.ini')

IPADDR = config.get('NETWORK', 'IPADDR')
PORT = int(config.get('NETWORK', 'PORT'))

sock_sv = socket.socket(socket.AF_INET)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

# クライアントのリスト (要素は辞書に変更)
client_list = []

# 過去のメッセージを保持するリスト
past_messages = []

def send_past_messages(sock):
    # 過去のメッセージをクライアントに送信
    for message in past_messages:
        time.sleep(0.1)
        sock.send(message.encode('utf-8'))

def recv_client(sock, addr):
    # クライアントからの名前を受け取る
    name = sock.recv(1024).decode('utf-8')

    # 過去メッセージの同期
    send_past_messages(sock)

    # 参加者リストに追加
    client_list.append({'socket': sock, 'address': addr, 'name': name})
    join_message = "system >>> {} がログインしました。".format(name)
    print("+ join client:{} as '{}'".format(addr, name))
    for client in client_list:
        client['socket'].send(join_message.encode('utf-8'))

    # ログに参加者を記録
    logging.info("+ join client:{} as '{}'".format(addr, name))

    time.sleep(3)
    past_messages.append(join_message)

    try:
        while True:
            data = sock.recv(1024)
            if data == b"":
                break

            message = "{} >>> {}".format(name, data.decode('utf-8'))

            # 受信データを全クライアントに送信
            for client in client_list:
                client['socket'].send(message.encode('utf-8'))

            # 過去のメッセージとして保持
            past_messages.append(message)

            # ログにメッセージを記録
            logging.info(message)

    except ConnectionResetError:
        pass

    # クライアントリストから削除
    client_list.remove({'socket': sock, 'address': addr, 'name': name})
    print("- close client:{} as '{}'".format(addr, name))

    disconnect_message = "system >>> {} がログアウトしました。".format(name)
    past_messages.append(disconnect_message)
    for client in client_list:
        client['socket'].send(disconnect_message.encode('utf-8'))
    
    # ログに接続終了を記録
    logging.info("Client {} as '{}' disconnected.".format(addr, name))

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

# クライアント接続待ちループ
while True:
    sock_cl, addr = sock_sv.accept()
    thread = threading.Thread(target=recv_client, args=(sock_cl, addr))
    thread.start()
