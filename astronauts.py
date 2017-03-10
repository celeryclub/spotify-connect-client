import requests
from time import sleep

url = "http://api.open-notify.org/astros.json"

while True:
  r = requests.get(url)
  j = r.json()
  n = j['number']
  print(n)
  sleep(60)  # update every minute
