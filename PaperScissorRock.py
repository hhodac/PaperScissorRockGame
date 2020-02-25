import pygame
import random

pygame.init()

display_width = 400
display_height = 200

white = (255, 255, 255)
blue = (0, 0, 128)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Paper - Scissor - Rock')

clock = pygame.time.Clock()

paperImg = pygame.image.load('gameIcon-paper.png')
scissorImg = pygame.image.load('gameIcon-scissor.png')
rockImg = pygame.image.load('gameIcon-rock.png')

def playerA_display(action):
    x = display_width * 0.2
    y = display_height * 0.2
    if action == 'paper':
        gameDisplay.blit(paperImg, (x, y))
    elif action == 'scissor':
        gameDisplay.blit(scissorImg, (x, y))
    else:   # action == 'rock'
        gameDisplay.blit(pygame.transform.rotate(rockImg, 180), (x, y))

def playerB_display(action):
    x = display_width * 0.6
    y = display_height * 0.2
    if action == 'paper':
        gameDisplay.blit(pygame.transform.rotate(paperImg, 180), (x, y))
    elif action == 'scissor':
        gameDisplay.blit(pygame.transform.rotate(scissorImg, 180), (x, y))
    else:   # action == 'rock'
        gameDisplay.blit(rockImg, (x, y))

def winner_display(player):
    font = pygame.font.Font('freesansbold.ttf', 32)
    if player is not None:
        text = 'Player ' + player + ' wins.'
    else:
        text = 'Draw'
    textDisplay = font.render(text, True, blue)
    textRect = textDisplay.get_rect()
    textRect.center = (display_width // 2, display_height * 0.9)
    gameDisplay.blit(textDisplay, textRect)

def playerA_action():
    actionChoice = random.choice([1, 2, 3])
    return actionMatching(actionChoice)

def playerB_action():
    actionChoice = random.choice([1, 2, 3])
    return actionMatching(actionChoice)

def actionMatching(num):
    if num == 1:
        return 'scissor'
    elif num == 2:
        return 'paper'
    else:
        return 'rock'

def whoWins(actionA, actionB):
    if (actionA, actionB) in (('paper', 'rock'), ('rock', 'scissor'), ('scissor', 'paper')):
        # print('Player A wins')
        return 'A'
    elif (actionB, actionA) in (('paper', 'rock'), ('rock', 'scissor'), ('scissor', 'paper')):
        # print('Player B wins')
        return 'B'
    else:
        # print('Draw')
        return None

crashed = False
actionA = playerA_action()
actionB = playerB_action()

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # print(event)

        ###
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                actionA = playerA_action()
                actionB = playerB_action()
                print(', '.join([actionA, actionB]))
        ###


    gameDisplay.fill(white)
    playerA_display(actionA)
    playerB_display(actionB)
    winner_display(whoWins(actionA, actionB))


    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()
