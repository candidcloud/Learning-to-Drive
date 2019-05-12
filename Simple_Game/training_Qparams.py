"""
A script for implementing Q-learning with agentQ.py and plotting the results
of decreasing policy values over time.
"""

import agentQ as Q00
import matplotlib.pyplot as plt
import numpy as np
import time

# Learning rate training

session_episodes = 1000
start_lr = 0.9
reduction = .2
y = []

# Plot fontsizes
general = 25
tiks = 22

fig1,ax1 = plt.subplots(figsize=(15,12))

for i in range(4):
    agent = Q00.Agent(policy = 0.25, lr = start_lr-i*reduction, discount = 0.2)
    print("Created Agent")
    ts = time.time()
    y.append(agent.play(session_episodes))
    tf = time.time()
    print(f"Finished Phase {i} in {tf-ts:.3} seconds...")
    y[i] = np.array(y[i])

    x = np.array(range(len(y[i])))
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y[i], rcond=None)[0]
    ax1.plot(x, m*x+c, linewidth=5.0, label=f"$\\alpha=${agent.lr}")

fig1.suptitle(r"Training Session (" + r"$\gamma=$" + f"{agent.discount}, " +
             r"$\epsilon=$" +  f"{agent.policy})" +
             f"\nLearning Rate reduction of {reduction} over {session_episodes} episodes.", fontsize=general)
ax1.set_xlabel('Episodes', fontsize=general)
ax1.set_ylabel('Game Score', fontsize=general)
ax1.tick_params(labelsize=tiks)
ax1.legend(loc=4, fontsize=tiks)
ax1.grid()
plt.show(block=False)

fig2,ax2 = plt.subplots(4, 1, figsize=(15,12), sharex=True)
fig2.subplots_adjust(hspace=0.4)
for i in range(4):
    ax2[i].plot(x, y[i])
    ax2[i].set_title(f"$\\alpha = {start_lr-i*reduction}$", fontsize=general)
    ax2[i].tick_params(labelsize=tiks)
    ax2[i].grid()

fig2.suptitle(r"Training Session (" + r"$\gamma=$" + f"{agent.discount}, " +
             r"$\epsilon=$" +  f"{agent.policy})" +
             f"\nLearning Rate Reduction of {reduction} over {session_episodes} episodes.", fontsize=general)
ax2[3].set_xlabel('Episodes', fontsize=general)
ax2[3].set_ylabel('Game Score', fontsize=general)
ax2[3].tick_params(labelsize=tiks)
plt.show(block=False)

#----------------------------------------------------------------------

# Discount rate training

session_episodes = 1000
start_discount = 0.9
reduction = .2
y = []

# Plot fontsizes
general = 25
tiks = 22

fig3,ax3 = plt.subplots(figsize=(15,12))

for i in range(4):
    agent = Q00.Agent(policy = 0.25, lr = 0.25, discount = start_discount-i*reduction)
    print("Created Agent")
    ts = time.time()
    y.append(agent.play(session_episodes))
    tf = time.time()
    print(f"Finished Phase {i} in {tf-ts:.3} seconds...")
    y[i] = np.array(y[i])

    x = np.array(range(len(y[i])))
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y[i], rcond=None)[0]
    ax3.plot(x, m*x+c, linewidth=5.0, label=f"$\\gamma=${agent.discount}")

fig3.suptitle(r"Training Session (" + r"$\alpha=$" + f"{agent.lr}, " +
             r"$\epsilon=$" +  f"{agent.policy})" +
             f"\nDiscount Rate Reduction of {reduction} over {session_episodes} episodes.", fontsize=general)
ax3.set_xlabel('Episodes', fontsize=general)
ax3.set_ylabel('Game Score', fontsize=general)
ax3.tick_params(labelsize=tiks)
ax3.legend(loc=4, fontsize=tiks)
ax3.grid()
plt.show(block=False)

fig4,ax4 = plt.subplots(4, 1, figsize=(15,12), sharex=True)
fig4.subplots_adjust(hspace=0.4)
for i in range(4):
    ax4[i].plot(x, y[i])
    ax4[i].set_title(f"$\\gamma = {start_lr-i*reduction}$", fontsize=general)
    ax4[i].tick_params(labelsize=tiks)
    ax4[i].grid()

fig4.suptitle(r"Training Session (" + r"$\alpha=$" + f"{agent.lr}, " +
             r"$\epsilon=$" +  f"{agent.policy})" +
             f"\nDiscount Rate Reduction of {reduction} over {session_episodes} episodes.", fontsize=general)
ax4[3].set_xlabel('Episodes', fontsize=general)
ax4[3].set_ylabel('Game Score', fontsize=general)
ax4[3].tick_params(labelsize=tiks)
plt.show(block=False)

print("Finished Training")
