import numpy as np
from solver import InputFile, buildGlobalK, constrainGlobalK, solve_disp, solveForces
import time
import src.modules.draw as draw
from src.objects.node import Node
import os
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to open file dialog and load file content
def open_file(text_box):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)  # Clear text box before loading new content
            text_box.insert(tk.END, content)
        messagebox.showinfo("File Loaded", f"Loaded file: {file_path}")


# Function to save content to a temporary file and solve
def run_and_create_temp_file(text_box, download_button):
    content = text_box.get(1.0, tk.END)  # Get content from the text box
    # Create a temporary file and write the content to it
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp_file.write(content.encode('utf-8'))
    temp_file.close()
    messagebox.showinfo("Temporary file with instructions was created", f"Temp file created at: {temp_file.name}")
    
    input = InputFile(temp_file.name)
    k = buildGlobalK()
    const_k, f_vec = constrainGlobalK(k)
    uuu = solve_disp(const_k, f_vec)
    fff = solveForces(k,uuu)

    download_button.config(state=tk.NORMAL)
    

def download_results_file(): #TODO
    pass



'''draw.draw_structure(ax=ax, plot=True, drawForces=True, drawConstraints=True, colors=True)
    Node.ToggleDeformation(scale=1000000)
    draw.draw_structure(ax=ax, drawForces=False, drawConstraints=False, colors='u')
    canvas.draw()'''