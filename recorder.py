from microbit import *
import radio


try:
  with open('scores.txt', 'r') as scores_file:
    scores = [score.split(':')[::-1] for score in scores_file.read().split() if score]
except OSError:
  scores = [(0, i) for i in range(11)]

radio.on()
radio.config(group=255, power=7)

sent = False
switch_state = pin0.is_touched()

while True:
  message = radio.receive()
  if message:
    try:
      team, score = map(int, message.split(':'))
      scores[team] = (score, team)
      uart.write('Team '+str(team)+': '+str(score)+'\r\n')
      with open('scores.txt', 'w') as scores_file:
        scores_file.write('\n'.join(str(team)+':'+str(score) for score in scores))
    except ValueError:
      pass

  if button_a.was_pressed():
    try:
      with open('scores.txt', 'r') as scores_file:
        scores = [score.split(':')[::-1] for score in scores_file.read().split() if score]
    except OSError:
      pass

    score_strings = [str(team)+':'+str(score) for score, team in scores]

    uart.write('='*40+'\r\n')
    for score_string in score_strings:
      radio.send(score_string)
      uart.write(score_string+'\r\n')
    uart.write('='*40+'\r\n')
