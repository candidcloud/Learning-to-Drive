"""
A script for implementing Q-learning with agentQ.py and plotting the results
of decreasing policy values over time.
"""

import agentQ
import matplotlib.pyplot as plt
import numpy as np
import time

agent = agentQ.Agent(policy = 0.45, lr = 0.2, discount = 0.2)
print("Created Agent")
y = []
session_epochs = 500
reduction = .1

fig,ax = plt.subplots(4, 1, figsize=(15,12), sharex=True)
fig.suptitle(r"Training Session ($\alpha$=" + f"{agent.lr}, " + r"$\gamma$=" +
             f"{agent.discount})" + f"\nPolicy Reduction of {reduction} per {session_epochs} epochs.", fontsize=20)

ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase I in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
ax[0].plot(x, m*x + c, color = 'r', linestyle='-.', label=f"Fitted line ({m:.3}x + {c:.3})")

ax[0].plot(y, label="Data")
ax[0].set_title(f"policy={agent.policy}")
ax[0].tick_params(labelsize=16)
ax[0].legend(loc=4)
ax[0].grid()

#-----------------------------------------------------------------------

agent.policy -= reduction
y = []
ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase II in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
ax[1].plot(x, m*x + c, color = 'r', linestyle='-.', label=f"Fitted line ({m:.3}x + {c:.3})")

ax[1].plot(y, label="Data")
ax[1].set_title(f"policy={agent.policy}")
ax[1].tick_params(labelsize=16)
ax[1].legend(loc=4)
ax[1].grid()

#-----------------------------------------------------------------------

agent.policy -= reduction
y = []
ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase III in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
ax[2].plot(x, m*x + c, color = 'r', linestyle='-.', label=f"Fitted line ({m:.3}x + {c:.3})")

ax[2].plot(y, label="Data")
ax[2].set_title(f"policy={agent.policy}")
ax[2].tick_params(labelsize=16)
ax[2].legend(loc=4)
ax[2].grid()

#-----------------------------------------------------------------------

agent.policy -= reduction
y = []
ts = time.time()
y.extend(agent.play(session_epochs))
tf = time.time()
print(f"Finished Phase IV in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
ax[3].plot(x, m*x + c, color = 'r', linestyle='-.', label=f"Fitted line ({m:.3}x + {c:.3})")

ax[3].plot(y, label="Data")
ax[3].set_title(f"policy={agent.policy}")
ax[3].tick_params(labelsize=16)
ax[3].set_xlabel('Epochs', fontsize=18)
ax[3].set_ylabel('Cumulative Reward', fontsize=18)
ax[3].legend(loc=4)
ax[3].grid()

plt.show(block=False)
print("Finished Training")
