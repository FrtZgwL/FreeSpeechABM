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

def simulate():
    print("wip")
    return

def set_up_ui(root):
    # root window
    root.title("ABM")

    # frames
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    input_frame = ttk.Frame(main_frame)
    input_frame['borderwidth'] = 2
    input_frame['relief'] = 'raised'
    input_frame.grid(column=0, row=0)

    # labels
    ttk.Label(input_frame, text="n agents").grid(column=0, row=0, sticky=W)
    ttk.Label(input_frame, text="alpha").grid(column=0, row=1, sticky=W)
    ttk.Label(input_frame, text="epsilon").grid(column=0, row=2, sticky=W)
    ttk.Label(input_frame, text="noise").grid(column=0, row=3, sticky=W)
    ttk.Label(input_frame, text="tau").grid(column=0, row=4, sticky=W)

    # input fields
    alpha = StringVar()
    alpha_entry = ttk.Entry(input_frame, width=20, textvariable=alpha)
    alpha_entry.grid(column=1, row=1, sticky=(W, E))

    ttk.Button(input_frame, text="SIMULATE!", command=simulate).grid(column=0, row=5)

    # canvas = Canvas(main_frame, background="white")
    # canvas.grid(row=0, column=1)

    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    ax = fig.add_subplot()
    line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
    ax.set_xlabel("time [s]")
    ax.set_ylabel("f(t)")

    figure = Figure(figsize=(6, 6))
    ax = figure.subplots()

    test = pd.DataFrame(data=[[0, 1], [1, 2], [2, 1]], columns=["time", "value"])
    sns.set_theme()
    sns.lineplot(
        data=test,
        x="time", y="value", ax=ax)

    # canvas
    canvas = FigureCanvasTkAgg(figure, master=main_frame)  # A tk.DrawingArea.
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, main_frame, pack_toolbar=False)
    toolbar.update()
    toolbar.grid(row=1, column=1)

    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event", key_press_handler)

    canvas.get_tk_widget().grid(row=0, column=1)

    for child in input_frame.winfo_children(): 
        child.grid_configure(padx=20, pady=5)


# --- main code --- #
root = Tk()
set_up_ui(root)
root.mainloop()