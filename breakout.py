#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:45:44 2020

@author: fabihahassan
"""

import pygame

#Initialize pygame
pygame.init()

#Set the screen size
screenSize = 960,540

# Screen
screen = pygame.display.set_mode(screenSize)


# Colours
grey = (211,211,211)
red = (255,0,0)
orange = (255,150,0)
green = (0,200,0)
yellow = (230, 230, 0)
blue = (0,100,255)
lightBlue = (0,150,255)
darkGrey = (50,50,50)

# Boundary
boundaryR = 890
boundaryL = 60
boundaryT = 60
boundaryB = 550

# Paddle
paddleX = 445
paddleY = 450
paddleHeight = 10
paddleWidth = 70
paddleMove = 0
paddleBound_L = 60
paddleBound_R = 900 - paddleWidth
vel = 0.7

#Ball
ballX = 475
ballY = 430
ballWidth = 10
ballHeight = 10    
velX = 0.3
velY = 0.3 

#List of Bricks
brickWidth = 40
brickHeight = 20
brickRow = []

#Font
font = pygame.font.Font('freesansbold.ttf', 32)
bigfont = pygame.font.Font('freesansbold.ttf', 60)

# Number of Lives
num_of_lives = 5
livesX = 800
livesY = 5

# Score count
num_of_points = 0
scoreX = 40
scoreY = 5

# Winner message
winX = 350
winY = 200
    
#Brick Class
class Brick(object):
    def __init__(self, colour, brickX, brickY):
        self.colour = colour
        self.brickX = brickX
        self.brickY = brickY
        
    def drawBrick(colour,brickX,brickY):  
        """ Draw the bricks """
        pygame.draw.rect(screen, colour, (brickX,brickY,brickWidth,brickHeight), 0)


# Walls (screen, colour, (x,y,width, height), thickness)
def walls():
    """ Draw the walls """
    #Top
    pygame.draw.rect(screen, grey, (40,40,880,20), 0)
    #Left
    pygame.draw.rect(screen, grey, (40,60,20,400), 0)
    #Right
    pygame.draw.rect(screen, grey, (900,60,20,400), 0)
    


# Draw the paddle   
def paddle(paddleX,paddleY):
    """ Draw the Paddle """
    pygame.draw.rect(screen, blue, (paddleX,paddleY,paddleWidth,paddleHeight), 0)
    
   

# ball movement and collisions 
def ball(ballX, ballY):
    """ Draw the ball """
    pygame.draw.rect(screen, blue, (ballX,ballY,ballWidth,ballHeight), 0)

    
def collisionPaddle():
    """ Detect collisions with the paddle"""
    dy = paddleY - ballY
    if dy <= 10 and dy >= -10:
        paddle_centreX = paddleX + (paddleWidth/2)
        dx = ballX - paddle_centreX
        if dx >= -45 and dx <= 35:
            return True, dx
    return False, False
        
def collisionBrick(brickX, brickY):
    """ Detect collisions with the bricks """
    if ballX >= bricks.brickX and ballX <= bricks.brickX + brickWidth:
        if ballY <= bricks.brickY:
            return True
    
#Rows of Bricks
def list_of_bricks(colour, row1, row2):
    """ Append to the list of bricks"""
    for brickX in range(60,880,brickWidth):
        bricks = Brick(colour, brickX, row1)
        brickRow.append(bricks)
        bricks = Brick(colour, brickX, row2)
        brickRow.append(bricks)
    return brickRow

        
list_of_bricks(red, 90, 110)
list_of_bricks(orange, 130, 150)
list_of_bricks(green, 170, 190)
list_of_bricks(yellow, 210, 230)


# Lives
def show_lives(x,y):
    """ show the lives"""
    lives = font.render("Lives: " + str(num_of_lives), True, grey)
    screen.blit(lives, (x, y)) 


# Score
def show_score(x,y):
    """Show the score"""
    score = font.render("Score: " + str(num_of_points), True, grey)
    screen.blit(score, (x, y))


# Winner
def winner(x,y):
    """ Show the winner message"""
    win = bigfont.render("YOU WON!", True, lightBlue)
    screen.blit(win, (x, y))


# MAIN LOOP

running = True

while running:
    

    # Constant background
    screen.fill(darkGrey)
    walls()
    show_lives(livesX, livesY) 
    show_score(scoreX, scoreY)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False              
            
        ## Keyboard paddle controls    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddleMove = -vel

            if event.key == pygame.K_RIGHT:
                paddleMove = vel

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddleMove = 0

  
    #Update bricks
    
    for bricks in brickRow:
        Brick.drawBrick(bricks.colour, bricks.brickX, bricks.brickY)  
        if collisionBrick(bricks.brickX, bricks.brickY):
            Brick.drawBrick(darkGrey, bricks.brickX, bricks.brickY)
            brickRow.remove(bricks)
            num_of_points += 5
            velY = -velY

             
    # Paddle Movement    
    paddle(paddleX, paddleY)
    paddleX += paddleMove
    
    # Paddle Boundary
    if paddleX <= paddleBound_L:
        paddleX = paddleBound_L
    if paddleX >= paddleBound_R:
        paddleX = paddleBound_R
        
    # Ball Movement
    ball(ballX,ballY)
    ballX += velX
    ballY -= velY    
        
    # Ball collisions with boundaries   
    if ballY <= boundaryT:
        velY = -velY      
        
    if ballX >= boundaryR:
        velX = -velX   
        
    if ballX <= boundaryL:
        velX = -velX  
        
    if ballY >= boundaryB:
        pygame.time.wait(700)
        ballX = 475
        ballY = 430 
        paddleX = 445
        paddleY = 450
        velX = 0.3
        velY = 0.3
        num_of_lives -= 1    
        
    # Ball collision with paddle   
    collision,dx = collisionPaddle()
    if collision == True:
        velY = -velY
        velX = dx/100
        
    #Player Loses    
    if num_of_lives == 0:
        velX = 0
        velY = 0
        exit()
        
    # Player Wins
    if len(brickRow) == 0:
        winner(winX, winY)
        velX = 0
        velY = 0
        exit()
        
    
    pygame.display.update() 

pygame.quit()