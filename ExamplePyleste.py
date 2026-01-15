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
. . . . . . . . w w w w . . . .
. . . . . . . . w . . . . . . .
. . . . . . . . w . . . . . . .
. . . . . . w w w . . . . . . .
. . . . . . w . . . . . . . . .
. . . . . . w . . . . . . . . .
. . . . w w w . . . . . . . . .
. . . . w . . . . . . . . . . .
. . . p w . . . . . . . . . . .
w w w w w w w w w w w w w w w w
# '''
# utils.replace_room(p8, 0, room_data)
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
class Input:
  def __init__(self, dir1,dir2,jump,dash):
    self.dir1 = dir1
    self.dir2 = dir2
    self.jump = jump
    self.dash = dash

def randomSequence():
  sequence = []
  for i in range(sequenceLength):
    sequence.append(Input(random.choice(inputs),random.choice(inputs2), random.random() < 0.15,random.random() < 0.15))
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
lowestY = 100

while lowestY > 10:
  print(lowestY)
  scores = []
  nextGen = []
  for p in population:
    utils.load_room(p8, 0)
    utils.skip_player_spawn(p8)
    lowestY = 10000
    for move in p:
      configMove(move)
      # not exactly sure what this does
      p8.step()
      if p8.game.get_player() != None:
        lowestY = min(lowestY, p8.game.get_player().y)
    scores.append(100-lowestY)
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
    child = []
    for inp in range(len(m1)):
      flip = bool(random.getrandbits(1)) 
      if random.random() < mutationRate:
        child.append(Input(random.choice(inputs),random.choice(inputs2), random.random() < 0.15,random.random() < 0.15))
      elif flip:
        child.append(m1[inp])
      else:
        child.append(m2[inp])
    nextGen.append(child)
  population = nextGen
print(p8.game)

for move in population[0]:
  configMove(move)
  p8.step() # not sure if these two lines are indented correctly
  print(p8.game.get_player())
    