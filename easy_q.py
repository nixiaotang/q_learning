
#import libraries
from random import *
import time

#variables
N_states = 6
Actions = 2 # 0 = left, 1 = right
Alpha = 0.1
Gamma = 0.9
Max_episodes = 15
Walking_reward = -0.04

#make the Q matrix
Q_table = []
for i in range(N_states) :
    Q_table.append([])
    for j in range(Actions) :
        Q_table[i].append(0.0)

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
def action(s, a) :
    r = Walking_reward
    s_ = s
    if a == 0 : #move left
        if s-1 >= 0 :
            s_ = s-1
    else : #move right
        if (s == N_states - 2) :
            s_ = 'terminal'
            r += 1
        else :
            s_ = s + 1

    return s_, r


def update_env (s) :
    string = ''
    for i in range(N_states) :
        if i == N_states-1 :
            string += ('T')
        elif i == s and s != 'terminal' :
            string += ('o')
        else :
            string += ('-')
    
    return string



def main() :

    for episode in range(Max_episodes) :
        step_counter = 0
        S = 0
        R = 0
        terminated = False

        while not terminated :
            time.sleep(0.05)

            print(update_env(S))
            
            A = choose_action(S)
            S_ = action(S, A)[0]
            R += action(S, A)[1]
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



