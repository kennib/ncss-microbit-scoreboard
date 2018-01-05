import math

import neopixel
from microbit import *
import radio

def reduce(function, iterable, initializer=None):
  it = iter(iterable)
  if initializer is None:
    value = next(it)
  else:
    value = initializer
  for element in it:
    value = function(value, element)
  return value

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def colour_list(number):
  return [hsv2rgb(hue, 0.9, 0.15) for hue in range(0, 360, int(360/number))]

colours = [
  (40, 40, 40),             # white
  hsv2rgb(0, 1, 0.2),       # red
  hsv2rgb(25, 1, 0.2),      # orange
  hsv2rgb(40, 1, 0.3),      # yellow
  hsv2rgb(115, 1, 0.3),     # blue green
  hsv2rgb(160, 1, 0.25),    # cyan
  hsv2rgb(220, 1, 0.3),     # navy blue 
  hsv2rgb(272, 1, 0.3),     # purple
  hsv2rgb(315, 1, 0.2),     # pink
  hsv2rgb(345, 1, 0.2),     # magenta
]

neo = neopixel.NeoPixel(pin0, 20*11)
neo.clear()

def fill_row(row, time, score, r, g, b):
  c = (r,g,b)
  for i in range(0, 20):
    neo[i + row*20] = c

def row(row, time, score, r, g, b):
  c = (r,g,b)
  blank = (0, 0, 0)
  zero = (int(r*0.1), int(g*0.1), int(b*0.1))

  hundreds = int(score/100)%10
  tens = int(score/10)%10
  units = score%10

  leds = [[c]*hundreds, [zero] if hundreds > 0 and tens == 0 else [c]*tens, [zero] if units == 0 else [c]*units]
  leds = reduce(lambda x,y: x+([blank] if x else [])+y, leds, []) 
  leds = leds + [blank]*(20-len(leds))

  if row % 2:
    leds.reverse()

  for i in range(0, 20):
    neo[i + row*20] = leds[i]
      
switch = False
rows = []
teams = 11
scores = [(0, team) for team in range(teams)]
rainbow_index = 0
time = 0

radio.on()
radio.config(group=255)

while True:
  try:
    message = radio.receive()
  except ValueError:
    pass

  if message:
    if message == 'switch-on':
      switch = True
    elif message == 'switch-off':
      switch = False 
    else:
      try:
        team, score = map(int, message.split(':'))
        scores[team] = (score, team)
      except ValueError:
        pass

  rows = sorted(scores)[::-1]
  empty_scoreboard = all(score == 0 for score, team in rows)
  for index, (score, team) in enumerate(rows):
    try:
      r, g, b = colours[team]
    except IndexError:
      r, g, b = hsv2rgb(rainbow_index, 1, 0.3)
      rainbow_index = (rainbow_index + 6) % 360

    if empty_scoreboard:
      fill_row(index, time, score, r, g, b)
    else:
      row(index, time, score, r, g, b)

  if switch:
    neo.show()
  else:
    neo.clear()
  time += 1
