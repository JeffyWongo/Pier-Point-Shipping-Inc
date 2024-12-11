import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from Container import Container
from Ship import Ship

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

        tk.Button(btn_frame, text="Load/Unload", command=self.balance, font=("SF Pro", 15),
                  bg="white", width=25, height=3).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(btn_frame, text="Balance", command=self.balance, font=("SF Pro", 15),
                  bg="white", width=25, height=3).grid(row=0, column=1, padx=10, pady=5)

    def balance(self):
        filename = filedialog.askopenfilename(title="Select Manifest", filetypes=[("Text Files", "*.txt")])
        if not filename:
            return

        # Create Ship
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
        
        
        # Display grid
        rows, cols = 8, 12
        for r in range(rows):
            for c in range(cols):
                container = ship.ship[7 - r][c]
                        
                container_label = tk.Label(grid_frame, text=container.name, font=("SF Pro", 10),
                            width=15, height=4, bg=container.color, relief='solid')
                container_label.grid(row=7 - r, column=c, padx=2, pady=2)
                    
        # "Next" Button
        next_button_frame = tk.Frame(window, bg='gray30')
        next_button_frame.pack(pady=10)

        next_button = tk.Button(next_button_frame, text="Next", font=("SF Pro", 12), bg='white', 
                                command=lambda: self.next_move(ship, grid_frame, window))
        next_button.grid(row=0, column=0)

        # Comment Box and Submit Button
        comment_frame = tk.Frame(window, bg='gray30')
        comment_frame.pack(pady=20)

        comment_label = tk.Label(comment_frame, text="Comments:", font=("SF Pro", 15), bg='gray30', fg='white')
        comment_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        comment_entry = tk.Text(comment_frame, font=("SF Pro", 12), width=50, height=5)
        comment_entry.grid(row=1, column=0, padx=10, pady=5)

        submit_button = tk.Button(comment_frame, text="Submit", font=("SF Pro", 12), bg='white',
                                command=lambda: self.submit_comment(comment_entry))
        submit_button.grid(row=2, column=0, pady=10)

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

    def next_move(self, ship, grid_frame, window):
        best_move = ship.find_best_move()
        
        if ship.is_balanced():
            if messagebox.showinfo("Balance Achieved", "Optimal Balance Achieved!"):
                window.destroy()
            return
        
        start_row, start_col = best_move
        print(start_row)
        print(start_col)
        container = ship.ship[start_row][start_col]
        path = ship.find_shortest_path(start_row, start_col)
        print(container.row)
        print(container.col)
        # Animate the container movement
        self.animate_path(path, container, grid_frame)
        ship.modify_ship(path[-1][0], path[-1][1], container.weight)
        ship.previous_best_move = path[-1]
        ship.modify_ship(start_row, start_col, 0)

    def animate_path(self, path, container, grid_frame):
        def move(step=0):
            if step == 0:
                print(container.row)
                print(container.col)
                # Clear the original position at the start of the animation
                original_label = grid_frame.grid_slaves(row=container.row, column=container.col)[0]
                original_label.config(
                    text="UNUSED",
                    bg="white"
                )
            
            if step > 0:
                # Clear the previous position
                prev_row, prev_col = path[step - 1]
                prev_label = grid_frame.grid_slaves(row=prev_row, column=prev_col)[0]
                prev_label.config(
                    text="UNUSED", 
                    bg="white"
                )
            
            if step < len(path):
                # Update the current position
                row, col = path[step]
                curr_label = grid_frame.grid_slaves(row=row, column=col)[0]
                curr_label.config(
                    text=container.name, 
                    bg="lightgreen"
                )
                # Schedule the next step
                grid_frame.after(500, move, step + 1)
                
            else:
                # At the end of the path, set the container at its final destination
                final_row, final_col = path[-1]
                final_label = grid_frame.grid_slaves(row=final_row, column=final_col)[0]
                final_label.config(
                    text=container.name,
                    bg=container.color
                )
   
        move()  # Start the animation


# Main
if __name__ == "__main__":
    app = CraneApp()
    app.mainloop()