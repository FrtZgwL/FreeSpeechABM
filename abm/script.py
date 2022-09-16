# --- imports --- #
from ast import match_case
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
import random
from enum import Enum, auto

# --- classes --- #

class Mode(Enum):
    NO_SILENCING = auto()
    RANGE = auto()
    RATIO = auto()
    TRESHOLD = auto()

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

class HGModel:
    def __init__(
            self, mode=Mode.NO_SILENCING, nagents=40, max_time=20, alpha=.75, epsilon=.1, tau=.4, noise=.1,
            range_from=.0, range_to=.2, silenced_ratio=.2, silencing_treshold=.2, trust_in_mainstream=True
        ):

        self.nagents = nagents 
        self.max_time = max_time 
        self.alpha = alpha 
        self.epsilon = epsilon 
        self.tau = tau 
        self.noise = noise 
        
        self.mode=mode

        self.range_from = range_from
        self.range_to = range_to
        self.silenced_ratio = silenced_ratio
        self.silencing_threshold = silencing_treshold
        self.trust_in_mainstream = trust_in_mainstream

    def update_peers(self, agent, agent_list):
        match self.mode:
            case Mode.NO_SILENCING:
                for potential_peer in agent_list:
                    if (abs(potential_peer.assesment - agent.assesment) < self.epsilon):
                        agent.peers.add(potential_peer)
            
            case Mode.RANGE:
                mainstream = set()
                silenced = set()

                # separating agents into mainstream and silenced based on given range
                for potential_peer in agent_list:
                    if (potential_peer.assesment >= self.range_from or potential_peer.assesment <= self.range_to):
                        silenced.add(potential_peer)
                    else:
                        mainstream.add(potential_peer)
                
                # updating peers based on mainstream and silenced
                if self.trust_in_mainstream or agent in mainstream:
                    for potential_peer in mainstream.union({agent}): # agents will always treat themselves as peers
                        if abs(potential_peer.assesment - agent.assesment) < self.epsilon:
                            agent.peers.add(potential_peer)
                else: # agents will only listen to silenced if they are silenced and not trusting in mainstream
                    for potential_peer in silenced:
                        if abs(potential_peer.assesment - agent.assesment) < self.epsilon:
                            agent.peers.add(potential_peer)

            case Mode.RATIO:
                print("wip: simulationg RATIO")

            case Mode.TRESHOLD:
                print("wip: simulationg TRESHOLD")

    # useful for debugging
    def print_agent_list(agent_list):
        print("[")
        for agent in agent_list:
            representation = f"    (Agent [{agent.id}]: {agent.assesment:.2f}, " + "{"
            representation += ", ".join(f"[{peer.id}]" for peer in agent.peers) + "})"
        
            print(representation)
        print("]")

    def run_simulation(self):
        print(f"running simulation in mode {self.mode}...") # TODO: why don't we arrive here?

        data = []

        # let there be n agents with random initial assesments
        agents = []
        for i in range(self.nagents): # TODO: can't I just loop over the list?
            agent = Agent(i)
            agents.append(agent)
            data.append([agent.id, 0, agent.assesment])

        # for each agent let there be a set of peers.
        # depending on restrictions on free speech agents will be limited in who 
        # they accept as peers. 
        for i in range(self.nagents): # TODO: can't I just loop over the list?
            self.update_peers(agents[i], agents)

        # for each time step
        for u in range(1, self.max_time + 1): # we did step 0 by setting everything up 
                # and we want to include the step of max_time

            # update the assesment of each agent to a ratio between the agents assesments and the mean of their peers
            for agent in agents:

                # observing
                observation = np.random.normal(self.tau, self.noise) # random value from bell curve around tau with noise as std deviation
                # while observation <= 0 or observation > 1: # cutting off observations outside (0, 1]
                #    observation = np.random.normal(self.tau, self.noise/2)
                observation *= (1 - self.alpha)

                # listening to peers
                collective_peer_assesment = self.alpha * stat.mean([peer.previous_assesment for peer in agent.peers])

                agent.assesment = observation + collective_peer_assesment
                data.append([agent.id, u, agent.assesment])

            # update each agents peers and prepare previous assesment for next loop
            for agent in agents:
                self.update_peers(agent, agents)
                agent.previous_assesment = agent.assesment
        
        dataframe = pd.DataFrame(data, columns=["agent", "time", "assesment"])
        
        return dataframe

class GUIApplication:
    # --- static functions --- #

    def clear_axes(self, axes):
        axes.clear()
        axes.set_ylim(0, 1)
        axes.set_xlim(0, int(self.max_time.get()))
        axes.grid(True, color="1")
        axes.set_facecolor("0.95")
        axes.set_ylabel("assesment")
        axes.set_xlabel("time")

    # --- class methods --- #

# asks the HGModel to run a simulation an plots the received data
    def simulate(self): 
        # update Hegselmann Krause values
        nagents = int(self.nagents.get())
        self.model.nagents = int(self.nagents.get())

        max_time = int(self.max_time.get())
        self.model.max_time = int(self.max_time.get())

        tau = float(self.tau.get())
        self.model.tau = float(self.tau.get())

        self.model.alpha = float(self.alpha.get())
        self.model.epsilon = float(self.epsilon.get())
        
        self.model.noise = float(self.noise.get())

        # update free speech values
        print(f"planning to run simulation with restriction type {self.restr_type.get()}")
        match self.restr_type.get():
            case "no restriction":
                self.model.mode = Mode.NO_SILENCING

            case "arbitrary silencing":
                self.model.mode = Mode.RATIO

            case "belief range":
                self.model.mode = Mode.RANGE

            case "unpopular_beliefs":
                self.model.mode = Mode.TRESHOLD

        print(self.range_from.get())

        self.model.range_from = self.range_from.get()
        self.model.range_to = self.range_to.get()
        self.model.silenced_ratio = self.silenced_ratio.get()
        self.model.silencing_threshold = self.silencing_threshold.get()
        self.model.trust_in_mainstream = True # TODO: add to gui

        data = self.model.run_simulation()

        # build numpy arrays from the pandas DataFrame
        time_x = np.linspace(0, max_time, max_time+1)
        agent_y_values = []

        for i in range(nagents):
            next_values = data[data["agent"] == i]["assesment"].values
            agent_y_values.append(next_values)
        
        self.clear_axes(self.axes)

        for i in range(nagents - 1):
            color = str(random.random() * .8)
            self.axes.plot(time_x, agent_y_values[i], color)
        self.axes.plot(time_x, agent_y_values[nagents - 1], ".4", label="agents") # label one agent plot line

        tau_y_values = np.linspace(tau, tau, max_time+1)
        self.axes.plot(time_x, tau_y_values, "#ed4e42", label="tau")
        self.axes.legend(loc=0)

        self.plotting_canvas.draw()

    def __init__(self):
        # the GUIApplication needs an instance of the model in order to 
        # run simulations on button click
        self.model = HGModel()

        # root window
        self.root = Tk()
        self.root.title("ABM")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # hg_orig_frame['borderwidth'] = 2
        # hg_orig_frame['relief'] = 'raised'

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid()

        # building the input area
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(column=1, row=0, sticky=N)

            # Hegselmann-Krause area
        hg_frame = ttk.Frame(input_frame)
        hg_frame.grid(column=0, row=0, sticky=(N, E, W))
        hg_frame["borderwidth"] = 2
        hg_frame['relief'] = 'groove'

        ttk.Label(hg_frame, text="Hegselmann-Krause parameters").grid(column=0, row=0)

        hg_smaller_frame = ttk.Frame(hg_frame)
        hg_smaller_frame.grid(column=0, row=1, sticky=(N, E, W))

        ttk.Label(hg_smaller_frame, text="n agents").grid(column=0, row=0, sticky=W)
        self.nagents = StringVar()
        self.nagents.set("40")
        nagents_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.nagents)
        nagents_entry.grid(column=1, row=0, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="max time").grid(column=0, row=1, sticky=W)
        self.max_time = StringVar()
        self.max_time.set("20")
        max_time_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.max_time)
        max_time_entry.grid(column=1, row=1, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="alpha").grid(column=0, row=2, sticky=W)
        self.alpha = StringVar()
        self.alpha.set("0.75")
        alpha_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.alpha)
        alpha_entry.grid(column=1, row=2, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="epsilon").grid(column=0, row=3, sticky=W)
        self.epsilon = StringVar()
        self.epsilon.set("0.1")
        epsilon_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.epsilon)
        epsilon_entry.grid(column=1, row=3, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="tau").grid(column=0, row=4, sticky=W)
        self.tau = StringVar()
        self.tau.set("0.4")
        tau_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.tau)
        tau_entry.grid(column=1, row=4, sticky=(W, E), padx=5, pady=3)

        ttk.Separator(hg_smaller_frame, orient='horizontal').grid(
            column=0, row=5, columnspan=2, sticky=(E, W), pady=5
        )

        ttk.Label(hg_smaller_frame, text="noise").grid(column=0, row=6, sticky=W)

        self.noise = StringVar()
        self.noise.set("0.1")
        noise_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.noise)
        noise_entry.grid(column=1, row=6, sticky=(W, E), padx=5, pady=3)

            # free speech area
        fs_frame = ttk.Frame(input_frame)
        fs_frame["borderwidth"] = 2
        fs_frame['relief'] = 'groove'
        fs_frame.grid(column=0, row=1, sticky=(N, E, W), pady=10)

        ttk.Label(fs_frame, text="Restrictions on Free Speech").grid(column=0, row=0)

        fs_smaller_frame = ttk.Frame(fs_frame)
        fs_smaller_frame.grid(column=0, row=1)

        self.restr_type = StringVar() # TODO: rename to mode
        restr_type_box = ttk.Combobox(fs_smaller_frame, textvariable=self.restr_type, width=20)
        restr_type_box.grid(column=0, row=0, columnspan=2, sticky=(W, E), pady=7, padx=5)
        restr_type_box["values"] = ("no restriction", "belief range", "arbitrary silencing", "unpopular_beliefs")
        restr_type_box.state(["readonly"])

        ttk.Label(fs_smaller_frame, text="range from").grid(column=0, row=1, sticky=W)
        self.range_from = DoubleVar()
        self.range_from.set(0.0)
        range_from_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.range_from, state="readonly")
        range_from_entry.grid(column=1, row=1, sticky=(W, E), padx=5, pady=3)

        ttk.Label(fs_smaller_frame, text="range to").grid(column=0, row=2, sticky=W)
        self.range_to = DoubleVar()
        self.range_to.set(0.2)
        range_to_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.range_to, state="readonly")
        range_to_entry.grid(column=1, row=2, sticky=(W, E), padx=5, pady=3)

        ttk.Label(fs_smaller_frame, text="silenced ratio").grid(column=0, row=3, sticky=W)
        self.silenced_ratio = DoubleVar()
        self.silenced_ratio.set(0.3)
        silenced_ratio_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.silenced_ratio, state="readonly")
        silenced_ratio_entry.grid(column=1, row=3, sticky=(W, E), padx=5, pady=3)

        ttk.Label(fs_smaller_frame, text="silencing threshold").grid(column=0, row=4, sticky=W)
        self.silencing_threshold = DoubleVar()
        self.silencing_threshold.set(0.3)
        silencing_threshold_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.silencing_threshold, state="readonly")
        silencing_threshold_entry.grid(column=1, row=4, sticky=(W, E), padx=5, pady=3)
        

        # gray out other options when restriction type changes
        def restr_type_change(event):
            for entry in [range_from_entry, range_to_entry, silenced_ratio_entry, silencing_threshold_entry]:
                entry["state"] = "readonly"

            selection = self.restr_type.get()
            match selection:
                # in case of "no restriction" all entries stay disabled
                case "arbitrary silencing":
                    silenced_ratio_entry["state"] = "enabled"

                case "belief range":
                    range_from_entry["state"] = "enabled"
                    range_to_entry["state"] = "enabled"

                case "unpopular_beliefs":
                    silencing_threshold_entry["state"] = "enabled"

            return
        restr_type_box.bind('<<ComboboxSelected>>', restr_type_change)

            # simbutton
        ttk.Button(input_frame, text="SIMULATE!", command=self.simulate).grid(
            column=0, row=10, sticky=(E, W))
        

        # building the plotting canvas
        self.figure = plt.figure(figsize=(5, 5))
        self.plotting_canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.plotting_canvas.draw()
        
        self.axes = self.figure.add_axes([.1, .1, .9, .9])
        self.clear_axes(self.axes)
        
        self.toolbar = NavigationToolbar2Tk(self.plotting_canvas, main_frame, pack_toolbar=False)
        self.toolbar.update()
        
        self.toolbar.grid(row=1, column=0)
        self.plotting_canvas.get_tk_widget().grid(row=0, column=0, padx=4)

        for child in hg_frame.winfo_children(): 
            child.grid_configure(padx=20, pady=5)

    def quit(self):
        print('quit')
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()
    







# --- main code --- #

my_abm_app = GUIApplication()
my_abm_app.run()