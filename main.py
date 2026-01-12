import pyperclip
import time

from datetime import datetime

from api import API
from parser import parse_js_clipboard
from colorful import print, cls

def ready():
  return pyperclip.paste().startswith("fetch(")

def guide():
  print("Welcome to Modrinth Statistics Collector!")
  print("To get your stats, please do the following steps:")
  print("1. Go to Modrinth website in the browser you use it in")
  print("2. Click {select}F12{reset} / {select}Ctrl+Shift+I")
  print("3. Go to the {select}Network{reset} Tab")
  print("4. Click on the Modrinth logo on the top-left corner of the page")
  print("5. Right-click on the last request in the network tab")
  print("6. Click {select}Copy{reset} > {select}Copy as fetch")
  print("After, this script should handle the rest. Just leave it running while you're doing it.")

  while True:
    time.sleep(.125)
    if ready():
      break

def main():
  if not ready():
    guide()

  cls()
  print("[API] Collected token")

  api = API()
  api.token = parse_js_clipboard()[2]['authorization']

  profile = api.get_profile()
  print("[API] Collected profile info")

  projects = api.get_projects()
  print("[API] Collected project list")

  projectTimes: dict[str, int] = {}
  ptAvg = 0
  for proj in projects:
    if proj['status'] == 'approved':
      publish_time = proj['queued']
      end_time = proj['approved']

      if None in (publish_time, end_time):
        continue

      projectTime = (
        datetime.fromisoformat(end_time) -
        datetime.fromisoformat(publish_time)
      )

      projectTimes[proj['slug']] = projectTime
      ptAvg += projectTime.total_seconds()

      print("[API] Collected %r times" % proj['slug'])
      time.sleep(.3)

  print("[API] Collected all project times")

  ptAvg /= len(projectTimes)
  ptAvgSTR = time.strftime('%w weeks, %d days, %H hours', time.gmtime(ptAvg))

  print("[API] Calculated project time average")
  time.sleep(.065)

  cls()

  print("┌─────────┤ Modrinth Stats ├─────────┐")
  print("│                                    │")
  print("│  {blue} • {reset}                               │")
  print("│  {blue}\_/{reset}     {gold}@%-24s{reset} │" % profile['username'])
  print("│  {blue} | {reset}     {gold}avg. approval time:{reset}       │")
  print("|  {blue} | {reset}    {select}%-25s{reset} │" % ptAvgSTR)
  print("│  {blue}/ \{reset}                               │")
  print("│                                    │")
  print("└────────────────────────────────────┘")

  print(  "┌─────────┤ Modrinth Projects ├─────────┐")
  print(  "│                                       │")
  print(  "│ {blue}|         Name         | MC Version |{reset} │")
  print(  "│ {blue}|----------------------|------------|{reset} │")
  for proj in projects:
    if proj['status'] != 'approved':
      continue

    print("│ {blue}| {gold}%20s{blue} | %10s |{reset} │" % (proj['slug'], get(proj['game_versions'], 0, "-")))
  print(  "│                                       │")
  print(  "└───────────────────────────────────────┘")

def get(arr, index, default):
  try:
    return arr[index]
  except IndexError:
    return default

if __name__ == '__main__':
  main()
