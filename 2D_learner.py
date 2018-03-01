

#import libraries
from pygame import *
from random import *
import time

#variables
Actions = 4 # 0 = up, 1 = right, 2 = down, 3 = left
Alpha = 0.4
Gamma = 0.9
Epsilon = 9
episode = 0
Initial_state = 20
Walking_reward = -0.04
Width = 5
Height = 5

End_state_good = 3
End_state_bad = 2
Treasure_states = [4, 8, 10, 23]
Wall_states = [0, 13, 16]
Negative_states = [6, 17]

#make the Q matrix
Q_table = []
for i in range(Width*Height) :
    Q_table.append([])
    for j in range(Actions) :
        Q_table[i].append(0.0)

#gui setup
screen = display.set_mode((600, 600))
running = True

#function to find the max integer in a array
def max_in_ary (ary, index) :
    largest = -999
    largest_index = []
    
    for i in range(len(ary)) :
        if ary[i] > largest :
            largest = ary[i]
            largest_index = [i]
        elif ary[i] == largest :
            largest_index.append(i)

    if index == True :
        if (len(largest_index) > 1) :
            return largest_index[randint(0, len(largest_index)-1)] 
        else :
            return largest_index[0]
    else :
        return largest

#function to choose the action with highest reward given the state
def choose_action(s) :
    if randint(0, 9) < Epsilon :
        return max_in_ary(Q_table[s], True)
    else :
        return randint(0, 3)

#function to do the actions of the agent
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
                for k in range(len(Negative_states)) :
                    if j * Height + i == Negative_states[k] :
                        draw.rect(screen, (0, 255, 255), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 180, 180), (i*100 + 50, j*100 + 50, 100, 100), 3)

                hi = []
                for k in range(Actions) :
                    hi.append(Q_table[j*Height + i][k]*50 + 200)
                    if hi[k] < 0 :
                        hi[k] = 0

                draw.circle(screen, (hi[0], hi[0], hi[0]), (i*100+50 + 50, j*100 + 60), 7)
                draw.circle(screen, (hi[3], hi[3], hi[3]), (i*100+50 + 10, j*100 + 50 + 50), 7)
                draw.circle(screen, (hi[2], hi[2], hi[2]), (i*100+50 + 50, j*100 + 140), 7)
                draw.circle(screen, (hi[1], hi[1], hi[1]), (i*100+ 140, j*100 + 50 + 50), 7)

                for k in range(len(Wall_states)) :
                    if j * Height + i == Wall_states[k] :
                        draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)

    
    display.flip()

#main loop
while running :
    for action in event.get() :
        if action.type == QUIT:
            running = False
            break
        
    step_counter = 0
    S = Initial_state
    R = 0
    terminated = False

    while not terminated :
        A = choose_action(S)
        S_ = do_action(S, A)[0]
        R += do_action(S, A)[1]
        q_predict = Q_table[S][A]

        update_env(S)
        
        if S_ != 'terminal' :
            q_target = R + Gamma * max_in_ary(Q_table[S_], False)
        else :
            q_target = R
            terminated = True

        Q_table[S][A] += Alpha * (q_target - q_predict)
        S = S_
        step_counter += 1
        #time.sleep(0.1)

    #print(' Episode: ' + str(episode+1) + '  Steps: ' + str(step_counter) + '  Reward: ' + str(R))    
    print(R)
    episode = episode + 1

quit()
