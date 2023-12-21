import json
import random
import socket
import threading
import time


class Follower():
  def __init__(self, server_host='localhost', server_port=9999):
    self.server_host = server_host
    self.server_port = server_port
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((self.server_host, self.server_port))
    self.location = (0, 0, 0)

  def send_message(self, msg):
    """
    Leader サーバにメッセージを送信する
    """
    self.client.send(msg.encode('utf-8'))

  def receive_message(self):
    """
    Leader サーバからメッセージを受信する
    """
    while True:
      data = self.client.recv(4096)
      message = data.decode('utf-8')
      state_dict = json.loads(message)
      print(state_dict)

  def update_location(self):
    """
    自身の位置を更新する
    TODO: 位置の更新方法を変更する
    """
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    z = random.randint(0, 100)
    self.location = (x, y, z)

  def simulate(self):
    """
    自身の位置を更新し、Leader サーバに位置を送信する
    TODO: 位置の更新方法を変更したら sleep は不要
    """
    while True:
      sleep_time = random.randint(1, 4)
      time.sleep(sleep_time)
      self.update_location()
      print(self.location)
      self.send_message(f'{self.location}')

  def run(self):
    update_thread = threading.Thread(target=self.simulate)
    update_thread.start()

    receive_thread = threading.Thread(target=self.receive_message)
    receive_thread.start()

if __name__ == '__main__':
  follower = Follower()
  follower.run()
