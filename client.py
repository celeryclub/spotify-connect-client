if __name__ == '__main__' and __package__ is None:
  from os import sys, path
  sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import threading
import requests
from smartie.smartie import Smartie

from time import sleep


# host = 'http://orange.local:4000'
host = 'http://localhost:4000'

status_url = host + '/api/info/status'
metadata_url = host + '/api/info/metadata'

smartie = Smartie()
smartie.backlight_off()

connect_active = False
metadata_thread = None

def clear_screen():
  smartie.write_line('', 1)
  smartie.write_line('', 2)
  smartie.write_line('', 3)
  smartie.write_line('', 4)

def write_json_to_screen(json):
  track, artist, album = json['track_name'], json['artist_name'], json['album_name']
  smartie.write_line(track, 1)
  smartie.write_line(artist, 2)
  smartie.write_line(album, 4)

def thready():
  global connect_active

  while connect_active:
    print('checking metadata')

    metadata_request = requests.get(metadata_url)
    metadata_json = metadata_request.json()
    write_json_to_screen(metadata_json)
    sleep(2)

def turn_on():
  global connect_active, metadata_thread
  connect_active = True

  clear_screen()
  smartie.backlight_on()
  metadata_thread = threading.Thread(target=thready)
  metadata_thread.start()

def turn_off():
  global connect_active, metadata_thread
  connect_active = False

  smartie.backlight_off()
  clear_screen()

  if metadata_thread:
    metadata_thread.join()

def handle_status(new_active):
  global connect_active

  if new_active and not connect_active:
    turn_on()
  elif connect_active and not new_active:
    turn_off()

try:
  while True:
    print('checking status')

    status_request = requests.get(status_url)
    status_json = status_request.json()
    active = status_json['active'] and status_json['playing']
    print(active)

    handle_status(active)
    sleep(10)
except KeyboardInterrupt:
  turn_off()
  print('Metadata thread joined')
