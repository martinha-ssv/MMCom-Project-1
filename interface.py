import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from src.modules.GUIbuilder import *


# Create the main window (root)
root = tk.Tk()
root.title("Tkinter App with 2 Screens")
root.geometry("1200x800")

# Create a notebook (tabbed view)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")

# Screen 1: Parameters and solving
frame_parameters = ttk.Frame(notebook, width=1000, height=400)
frame_parameters.pack(fill="both", expand=True)
notebook.add(frame_parameters, text="Parameters & Solving")

# Screen 2: Results with matplotlib canvas
frame_results = ttk.Frame(notebook, width=1000, height=400)
frame_results.pack(fill="both", expand=True)
notebook.add(frame_results, text="Results")


open_button = ttk.Button(frame_parameters, text="Open File", command=lambda: open_file(text_box=text_box))
open_button.pack(pady=5)

run_button = ttk.Button(frame_parameters, text="Run", command=lambda: run_and_create_temp_file(text_box=text_box, download_button=download_button))
run_button.pack(pady=20)

download_button = ttk.Button(frame_parameters, text="Download", state="disabled", command=download_results_file)
download_button.pack(pady=5)


# Screen 1 content (Parameters & Solving)
label_params = ttk.Label(frame_parameters, text="Select a file and edit content:", font=("Arial", 14))
label_params.pack(pady=10)

# Text box to display and edit file content
text_box = tk.Text(frame_parameters, height=30, width=100)
text_box.pack(pady=50)

# Screen 2 content (Results)
label_results = ttk.Label(frame_results, text="Results", font=("Arial", 14))
label_results.pack(pady=10)

# Create a matplotlib figure and embed it in a canvas
fig = plt.Figure(figsize=(4,3), dpi=200)
canvas = FigureCanvasTkAgg(fig, master=frame_results)
canvas.get_tk_widget().pack(pady=20)

# Start the main loop
root.mainloop()