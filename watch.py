import random
from microbit import *
import radio

def show_score(score):
  if score < 10:
    display.show(str(score), wait=False)
  else:
    display.scroll(str(score), wait=False)

def send_score(score, team):
  radio.send(str(team)+':'+str(score))

radio.on()
radio.config(group=255)

uart.write('-'*30 + '\r\n')

teams = 11
team = 0
score = 0
state = 'choose team'


display.show(str(team))

while True:
  if state == 'choose team':
    a = button_a.was_pressed()
    b = button_b.was_pressed()
    if a and b:
      state = 'update score'
      display.show(Image.YES)
      sleep(400)
      show_score(score)
      button_a.get_presses()
      button_b.get_presses()
    elif a:
      team -= 1
      if team < 0:
        team = 0
      display.show(str(team))
    elif b:
      team += 1
      if team > teams-1:
        team = teams-1
      display.show(str(team))
    sleep(100)
        
  elif state == 'update score':
    a = button_a.get_presses()
    b = button_b.get_presses()
    if a and b:
      score += 10
      show_score(score)
      send_score(score, team)
    elif a:
      score -= a
      show_score(score)
      send_score(score, team)
    elif b:
      score += b
      show_score(score)
      send_score(score, team)
    sleep(100)
