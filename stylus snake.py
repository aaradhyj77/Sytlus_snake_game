# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 23:53:41 2021

@author: dell
"""

import random
import pygame
import time
import numpy as np
import cv2 as cv
import sys
#captures the video from web cam0
cap = cv.VideoCapture(0)
#to check camera if open or not
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# Capturing the template of stylus
while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    
    cv.line(frame,(0,160),(639,160),(100,100,100),3)
    cv.line(frame,(0,320),(639,320),(100,100,100),3)
    cv.line(frame,(210,0),(210,479),(100,100,100),3)
    cv.line(frame,(430,0),(430,479),(100,100,100),3)
    cv.putText(frame,'Please put the stylus in the middle square and PRESS C to capture the stylus',(10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,255),1,cv.LINE_AA)
    cv.imshow('CAPTURING SCREEN',frame)
    if cv.waitKey(1) == ord('c'):
        break
    
temp=frame[170:310,240:410,:]
#cv.imshow('Template',temp)
#cap.release()

# Calculation of HSV limiting values
temp = cv.resize(temp,None,fx=0.1, fy=0.1, interpolation = cv.INTER_CUBIC)
hsv = cv.cvtColor(temp, cv.COLOR_BGR2HSV)
# crop the template to remove background
sam=hsv[2:12,5:12,:]
#H,S,V values are taken out separately
h=sam[:,:,:1]
s=sam[:,:,1:2]
v=sam[:,:,2:3]
#max and min H,S,V values are calculated
mi_h=h.min() 
mi_s=s.min()
mi_v=v.min()
ma_h=h.max()
ma_s=s.max()
ma_v=v.max()
mi_h=(int(mi_h/10))*10
ma_h=(int(ma_h/10+1))*10
mi_s=(int(mi_s/10))*10
ma_s=(int(ma_s/10+1))*10
mi_v=(int(mi_v/10))*10
ma_v=(int(ma_v/10+1))*10
lower=np.array([mi_h,mi_s,mi_v])
high=np.array([ma_h,ma_s,ma_v])
time.sleep(3)
"""
#captures the video from web cam0
cap = cv.VideoCapture(0)
#to check camera if open or not
if not cap.isOpened():
    print("Cannot open camera")
    exit()
"""
# Difficulty settings
# Easy      ->  8
# Medium    ->  15
# Hard      ->  20

difficulty = 5

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
#pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True



direction = 'RIGHT'
change_to = direction

score = 0
i,j,k=0,0,0
d=0
# fuction to gerarate hurdles
def hurdle(food_pos):
    hurdle_pos=[]
    if food_pos[1]+50<frame_size_y and food_pos[1]-50>0:
        if food_pos[0]-360>0:
            for i in range(-2,3):
                hurdle_pos.append([food_pos[0]-60,food_pos[1]+10*i])
        else :
            for i in range(-2,3):
                hurdle_pos.append([food_pos[0]+60,food_pos[1]+10*i])
    elif food_pos[0]+50<frame_size_y and food_pos[0]-50>0:
        if food_pos[1]-240>0:
            for i in range(-2,3):
                hurdle_pos.append([food_pos[0]+10*i,food_pos[1]-40])
        else :
            for i in range(-2,3):
                hurdle_pos.append([food_pos[0]+10*i,food_pos[1]+40]) 
    else:
        for i in range(-5,6):
                hurdle_pos.append([300+10*i,240])
       
    return hurdle_pos
#to generate initial hurdel
hurdle_pos=hurdle(food_pos)

# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('GAME OVER', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(7)
    #cap.release()
    pygame.quit()
    #cv.distroy_AllWindows()
    exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()



    
# Main logic
while True:
    
    k+=1
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    #this detect the only the cap or stylus
    mask = cv.inRange(hsv, lower, high)
    
    #coutours is calculated to find centroid of stylus
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(frame, contours, -1, (0,255,0), 3)
    
    if contours and cv.contourArea(max(contours,key=cv.contourArea)):
        c=max(contours,key=cv.contourArea)
        M=cv.moments(c)
        #x1 and y1 are coordinated of centroid
        x1=int(M['m10']/M['m00'])
        y1=int(M['m01']/M['m00'])
        # for value of i,j=, this will assign it a new value and at this frame drawing does not occurs
        if i==0 and j==0:
            i,j=x1,y1
        #to get the direction of stylus
        if k%10==0:
            score+=1
            if x1==i:
                if j-y1>60:
                    d=90                    
                elif y1-j>60:
                    d=270 
                                   
                i,j=x1,y1
                continue
            slope=(y1-j)/(x1-i)
            
            if slope<=0.466 and slope>=-0.466:
                if x1-i>80:
                    d=0                    
                elif i-x1>80:
                    d=180
                    
            elif slope<=-2.14 or slope>=3.73:
                if j-y1>60:
                    d=90                    
                elif y1-j>60:
                    d=270                    
            i,j=x1,y1
        
        if d==0:
            change_to="RIGHT"
        elif d==90:
            change_to="UP"
        elif d==180:
            change_to="LEFT"
        elif d== 270:
            change_to="DOWN"
    
        
        
    else:
        i,j=0,0
        # if coutour is not detected i,j will again be equal 0 , this will give us a perfect output
    
    
    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        hurdle_pos=hurdle(food_pos)
    food_spawn = True
    
    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # draw snak body
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake Fruit
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    # draw hurdle
    for pos in hurdle_pos:
        # same as in drawin the snake body
        pygame.draw.rect(game_window, blue , pygame.Rect(pos[0], pos[1], 10, 10))
    
    # Game Over conditions
    
    if snake_pos[0]<0 or snake_pos[0]>frame_size_x-10:
        game_over()
    if snake_pos[1]<0 or snake_pos[1]>frame_size_y-10:
        game_over()
    if snake_pos in hurdle_pos:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            break       
    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    
    #The frames is displayed to user
    
    
    cv.line(frame,(0,160),(639,160),(100,100,100),3)
    cv.line(frame,(0,320),(639,320),(100,100,100),3)
    cv.line(frame,(210,0),(210,479),(100,100,100),3)
    cv.line(frame,(430,0),(430,479),(100,100,100),3)
    cv.imshow('STYLUS SCREEN',frame)
    #user need to press 'q' to quit vertual pad
    if cv.waitKey(1) == ord('q'):
        break
game_over()
cap.release()
cv.distroy_AllWindows()