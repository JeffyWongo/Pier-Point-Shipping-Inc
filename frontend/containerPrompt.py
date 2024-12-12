import tkinter as tk

class ContainerPromptWindow(tk.Toplevel):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.title("Enter Container Details")
        self.container = container

        self.parent = parent
        self.closedAutomatically = False

        # Label for container name
        tk.Label(self, text="Enter Container Name:").grid(row=0, column=0, padx=5, pady=5)

        # Entry field for container name
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label for container weight
        tk.Label(self, text="Enter Container Weight:").grid(row=1, column=0, padx=5, pady=5)

        # Entry field for container weight
        self.weight_entry = tk.Entry(self)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=lambda: self.submit_details(container))
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Error message label (initially empty)
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.grab_set()  # Make the window (blocks interaction with other windows)

        # qol changes
        self.bind('<Return>', lambda event: self.submit_details(container))
        self.name_entry.focus_set()

    def submit_details(self, container):
        container_name = self.name_entry.get()
        container_weight = self.weight_entry.get()

        # Validate the input
        if container_name and container_weight.isdigit():  # Check if valid name and weight
            for widget in self.parent.grid_frame.winfo_children():
                # Check if the widget is the label for the given container
                widget_text = widget.cget('text').splitlines()[0]
                expected_text = f"Pos: [{self.container.row:02},{self.container.col:02}]"
                if widget_text == expected_text:
                    new_text = f"Pos: [{self.container.row:02},{self.container.col:02}]\nWeight: {container_weight}\nName: {container_name}"
                    widget.config(text=new_text)

            container.name = container_name
            container.weight = int(container_weight)

            self.closedAutomatically = True
            self.destroy()  # Close the window
        else:
            # Show error message in the prompt window
            self.error_label.config(text="Invalid input. Please enter valid details.")
