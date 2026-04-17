import sys
import pygame
import random

pygame.init()

width = 800
height = 600
size = (width, height)
black = (0,0,0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chicken Click Game")

chicken = pygame.image.load("chicken.png")
powerUp = pygame.image.load("powerUp.png")
bg = pygame.image.load("bg.png")

"""
  Game Modifiers
"""
gravityScale = 1.0
extraLives = 0

# deltatime, to ensure chickens don't fall at 99 mph if FPS is too high!
deltatime = 0
clock = pygame.time.Clock() 
fallSpeed = 300 * gravityScale

"""
  Powerup Setup
"""
powerUpPosition = [0, 0] # x, y
powerUpSpawnTimer = 0 # timer until powerup respawns

iterator = 0
numofchickens = 5
startX = []
startY = []
speed = []

while iterator < numofchickens:
  startX.append(random.randint(0, width - chicken.get_width() + 1))
  startY.append(0 - random.randint(chicken.get_height(), chicken.get_height() * 2))
  speed.append(fallSpeed)
  iterator += 1

replayscreen = False
#Set up game over stuff
bigfont = pygame.font.SysFont(None, 200)
playagaintext = bigfont.render("Play Again?", True, (0,200,0))
pax = width/2 - playagaintext.get_rect().width/2

smallfont = pygame.font.SysFont(None, 100)
yestext = smallfont.render("YES", True, (0, 200, 0))
yesx = width/4 - yestext.get_rect().width/2
notext = smallfont.render("NO", True, (0,200,0))
nox = width - width/4 - yestext.get_rect().width/2

#Game Loop

gameover = False

while gameover == False:
  
  deltatime = clock.tick(60) / 1000 # 1000ms = 1 second

  fallSpeed = 300 * gravityScale # Replaces any gravity with fallSpeed to make things easier to modify.

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameover = True

  #Clicking on the Chickens
  if pygame.mouse.get_pressed()[0]:
    coords = pygame.mouse.get_pos()
    if replayscreen == False:
      iterator = 0
      while iterator < numofchickens:
        if coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + chicken.get_width() and coords[1] > startY[iterator] and coords[1] < startY[iterator] + chicken.get_height():
          startX[iterator] =  random.randint(0, width - chicken.get_width() + 1)
          startY[iterator] = 0 - random.randint(chicken.get_height(), chicken.get_height() * 2)
          speed[iterator] = fallSpeed
          break
        iterator += 1
    else:
      if coords[0] > yesx and coords[0] < yesx + yestext.get_rect().width and coords[1] > 450 and coords[1] < 450 + yestext.get_rect().height:
        iterator = 0
        while iterator < numofchickens:
          startX[iterator] =  random.randint(0, width - chicken.get_width() + 1)
          startY[iterator] = 0 - random.randint(chicken.get_height(), chicken.get_height() * 2)
          speed[iterator] = fallSpeed
          iterator +=1
        replayscreen = False

      if coords[0] > nox and coords[0] < nox + notext.get_rect().width and coords[1] > 450 and coords[1] < 450 + notext.get_rect().height:
        gameover = True



  #Updating
  if replayscreen == False:
    iterator = 0
    #Game over
    while iterator < numofchickens:
      if startY[iterator] + chicken.get_height() > height:
        replayscreen = True
        break
      startY[iterator] += speed[iterator] * deltatime
      iterator += 1
  
  # Extra life!
  if replayscreen and extraLives > 0:
    replayscreen = False
    
    extraLives -= 1

    # Chickens are set back at the top of the screen
    iterator = 0
    while iterator < numofchickens:
      startY[iterator] = 0
      iterator += 1
  #Drawing

  if replayscreen == False:
    screen.fill(black)
    screen.blit(bg, (0,0))
    iterator = 0
    while iterator < numofchickens:
      screen.blit(chicken, (startX[iterator], startY[iterator]))
      iterator += 1

    iterator = 0
    screen.blit(powerUp, (0, 0))
  else:
    screen.fill((50,120,20))

    screen.blit(playagaintext, (pax, 150))
    screen.blit(yestext, (yesx, 450))
    screen.blit(notext, (nox, 450))

  pygame.display.flip()

pygame.display.quit()