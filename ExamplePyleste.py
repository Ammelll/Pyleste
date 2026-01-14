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
utils.load_room(p8, 0)

# skip the player spawn
utils.skip_player_spawn(p8)

# view the room
print(p8.game)


# run for 20f while outputting player info
# print(p8.game.get_player())
# for f in range(20):

inputs = ["u","d","l","r"]
inputs2 = ["u","d","l","r","N","N","N","N"]
populationSize = 1000
mutationRate = 0.05
population = []
sequenceLength = 200
class Input:
  def __init__(self, dir1,dir2,jump,dash):
    self.dir1 = dir1
    self.dir2 = dir2
    self.jump = jump
    self.dash = dash

def randomSequence():
  sequence = []
  for i in range(sequenceLength):
    sequence.append(Input(random.choice(inputs),random.choice(inputs2),bool(random.getrandbits(1)),bool(random.getrandbits(1))))
  return sequence
def initialSeeding():
  for i in range(populationSize):
    population.append(randomSequence())
def configMove(move):
  match move.dir1:
    case "u": p8.set_inputs(u=True)
    case "d": p8.set_inputs(d=True)
    case "l": p8.set_inputs(l=True)
    case "r": p8.set_inputs(r=True)
  match move.dir2:
    case "u": p8.set_inputs(u=True)
    case "d": p8.set_inputs(d=True)
    case "l": p8.set_inputs(l=True)
    case "r": p8.set_inputs(r=True)
  if move.jump:
    p8.set_inputs(z=True)
  if move.dash:
    p8.set_inputs(x=True)

initialSeeding()

for i in range(10):
  scores = []
  nextGen = []
  for p in population:
    lowestY = 10000
    for move in p:
      configMove()
      # not exactly sure what this does
      p8.step()
      if p8.game.get_player() != None:
        lowestY = min(lowestY, p8.game.get_player().y)
    scores.append(100-lowestY)
  indices = sorted(range(len(scores)), key=lambda i: scores[i])[-10:]
  # I'd change this to index, but indice is too funny
  for indice in indices:
    nextGen.append(population[indice])
  for j in range(90):
    r1 = random.randint(0,9)
    r2 = random.randint(0,9)
    while(r1 == r2):
      r2 = random.randint(0,9)
    m1 = nextGen[r1]
    m2 = nextGen[r2]
    child = []
    for inp in range(len(m1)):
      flip = bool(random.getrandbits(1)) 
      if random.random() < mutationRate:
        child.append(Input(random.choice(inputs),random.choice(inputs2),bool(random.getrandbits(1)),bool(random.getrandbits(1))))
      elif flip:
        child.append(m1[i])
      else:
        child.append(m2[i])
    nextGen.append(child)
  population = nextGen
print(p8.game)
lowestY = 100
# the bug is most likeley here.
# move is the name of both the variables in the inner and outer loops.
# I can't really tell what this code is trying to do though.
# also the variable 'p' doesn't seem to exist.
for move in population[0]:
  p8.set_inputs(r=True, x=True)
  for move in p:
    configMove(move)

      p8.step() # not sure if these two lines are indented correctly
      print(p8.game.get_player())
      