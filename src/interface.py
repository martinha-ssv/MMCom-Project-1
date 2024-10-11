import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from results import Results
from modules.GUIbuilder import open_file, run_and_create_temp_file, download_results_file, Checkbox
from modules.draw import Artist

class Interface:
    def __init__(self, root):
        self.artist = None

        # Create the main window (root)
        self.root = root
        self.root.title("FEA 2D Bar Solver")
        self.root.geometry("1200x900")

        # Create a notebook (tabbed view)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Screen 1: Parameters and solving
        self.frame_parameters = ttk.Frame(self.notebook, width=1000, height=400)
        self.frame_parameters.pack(fill="both", expand=True)
        self.notebook.add(self.frame_parameters, text="Parameters & Solving")

        # Screen 2: Results with matplotlib canvas
        self.frame_results = ttk.Frame(self.notebook, width=1000, height=400)
        self.frame_results.pack(fill="both", expand=True)
        self.notebook.add(self.frame_results, text="Results")

        self.button_frame = ttk.Frame(self.frame_parameters)
        self.button_frame.pack(pady=5)

        self.open_button = ttk.Button(self.button_frame, text="Open Abaqus .inp File", command=lambda: open_file(text_box=self.text_box))
        self.open_button.pack(side="left", padx=5)

        self.run_button = ttk.Button(self.button_frame, text="Run Solver", command=self.run_solver)
        self.run_button.pack(side="left", padx=5)

        self.download_button = ttk.Button(self.button_frame, text="Download Results File", state="disabled", command=lambda: download_results_file(results_text=Results.results_string))
        self.download_button.pack(side="left", padx=5)

        # Screen 1 content (Parameters & Solving)
        self.label_params = ttk.Label(self.frame_parameters, text="Select a file and edit content. \n\nThe file should be structured as an Abaqus .inp file, but you can provide a .txt file or equivalent.\nWhen you click 'Run Solver', your results will be displayed in the text box below.\nShould you want to, you may save the results in a text file by clicking 'Download Results File'.", font=("Arial", 14))
        self.label_params.pack(pady=10)

        # Text box to display and edit file content
        self.text_box = tk.Text(self.frame_parameters, height=50, width=150)
        self.text_box.pack(pady=20)

        # Screen 2 content (Results)
        self.label_results = ttk.Label(self.frame_results, text="Results", font=("Arial", 14))
        self.label_results.pack(pady=10)

        # Create a matplotlib figure and embed it in a canvas
        self.fig = plt.Figure(figsize=(4, 3), dpi=200)

        # Create a frame for the sidebar
        self.sidebar_frame = ttk.Frame(self.frame_results)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        # PLOT UPDATE BUTTON
        self.update_button = ttk.Button(self.sidebar_frame, text="Update Plot", command=self.update_plot)
        self.update_button.pack(anchor=tk.W, padx=20, pady=5)

        # DEFORMED STRUCTURE?
        self.undeformed = Checkbox(self.sidebar_frame, text="Undeformed Structure")
        self.undeformed.pack(anchor=tk.W, padx=20, pady=5)

        # UNDEFORMED STRUCTURE?
        self.deformed = Checkbox(self.sidebar_frame, text="Deformed Structure")
        self.deformed.pack(anchor=tk.W, padx=20, pady=5)

        # STRUCTURE SCALE ENTRY
        self.scale_label = ttk.Label(self.sidebar_frame, text="Deformations Scale")
        self.scale_label.pack(anchor=tk.W, padx=20, pady=5)

        self.scale_entry = ttk.Entry(self.sidebar_frame, width=10)
        self.scale_entry.insert(0, '1e6')
        self.scale_entry.pack(anchor=tk.W, padx=40, pady=5)

        # FORCES SCALE ENTRY
        self.forces_scale_label = ttk.Label(self.sidebar_frame, text="Forces Scale")
        self.forces_scale_label.pack(anchor=tk.W, padx=20, pady=5)

        self.forces_scale_entry = ttk.Entry(self.sidebar_frame, width=10)
        self.forces_scale_entry.insert(0, '1e-2')
        self.forces_scale_entry.pack(anchor=tk.W, padx=40, pady=5)  # Increased padx to push the Entry to the right

        # DRAW OPTIONS
        self.nodes_checkbox = Checkbox(self.sidebar_frame, text="Draw Nodes")
        self.nodes_checkbox.pack(anchor=tk.W, padx=20, pady=5)

        self.elements_checkbox = Checkbox(self.sidebar_frame, text="Draw Elements")
        self.elements_checkbox.pack(anchor=tk.W, padx=20, pady=5)

        self.element_numbers = Checkbox(self.sidebar_frame, text="Draw Element Numbers")
        self.element_numbers.pack(anchor=tk.W, padx=20, pady=5)

        # COLOR OPTIONS

        # UNDEFORMED COLOR
        self.undeformed_color_label = ttk.Label(self.sidebar_frame, text="Undeformed Element Color")
        self.undeformed_color_label.pack(anchor=tk.W, padx=20, pady=5)

        self.undeformed_color_var = tk.StringVar(value="black")

        undeformed_color_options = ["u_1", "u_2", "u", "strain", "stress", "black"]
        for option in undeformed_color_options:
            rb = ttk.Radiobutton(self.sidebar_frame, text=option, variable=self.undeformed_color_var, value=option)
            rb.pack(anchor=tk.W, padx=40, pady=2)

        # DEFORMED COLOR
        self.deformed_color_label = ttk.Label(self.sidebar_frame, text="Deformed Element Color")
        self.deformed_color_label.pack(anchor=tk.W, padx=20, pady=5)

        self.deformed_color_var = tk.StringVar(value="black")

        deformed_color_options = ["u_1", "u_2", "u", "strain", "stress", "black"]
        for option in deformed_color_options:
            rb = ttk.Radiobutton(self.sidebar_frame, text=option, variable=self.deformed_color_var, value=option)
            rb.pack(anchor=tk.W, padx=40, pady=2)

        # DRAW FORCES AND CONSTRAINTS
        self.forces = Checkbox(self.sidebar_frame, text="Draw Forces (Loads and Reactions)")
        self.forces.pack(anchor=tk.W, padx=20, pady=5)

        self.constraints = Checkbox(self.sidebar_frame, text="Draw Constraints")
        self.constraints.pack(anchor=tk.W, padx=20, pady=5)

    def run_solver(self):
        run_and_create_temp_file(text_box=self.text_box, download_button=self.download_button)
        if self.artist is None:
            self.artist = Artist(self.fig, self.frame_results)
        # Update the plot or perform other actions with the artist

    def update_plot(self):
        if self.artist:
            self.artist.update_plot(
                draw_undeformed=self.undeformed.checked(),
                draw_deformed=self.deformed.checked(),
                deformation_scale=self.scale_entry.get(),
                forces_scale=self.forces_scale_entry.get(),
                draw_nodes=self.nodes_checkbox.checked(),
                draw_elements=self.elements_checkbox.checked(),
                element_numbers=self.element_numbers.checked(),
                undeformed_colors=self.undeformed_color_var.get(),
                deformed_colors=self.deformed_color_var.get(),
                draw_forces=self.forces.checked(),
                draw_constraints=self.constraints.checked()
            )

# Create the main application
root = tk.Tk()
app = Interface(root)
root.mainloop()