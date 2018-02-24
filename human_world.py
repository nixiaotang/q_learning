


#import important libraries
from pygame import *
from random import *
import time

#variables
Width = 5
Height = 5
Initial_state = 20
Walking_reward = -0.04
End_state_good = 3
End_state_bad = 2
Treasure_states = [4, 8, 10, 23]
Wall_states = [0, 13, 16]
Negative_states = [6, 17]
Episode = 0
S = Initial_state
R = 0

#gui settings
screen = display.set_mode((600, 600))
running = True

#function to do the action
def do_action(s, a) :
    r = 0
    r += Walking_reward
    s_ = s
    
    if a == 0 : #move up
        if s - Height >= 0 :
            s_ = s - Height
    elif a == 1 : #move right
        if (s + 1) % Width != 0 :
            s_ = s + 1
    elif a == 2 : #move down
        if s + Height <= Width*Height-1 :
            s_ = s + Height
    else : #move left
        if s % Width != 0 :
            s_ = s - 1

    if s_ == End_state_good :
        s_ = 'terminal'
        r += 1
    elif s_ == End_state_bad :
        s_ = 'terminal'
        r -= 1

    for i in range(len(Treasure_states)) :
        if s_ == Treasure_states[i] :
            r += 0.04
    for i in range(len(Wall_states)) :
        if s_ == Wall_states[i] :
            s_ = s
    for i in range(len(Negative_states)) :
        if s_ == Negative_states[i] :
            r-=0.04
    
    return s_, r

#function to draw the updated board
def update_env (s) :
    screen.fill((255, 255, 255))
    
    for i in range(Width) :
        for j in range(Height) :
            if j * Height + i == s :
                draw.rect(screen, (0, 255, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (0, 180, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            else :
                draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            '''elif j * Height + i == s :
                draw.rect(screen, (0, 255, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (0, 180, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            elif j * Height + i == End_state_good:
                draw.rect(screen, (255, 255, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (180, 180, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            elif j * Height + i == End_state_bad:
                draw.rect(screen, (255, 0, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (180, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            else :
                draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)

                for k in range(len(Treasure_states)) :
                    if j * Height + i == Treasure_states[k] :
                        draw.rect(screen, (0, 0, 255), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 0, 180), (i*100 + 50, j*100 + 50, 100, 100), 3)
                for k in range(len(Wall_states)) :
                    if j * Height + i == Wall_states[k] :
                        draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
                for k in range(len(Negative_states)) :
                    if j * Height + i == Negative_states[k] :
                        draw.rect(screen, (0, 255, 255), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 180, 180), (i*100 + 50, j*100 + 50, 100, 100), 3)
'''
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

            R = R + tempR
            S = S_
            print('Reward: ' + str(R))
    
    update_env(S)
    
    if S == 'terminal' :
        Episode += 1
        S = Initial_state
        print('End of Episode ' + str(Episode) + '  Total Reward: ' + str(R))
        R = 0

    
    display.flip()
quit()


