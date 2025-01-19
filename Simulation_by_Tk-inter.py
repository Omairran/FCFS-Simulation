import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
import random

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.state = "New"

def calculate_fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0

    for process in processes:
        # Move process to Ready state
        process.state = "Ready"
        update_queues()
        time.sleep(1)

        # If CPU is idle, move the time forward
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        # Move process to Running state
        process.state = "Running"
        update_queues()
        time.sleep(1)

        # Simulate process execution
        time.sleep(process.burst_time)
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        
        # Move process to Termination state
        process.state = "Termination"
        update_queues()
        current_time = process.completion_time


def animate_gantt_chart(canvas, processes):
    canvas.delete("all")
    x_start = 10
    y_start = 50
    height = 50
    unit_width = 50  # Each unit of time = 50px
    current_time = 0
    colors = ["#ff9999", "#99ccff", "#99ff99", "#ffcc99", "#cc99ff"]  # Color palette for processes

    for process in processes:
        if current_time < process.arrival_time:
            idle_width = (process.arrival_time - current_time) * unit_width
            canvas.create_rectangle(x_start, y_start, x_start + idle_width, y_start + height, fill="gray")
            canvas.create_text(x_start + idle_width / 2, y_start + height / 2, text="Idle", fill="white")
            canvas.create_text(x_start, y_start + height + 15, text=str(current_time), anchor="w", font=("Helvetica", 10))
            canvas.update()
            time.sleep(0.5)
            x_start += idle_width
            current_time = process.arrival_time

        burst_width = process.burst_time * unit_width
        process_color = random.choice(colors)
        canvas.create_rectangle(x_start, y_start, x_start + burst_width, y_start + height, fill=process_color)
        canvas.create_text(x_start + burst_width / 2, y_start + height / 2, text=f"P{process.pid}", fill="black")
        canvas.create_text(x_start, y_start + height + 30, text=f"Arr: {process.arrival_time}", anchor="w", font=("Helvetica", 10), fill="blue")
        canvas.create_text(x_start, y_start + height + 15, text=str(current_time), anchor="w", font=("Helvetica", 10))
        canvas.update()
        time.sleep(0.5)
        x_start += burst_width
        current_time += process.burst_time

    canvas.create_text(x_start, y_start + height + 15, text=str(current_time), anchor="w", font=("Helvetica", 10))
    canvas.config(scrollregion=canvas.bbox("all"))

def display_process_info(tree, processes):
    for row in tree.get_children():
        tree.delete(row)
    for process in processes:
        tree.insert("", "end", values=(
            process.pid,
            process.arrival_time,
            process.burst_time,
            process.completion_time,
            process.turnaround_time,
            process.waiting_time,
            process.state,
        ))

def add_process():
    try:
        pid = len(process_list) + 1
        arrival_time = int(arrival_time_var.get())
        burst_time = int(burst_time_var.get())
        process_list.append(Process(pid, arrival_time, burst_time))
        arrival_time_var.set("")
        burst_time_var.set("")
        update_process_list()
        update_queues()
    except ValueError:
        pass

def simulate_fcfs():
    if not process_list:
        return
    simulation_thread = Thread(target=run_simulation)
    simulation_thread.start()

def run_simulation():
    calculate_fcfs(process_list)
    display_process_info(process_table, process_list)

    # Run the Gantt Chart animation in a separate thread
    animation_thread = Thread(target=animate_gantt_chart, args=(gantt_canvas, process_list))
    animation_thread.start()

def update_process_list():
    process_list_label.config(text=f"Total Processes: {len(process_list)}")

def update_queues():
    new_queue.delete("1.0", tk.END)
    ready_queue.delete("1.0", tk.END)
    running_queue.delete("1.0", tk.END)
    waiting_queue.delete("1.0", tk.END)
    termination_queue.delete("1.0", tk.END)

    for process in process_list:
        if process.state == "New":
            new_queue.insert(tk.END, f"P{process.pid}\n")
        elif process.state == "Ready":
            ready_queue.insert(tk.END, f"P{process.pid}\n")
        elif process.state == "Running":
            running_queue.insert(tk.END, f"P{process.pid}\n")
        elif process.state == "Waiting":
            waiting_queue.insert(tk.END, f"P{process.pid}\n")
        elif process.state == "Termination":
            termination_queue.insert(tk.END, f"P{process.pid}\n")

# Main Tkinter Application
root = tk.Tk()
root.title("FCFS Scheduling Simulation")
root.geometry("1200x800")
root.configure(bg="#f0f4f7")

# Title
title_label = tk.Label(root, text="First-Come, First-Served (FCFS) Scheduling Simulation", font=("Helvetica", 16, "bold"), bg="#f0f4f7")
title_label.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="#f0f4f7", padx=10, pady=10)
input_frame.pack(fill="x")

tk.Label(input_frame, text="Arrival Time:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=5)
arrival_time_var = tk.StringVar()
arrival_entry = tk.Entry(input_frame, textvariable=arrival_time_var, font=("Helvetica", 12), width=10)
arrival_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Burst Time:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=2, padx=5)
burst_time_var = tk.StringVar()
burst_entry = tk.Entry(input_frame, textvariable=burst_time_var, font=("Helvetica", 12), width=10)
burst_entry.grid(row=0, column=3, padx=5)

add_button = tk.Button(input_frame, text="Add Process", font=("Helvetica", 12), command=add_process, bg="#4caf50", fg="white")
add_button.grid(row=0, column=4, padx=10)

simulate_button = tk.Button(input_frame, text="Simulate FCFS", font=("Helvetica", 12), command=simulate_fcfs, bg="#2196f3", fg="white")
simulate_button.grid(row=0, column=5, padx=10)

process_list_label = tk.Label(input_frame, text="Total Processes: 0", font=("Helvetica", 12, "italic"), bg="#f0f4f7")
process_list_label.grid(row=0, column=6, padx=10)

# Process Table
process_table_frame = tk.Frame(root, bg="#f0f4f7")
process_table_frame.pack(pady=10, fill="x")

process_table_label = tk.Label(process_table_frame, text="Process Details", font=("Helvetica", 14, "bold"), bg="#f0f4f7")
process_table_label.pack(anchor="w", padx=10)

process_table = ttk.Treeview(process_table_frame, columns=("PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting", "State"), show="headings", height=8)
process_table.pack(fill="x", padx=10)

for col in process_table["columns"]:
    process_table.heading(col, text=col)
    process_table.column(col, anchor="center", width=100)

# Queues Frame
queues_frame = tk.Frame(root, bg="#f0f4f7")
queues_frame.pack(pady=10, fill="x")

tk.Label(queues_frame, text="New Queue", font=("Helvetica", 12, "bold"), bg="#f0f4f7").grid(row=0, column=0, padx=10)
tk.Label(queues_frame, text="Ready Queue", font=("Helvetica", 12, "bold"), bg="#f0f4f7").grid(row=0, column=1, padx=10)
tk.Label(queues_frame, text="Running Queue", font=("Helvetica", 12, "bold"), bg="#f0f4f7").grid(row=0, column=2, padx=10)
tk.Label(queues_frame, text="Waiting Queue", font=("Helvetica", 12, "bold"), bg="#f0f4f7").grid(row=0, column=3, padx=10)
tk.Label(queues_frame, text="Termination Queue", font=("Helvetica", 12, "bold"), bg="#f0f4f7").grid(row=0, column=4, padx=10)

new_queue = tk.Text(queues_frame, height=10, width=30, state="normal")
new_queue.grid(row=1, column=0, padx=10)

ready_queue = tk.Text(queues_frame, height=10, width=30, state="normal")
ready_queue.grid(row=1, column=1, padx=10)

running_queue = tk.Text(queues_frame, height=10, width=30, state="normal")
running_queue.grid(row=1, column=2, padx=10)

waiting_queue = tk.Text(queues_frame, height=10, width=30, state="normal")
waiting_queue.grid(row=1, column=3, padx=10)

termination_queue = tk.Text(queues_frame, height=10, width=30, state="normal")
termination_queue.grid(row=1, column=4, padx=10)

# Gantt Chart Frame
gantt_frame = tk.Frame(root, bg="#f0f4f7", pady=10)
gantt_frame.pack(fill="both", expand=True)

gantt_canvas_label = tk.Label(gantt_frame, text="Gantt Chart", font=("Helvetica", 14, "bold"), bg="#f0f4f7")
gantt_canvas_label.pack(anchor="w", padx=10)

gantt_canvas = tk.Canvas(gantt_frame, height=100, bg="white")
gantt_canvas.pack(fill="both", expand=True, padx=10, pady=10)

process_list = []  # Global list to store processes

root.mainloop()