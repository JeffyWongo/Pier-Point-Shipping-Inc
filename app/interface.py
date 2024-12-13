import tkinter as tk
from tkinter import filedialog, messagebox
from Container import Container
from Ship import Ship
from datetime import datetime, timedelta
from containerPrompt import ContainerPromptWindow
import random
import copy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adds the root directory to sys.path

from load import Load
from load import Container as loadContainer

current_year = datetime.now().year
log_file_name = f"logfile{current_year}.txt"

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

class Container2:
    def __init__(self, row, col, weight, name):
        self.row = row
        self.col = col
        self.weight = weight
        self.name = name
        
    def get_info(self):
        return f"Pos: [{self.row:02},{self.col:02}]\n{self.weight}\n{self.name}"
    
class CraneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pier Point Shipping Inc. Crane Container Optimizer")
        self.geometry("1920x1080")
        self.configure(bg="gray30")
        self.username = None
        self.paths_to_animate = []
        self.current_path_index = 0
        self.reset_load_unload()
        self.grid_frame = tk.Frame(self)
        self.current_move_time = 0

        self.show_login()

    def show_login(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, username):
        self.username = username
        # log sign-in
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"{current_time}        {username} has signed in\n"
        with open(log_file_name, "a") as log_file:
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
                            container = Container2(row=row, col=col, weight=weight, name=name)
                            self.containers.append(container)
                        except ValueError:
                            print(f"Skipping invalid line: {line}")

            log_entry = f"{current_time}        Manifest {filename.split('/')[-1]} is opened, there are {container_count} containers on the ship\n"
            with open(log_file_name, "a") as log_file:
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

        instruction_label = tk.Label(instruction_frame, text="Left click spot to load. Right click container to unload", font=("SF Pro", 15),
                                     bg='gray25', fg='white', relief='solid', padx=10, pady=5, wraplength=600)
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
                        container = Container2(row=row_index + 1, col=col_index + 1, weight=item.weight, name=item.name)
                        
                        current_state.append(container)
                self.containers = current_state
                self.display_containers(name_colors, grid_frame)
                
                # TODO: "animations"
                if info[1] is None:
                    instruction_label.config(text="Operation Finished")
                else:
                    current_layout = info[0]
                    # TODO: highlight the destination grid green
                    # TODO: highlight the grid to move yellow
                    # loading
                    if(info[1]==(8,0)):
                        # finds container in load list
                        container_name = ""
                        for item in self.load_containers:
                            if (item.row-1, item.col-1) == info[2]:
                                container_name = item.name
                                break
                        instruction_label.config(text=f"Load container \"{container_name}\" to {tuple(x+1 for x in info[2])} (green)")

                        self.submit_comment_load(f"\"{container_name}\" is onloaded.")

                        to_row, to_col = tuple(x+1 for x in info[2])
                        to_container = next((cont for cont in self.containers if cont.row == to_row and cont.col == to_col), None)

                        self.set_container_color(to_container, 'green', name_colors)
                    # unloading
                    elif(info[2]==(8,0)):
                        container_name = current_layout[info[1][0]][info[1][1]].name
                        instruction_label.config(text=f"Unload container \"{container_name}\" from {tuple(x+1 for x in info[1])} (red)")

                        self.submit_comment_load(f"\"{container_name}\" is offloaded.")

                        from_row, from_col = tuple(x+1 for x in info[1])
                        from_container = next((cont for cont in self.containers if cont.row == from_row and cont.col == from_col), None)

                        self.set_container_color(from_container, 'red', name_colors)
                    else:
                        instruction_label.config(text=f"Move container \"{current_layout[info[1][0]][info[1][1]].name}\" from {tuple(x+1 for x in info[1])} (red) to {tuple(x+1 for x in info[2])} (green)")

                        to_row, to_col = tuple(x+1 for x in info[2])
                        to_container = next((cont for cont in self.containers if cont.row == to_row and cont.col == to_col), None)
                        
                        from_row, from_col = tuple(x+1 for x in info[1])
                        from_container = next((cont for cont in self.containers if cont.row == from_row and cont.col == from_col), None)
                        
                        self.set_container_color(from_container, 'red', name_colors)
                        self.set_container_color(to_container, 'green', name_colors)
                
                self.current_step += 1
            # we're done printing steps
            else:
                # outbound manifest
                output_filename = filename.replace(".txt", "OUTBOUND.txt").split('/')[-1]
                self.write_output_manifest(output_filename)
                self.reminder_popup(output_filename)
                load_window.destroy()

    def reminder_popup(self, filename):
        popup = tk.Toplevel(self)
        popup.title("Email Instructions")

        # Set the size of the popup window
        popup.geometry("300x150")

        # Label instructing the user to email the manifest
        label = tk.Label(popup, text=f"Please email the outbound manifest file:\n{filename}\nto the docked ship.")
        label.pack(pady=20)

        # Button to close the popup
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

        # Make the popup modal (user cannot interact with the main window until the popup is closed)
        popup.grab_set()

        # Wait for the popup to close before continuing
        popup.wait_window()

    def write_output_manifest(self, filename):
        # Open the output file (for writing)
        with open(filename, 'w') as file:
            # Iterate over the containers and write each container's data
            for container in self.containers:
                position = f"[{container.row:02},{container.col:02}]"
                weight = f"{{{container.weight:05}}}"
                name = container.name

                # Write the formatted line to the file
                file.write(f"{position}, {weight}, {name}\n")
        
        # Log the operation with a timestamp
        log_entry = f"Finished a cycle. Manifest \"{filename.split('/')[-1]}\" has been written, and a reminder pop-up to the operator to send the file was displayed."
        self.submit_comment_load(log_entry)
    
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
                self.set_container_color(container, "deep sky blue", name_colors)  # Highlight with blue color
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
            self.set_container_color(container, "red2", name_colors)  # Highlight with red color

    def set_container_color(self, container, color, name_colors):
        widget = self.find_container_widget(container)
        widget.grid_forget()
        # Create a new label with updated color and info
        new_label = tk.Label(self.grid_frame, 
                             text=container.get_info(), 
                             font=("SF Pro", 10),
                             width=15, height=4, 
                             bg=color, relief='solid')

        # Re-add the new label to the same position
        new_label.grid(row=8 - container.row, column=container.col - 1, padx=2, pady=2)

        new_label.bind("<Button-1>", lambda event, container=container: self.on_left_click(event, container, name_colors))
        new_label.bind("<Button-3>", lambda event, container=container: self.on_right_click(event, container, name_colors))
        
        # Refresh the layout
        self.grid_frame.update_idletasks()

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

        self.set_container_color(container, original_color, name_colors)

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

    def write_output_manifest_balance(self, ship, filename):
        base, ext = filename.rsplit('.', 1)
        filename = f"{base}OUTBOUND.{ext}"
        with open(filename, 'w') as file:
            
            for r in range(7, -1, -1):
                for c in range(12):
                    container = ship.ship[r][c]
                    position = f"[{7-r+1:02},{c+1:02}]"
                    weight = f"{{{container.weight:05}}}"
                    name = container.name

                    file.write(f"{position}, {weight}, {name}\n")

    def balance(self):
        filename = filedialog.askopenfilename(title="Select Manifest", filetypes=[("Text Files", "*.txt")])
        if not filename:
            return

        # create Ship
        initial_ship = [[Container(weight=0, name="UNUSED", row=r, col=c, color='white') for c in range(12)] for r in range(8)]
        ship = Ship(initial_ship)
        
        ship.read_file(filename)
        
        window = tk.Toplevel(self)
        window.title("Balance")
        window.geometry("1920x1080")
        window.configure(bg='gray30')

        home_button = tk.Button(window, text="Home", font=("SF Pro", 12), bg='white', command=window.destroy)
        home_button.place(x=10, y=10)

        title_label = tk.Label(window, text="Balance", font=("SF Pro", 30, "bold"), bg='gray30', fg='white')
        title_label.pack(pady=20)

        grid_frame = tk.Frame(window, bg='gray30')
        grid_frame.pack(pady=20)
        
        
        # display grid
        rows, cols = 8, 12
        for r in range(rows):
            for c in range(cols):
                container = ship.ship[7 - r][c]
                        
                container_label = tk.Label(grid_frame, text=container.show_info(), font=("SF Pro", 10),
                            width=15, height=4, bg=container.color, relief='solid')
                container_label.grid(row=7 - r, column=c, padx=2, pady=2)
        
        bottom_frame = tk.Frame(window, bg='gray30')
        bottom_frame.pack(pady=20, fill='x')

        # For alignment
        bottom_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        bottom_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        bottom_frame.grid_columnconfigure(2, weight=1, uniform="group1")
        
        # Time Left Box (Left Column)
        time_frame = tk.Frame(bottom_frame, bg='gray30')
        time_frame.grid(row=0, column=0, padx=20, pady=5, sticky='ns')

        time_label = tk.Label(time_frame, text="Est. Time of Current Move: ", font=("SF Pro", 15), bg='gray30', fg='white')
        time_label.grid(row=0, column=0, padx=5)

        curr_move_label = tk.Label(time_frame, text=f"{self.current_move_time} minutes", font=("SF Pro", 15, "bold"), bg='gray20', fg='white', relief='solid', width=10)
        curr_move_label.grid(row=0, column=1, padx=5)
        
        next_button = tk.Button(bottom_frame, text="Next", font=("SF Pro", 12), bg='white', width=10, height=2,
                                command=lambda: [self.next_move(ship, grid_frame, window, filename),
                                                    curr_move_label.config(text=f"{self.current_move_time} minutes")])
        next_button.grid(row=0, column=1)

        # Comment Box and Submit Button (Middle Column)
        comment_frame = tk.Frame(bottom_frame, bg='gray30')
        comment_frame.grid(row=0, column=2, padx=20, pady=5, sticky='ew')

        comment_label = tk.Label(comment_frame, text="Comments:", font=("SF Pro", 15), bg='gray30', fg='white')
        comment_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        comment_entry = tk.Text(comment_frame, font=("SF Pro", 12), width=50, height=3)
        comment_entry.grid(row=1, column=0, padx=10, pady=5)

        submit_button = tk.Button(comment_frame, text="Submit", font=("SF Pro", 12), bg='white',
                                command=lambda: self.submit_comment(comment_entry))
        submit_button.grid(row=2, column=0, pady=10)
        
    def submit_comment_load(self, comment):
        if comment:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = f"{current_time}        {comment}\n"
            with open(log_file_name, "a") as log_file:
                log_file.write(log_entry)

    def submit_comment(self, comment_entry):
        comment = comment_entry.get("1.0", tk.END).strip()
        if comment:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = f"{current_time}        {comment}\n"
            with open(log_file_name, "a") as log_file:
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

    def next_move(self, ship, grid_frame, window, filename):
        best_move = ship.find_best_move()
        if not self.paths_to_animate:
            if ship.previous_best_move == best_move:
                self.write_output_manifest_balance(ship, filename)
                messagebox.showinfo("Balance Achieved", f"Optimal Balance Achieved! The file '{ship.filename}'.txt has been successfully saved to the desktop. Please review the details and send the file to the appropriate recipient.")
                window.destroy()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                log_entry = f"{current_time}        Finished a Cycle. Manifest '{ship.filename}OUTBOUND.txt' was written to desktop, and a reminder pop-up to operator to send file was displayed\n"
                with open(log_file_name, "a") as log_file:
                    log_file.write(log_entry)
                return
            
            start_row, start_col = best_move
            obstacles = ship.find_obstacles(start_row, start_col) # obstacles contain the position of obstacles above target
            
            if obstacles: # find paths for all obstacles
                for obstacle in obstacles:
                    row, col = obstacle
                    tempContainer = ship.ship[row][col]
                    tempObPath = ship.find_ob_path(row, col)
                    self.paths_to_animate.append((tempObPath, tempContainer))
                    ship.swap_containers(tempObPath[-1][0], tempObPath[-1][1], row, col)
            
            # find path for original target container
            container = ship.ship[start_row][start_col]
            path = ship.find_shortest_path(start_row, start_col)
            self.paths_to_animate.append((path, container))
            ship.swap_containers(start_row, start_col, path[-1][0], path[-1][1])
            ship.previous_best_move = path[-1]
        
        # animate paths for each obstacle
        if self.current_path_index < len(self.paths_to_animate):
            temp_ob_path, temp_container = self.paths_to_animate[self.current_path_index]
            self.animate_path(ship, temp_ob_path, temp_container, grid_frame)
            self.current_path_index += 1
        else: # no more paths to animate
            self.paths_to_animate = []
            self.current_path_index = 0
            if ship.is_balanced():
                self.write_output_manifest_balance(ship, filename)
                messagebox.showinfo("Balance Achieved", f"Optimal Balance Achieved! The file '{ship.filename}'.txt has been successfully saved to the desktop. Please review the details and send the file to the appropriate recipient.")
                window.destroy()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                log_entry = f"{current_time}        Finished a Cycle. Manifest '{ship.filename}OUTBOUND.txt' was written to desktop, and a reminder pop-up to operator to send file was displayed\n"
                with open(log_file_name, "a") as log_file:
                    log_file.write(log_entry)
                return
        

    def animate_path(self, ship, path, container, grid_frame):
        self.current_move_time = calculate_cost((container.row, container.col), (path[-1][0], path[-1][1]))
        def move(step=0): 
            if step == 0: # make 1st step empty
                original_label = grid_frame.grid_slaves(row=container.row, column=container.col)[0]
                original_label.config(
                    text="UNUSED\n0",
                    bg="white"
                )

            # clear previous position
            if step > 0:
                prev_row, prev_col = path[step - 1]
                prev_label = grid_frame.grid_slaves(row=prev_row, column=prev_col)[0]
                prev_label.config(
                    text="UNUSED\n0",
                    bg="white"
                )

            # update the current position
            if step < len(path):
                row, col = path[step]
                curr_label = grid_frame.grid_slaves(row=row, column=col)[0]
                curr_label.config(
                    text=ship.ship[path[-1][0]][path[-1][1]].show_info(),
                    bg=ship.ship[path[-1][0]][path[-1][1]].color
                )
                grid_frame.after(300, move, step + 1)
                
            else: # target container
                final_row, final_col = path[-1]
                final_container = ship.ship[final_row][final_col]
                final_label = grid_frame.grid_slaves(row=final_row, column=final_col)[0]
                final_label.config(
                    text=final_container.show_info(),
                    bg=final_container.color
                )

        move()

def calculate_cost(coord1, coord2):
    return abs(coord2[0] - coord1[0]) + abs(coord2[1] - coord1[1])\
        
# Main
if __name__ == "__main__":
    app = CraneApp()
    app.mainloop()