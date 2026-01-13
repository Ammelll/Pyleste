if __name__ == '__main__':
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
      sequence.append(Input(random.choice(inputs),random.choice(inputs2),bool(random.getrandbits(1)),bool(random.getrandbits(1))))
    return sequence
  def initialSeeding():
    for i in range(populationSize):
      population.append(randomSequence())

  initialSeeding()
  
  for i in range(10):
    scores = []
    nextGen = []
    for p in population:
      lowestY = 10000
      for move in p:
        dir1 = move.dir1
        dir2 = move.dir2
        jump = move.jump
        dash = move.dash
        if dir1 == "u":
          p8.set_inputs(u=True)
        elif dir1 == "d":
          p8.set_inputs(d=True)
        elif dir1 == "l":
          p8.set_inputs(l=True)
        elif dir1 == "r":
          p8.set_inputs(r=True)
        if dir2 == "u":
          p8.set_inputs(u=True)
        elif dir1 == "d":
          p8.set_inputs(d=True)
        elif dir1 == "l":
          p8.set_inputs(l=True)
        elif dir1 == "r":
          p8.set_inputs(r=True)
        if jump:
          p8.set_inputs(z=True)
        if dash:
          p8.set_inputs(x=True)

        p8.step()
        if p8.game.get_player() != None:
          y = p8.game.get_player().y
          if y < lowestY:
            lowestY = y
      scores.append(100-lowestY)
    indices = sorted(range(len(scores)), key=lambda i: scores[i])[-10:]
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
        flip =bool(random.getrandbits(1)) 
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
  for move in population[0]:
    p8.set_inputs(r=True, x=True)
    for move in p:
        dir1 = move.dir1
        dir2 = move.dir2
        jump = move.jump
        dash = move.dash
        if dir1 == "u":
          p8.set_inputs(u=True)
        elif dir1 == "d":
          p8.set_inputs(d=True)
        elif dir1 == "l":
          p8.set_inputs(l=True)
        elif dir1 == "r":
          p8.set_inputs(r=True)
        if dir2 == "u":
          p8.set_inputs(u=True)
        elif dir1 == "d":
          p8.set_inputs(d=True)
        elif dir1 == "l":
          p8.set_inputs(l=True)
        elif dir1 == "r":
          p8.set_inputs(r=True)
        if jump:
          p8.set_inputs(z=True)
        if dash:
          p8.set_inputs(x=True)

        p8.step()
        print(p8.game.get_player())
        