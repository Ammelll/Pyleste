#!/usr/bin/env python3

import sys
if __name__ != '__main__': sys.exit()
# import PICO-8 emulator and Celeste
from PICO8 import PICO8
from Carts.Celeste import Celeste

# useful Celeste utils
import CelesteUtils as utils
import random

# create a PICO-8 instance with Celeste loaded
p8 = PICO8(Celeste)

# swap 100m with this level and reload it
room_data = '''
w w w w w w w w w w . . w . w w
w w w w w w w w w w . . w . < w
w w w v v v v . . . . . w . < w
w w > . . . . . . . . w w . . .
w > . . . . . . . . . w . . . .
. . . . . . . . . . . w . . . .
. . . . . . . . . . w w . . . .
. . . . . . . . w w w . . . . .
. . . . . . . . w . . . . . . .
. . . . . . w w w . . . . . . .
. . . . . . w . . . . . . . . .
. . . . . . w . . . . . . . . .
. . . . w w w . . . . . . . . .
. . . . w . . . . . . . . . . .
. . . p w . . . . . . . . . . .
w w w w w w w w w w w w w w w w
# '''
utils.replace_room(p8, 0, room_data)
utils.load_room(p8, 0)
# skip the player spawn
utils.skip_player_spawn(p8)

# view the room
print(p8.game)


# run for 20f while outputting player info
# print(p8.game.get_player())
# for f in range(20):

inputs = ["l","r","r","r"]
inputs2 = ["u","d","N","N"]
populationSize = 100
mutationRate = 0.05
population = []
sequenceLength = 200
def get_digit(number, n):
    return number // 10**n % 10
def randomSequence():
  sequence = ""
  for i in range(sequenceLength):
    dir1 = random.choice(inputs)
    dir2 = random.choice(inputs2)
    jump = random.random() < 0.15
    dash = random.random() < 0.15
    num1=0
    num2=0
    num3=0
    num4=0
    if dir1 == "l":
      num1=1
    if dir2 == "u":
      num2=1
    elif dir2 == "d":
      num2=2
    if jump:
      num3=1
    if dash:
      num4=1
    sequence+=str(num1*1000+num2*100+num3*10+num4)
  return sequence
def initialSeeding():
  for i in range(populationSize):
    population.append(randomSequence())
def configMove(move):
  p8.set_inputs(l=False, r=False, u=False, d=False, z=False, x=False)
  move = int(move)
  if get_digit(move,3)==1:
    p8.set_inputs(l=True)
  else:
    p8.set_inputs(r=True)
  if get_digit(move,2)==1:
    p8.set_inputs(u=True)
  elif get_digit(move,2)==2:
    p8.set_inputs(d=True)
  if get_digit(move,1)==1:
    p8.set_inputs(z=True)
  if get_digit(move,0)==1:
    p8.set_inputs(x=True)


initialSeeding()
lowestY = 100

while lowestY > 10:
  scores = []
  nextGen = []
  for p in population:
    utils.load_room(p8, 0)
    utils.skip_player_spawn(p8)
    lowestY = 10000
    for i in range(0, len(p), 4):      
      move = p[i:i + 4]
      configMove(move)
      # not exactly sure what this does
      p8.step()
      if p8.game.get_player() != None:
        lowestY = min(lowestY, p8.game.get_player().y)
      else:
        break
    scores.append(100-lowestY)
    print(lowestY)
  indices = sorted(range(len(scores)), key=lambda i: scores[i])[-int(populationSize*1/10):]
  # I'd change this to index, but indice is too funny
  for indice in indices:
    nextGen.append(population[indice])
  for j in range(int(populationSize*9/10)):
    r1 = random.randint(0,9)
    r2 = random.randint(0,9)
    while(r1 == r2):
      r2 = random.randint(0,9)
    m1 = nextGen[r1]
    m2 = nextGen[r2]
    child = ""
    for inp in range(0, len(m1), 4):     
      flip = bool(random.getrandbits(1)) 
      if random.random() < mutationRate:
        dir1 = random.choice(inputs)
        dir2 = random.choice(inputs2)
        jump = random.random() < 0.15
        dash = random.random() < 0.15
        num1=0
        num2=0
        num3=0
        num4=0
        if dir1 == "l":
          num1=1
        if dir2 == "u":
          num2=1
        elif dir2 == "d":
          num2=2
        if jump:
          num3=1
        if dash:
          num4=1
        child+=str(num1*1000+num2*100+num3*10+num4)
      elif flip:
        child+=m1[inp:inp + 4]
      else:
        child+=m2[inp:inp + 4]
    nextGen.append(child)
  population = nextGen
print(p8.game)

