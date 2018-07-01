from myWorld import myEnv
import time
import numpy as np

env = myEnv()

eps = 0.2
np.random.seed(0)
initial_lr = 1.0 # Learning rate
min_lr = 0.003
rew = 0.0
q = np.zeros((30,30,30,30,900,4))

def ots(obs):
    e = 0
    mx = 0
    f = 0
    a = 0
    b = 0
    c = 0
    d = 0
    for i in range(30):
        for j in range(30):
            if obs[i][j][0] == 1:
                a = i
                b = j
            elif obs[i][j][1] == 1:
                e+=1
                if obs[i][j][2] + obs[i][j][3] > mx:
                    f += obs[i][j][2] + obs[i][j][3]
                    mx = obs[i][j][2] + obs[i][j][3]
                    c = i
                    d = j
        if e > 4:
            e = 4
        if f >= 40:
            f = 39
    return a,b,c,d,e

for it in range(10):
    obs = env.reset()
    a,b,c,d,e = ots(obs)

    rw = 0
    gamma = 1
    eta = max(min_lr, initial_lr * (0.85 ** (it // 100)))
    done = False
    while not done:
        a, b, c, d, e = ots(obs)

        if np.random.uniform(0, 1) < eps:
            action = np.random.choice(3)
        else:
            action = np.argmax(q[a][b][c][d][e])

        while not env.is_action_available(action):
            if np.random.uniform(0, 1) < eps:
                action = np.random.choice(3)
            else:
                action = np.argmax(q[a][b][c][d][e])
        obs,done,reward = env.execute(action)
        a1, b1, c1, d1, e1 = ots(obs)
        q[a][b][c][d][e][action] = q[a][b][c][d][e][action] + eta*(reward + gamma*np.max(q[a1][b1][c1][d1][e1]) - q[a][b][c][d][e][action])
        rw+=reward
    eps *= 0.8
    print(rw)


pol = np.argmax(q,axis=5)
for it in range(10):
    obs = env.reset()
    rw = 0
    gamma = 0.8
    eta = max(min_lr, initial_lr * (0.85 ** (it // 100)))
    done = False
    step = 0
    while not done:
        a,b,c,d,e = ots(obs)
        action = pol[a][b][c][d][e]
        obs, done, reward = env.execute(action)
        rw+= reward
        step += 1

    rew+=rw
print(rew/100.0)
obs = env.reset()
rw = 0
gamma = 0.8
eta = max(min_lr, initial_lr * (0.85 ** (it // 100)))
done = False
step = 0
while not done:
    a, b, c, d, e = ots(obs)
    print(a,b,c,d,e)
    action = pol[a][b][c][d][e]
    obs, done, reward = env.execute(action)
    rw += reward
    step += 1

rew += rw
