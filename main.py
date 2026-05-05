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

        if burst <= 0:
            messagebox.showerror("Error", "Burst Time must be greater than 0")
            return

        # Check for duplicate PID
        if any(p['pid'] == pid for p in processes):
            messagebox.showerror("Error", f"PID {pid} already exists")
            return

        processes.append({
            'pid': pid,
            'arrival': arrival,
            'burst': burst,
            'priority': priority
        })

        table.insert("", "end", values=(pid, arrival, burst, priority))

        # Clear input fields after adding
        pid_entry.delete(0, tk.END)
        arrival_entry.delete(0, tk.END)
        burst_entry.delete(0, tk.END)
        priority_entry.delete(0, tk.END)
        pid_entry.focus()

    except ValueError:
        messagebox.showerror("Error", "All fields must be valid integers")


def clear_processes():
    processes.clear()
    for row in table.get_children():
        table.delete(row)
    for row in result_table.get_children():
        result_table.delete(row)
    avg_label.config(text="")


def run_algorithm():
    if not processes:
        messagebox.showerror("Error", "No processes added")
        return

    algo = algo_combo.get()

    # Clear previous results
    for row in result_table.get_children():
        result_table.delete(row)
    avg_label.config(text="")

    if algo == "FCFS":
        result = fcfs(processes)
        show_results(result)
        draw_gantt(result, title="FCFS Gantt Chart")

    elif algo == "SJF":
        result = sjf(processes)
        show_results(result)
        draw_gantt(result, title="SJF Gantt Chart")

    elif algo == "Priority":
        result = priority_scheduling(processes)
        show_results(result)
        draw_gantt(result, title="Priority Scheduling Gantt Chart")

    elif algo == "Round Robin":
        # BUG FIX: validate quantum before running
        try:
            quantum = int(quantum_entry.get())
            if quantum <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for Quantum")
            return
        result, timeline = round_robin(processes, quantum)
        show_results(result)
        draw_rr_gantt(timeline, completed=result)

    else:
        messagebox.showerror("Error", "Please select a scheduling algorithm")


def show_results(result):
    """BUG FIX: Display WT and TAT in the results table."""
    for p in result:
        result_table.insert("", "end", values=(
            p['pid'], p['arrival'], p['burst'],
            p.get('start', '-'), p['completion'],
            p['wt'], p['tat']
        ))

    avg_wt = sum(p['wt'] for p in result) / len(result)
    avg_tat = sum(p['tat'] for p in result) / len(result)
    avg_label.config(
        text=f"Average Waiting Time: {avg_wt:.2f}    |    Average Turnaround Time: {avg_tat:.2f}"
    )


# ── GUI ───────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("900x650")
root.resizable(True, True)

# ── Input frame ───────────────────────────────────────────────────────────────
input_frame = tk.LabelFrame(root, text="Add Process", padx=10, pady=5)
input_frame.pack(fill="x", padx=10, pady=5)

labels = ["PID", "Arrival Time", "Burst Time", "Priority"]
for i, lbl in enumerate(labels):
    tk.Label(input_frame, text=lbl).grid(row=0, column=i, padx=5)

pid_entry     = tk.Entry(input_frame, width=8)
arrival_entry = tk.Entry(input_frame, width=8)
burst_entry   = tk.Entry(input_frame, width=8)
priority_entry = tk.Entry(input_frame, width=8)

for i, entry in enumerate([pid_entry, arrival_entry, burst_entry, priority_entry]):
    entry.grid(row=1, column=i, padx=5)

tk.Button(input_frame, text="Add Process", command=add_process,
          bg="#4e79a7", fg="white").grid(row=1, column=4, padx=5)
tk.Button(input_frame, text="Clear All", command=clear_processes,
          bg="#e15759", fg="white").grid(row=1, column=5, padx=5)

# ── Process table ─────────────────────────────────────────────────────────────
proc_frame = tk.LabelFrame(root, text="Processes", padx=10, pady=5)
proc_frame.pack(fill="x", padx=10, pady=5)

columns = ("PID", "Arrival", "Burst", "Priority")
table = ttk.Treeview(proc_frame, columns=columns, show="headings", height=4)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=80, anchor="center")
table.pack(fill="x")

# ── Algorithm selection ───────────────────────────────────────────────────────
algo_frame = tk.LabelFrame(root, text="Algorithm", padx=10, pady=5)
algo_frame.pack(fill="x", padx=10, pady=5)

tk.Label(algo_frame, text="Algorithm:").grid(row=0, column=0, padx=5)
algo_combo = ttk.Combobox(algo_frame, values=["FCFS", "SJF", "Priority", "Round Robin"],
                          state="readonly", width=15)
algo_combo.grid(row=0, column=1, padx=5)

tk.Label(algo_frame, text="Quantum (RR only):").grid(row=0, column=2, padx=5)
quantum_entry = tk.Entry(algo_frame, width=6)
quantum_entry.grid(row=0, column=3, padx=5)

tk.Button(algo_frame, text="  Run  ", command=run_algorithm,
          bg="#59a14f", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10)

# ── Results table ─────────────────────────────────────────────────────────────
result_frame = tk.LabelFrame(root, text="Results", padx=10, pady=5)
result_frame.pack(fill="both", expand=True, padx=10, pady=5)

res_cols = ("PID", "Arrival", "Burst", "Start", "Completion", "Waiting Time", "Turnaround Time")
result_table = ttk.Treeview(result_frame, columns=res_cols, show="headings", height=6)
for col in res_cols:
    result_table.heading(col, text=col)
    result_table.column(col, width=110, anchor="center")
result_table.pack(fill="both", expand=True)

avg_label = tk.Label(result_frame, text="", font=("Arial", 10, "bold"), fg="#4e79a7")
avg_label.pack(pady=5)

root.mainloop()
