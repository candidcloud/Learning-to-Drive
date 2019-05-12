"""
A script for implementing Q-learning with agentQ.py and plotting the results
of decreasing policy values over time.
"""

import agentQ as Q00
import matplotlib.pyplot as plt
import numpy as np
import time

agent = Q00.Agent(policy = 0.45, lr = 0.25, discount = 0.25)
print("Created Agent")
y = []
session_episodes = 50
reduction = .1

# Plot fontsizes
general = 25
tiks = 22
legd = 16

# Make plot of data
fig,ax = plt.subplots(4, 1, figsize=(15,12), sharex=True)
fig.subplots_adjust(hspace=0.4)
fig.suptitle(r"Training Session ($\alpha$=" + f"{agent.lr}, " + r"$\gamma$=" +
             f"{agent.discount})" + f"\nPolicy Reduction of {reduction} over {session_episodes} episodes.", fontsize=general)

# Make plot of lines of best fit
fig2,ax2 = plt.subplots(1, 1, figsize=(15,12))
fig2.suptitle(r"Training Session ($\alpha$=" + f"{agent.lr}, " + r"$\gamma$=" +
             f"{agent.discount})" + f"\nPolicy Reduction of {reduction} over {session_episodes} episodes.", fontsize=general)
ax2.set_xlabel('Episodes', fontsize=general)
ax2.set_ylabel('Game Score', fontsize=general)
ax2.grid()
ax2.tick_params(labelsize=tiks)

ts = time.time()
y.extend(agent.play(session_episodes))
tf = time.time()
print(f"Finished Phase I in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m0, c0 = np.linalg.lstsq(A, y, rcond=None)[0]
ax[0].plot(x, m0*x + c0, color = 'r', linestyle='-.', label=f"Fitted line ({m0:.3}x + {c0:.3})")
ax2.plot(x, m0*x + c0, label=f"Fitted line ({m0:.3}x + {c0:.3})", linewidth=5.0)
ax[0].plot(y, label="Data")
ax[0].set_title(f"policy={agent.policy}", fontsize=general)
ax[0].tick_params(labelsize=tiks)
ax[0].legend(loc=4, fontsize=legd)
ax[0].grid()

#-----------------------------------------------------------------------

agent.policy -= reduction
y = []
ts = time.time()
y.extend(agent.play(session_episodes))
tf = time.time()
print(f"Finished Phase II in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m1, c1 = np.linalg.lstsq(A, y, rcond=None)[0]
ax[1].plot(x, m1*x + c1, color = 'r', linestyle='-.', label=f"Fitted line ({m1:.3}x + {c1:.3})")
ax2.plot(x, m1*x + c1, label=f"Fitted line ({m1:.3}x + {c1:.3})", linewidth=5.0)
ax[1].plot(y, label="Data")
ax[1].set_title(f"policy={agent.policy}", fontsize=general)
ax[1].tick_params(labelsize=tiks)
ax[1].legend(loc=4, fontsize=legd)
ax[1].grid()

#-----------------------------------------------------------------------

agent.policy -= reduction
y = []
ts = time.time()
y.extend(agent.play(session_episodes))
tf = time.time()
print(f"Finished Phase III in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m2, c2 = np.linalg.lstsq(A, y, rcond=None)[0]
ax[2].plot(x, m2*x + c2, color = 'r', linestyle='-.', label=f"Fitted line ({m2:.3}x + {c2:.3})")
ax2.plot(x, m2*x + c2, label=f"Fitted line ({m2:.3}x + {c2:.3})", linewidth=5.0)
ax[2].plot(y, label="Data")
ax[2].set_title(f"policy={agent.policy}", fontsize=general)
ax[2].tick_params(labelsize=tiks)
ax[2].legend(loc=4, fontsize=legd)
ax[2].grid()

#-----------------------------------------------------------------------

agent.policy -= reduction
y = []
ts = time.time()
y.extend(agent.play(session_episodes))
tf = time.time()
print(f"Finished Phase IV in {tf-ts:.3} seconds...")

y = np.array(y)
x = np.array(range(len(y)))
A = np.vstack([x, np.ones(len(x))]).T
m3, c3 = np.linalg.lstsq(A, y, rcond=None)[0]
ax[3].plot(x, m3*x + c3, color = 'r', linestyle='-.', label=f"Fitted line ({m3:.3}x + {c3:.3})")
ax2.plot(x, m3*x + c3, label=f"Fitted line ({m3:.3}x + {c3:.3})", linewidth=5.0)
ax[3].plot(y, label="Data")
ax[3].set_title(f"policy={agent.policy}", fontsize=general)
ax[3].tick_params(labelsize=tiks)
ax[3].set_xlabel('Episodes', fontsize=general)
ax[3].set_ylabel('Game Score', fontsize=general)
ax[3].legend(loc=4, fontsize=legd)
ax[3].grid()

plt.show(block=False)
print("Finished Training")

#-----------------------------------------------------------------------

plt.show(block=False)
