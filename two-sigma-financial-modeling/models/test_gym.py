# - test_gym.py  is a file with the following content:
#

import kagglegym

env = kagglegym.make()
observation = env.reset()

print(len(observation.target))
print(len(observation.train))

n = 0
rewards = []
while True:
    target = observation.target
    target.loc[:, 'y'] = 0.01
    observation, reward, done, info = env.step(target)
    if done:
        break
    rewards.append(reward)
    n = n + 1

print(info)
print(n)
print(rewards[0:15])

