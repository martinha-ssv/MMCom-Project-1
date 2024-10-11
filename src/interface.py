import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from results import Results
from modules.GUIbuilder import open_file, run_and_create_temp_file, download_results_file, Checkbox
from modules.draw import Artist


# Create the main window (root)
root = tk.Tk()
root.title("FEA 2D Bar Solver")
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


button_frame = ttk.Frame(frame_parameters)
button_frame.pack(pady=5)

open_button = ttk.Button(button_frame, text="Open Abaqus .inp File", command=lambda: open_file(text_box=text_box))
open_button.pack(side="left", padx=5)

run_button = ttk.Button(button_frame, text="Run Solver", command=lambda: run_and_create_temp_file(text_box=text_box, download_button=download_button))
run_button.pack(side="left", padx=5)

download_button = ttk.Button(button_frame, text="Download Results File", state="disabled", command=lambda: download_results_file(results_text=Results.results_string))
download_button.pack(side="left", padx=5)


# Screen 1 content (Parameters & Solving)
label_params = ttk.Label(frame_parameters, text="Select a file and edit content. \n\nThe file should be structured as an Abaqus .inp file, but you can provide a .txt file or equivalent.\nWhen you click 'Run Solver', your results will be displayed in the text box below.\nShould you want to, you may save the results in a text file by clicking 'Download Results File'.", font=("Arial", 14))
label_params.pack(pady=10)

# Text box to display and edit file content
text_box = tk.Text(frame_parameters, height=50, width=150)
text_box.pack(pady=20)

# Screen 2 content (Results)
label_results = ttk.Label(frame_results, text="Results", font=("Arial", 14))
label_results.pack(pady=10)

# Create a matplotlib figure and embed it in a canvas
fig = plt.Figure(figsize=(4,3), dpi=200)
ax = fig.add_subplot(111)
#canvas = FigureCanvasTkAgg(fig, master=frame_results)
#canvas.get_tk_widget().pack(pady=20)

artist = Artist(fig, ax, master=frame_results)



# Create a frame for the sidebar
sidebar_frame = ttk.Frame(frame_results)
sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

# Add checkboxes to the sidebar
checkbox1 = Checkbox(sidebar_frame, text="Nodes")
checkbox1.pack(anchor=tk.W, padx=20, pady=5)

checkbox2 = Checkbox(sidebar_frame, text="Elements")
checkbox2.pack(anchor=tk.W, padx=20, pady=5)

checkbox3 = Checkbox(sidebar_frame, text="")
checkbox3.pack(anchor=tk.W, padx=20, pady=5)

# Embed the matplotlib canvas in the main frame


# Start the main loop
root.mainloop()