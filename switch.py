import random
from microbit import *
import radio

scores = [(0, i) for i in range(11)]

radio.on()
radio.config(group=255)

sent = False
switch_state = pin0.is_touched()

while True:
  message = radio.receive()
  if message:
    try:
      team, score = map(int, message.split(':'))
      scores[team] = (score, team)
    except ValueError:
      pass

  switch = pin0.is_touched()
  if switch != switch_state:
    switch_state = switch
    sent = False

  if switch_state:
    display.show(Image.YES)

    if not sent:
      radio.send('switch-on')
      score_strings = [str(team)+':'+str(score) for score, team in scores]
      for score_string in score_strings:
        radio.send(score_string)
      sent = True

  else:
    display.show(Image.NO)

    if not sent:
      radio.send('switch-off')
      sent = True
