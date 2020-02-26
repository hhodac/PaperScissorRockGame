import pygame
import random
import mysql.connector
from mysql.connector import Error

try:
    mydb = mysql.connector.connect( host = "localhost",
                                    database = "PaperScissorRock",
                                    user = "root",
                                    password = "password",
                                    auth_plugin = "mysql_native_password")
    if mydb.is_connected():
        print('Database successfully connected!')
        cursor = mydb.cursor()
except Error as e:
    print('Error while connecting to MySQL', e)

pygame.init()

display_width = 400
display_height = 200

black = (0, 0 , 0)
white = (255, 255, 255)
blue = (0, 0, 128)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

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
    return text

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

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 10)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                game_quit()

        gameDisplay.fill(white)
        normalText = pygame.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects("Paper - Scissor - Rock", normalText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 50, 150, 100, 40, bright_green, green, game_loop)
        button("QUIT!", 250, 150, 100, 40, bright_red, red, game_quit)

        pygame.display.update()
        clock.tick(15)

def game_loop():
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
                    cursor.execute("INSERT INTO GameRecords (P1Action, P2Action, Results) "
                                   "VALUES (%s, %s, %s);",
                                   (actionA, actionB, winner_display(whoWins(actionA, actionB))))
                    mydb.commit()
                    print("Record inserted successfully into GameRecords table.")
            ###


        gameDisplay.fill(white)
        playerA_display(actionA)
        playerB_display(actionB)
        winner_display(whoWins(actionA, actionB))


        pygame.display.update()
        clock.tick(30)

def game_quit():
    pygame.quit()
    quit()

game_intro()
if mydb.is_connected():
    mydb.close()