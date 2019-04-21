import agentQ
import matplotlib.pyplot as plt
import numpy as np

agent = agentQ.Agent()
print("Created Agent")
y = []
y.append(agent.play(1000))
print("Finished Phase I...")
agent.policy = .3
y.append(agent.play(1000))
print("Finished Phase II...")
agent.policy = .2
y.append(agent.play(1000))
print("Finished Phase III...")

y = np.array(y).flatten().T

plt.plot(y)
print("Finished Training")
