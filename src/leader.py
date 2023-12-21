import ast
import json
import random
import socket
import threading
import time


class Leader():
  def __init__(self, host='localhost', port=9999):
    self.host = host
    self.port = port
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((self.host, self.port))
    self.server.listen(5)
    self.clients = []
    self.threads = []
    self.location = (0, 0, 0)
    self.state_dict = {
      'leader': self.location
    }

  def handle_client(self, client):
    """
    クライアントからのメッセージを受信して
    state_dict を更新し、すべてのクライアントに送信する
    """
    while True:
      data = client.recv(4096)
      message = data.decode('utf-8')
      location = ast.literal_eval(message)

      host, port = client.getpeername()
      self.state_dict[f'{host}:{port}'] = location
      print(self.state_dict)

      if not message:
        break

      json_message = json.dumps(self.state_dict)
      for c in self.clients:
        c.send(json_message.encode('utf-8'))

    client.close()

  def update_location(self):
    """
    自身の位置を更新する
    TODO: 位置の更新方法を変更する
    """
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    z = random.randint(0, 100)
    self.location = (x, y, z)
    self.state_dict['leader'] = self.location

  def simulate(self):
    """
    自身の位置を更新する
    TODO: 位置の更新方法を変更したら sleep は不要
    """
    while True:
      sleep_time = random.randint(1, 4)
      time.sleep(sleep_time)
      self.update_location()
      print(self.location)

  def run(self):
    update_thread = threading.Thread(target=self.simulate)
    update_thread.start()

    while True:
      client, address = self.server.accept()
      host, port = address
      self.clients.append(client)
      self.state_dict[f'{host}:{port}'] = (0, 0, 0)

      print(f'Connected to {host}:{port}')
      thread = threading.Thread(target=self.handle_client, args=(client,))
      thread.start()
      self.threads.append(update_thread)

if __name__ == '__main__':
  leader = Leader()
  leader.run()
