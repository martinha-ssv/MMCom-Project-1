from solver import InputFile, buildGlobalK, constrainGlobalK, solve_disp, solveForces
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from results import Results
import matplotlib.pyplot as plt
from modules.file_input import clear_pycache
from objects.node import Node
from objects.element import Element

# TODO add units textbox, also add to result writer


class Checkbox(ttk.Checkbutton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = tk.BooleanVar(self)
        self.config(variable=self.variable)
        self.check()

    def checked(self):
        return self.variable.get()

    def check(self):
        self.variable.set(True)

    def uncheck(self):
        self.variable.set(False)

    
    def checkbox_clicked(self):
        print("New state:", self.checked())


# Function to open file dialog and load file content
def open_file(text_box):
    clear_pycache()
    Element.elements = {}
    Node.nodes = {}
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Input Files", "*.inp"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)  # Clear text box before loading new content
            text_box.insert(tk.END, content)


# Function to save content to a temporary file and solve
def run_and_create_temp_file(text_box, download_button):
    content = text_box.get(1.0, tk.END)  # Get content from the text box
    # Create a temporary file and write the content to it
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp_file.write(content.encode('utf-8'))
    temp_file.close()
    
    input = InputFile(temp_file.name)
    k = buildGlobalK()
    const_k, f_vec = constrainGlobalK(k)
    uuu = solve_disp(const_k, f_vec)
    fff = solveForces(k,uuu)

    download_button.config(state=tk.NORMAL)

    Results.build_results_string(k)

    # Update the text box with the results
    text_box.delete(1.0, tk.END)  # Clear text box before loading new content
    text_box.insert(tk.END, Results.results_string)


def download_results_file(results_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(results_text)
        messagebox.showinfo("Results file Saved", f"Results saved to: {file_path}")