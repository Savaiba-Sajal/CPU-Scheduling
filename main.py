import tkinter as tk
from tkinter import ttk, messagebox
from algorithms import fcfs, sjf, priority_scheduling, round_robin
from gantt import draw_gantt, draw_rr_gantt

processes = []

def add_process():
    try:
        pid = int(pid_entry.get())
        arrival = int(arrival_entry.get())
        burst = int(burst_entry.get())
        priority = int(priority_entry.get())

        processes.append({
            'pid': pid,
            'arrival': arrival,
            'burst': burst,
            'priority': priority
        })

        table.insert("", "end", values=(pid, arrival, burst, priority))

    except:
        messagebox.showerror("Error", "Invalid Input")


def run_algorithm():
    if not processes:
        messagebox.showerror("Error", "No processes added")
        return

    algo = algo_combo.get()

    if algo == "FCFS":
        result = fcfs(processes)
        draw_gantt(result)

    elif algo == "SJF":
        result = sjf(processes)
        draw_gantt(result)

    elif algo == "Priority":
        result = priority_scheduling(processes)
        draw_gantt(result)

    elif algo == "Round Robin":
        quantum = int(quantum_entry.get())
        result, timeline = round_robin(processes, quantum)
        draw_rr_gantt(timeline)

    else:
        messagebox.showerror("Error", "Select algorithm")


# GUI
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("800x600")

# Inputs
tk.Label(root, text="PID").grid(row=0, column=0)
tk.Label(root, text="Arrival").grid(row=0, column=1)
tk.Label(root, text="Burst").grid(row=0, column=2)
tk.Label(root, text="Priority").grid(row=0, column=3)

pid_entry = tk.Entry(root)
arrival_entry = tk.Entry(root)
burst_entry = tk.Entry(root)
priority_entry = tk.Entry(root)

pid_entry.grid(row=1, column=0)
arrival_entry.grid(row=1, column=1)
burst_entry.grid(row=1, column=2)
priority_entry.grid(row=1, column=3)

tk.Button(root, text="Add Process", command=add_process).grid(row=1, column=4)

# Table
columns = ("PID", "Arrival", "Burst", "Priority")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)

table.grid(row=2, column=0, columnspan=5, pady=20)

# Algorithm selection
algo_combo = ttk.Combobox(root, values=["FCFS", "SJF", "Priority", "Round Robin"])
algo_combo.grid(row=3, column=0)

tk.Label(root, text="Quantum").grid(row=3, column=1)
quantum_entry = tk.Entry(root)
quantum_entry.grid(row=3, column=2)

tk.Button(root, text="Run", command=run_algorithm).grid(row=3, column=3)

root.mainloop()