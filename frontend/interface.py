import tkinter as tk
from tkinter import filedialog

class LoginPage(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.master = master
        self.on_login = on_login
        self.configure(bg="gray30")
        self.initialize_gui()
    
    def initialize_gui(self):
        # title
        title_label = tk.Label(self, text="Pier Point Shipping Inc. Login Page", font=("SF Pro", 30, "bold"), bg='gray30', fg='white')
        title_label.pack(pady=50)

        # username
        username_label = tk.Label(self, text="Username:", font=("SF Pro", 15), bg='gray30', fg='white')
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("SF Pro", 15), width=30)
        self.username_entry.pack(pady=10)

        # login
        login_button = tk.Button(self, text="Login", command=self.handle_login, font=("SF Pro", 15), bg="white", width=15, height=2)
        login_button.pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        if username:
            self.on_login(username)
        else:
            error_label = tk.Label(self, text="Please enter a username", font=("SF Pro", 12), bg='gray30', fg='red')
            error_label.pack(pady=5)

# represents each square in grid
class Container:
    def __init__(self, row, col, weight, name):
        self.row = row
        self.col = col
        self.weight = weight
        self.name = name
        
    def get_info(self):
        return f"Pos: [{self.row:02},{self.col:02}]\nWeight: {self.weight}\nName: {self.name}"
        

class CraneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pier Point Shipping Inc. Crane Container Optimizer")
        self.geometry("1920x1080")
        self.configure(bg="gray30")
        self.username = None

        self.show_login()

    def show_login(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, username):
        self.username = username
        self.login_page.destroy()  # remove login page
        self.show_main_interface()

    def show_main_interface(self):
        # title
        title_label = tk.Label(self, text="Pier Point Shipping Inc. Crane Container Optimizer", font=("SF Pro", 35, "bold"), bg="gray30", fg="white")
        title_label.pack(pady=50)

        # buttons
        btn_frame = tk.Frame(self, bg='gray30')
        btn_frame.pack(pady=50)

        tk.Button(btn_frame, text="Load/Unload", command=self.load_unload, font=("SF Pro", 15),
                  bg="white", width=25, height=3).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(btn_frame, text="Balance", command=self.balance, font=("SF Pro", 15),
                  bg="white", width=25, height=3).grid(row=0, column=1, padx=10, pady=5)

    def load_unload(self):
        filename = filedialog.askopenfilename(title="Select Manifest")

    def balance(self):
        filename = filedialog.askopenfilename(title="Select Manifest")

        balance_window = tk.Toplevel(self)
        balance_window.title("Balance")
        balance_window.geometry("1920x1080")
        balance_window.configure(bg='gray30')

        home_button = tk.Button(balance_window, text="Home", font=("SF Pro", 12), bg='white', command=balance_window.destroy)
        home_button.place(x=10, y=10)

        title_label = tk.Label(balance_window, text="Balance", font=("SF Pro", 30, "bold"), bg='gray30', fg='white')
        title_label.pack(pady=20)

        grid_frame = tk.Frame(balance_window, bg='gray30')
        grid_frame.pack(pady=20)

        #display grid
        rows, cols = 8, 12
        containers = []
        for r in range(rows):
            for c in range(cols):
                container_row = rows - r
                container_col = c + 1
                name = "DOG" if (r + c) % 3 == 0 else "UNUSED"
                container = Container(row=container_row, col=container_col, weight="5000",name=name)
                containers.append(container)

                container_label = tk.Label(grid_frame, text=container.get_info(), font=("SF Pro", 10),
                                        width=15, height=4, bg='white', relief='solid')
                container_label.grid(row=r, column=c, padx=2, pady=2)

        #comment box
        comment_frame = tk.Frame(balance_window, bg='gray30')
        comment_frame.pack(pady=20)

        comment_label = tk.Label(comment_frame, text="Comments:", font=("SF Pro", 15), bg='gray30', fg='white')
        comment_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        comment_entry = tk.Text(comment_frame, font=("SF Pro", 12), width=50, height=5)
        comment_entry.grid(row=1, column=0, padx=10, pady=5)

        #submit
        submit_button = tk.Button(comment_frame, text="Submit", font=("SF Pro", 12), bg='white',
                           command=lambda: self.submit_comment(comment_entry))

        submit_button.grid(row=2, column=0, pady=10)


# Main
if __name__ == "__main__":
    app = CraneApp()
    app.mainloop()
