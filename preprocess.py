"""Sample analyses."""

import json

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

import dallinger

# b2c86911-a372-2bc2-eb6f-1179ced58e9d
# d8f46512-efcb-6f3f-969c-84a6351621b0


def data2states(data):
    states = []
    timestamps = []
    for info in data.infos.list:
        if info[10] == "state":
            state = json.loads(info[13])
            states.append(state)
            timestamps.append(info[1])
    times = np.array([np.datetime64(t).astype("int64")/1e6 for t in timestamps])
    times = times - times.min()
    sorted_idx = np.argsort(times)
    times = np.sort(times)
    states = [states[sorted_idx[i]] for i in range(len(sorted_idx))]
    return (states, times)


def unique_player_ids(data):
    (states, timestamps) = data2states(data)
    ids = set()
    for i, state in enumerate(states):
        ids = ids.union(set(int(p["id"]) for p in state["players"]))
    return list(ids)


def timecourse_num_players(data):
    (states, times) = data2states(data)
    num_players = np.zeros(len(states))
    for i, state in enumerate(states):
        num_players[i] = len(state["players"])
    return (times, num_players)


def timecourse_player_scores(data):
    (states, times) = data2states(data)
    players = unique_player_ids(data)
    scores = np.zeros((len(states), len(players)))
    for i, state in enumerate(states):
        for player in state["players"]:
            scores[i, players.index(int(player["id"]))] = float(player["score"])
    return (times, scores)


def timecourse_player_positions(data):
    (states, times) = data2states(data)
    players = unique_player_ids(data)
    positions_x = np.zeros((len(states), len(players)))
    positions_y = np.zeros((len(states), len(players)))
    for i, state in enumerate(states):
        for player in state["players"]:
            player_id = players.index(int(player["id"]))
            positions_x[i, player_id] = player["position"][0]
            positions_y[i, player_id] = player["position"][1]

    return (times, positions_x, positions_y)


# Subplots of player positions over time:
# (times, positions_x, positions_y) = timecourse_player_positions(data)
# print(times)
# print(positions_x)
# print(positions_y)
# plt.xlim([0, 48])
# plt.ylim([0, 48])
# plt.axis("off")
#
# for i in range(positions_x.shape[1]):
#     plt.subplot(3, 5, i+1)
#     plt.plot(positions_x[:, i], positions_y[:, i], alpha=0.50)
# plt.show()

# # Plot score per player over time.
# (t, s) = timecourse_player_scores(data)
# plt.ylim([0, np.max(s)])
# plt.xlabel("Time")
# plt.ylabel("Score")
# for column in s.T:
#     plt.plot(t, column)
# plt.show()
#
# # Plot total collected resource over time.
# (t, s) = timecourse_player_scores(data)
# plt.ylim([0, 1000])
# plt.xlabel("Time")
# plt.ylabel("Total score")
# plt.plot(t, np.sum(s, axis=1))
# plt.show()
#
# # Plot the number of players over time.
# (t, n) = timecourse_num_players(data)
# plt.ylim([0, 20])
# plt.xlabel("Time")
# plt.ylabel("Number of players in game")
# plt.plot(t, n)
# plt.show()
