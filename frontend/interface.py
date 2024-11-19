import tkinter as tk
from tkinter import filedialog

class CraneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pier Point Shipping Inc. Crane Container Optimizer")
        self.geometry("1350x900")
        self.configure(bg='gray30')
        self.initialize_gui()

    def initialize_gui(self):
        # Title
        title_label = tk.Label(self, text="Pier Point Shipping Inc. Crane Container Optimizer", font=("SF Pro", 35, "bold"), bg='gray30', fg='white')
        title_label.pack(pady=50)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=50)

        tk.Button(btn_frame, text="Load/Unload", command=self.load_unload, font=("Arial", 15),
                  bg="white", width=25, height=3).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(btn_frame, text="Balance", command=self.balance, font=("Arial", 15),
                  bg="white", width=25, height=3).grid(row=0, column=1, padx=10, pady=5)

    def load_unload(self):
        filename = filedialog.askopenfilename(title="Select Manifest")

    def balance(self):
        filename = filedialog.askopenfilename(title="Select Manifest")

# Main
if __name__ == "__main__":
    app = CraneApp()
    app.mainloop()