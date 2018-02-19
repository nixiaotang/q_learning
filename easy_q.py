
#import libraries
from pygame import *
from random import *
import time

#variables
N_states = 6
Actions = 2 # 0 = left, 1 = right
Alpha = 0.1
Gamma = 0.9
Max_episodes = 15
Walking_reward = -0.04
Treasure_state = 5

#make the Q matrix
Q_table = []
for i in range(N_states) :
    Q_table.append([])
    for j in range(Actions) :
        Q_table[i].append(0.0)

#gui setup
screen = display.set_mode((500, 275))
running = True

#function to find the max integer in a array
def max_in_ary (ary, index) :
    largest = -1 
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
    return max_in_ary(Q_table[s], True)

#function to do the actions of the agent
def do_action(s, a) :
    r = Walking_reward
    s_ = s
    if a == 0 : #move left
        if s-1 >= 0 :
            s_ = s-1
    else : #move right
        if (s == Treasure_state - 1) :
            s_ = 'terminal'
            r += 1
        else :
            s_ = s + 1

    return s_, r

#draw the environment
def update_env(s):
    screen.fill((255, 255, 255))
    
    for i in range(N_states) :
        if i == s :
            draw.rect(screen, (0, 0, 255), (i*70 + 40, 100, 70, 70))
            draw.rect(screen, (0, 0, 180), (i*70 + 40, 100, 70, 70), 4)
        elif i == Treasure_state :
            draw.rect(screen, (255, 255, 0), (i*70 + 40, 100, 70, 70))
            draw.rect(screen, (180, 180, 0), (i*70 + 40, 100, 70, 70), 4)
        else :
            draw.rect(screen, (0, 0, 0), (i*70 + 40, 100, 70, 70), 3)
        
    display.update()

episode = 0

while running :
    for action in event.get() :
        if action.type == QUIT:
            running = False
            break
    step_counter = 0
    S = 0
    R = 0
    terminated = False

    while not terminated :
        time.sleep(0.1)
        update_env(S)

        A = choose_action(S)
        S_ = do_action(S, A)[0]
        R += do_action(S, A)[1]
        q_predict = Q_table[S][A]

        if S_ != 'terminal' :
            q_target = R + Gamma * max_in_ary(Q_table[S_], False)
        else :
            q_target = R
            terminated = True

        Q_table[S][A] += Alpha * (q_target - q_predict)
        S = S_
        step_counter += 1

    print(' Episode: ' + str(episode+1) + '  Steps: ' + str(step_counter) + '  Reward: ' + str(R))
    episode = episode + 1

quit()

