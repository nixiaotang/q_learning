

#import libraries
from pygame import *
from sys import *
from random import *
init()

#variables
actions = 4 # 0 = up, 1 = right, 2 = down, 3 = left
alpha = 0.5 #learning rate
eplison = 9
gamma = 0.9 #discount
episode = 0
initial_state = 20
walking_reward = -0.04
width = 5
height = 5
good_end = 3
bad_end = 2
positive_states = [4, 8, 10, 23]
negative_states = [6, 17]
wall_states = [0, 13, 16]
show_values = True

#make the Q matrix
Q_table = []
for i in range(width*height) :
    Q_table.append([])
    for j in range(actions) :
        Q_table[i].append(0.0)

#setup
screen = display.set_mode((600, 600))
running = True

#function to find the largest integer in a array
def maxQ (ary, index) :
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

#function to choose the action with highest value given the state
def choose_action(s) :
    if randint(0, 9) < eplison :
        return maxQ(Q_table[s], True)
    else :
        return randint(0, 3)

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

    for i in range(len(positive_states)) :
        if s_ == positive_states[i] :
            r += 0.04
    for i in range(len(negative_states)) :
        if s_ == negative_states[i] :
            r -= 0.04
    for i in range(len(wall_states)) :
        if s_ == wall_states[i] :
            s_ = s
    
    return s_, r

#function to draw the updated board
def update_env (s) :
    screen.fill((255, 255, 255))
    for i in range(width) :
        for j in range(height) :
            
            if j * height + i == s :
                draw.rect(screen, (0, 255, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (0, 180, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            elif j * height + i == good_end:
                draw.rect(screen, (255, 255, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (180, 180, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            elif j * height + i == bad_end:
                draw.rect(screen, (255, 0, 0), (i*100 + 50, j*100 + 50, 100, 100))
                draw.rect(screen, (180, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
            else :
                draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)

                for k in range(len(positive_states)) :
                    if j * height + i == positive_states[k] :
                        draw.rect(screen, (0, 0, 255), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 0, 180), (i*100 + 50, j*100 + 50, 100, 100), 3)
                for k in range(len(negative_states)) :
                    if j * height + i == negative_states[k] :
                        draw.rect(screen, (0, 255, 255), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 180, 180), (i*100 + 50, j*100 + 50, 100, 100), 3)
                        
                if show_values :
                    hi = []
                    for k in range(4) :
                        hi.append(Q_table[j*width + i][k]*50+200)
                        if hi[k] < 0 :
                            hi[k] = 0
                    
                    draw.circle(screen, (hi[0], hi[0], hi[0]), (i*100+50 + 50, j*100 + 60), 7)
                    draw.circle(screen, (hi[3], hi[3], hi[3]), (i*100+50 + 10, j*100 + 50 + 50), 7)
                    draw.circle(screen, (hi[2], hi[2], hi[2]), (i*100+50 + 50, j*100 + 140), 7)
                    draw.circle(screen, (hi[1], hi[1], hi[1]), (i*100+ 140, j*100 + 50 + 50), 7)

                for k in range(len(wall_states)) :
                    if j * height + i == wall_states[k] :
                        draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100))
                        draw.rect(screen, (0, 0, 0), (i*100 + 50, j*100 + 50, 100, 100), 3)
    
    display.flip()

#main loop
while running :
    for action in event.get() :
        if action.type == QUIT:
            running = False
            break
    S = initial_state
    R = 0
    terminated = False

    while not terminated :

        #init
        tempR = 0
        A = choose_action(S)
        S_, tempR = do_action(S, A)
        R += tempR
        q_predict = Q_table[S][A]
        
        #update board
        update_env(S)
        
        if S_ != 'end' :
            #Bellman Equation Q(s, a) = r+gamma maxQ(s')
            q_target = R + gamma * maxQ(Q_table[S_], False)
        else :
            q_target = R
            terminated = True

        #TD Learning Q(s, a) = Q(s, a) + alpha(r+gamma*maxQ(s') - Q(s, a))
        Q_table[S][A] += alpha * (q_target - q_predict)
        S = S_

    alpha = alpha/1.05

    #print(' Episode: ' + str(episode+1) + '  Reward: ' + str(R))    
    print("Episode " + str(episode) + "  Reward" + str(R) + '  Alpha' + str(alpha))
    
    episode = episode + 1

quit()
