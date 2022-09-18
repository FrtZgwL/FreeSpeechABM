# --- imports --- #
from ast import match_case
from tkinter import *
from tkinter import ttk
from tokenize import Double

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
        self.assesment = 1 - random.random() # values in (0, 1]
        self.previous_assesment = self.assesment # later needed to make the assesments of all agents change simultaneously
        self.peers = set()
        self.id = id
    
    def __str__(self):
        return f"assesment: {self.assesment} and peers: {self.peers}"

    def __repr__(self):
        return f"(Agent [{self.id}]: {self.assesment:.2f})"

class HGModel:
    def __init__(
            self, mode=Mode.NO_SILENCING, nagents=40, max_time=20, alpha=.75, epsilon=.1, tau=.4, noise=.1,
            range_from=.0, range_to=.2, silenced_ratio=.2, silencing_treshold=.2, trust_in_mainstream=True, keep_seed=False
        ):

        self.nagents = nagents 
        self.max_time = max_time 
        self.alpha = alpha 
        self.epsilon = epsilon 
        self.tau = tau 
        self.noise = noise 
        
        self.mode=mode
        self.keep_seed=keep_seed

        self.range_from = range_from
        self.range_to = range_to
        self.silenced_ratio = silenced_ratio
        self.silencing_threshold = silencing_treshold
        self.trust_in_mainstream = trust_in_mainstream

        self.silenced_group = set()
        self.mainstream_group = set()

        self.current_seed = (
            "Fliehe, mein Freund, in deine Einsamkeit und dorthin, wo eine rauhe, starke Luft weht."
            + " Nicht ist es dein Loos, Fliegenwedel zu sein. —"
        )
        random.seed(self.current_seed)

    def update_peers(self, agent, agent_list):
        agent.peers = set()
        mainstream = set()
        silenced = set()


        if self.mode == Mode.NO_SILENCING:
            for potential_peer in agent_list:
                if (abs(potential_peer.assesment - agent.assesment) < self.epsilon):
                    agent.peers.add(potential_peer)

        else:
            match self.mode:
                case Mode.RANGE:
                    in_range = set()
                    out_of_range = set()

                    # separating agents based on given range TODO: this does not need to be redone for every single agent
                    for potential_peer in agent_list:
                        if (potential_peer.assesment >= self.range_to or potential_peer.assesment <= self.range_from):
                            out_of_range.add(potential_peer)
                        else:
                            in_range.add(potential_peer)
                    
                    # updating peers based separation
                    mainstream = out_of_range
                    silenced = in_range

                case Mode.RATIO:
                    # these groups don't need to change with every updating of peers
                    # since they represent innate characteristics 
                    mainstream = self.mainstream_group 
                    silenced = self.silenced_group

                case Mode.TRESHOLD:
                    popularity_ranking = agent_list.copy()

                    # the higher the mean distance of one agents assesment to those of the others, 
                    # the less popular the agents assesment
                    def unpopularity(agent):
                        distances = [
                            abs(agent.assesment - other_agent.assesment) for other_agent in agent_list
                        ]
                        return(stat.mean(distances))
                    
                    popularity_ranking.sort(key=unpopularity)
                    popularity_ranking.reverse() # the list should start with the least popular agents

                    last_unpopular_agent = round(self.silencing_threshold * self.nagents)
                    mainstream = set(popularity_ranking[last_unpopular_agent:])
                    silenced = set(popularity_ranking[:last_unpopular_agent])

            if self.trust_in_mainstream or agent in mainstream:
                for potential_peer in mainstream.union({agent}): # agents will always treat themselves as peers
                    if abs(potential_peer.assesment - agent.assesment) < self.epsilon:
                        agent.peers.add(potential_peer)
            else: # agents will only listen to silenced if they are silenced and not trusting in mainstream
                for potential_peer in silenced:
                    if abs(potential_peer.assesment - agent.assesment) < self.epsilon:
                        agent.peers.add(potential_peer)
        
        # ^print(f"mainstream: {mainstream}\nsilenced{silenced}")

    # useful for debugging
    def print_agent_list(agent_list):
        print("[")
        for agent in agent_list:
            representation = f"    (Agent [{agent.id}]: {agent.assesment:.2f}, " + "{"
            representation += ", ".join(f"[{peer.id}]" for peer in agent.peers) + "})"
        
            print(representation)
        print("]")

    def run_simulation(self):
        if not self.keep_seed:
            self.current_seed = random.Random().random()
        random.seed(self.current_seed)

        data = []

        # let there be n agents with random initial assesments
        agent_list = []
        for i in range(self.nagents):
            agent = Agent(i)
            agent_list.append(agent)
            data.append([agent.id, 0, agent.assesment])

        if self.mode.RATIO:
            silenced_amount = round(self.nagents * self.silenced_ratio)
            self.silenced_group = set(agent_list[:silenced_amount])
            self.mainstream_group = set(agent_list) - self.silenced_group

        # for each agent let there be a set of peers.
        # depending on restrictions on free speech agents will be limited in who 
        # they accept as peers. 
        for agent in agent_list:
            self.update_peers(agent, agent_list)

        # for each time step
        for u in range(1, self.max_time + 1): # we did step 0 by setting everything up 
                # and we want to include the step of max_time

            # update the assesment of each agent to a ratio between the agents assesments and the mean of their peers
            for agent in agent_list:

                # observing
                observation = random.gauss(self.tau, self.noise) # random value from bell curve around tau with noise as std deviation
                # while observation <= 0 or observation > 1: # cutting off observations outside (0, 1]
                #    observation = random.gauss(self.tau, self.noise/2)
                observation *= (1 - self.alpha)

                # listening to peers
                collective_peer_assesment = self.alpha * stat.mean([peer.previous_assesment for peer in agent.peers])

                agent.assesment = observation + collective_peer_assesment
                data.append([agent.id, u, agent.assesment])

            # update each agents peers and prepare previous assesment for next loop
            for agent in agent_list:
                self.update_peers(agent, agent_list)
                agent.previous_assesment = agent.assesment
        
        dataframe = pd.DataFrame(data, columns=["agent", "time", "assesment"])
        
        return dataframe

class GUIApplication:
    def clear_axes(self, axes):
        axes.clear()
        axes.set_ylim(0, 1)
        axes.set_xlim(0, self.max_time.get())
        axes.grid(True, color="1")
        axes.set_facecolor("0.95")
        axes.set_ylabel("assesment")
        axes.set_xlabel("time")

# asks the HGModel to run a simulation an plots the received data
    def simulate(self): 
        # update Hegselmann Krause values
        self.model.nagents = self.nagents.get()
        self.model.max_time = self.max_time.get()
        self.model.tau = self.tau.get()
        self.model.alpha = self.alpha.get()
        self.model.epsilon = self.epsilon.get()
        self.model.noise = self.noise.get()
        self.model.keep_seed = self.keep_seed.get()

        # update free speech values
        match self.restr_type.get():
            case "no restriction":
                self.model.mode = Mode.NO_SILENCING

            case "arbitrary silencing":
                self.model.mode = Mode.RATIO

            case "belief range":
                self.model.mode = Mode.RANGE

            case "unpopular_beliefs":
                self.model.mode = Mode.TRESHOLD
        print(f"planning to run simulation with restriction type {self.restr_type.get()}, {self.model.mode}")

        self.model.range_from = self.range_from.get()
        self.model.range_to = self.range_to.get()
        self.model.silenced_ratio = self.silenced_ratio.get()
        self.model.silencing_threshold = self.silencing_threshold.get()
        self.model.trust_in_mainstream = self.trust_in_mainstream.get()

        data = self.model.run_simulation()

        # build numpy arrays from the pandas DataFrame
        time_x = np.linspace(0, self.model.max_time, self.model.max_time+1)
        agent_y_values = []

        for i in range(self.model.nagents):
            next_values = data[data["agent"] == i]["assesment"].values
            agent_y_values.append(next_values)
        
        self.clear_axes(self.axes)

        for i in range(self.model.nagents - 1):
            color = str(random.random() * .8)
            self.axes.plot(time_x, agent_y_values[i], color)
        self.axes.plot(time_x, agent_y_values[self.model.nagents - 1], ".4", label="agents") # label one agent plot line

        tau_y_values = np.linspace(self.model.tau, self.model.tau, self.model.max_time+1)
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
        self.nagents = IntVar()
        self.nagents.set("40")
        nagents_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.nagents)
        nagents_entry.grid(column=1, row=0, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="max time").grid(column=0, row=1, sticky=W)
        self.max_time = IntVar()
        self.max_time.set("20")
        max_time_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.max_time)
        max_time_entry.grid(column=1, row=1, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="alpha").grid(column=0, row=2, sticky=W)
        self.alpha = DoubleVar()
        self.alpha.set("0.75")
        alpha_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.alpha)
        alpha_entry.grid(column=1, row=2, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="epsilon").grid(column=0, row=3, sticky=W)
        self.epsilon = DoubleVar()
        self.epsilon.set("0.1")
        epsilon_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.epsilon)
        epsilon_entry.grid(column=1, row=3, sticky=(W, E), padx=5, pady=3)

        ttk.Label(hg_smaller_frame, text="tau").grid(column=0, row=4, sticky=W)
        self.tau = DoubleVar()
        self.tau.set("0.42")
        tau_entry = ttk.Entry(hg_smaller_frame, width=20, textvariable=self.tau)
        tau_entry.grid(column=1, row=4, sticky=(W, E), padx=5, pady=3)

        ttk.Separator(hg_smaller_frame, orient='horizontal').grid(
            column=0, row=5, columnspan=2, sticky=(E, W), pady=5
        )

        ttk.Label(hg_smaller_frame, text="noise").grid(column=0, row=6, sticky=W)

        self.noise = DoubleVar()
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

        self.restr_type = StringVar()
        self.restr_type.set("--- type of restriction ---")
        restr_type_box = ttk.Combobox(fs_smaller_frame, textvariable=self.restr_type, width=20)
        restr_type_box.grid(column=0, row=0, columnspan=2, sticky=(W, E), pady=7, padx=5)
        restr_type_box["values"] = ("no restriction", "belief range", "arbitrary silencing", "unpopular_beliefs")
        restr_type_box.state(["readonly"])

        self.trust_in_mainstream = BooleanVar()
        self.trust_in_mainstream.set(True)
        trust_in_mainstream_button = ttk.Checkbutton(fs_smaller_frame, variable=self.trust_in_mainstream,
            onvalue=True, offvalue=False, text="silenced agents keep trust in mainstream")
        trust_in_mainstream_button.state(["disabled"])
        trust_in_mainstream_button.grid(column=0, row=1, columnspan=2, padx=5, pady=3, sticky=W)

        ttk.Label(fs_smaller_frame, text="range from").grid(column=0, row=2, sticky=W, padx=5)
        self.range_from = DoubleVar()
        self.range_from.set(0.0)
        range_from_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.range_from, state="disabled")
        range_from_entry.grid(column=1, row=2, sticky=(W, E), padx=5, pady=3)

        ttk.Label(fs_smaller_frame, text="range to").grid(column=0, row=3, sticky=W, padx=5)
        self.range_to = DoubleVar()
        self.range_to.set(0.2)
        range_to_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.range_to, state="disabled")
        range_to_entry.grid(column=1, row=3, sticky=(W, E), padx=5, pady=3)

        ttk.Label(fs_smaller_frame, text="silenced ratio").grid(column=0, row=4, sticky=W, padx=5)
        self.silenced_ratio = DoubleVar()
        self.silenced_ratio.set(0.3)
        silenced_ratio_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.silenced_ratio, state="disabled")
        silenced_ratio_entry.grid(column=1, row=4, sticky=(W, E), padx=5, pady=3)

        ttk.Label(fs_smaller_frame, text="silencing threshold").grid(column=0, row=5, sticky=W, padx=5)
        self.silencing_threshold = DoubleVar()
        self.silencing_threshold.set(0.3)
        silencing_threshold_entry = ttk.Entry(fs_smaller_frame, width=20, textvariable=self.silencing_threshold, state="disabled")
        silencing_threshold_entry.grid(column=1, row=5, sticky=(W, E), padx=5, pady=3)

        # gray out other options when restriction type changes
        def restr_type_change(event):
            for entry in [range_from_entry, range_to_entry, silenced_ratio_entry, silencing_threshold_entry]:
                entry["state"] = "disabled"
            trust_in_mainstream_button["state"] = "enabled"

            selection = self.restr_type.get()
            match selection:
                case "no restriction":
                    trust_in_mainstream_button["state"] = "disabled"
                
                case "arbitrary silencing":
                    silenced_ratio_entry["state"] = "enabled"

                case "belief range":
                    range_from_entry["state"] = "enabled"
                    range_to_entry["state"] = "enabled"

                case "unpopular_beliefs":
                    silencing_threshold_entry["state"] = "enabled"

            return
        restr_type_box.bind('<<ComboboxSelected>>', restr_type_change)
        
        self.keep_seed = BooleanVar()
        self.keep_seed.set(False)
        keep_seed_button = ttk.Checkbutton(input_frame, variable=self.keep_seed,
            onvalue=True, offvalue=False, text="keep random seed")
        keep_seed_button.grid(column=0, row=9, padx=5, sticky=W)

            # simbutton
        ttk.Button(input_frame, text="SIMULATE!", command=self.simulate).grid(
            column=0, row=10, sticky=(E, W), pady=10)


        # building the plotting canvas
        self.figure = plt.figure(figsize=(6, 6))
        self.plotting_canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.plotting_canvas.draw()
        
        self.axes = self.figure.add_axes([.1, .1, .85, .85])
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

if __name__ == "__main__":
    my_abm_app = GUIApplication()
    my_abm_app.run()