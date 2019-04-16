import agentQ
import matplotlib.pyplot as plt
import numpy as np
import time

agent = agentQ.Agent(policy = 0.5, lr = 0.25, discount = 0.8)
print("Created Agent")
y = []
session_epochs = 1000

ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase I in {tf-ts:.3} seconds...")

agent.policy = 0.35
ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase II in {tf-ts:.3} seconds...")

agent.policy = 0.20
ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase III in {tf-ts:.3} seconds...")

agent.policy = 0.05
ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase IV in {tf-ts:.3} seconds...")

y = np.array(y)

fig,ax = plt.subplots(figsize=(15,12))
ax.plot(y)
ax.set_title("Training Session", fontsize=20)
ax.axvline(x=session_epochs, color='r')
ax.axvline(x=session_epochs*2, color='r')
ax.axvline(x=session_epochs*3, color='r')
ax.tick_params(labelsize=16)
ax.set_xlabel('Epochs', fontsize=18)
ax.set_ylabel('Cumulative Reward', fontsize=18)
ax.grid()
plt.show(block=False)
print("Finished Training")
