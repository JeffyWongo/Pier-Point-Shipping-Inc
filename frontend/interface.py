import tkinter as tk
from tkinter import filedialog
import random
from datetime import datetime, timedelta
from containerPrompt import ContainerPromptWindow
import copy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adds the root directory to sys.path

from backend.load import Load
from backend.load import Container as loadContainer

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

        # quality of life
        self.master.bind('<Return>', lambda event: self.handle_login())
        self.username_entry.focus_set()

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

        self.reset_load_unload()
        self.grid_frame = tk.Frame(self)

        self.show_login()

    def show_login(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, username):
        self.username = username
        # log sign-in
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"{current_time}        {username} has signed in\n"
        with open("logfile2024.txt", "a") as log_file:
            log_file.write(log_entry)
        
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

    def reset_load_unload(self):
        self.processed_moves = False
        self.original_containers = []
        self.containers = []
        self.best_moves = []
        self.current_step = 0
        self.load_containers = []
        self.unload_containers = []

    def load_unload(self):
        filename = filedialog.askopenfilename(title="Select Manifest", filetypes=[("Text Files", "*.txt")])
        if not filename:
            return

        self.reset_load_unload()

        # log the file opening
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(filename, 'r') as file:
            self.containers = []
            name_colors = {}
            container_count = 0
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    if len(parts) == 3:
                        position = parts[0].strip("[]").split(",")
                        weight = parts[1].strip("{}")
                        name = parts[2]

                        try:
                            row = int(position[0])
                            col = int(position[1])

                            if name not in ("NAN", "UNUSED"):
                                if name not in name_colors:
                                    name_colors[name] = "#{:02x}{:02x}{:02x}".format(
                                        random.randint(150, 255),  # random light red
                                        random.randint(150, 255),  # random light green
                                        random.randint(150, 255))  # random light blue
                                container_count += 1
                            container = Container(row=row, col=col, weight=weight, name=name)
                            self.containers.append(container)
                        except ValueError:
                            print(f"Skipping invalid line: {line}")

            log_entry = f"{current_time}        Manifest {filename.split('/')[-1]} is opened, there are {container_count} containers on the ship\n"
            with open("logfile2024.txt", "a") as log_file:
                log_file.write(log_entry)

        self.original_containers = copy.deepcopy(self.containers)

        load_window = tk.Toplevel(self)
        load_window.title("Load Unload")
        load_window.geometry("1920x1080")
        load_window.configure(bg='gray30')

        home_button = tk.Button(load_window, text="Home", font=("SF Pro", 12), bg='white', command=load_window.destroy)
        home_button.place(x=10, y=10)

        title_label = tk.Label(load_window, text="Load Unload", font=("SF Pro", 30, "bold"), bg='gray30', fg='white')
        title_label.pack(pady=20)

        self.grid_frame = tk.Frame(load_window, bg='gray30')
        self.grid_frame.pack(pady=20)

        # display grid
        self.display_container_select(name_colors, self.grid_frame)

        # bottom frame for comments and buttons
        bottom_frame = tk.Frame(load_window, bg='gray30')
        bottom_frame.pack(pady=20, fill='x')

        # For alignment
        bottom_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        bottom_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        bottom_frame.grid_columnconfigure(2, weight=1, uniform="group1")

        # First Time Left Box
        time_frame = tk.Frame(bottom_frame, bg='gray30')
        time_frame.grid(row=0, column=0, padx=20, pady=5, sticky='ns')

        time_label = tk.Label(time_frame, text="Estimated Finish Time:", font=("SF Pro", 15), bg='gray30', fg='white')
        time_label.grid(row=0, column=0, padx=5)

        time_display = tk.Label(time_frame, text="__:__", font=("SF Pro", 15, "bold"), bg='gray20', fg='white', relief='solid', width=10)
        time_display.grid(row=0, column=1, padx=5)

        # instructions box
        instruction_frame = tk.Frame(bottom_frame, bg='gray30')
        instruction_frame.grid(row=0, column=1, padx=20, pady=5)

        instruction_label = tk.Label(instruction_frame, text="Left click spot to load. Right click container to unload", font=("SF Pro", 15), bg='gray25', fg='white', relief='solid', padx=10, pady=5)
        instruction_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Comment Box and Submit Button
        comment_frame = tk.Frame(bottom_frame, bg='gray30')
        comment_frame.grid(row=1, column=1, padx=20, pady=5)

        comment_label = tk.Label(comment_frame, text="Comments:", font=("SF Pro", 15), bg='gray30', fg='white')
        comment_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        comment_entry = tk.Text(comment_frame, font=("SF Pro", 12), width=50, height=3)
        comment_entry.grid(row=1, column=0, padx=10, pady=5)

        submit_button = tk.Button(comment_frame, text="Submit", font=("SF Pro", 12), bg='white',
                                command=lambda: self.submit_comment(comment_entry))
        submit_button.grid(row=2, column=0, pady=10)

        # start/next button
        button_frame = tk.Frame(bottom_frame, bg='gray30')
        button_frame.grid(row=0, column=2, padx=20)

        next_button = tk.Button(button_frame, text="Start", font=("SF Pro", 12), bg='white', width=10, height=2,
                                command=lambda: self.next_state(name_colors, self.grid_frame, instruction_label, next_button, load_window, time_display, filename))
        next_button.pack()

    def next_state(self, name_colors, grid_frame, instruction_label, next_button, load_window, time_display, filename):
        # call Load Unload
        if not self.processed_moves:
            self.processed_moves = True
            # convert ship_layout for load operation
            ship_layout = [[loadContainer() for i in range(0,12)] for j in range(0,8)]
            for item in self.original_containers:
                ship_layout[item.row-1][item.col-1] = loadContainer(item.name, item.weight)

            # convert load and unload lists
            unload_list = []
            load_list = []
            for item in self.unload_containers:
                container = loadContainer(item.name, item.weight)
                cord = (item.row-1, item.col-1)
                unload_list.append((container, cord))
            for item in self.load_containers:
                container = loadContainer(item.name, item.weight)
                cord = (item.row-1, item.col-1)
                load_list.append((container, cord))

            self.best_moves = Load.run(ship_layout, unload_list, load_list)

            next_button.config(text="Next")

            cost = 0
            if self.best_moves is not None:
                instruction_label.config(text="Optimal Moves Found")
                for move in self.best_moves:
                    if move[1] is None:
                        break
                    if move[1] == (8,0) or move[2] == (8,0):
                        cost += 2
                    cost += abs(move[1][0] - move[2][0]) + abs(move[1][1] - move[2][1])
            else:
                instruction_label.config(text="Solution Not Found")

            eta = (datetime.now() + timedelta(minutes=cost)).strftime("%H:%M")
            time_display.config(text=eta)
        # show next move
        else:
            # print next step
            if self.best_moves is not None and self.current_step < len(self.best_moves):
                current_state = []
                info = self.best_moves[self.current_step]
                for row_index, row in enumerate(info[0]):
                    for col_index, item in enumerate(row):
                        container = Container(row=row_index + 1, col=col_index + 1, weight=item.weight, name=item.name)
                        
                        current_state.append(container)
                self.containers = current_state
                self.display_containers(name_colors, grid_frame)
                
                # TODO: "animations"
                if info[1] is None:
                    instruction_label.config(text="Operation Finished")
                else:
                    current_layout = info[0]
                    # loading
                    if(info[1]==(8,0)):
                        # finds container in load list
                        container_name = ""
                        for item in self.load_containers:
                            if (item.row-1, item.col-1) == info[2]:
                                container_name = item.name
                                break
                        instruction_label.config(text=f"Load container \"{container_name}\" to {tuple(x+1 for x in info[2])}")

                        self.submit_comment_load(f"\"{container_name}\" was onloaded")
                    # unloading
                    elif(info[2]==(8,0)):
                        container_name = current_layout[info[1][0]][info[1][1]].name
                        instruction_label.config(text=f"Unload container \"{container_name}\" from {tuple(x+1 for x in info[1])}")

                        self.submit_comment_load(f"\"{container_name}\" was offloaded")                
                    else:
                        instruction_label.config(text=f"Move container \"{current_layout[info[1][0]][info[1][1]].name}\" from {tuple(x+1 for x in info[1])} to {tuple(x+1 for x in info[2])}")
                
                self.current_step += 1
            # we're done printing steps
            else:
                self.submit_comment_load(f"Finished a cycle. Manifest {filename.replace(".txt", "OUTBOUND.txt").split('/')[-1]} was written to the desktop, and a reminder pop-up to the operator to send the file was displayed.")
                # TODO: outbound manifest
                load_window.destroy()

    # takes containers, colors, and frame element
    # prints out ship layout
    def display_container_select(self, name_colors, grid_frame):
        rows, cols = 8, 12
        for r in range(rows):
            for c in range(cols):
                container = next((cont for cont in self.containers if cont.row == rows - r and cont.col == c + 1), None)
                if container:
                    info = container.get_info()
                    if container.name == "NAN":
                        bg_color = 'gray20'  # Set background color for 'NAN' containers
                    else:
                        bg_color = name_colors.get(container.name, 'white')

                    container_label = tk.Label(grid_frame, text=info, font=("SF Pro", 10),
                                               width=15, height=4, bg=bg_color, relief='solid')

                    # Bind left-click and right-click events
                    container_label.bind("<Button-1>", lambda event, container=container: self.on_left_click(event, container, name_colors))
                    container_label.bind("<Button-3>", lambda event, container=container: self.on_right_click(event, container, name_colors))

                    container_label.grid(row=r, column=c, padx=2, pady=2)
                else:
                    info = f"Pos: [{rows - r:02},{c + 1:02}]\nWeight: 00000\nName: UNUSED"
                    bg_color = 'white'
                    container_label = tk.Label(grid_frame, text=info, font=("SF Pro", 10),
                                               width=15, height=4, bg=bg_color, relief='solid')
                    container_label.grid(row=r, column=c, padx=2, pady=2)

    # load
    def on_left_click(self, event, container, name_colors):
        if(container.name != "UNUSED" and container not in self.load_containers):
            return
        if container in self.unload_containers:
            return

        if container in self.load_containers:
            self.load_containers.remove(container)
            self.reset_container_color(container, name_colors)
            self.set_container_empty(container)
        else:
            prompt_window = ContainerPromptWindow(self, container)
            self.wait_window(prompt_window)

            if prompt_window.closedAutomatically:
                self.set_container_color(container, "deep sky blue")  # Highlight with blue color
                self.load_containers.append(container)

    # unload
    def on_right_click(self, event, container, name_colors):
        if(container.name == "UNUSED" or container.name == "NAN"):
            return
        if container in self.load_containers:
            return

        if container in self.unload_containers:
            self.unload_containers.remove(container)
            self.reset_container_color(container, name_colors)
        else:
            self.unload_containers.append(container)
            self.set_container_color(container, "red2")  # Highlight with red color

    def set_container_color(self, container, color):
        widget = self.find_container_widget(container)
        widget.config(bg=color)

    def set_container_empty(self, container):
        new_text = f"Pos: [{container.row:02},{container.col:02}]\nWeight: 00000\nName: UNUSED"
        widget = self.find_container_widget(container)
        container.weight = 0
        container.name = "UNUSED"
        widget.config(text=new_text)

    def reset_container_color(self, container, name_colors):
        # Get the container's name and lookup its original color from name_colors
        container_name = container.name
        if container_name in name_colors:
            original_color = name_colors[container_name]
        else:
            original_color = 'white'  # Default color if not found in name_colors

        self.set_container_color(container, original_color)

    def find_container_widget(self, container):
        for widget in self.grid_frame.winfo_children():
            # Check if the widget is the label for the given container
            widget_text = widget.cget('text').splitlines()[0]
            expected_text = f"Pos: [{container.row:02},{container.col:02}]"
            if widget_text == expected_text:
                return widget

    # takes containers, colors, and frame element
    # prints out ship layout
    def display_containers(self, name_colors, grid_frame):
        rows, cols = 8, 12
        for r in range(rows):
            for c in range(cols):
                container = next((cont for cont in self.containers if cont.row == rows - r and cont.col == c + 1), None)
                if container:
                    info = container.get_info()
                    if container.name == "NAN":
                        bg_color = 'gray20'
                    elif container.name == "UNUSED":
                        bg_color = 'white'
                    else:
                        name = container.name
                        if name not in name_colors:
                            name_colors[name] = "#{:02x}{:02x}{:02x}".format(
                                random.randint(150, 255),  # random light red
                                random.randint(150, 255),  # random light green
                                random.randint(150, 255))  # random light blue
                        bg_color = name_colors.get(container.name, 'white')

                else:
                    info = f"Pos: [{rows - r:02},{c + 1:02}]\nWeight: 00000\nName: UNUSED"
                    bg_color = 'white'

                container_label = tk.Label(grid_frame, text=info, font=("SF Pro", 10),
                                        width=15, height=4, bg=bg_color, relief='solid')
                container_label.grid(row=r, column=c, padx=2, pady=2)

    def balance(self):
        filename = filedialog.askopenfilename(title="Select Manifest", filetypes=[("Text Files", "*.txt")])
        if not filename:
            return

        # log the file opening
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(filename, 'r') as file:
            containers = []
            name_colors = {}
            container_count = 0
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    if len(parts) == 3:
                        position = parts[0].strip("[]").split(",")
                        weight = parts[1].strip("{}")
                        name = parts[2]

                        try:
                            row = int(position[0])
                            col = int(position[1])

                            if name not in ("NAN", "UNUSED"):
                                if name not in name_colors:
                                    name_colors[name] = "#{:02x}{:02x}{:02x}".format(
                                        random.randint(150, 255),  # random light red
                                        random.randint(150, 255),  # random light green
                                        random.randint(150, 255))  # random light blue
                                container_count += 1
                            container = Container(row=row, col=col, weight=weight, name=name)
                            containers.append(container)
                        except ValueError:
                            print(f"Skipping invalid line: {line}")

            log_entry = f"{current_time}        Manifest {filename.split('/')[-1]} is opened, there are {container_count} containers on the ship\n"
            with open("logfile2024.txt", "a") as log_file:
                log_file.write(log_entry)

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
        for r in range(rows):
            for c in range(cols):
                container = next((cont for cont in containers if cont.row == rows - r and cont.col == c + 1), None)
                if container:
                    info = container.get_info()
                    if container.name == "NAN":
                        bg_color = 'gray20'
                    elif container.name == "UNUSED":
                        bg_color = 'white'
                    else:
                        bg_color = name_colors.get(container.name, 'white')
                else:
                    info = f"Pos: [{rows - r:02},{c + 1:02}]\nWeight: 00000\nName: UNUSED"
                    bg_color = 'white'

                container_label = tk.Label(grid_frame, text=info, font=("SF Pro", 10),
                                        width=15, height=4, bg=bg_color, relief='solid')
                container_label.grid(row=r, column=c, padx=2, pady=2)

        # Comment Box and Submit Button
        comment_frame = tk.Frame(balance_window, bg='gray30')
        comment_frame.pack(pady=20)

        comment_label = tk.Label(comment_frame, text="Comments:", font=("SF Pro", 15), bg='gray30', fg='white')
        comment_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        comment_entry = tk.Text(comment_frame, font=("SF Pro", 12), width=50, height=5)
        comment_entry.grid(row=1, column=0, padx=10, pady=5)

        submit_button = tk.Button(comment_frame, text="Submit", font=("SF Pro", 12), bg='white',
                                command=lambda: self.submit_comment(comment_entry))
        submit_button.grid(row=2, column=0, pady=10)

    def submit_comment_load(self, comment):
        if comment:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = f"{current_time}        {comment}\n"
            with open("logfile2024.txt", "a") as log_file:
                log_file.write(log_entry)

    def submit_comment(self, comment_entry):
        comment = comment_entry.get("1.0", tk.END).strip()
        if comment:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = f"{current_time}        {comment}\n"
            with open("logfile2024.txt", "a") as log_file:
                log_file.write(log_entry)
            
            comment_entry.delete("1.0", tk.END)
            feedback_label = tk.Label(comment_entry.master, text="Comment submitted successfully!", 
                                    font=("SF Pro", 12), bg='gray30', fg='green')
            feedback_label.grid(row=3, column=0, pady=5)
            self.after(3000, feedback_label.destroy)
        else:
            feedback_label = tk.Label(comment_entry.master, text="Comment cannot be empty!", 
                                    font=("SF Pro", 12), bg='gray30', fg='red')
            feedback_label.grid(row=3, column=0, pady=5)
            self.after(3000, feedback_label.destroy)

# Main
if __name__ == "__main__":
    app = CraneApp()
    app.mainloop()
