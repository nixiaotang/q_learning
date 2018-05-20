


#import important libraries
from pygame import *
from random import *

#variables
width = 5
height = 5
initial_state = 20
walking_reward = -0.04
good_end = 3
bad_end = 2
treasure_states = [4, 8, 10, 23]
wall_states = [0, 13, 16]
negative_states = [6, 17]
episode = 0
S = initial_state
S_ = S
R = 0

#gui settings
screen = display.set_mode((600, 600))
running = True

#function to do the action
def do_action(s, a) :
    r = 0
    r += walking_reward
    s_ = s
    
    if a == 0 : #move up
        if s - height >= 0 :
            s_ = s - height
    elif a == 1 : #move right
        if (s + 1) % width != 0 :
            s_ = s + 1
    elif a == 2 : #move down
        if s + height <= width*height-1 :
            s_ = s + height
    else : #move left
        if s % width != 0 :
            s_ = s - 1

    if s_ == good_end :
        s_ = 'end'
        r += 1
    elif s_ == bad_end :
        s_ = 'end'
        r -= 1

    for i in range(len(treasure_states)) :
        if s_ == treasure_states[i] :
            r += 0.04
    for i in range(len(wall_states)) :
        if s_ == wall_states[i] :
            s_ = s
    for i in range(len(negative_states)) :
        if s_ == negative_states[i] :
            r-=0.04
    
    return s_, r

#function to draw the updated board
def update(s) :
    screen.fill((255, 255, 255))
    
    for i in range(width) :
        for j in range(height) :
            if j * height + i == s :
                draw.rect(screen, (0, 255, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (0, 180, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            else :
                draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            
#main loop
while running :
    for action in event.get() :
        if action.type == QUIT:
            running = False
            break
        elif action.type == KEYDOWN :
            tempR = 0
            if action.key == K_UP :
                S_, tempR = do_action(S, 0)
            if action.key == K_RIGHT:
                S_, tempR = do_action(S, 1)
            elif action.key == K_DOWN:
                S_, tempR = do_action(S, 2)
            elif action.key == K_LEFT:
                S_, tempR = do_action(S, 3)

            R += tempR
            S = S_
            print('Reward: ' + str(R))
    
    update(S)
    
    if S == 'end' :
        episode += 1
        S = initial_state
        print('End of Episode ' + str(episode) + '  Total Reward: ' + str(R))
        R = 0

    
    display.flip()
quit()
