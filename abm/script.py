# --- imports --- #
from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import pandas as pd
import seaborn as sns
import random as rnd
import statistics as stat
import matplotlib.pyplot as plt

# --- classes --- #

class Agent:
    def __init__(self, id):
        self.assesment = 1 - rnd.random() # values in (0, 1]
        self.previous_assesment = self.assesment # later needed to make the assesments of all agents change simultaneously
        self.peers = set()
        self.id = id
    
    def __str__(self):
        return f"assesment: {self.assesment} and peers: {self.peers}"

    def __repr__(self):
        return f"(Agent [{self.id}]: {self.assesment:.2f}, {self.peers})"

    def update_peers(self, agent_list, epsilon):
        for potential_peer in agent_list:
            if (abs(potential_peer.assesment - self.assesment) < epsilon):
                self.peers.add(potential_peer)

class HGModel:
    def __init__(self, nagents=40, max_time=20, alpha=.75, epsilon=.1, tau=.4, noise=.1):
        self.nagents=40
        self.max_time=20
        self.alpha=.75
        self.epsilon=.1
        self.tau=.4
        self.noise=.1

    def print_agent_list(agent_list):
        print("[")
        for agent in agent_list:
            representation = f"    (Agent [{agent.id}]: {agent.assesment:.2f}, " + "{"
            representation += ", ".join(f"[{peer.id}]" for peer in agent.peers) + "})"
        
            print(representation)
        print("]")

    def run_simulation(self):
        data = []

        # let there be n agents with random initial assesments
        agents = []
        for i in range(self.nagents): # TODO: ist hier self.nagents ein tupel? Warum?
            agent = Agent(i)
            agents.append(agent)
            data.append([agent.id, 0, agent.assesment])

        # for each agent let there be a set of agents with similar assesments
        for i in range(self.nagents):
            agents[i].update_peers(agents, self.epsilon)

        # for each time step
        for u in range(1, self.max_time): # we did the fist step by setting everything up

            # update the assesment of each agent to a ratio between the agents assesments and the mean of their peers
            for agent in agents:

                # observing
                observation = np.random.normal(self.tau, self.noise) # random value from bell curve around tau with noise as 2 std deviations
                while observation <= 0 or observation > 1: # cutting off observations outside (0, 1]
                    observation = np.random.normal(self.tau, self.noise/2)
                observation *= (1 - self.alpha)

                # listening to peers
                collective_peer_assesment = self.alpha * stat.mean([peer.previous_assesment for peer in agent.peers])

                agent.assesment = observation + collective_peer_assesment
                data.append([agent.id, u, agent.assesment])

            # update each agents peers and prepare previous assesment for next loop
            for agent in agents:
                agent.update_peers(agents, self.epsilon)
                agent.previous_assesment = agent.assesment
        
        dataframe = pd.DataFrame(data, columns=["agent", "time", "assesment"])
        
        return dataframe


# TODO: this is probably prettier in another class
# --- global variables --- #

model = HGModel()

# --- functions --- #

def generate_data(nagents, max_time, alpha, epsilon, tau, noise):
    print(f"simulating...")
    return model.run_simulation()

def set_up_ui(root):
    # root window
    root.title("ABM")

    # frames
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    input_frame = ttk.Frame(main_frame)
    input_frame['borderwidth'] = 2
    input_frame['relief'] = 'raised'
    input_frame.grid(column=1, row=0, sticky=N, padx=4)

    # labels
    ttk.Label(input_frame, text="n agents").grid(column=0, row=0, sticky=W)
    ttk.Label(input_frame, text="max time").grid(column=0, row=1, sticky=W)
    ttk.Label(input_frame, text="alpha").grid(column=0, row=2, sticky=W)
    ttk.Label(input_frame, text="epsilon").grid(column=0, row=3, sticky=W)
    ttk.Label(input_frame, text="tau").grid(column=0, row=4, sticky=W)
    ttk.Label(input_frame, text="noise").grid(column=0, row=5, sticky=W)

    # input fields
    nagents = StringVar()
    nagents.set("40")
    nagents_entry = ttk.Entry(input_frame, width=20, textvariable=nagents)
    nagents_entry.grid(column=1, row=0, sticky=(W, E))

    max_time = StringVar()
    max_time.set("20")
    max_time_entry = ttk.Entry(input_frame, width=20, textvariable=max_time)
    max_time_entry.grid(column=1, row=1, sticky=(W, E))

    alpha = StringVar()
    alpha.set("0.75")
    alpha_entry = ttk.Entry(input_frame, width=20, textvariable=alpha)
    alpha_entry.grid(column=1, row=2, sticky=(W, E))

    epsilon = StringVar()
    epsilon.set("0.1")
    epsilon_entry = ttk.Entry(input_frame, width=20, textvariable=epsilon)
    epsilon_entry.grid(column=1, row=3, sticky=(W, E))

    tau = StringVar()
    tau.set("0.4")
    tau_entry = ttk.Entry(input_frame, width=20, textvariable=tau)
    tau_entry.grid(column=1, row=4, sticky=(W, E))

    noise = StringVar()
    noise.set("0.1")
    noise_entry = ttk.Entry(input_frame, width=20, textvariable=noise)
    noise_entry.grid(column=1, row=5, sticky=(W, E))    

    def simulate():
        figure = Figure(figsize=(6, 6))
        ax = figure.subplots()

        canvas = FigureCanvasTkAgg(figure, master=main_frame)  # A tk.DrawingArea.
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, main_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=1, column=0)

        canvas.get_tk_widget().grid(row=0, column=0, padx=4)

        data = generate_data( # TODO: die werte werden hier einmal gespeichert. sollen eigentlich jedes mal neu ausgelesen werden
            int(nagents.get()), # TODO: das programm hängt sich beim Beenden auf
            int(max_time.get()), 
            float(alpha.get()), 
            float(epsilon.get()), 
            float(tau.get()), 
            float(noise.get())
        )
        
        ax.clear()

        plt.clf()
        sns.set_theme()
        sns.lineplot(
            data=data,
            x="time", y="assesment", hue="agent", ax=ax)

        canvas.draw()

    ttk.Button(input_frame, text="SIMULATE!", command=simulate).grid(column=0, row=10)

    for child in input_frame.winfo_children(): 
        child.grid_configure(padx=20, pady=5)

# --- main code --- #
root = Tk()
set_up_ui(root)
root.mainloop()