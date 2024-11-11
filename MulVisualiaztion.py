# import tkinter as tk
# from tkinter import filedialog
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class CSVPlotter:

#     def __init__(self, root):
#         self.root = root
#         root.title('CSVPlotter')

#         self.plot_types = ['Line Plot', 'Bar Plot', 'Scatter Plot']
#         self.plot_type_var = tk.StringVar(value = self.plot_types[0])
#         plot_menu = tk.OptionMenu(self.root, self.plot_type_var, *self.plot_types, command = self.update_plot)
#         plot_menu.pack(padx=10, pady=10)

#         load_button = tk.Button(self.root, text = 'Load CSV', command = self.load_csv )
#         load_button.pack(padx=10, pady=10)

#         self.fig, self.ax = plt.subplots()
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

#         self.widget = self.canvas.get_tk_widget()
#         self.widget.pack(padx=10, pady=10)

#         self.df = None

#     def load_csv(self):
#             file_path = filedialog.askopenfilename()
#             if file_path:
#                 self.df = pd.read_csv(file_path)
#                 self.update_plot
        
#     def update_plot(self, event = None):
#             if self.df is not None:
#                 plot_type = self.plot_type_var.get()
#                 x = self.df.columns[0]
#                 y = self.df.columns[1]

#             self.ax.clear()
#             if plot_type == 'Line Plot':
#                 self.ax.plot(self.df[x], self.df[y], label = f'{y} vs {x}')
#             if plot_type == 'Bar Plot':
#                 self.ax.bar(self.df[x], self.df[y], label = f'{y} vs {x}')
#             if plot_type == 'Scatter Plot':
#                 self.ax.scatter(self.df[x], self.df[y], label = f'{y} vs {x}')

#             self.ax.set_xlabel(x)
#             self.ax.set_ylabel(y)
#             self.ax.legend()
#             self.canvas.draw()

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.geometry("800x400")
#     app = CSVPlotter(root)
#     root.mainloop()


import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Graph Viewer")
        self.file_paths = []
        self.data_frames = []

        # Interface elements
        self.load_button = tk.Button(root, text="Load CSV Files", command=self.load_files)
        self.load_button.pack()

        self.graph_type_label = tk.Label(root, text="Select Graph Type:")
        self.graph_type_label.pack()

        self.graph_type = tk.StringVar(value="Line")
        self.graph_type_menu = tk.OptionMenu(root, self.graph_type, "Line", "Bar", "Scatter")
        self.graph_type_menu.pack()

        self.plot_button = tk.Button(root, text="Plot Graph", command=self.plot_graph)
        self.plot_button.pack()

        # Matplotlib figure
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack()

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        if file_paths:
            self.file_paths = file_paths
            self.data_frames = [pd.read_csv(file) for file in self.file_paths]
            messagebox.showinfo("Files Loaded", f"Loaded {len(self.file_paths)} files successfully.")

    def plot_graph(self):
        if not self.data_frames:
            messagebox.showwarning("No Files Loaded", "Please load CSV files first.")
            return

        # Ask for columns to plot
        columns = self.data_frames[0].columns.tolist()
        column_to_plot = simpledialog.askstring("Columns to Plot", f"Available columns: {columns}\nEnter columns separated by commas:")

        if not column_to_plot:
            return

        selected_columns = [col.strip() for col in column_to_plot.split(",")]

        # Check if all selected columns exist in each DataFrame
        for col in selected_columns:
            for i, df in enumerate(self.data_frames):
                if col not in df.columns:
                    messagebox.showerror("Error", f"Column '{col}' does not exist in file {i+1}.")
                    return

        # Plot each file's selected columns
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Handle scatter plot with at least two columns
        if self.graph_type.get() == "Scatter" and len(selected_columns) < 2:
            messagebox.showwarning("Scatter Plot Error", "Scatter plot requires at least two columns: an x-axis and a y-axis.")
            return

        # Use the first column as x-axis if multiple columns are provided
        x_col = selected_columns[0] if len(selected_columns) > 1 else None
        y_cols = selected_columns[1:] if len(selected_columns) > 1 else [selected_columns[0]]

        for i, df in enumerate(self.data_frames):
            try:
                for y_col in y_cols:
                    if self.graph_type.get() == "Line":
                        if x_col:
                            df.plot(kind='line', x=x_col, y=y_col, ax=ax, label=f"{y_col} (File {i+1})")
                        else:
                            df[y_col].plot(kind='line', ax=ax, label=f"{y_col} (File {i+1})")
                    elif self.graph_type.get() == "Bar":
                        if x_col:
                            df.plot(kind='bar', x=x_col, y=y_col, ax=ax, label=f"{y_col} (File {i+1})")
                        else:
                            df[y_col].plot(kind='bar', ax=ax, label=f"{y_col} (File {i+1})")
                    elif self.graph_type.get() == "Scatter":
                        df.plot(kind='scatter', x=x_col, y=y_col, ax=ax, label=f"{y_col} (File {i+1})")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot {y_col} in file {i+1}.\nError: {e}")
                return

        ax.legend()
        self.canvas.draw()

# Run the application
root = tk.Tk()
app = CSVGraphApp(root)
root.mainloop()