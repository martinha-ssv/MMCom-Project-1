import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import tempfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from solver import InputFile, buildGlobalK, constrainGlobalK, solve_disp, solveForces

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

# Function to open file dialog and load file content
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)  # Clear text box before loading new content
            text_box.insert(tk.END, content)
        messagebox.showinfo("File Loaded", f"Loaded file: {file_path}")


# Function to save content to a temporary file and solve
def run_and_create_temp_file():
    content = text_box.get(1.0, tk.END)  # Get content from the text box
    # Create a temporary file and write the content to it
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp_file.write(content.encode('utf-8'))
    temp_file.close()
    messagebox.showinfo("Temporary File Created", f"Temp file created at: {temp_file.name}")
    fig.clear()  # Clear the figure for new plots
    ax = fig.add_subplot(111)
    
    input = InputFile('work1_input_file.txt')
    k = buildGlobalK()
    const_k, f_vec = constrainGlobalK(k)
    uuu = solve_disp(const_k, f_vec)
    fff = solveForces(k,uuu)
    canvas.draw()

open_button = ttk.Button(frame_parameters, text="Open File", command=open_file)
open_button.pack(pady=5)

run_button = ttk.Button(frame_parameters, text="Run", command=run_and_create_temp_file)
run_button.pack(pady=20)


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