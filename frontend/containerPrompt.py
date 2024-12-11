import tkinter as tk

class ContainerPromptWindow(tk.Toplevel):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.title("Enter Container Details")
        self.container = container

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
        submit_button = tk.Button(self, text="Submit", command=self.submit_details)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Error message label (initially empty)
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.grab_set()  # Make the window (blocks interaction with other windows)

    def submit_details(self):
        container_name = self.name_entry.get()
        container_weight = self.weight_entry.get()

        # Validate the input
        if container_name and container_weight.isdigit():  # Check if valid name and weight
            self.container.name = container_name
            self.container.weight = int(container_weight)
            self.destroy()  # Close the window
        else:
            # Show error message in the prompt window
            self.error_label.config(text="Invalid input. Please enter valid details.")
