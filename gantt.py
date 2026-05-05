import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# A set of distinct colors for up to 10 processes
COLORS = [
    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
    '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
    '#9c755f', '#bab0ac'
]


def draw_gantt(schedule, title="Gantt Chart"):
    fig, ax = plt.subplots(figsize=(10, 3))

    pid_list = sorted(set(p['pid'] for p in schedule))
    color_map = {pid: COLORS[i % len(COLORS)] for i, pid in enumerate(pid_list)}

    for p in schedule:
        color = color_map[p['pid']]
        ax.barh(0, p['burst'], left=p['start'], color=color,
                edgecolor='black', height=0.5)
        # BUG FIX: center the label inside each bar
        ax.text(p['start'] + p['burst'] / 2, 0,
                f"P{p['pid']}", ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    # Add time ticks at each process boundary
    ticks = sorted(set([p['start'] for p in schedule] +
                       [p['completion'] for p in schedule]))
    ax.set_xticks(ticks)

    legend_patches = [mpatches.Patch(color=color_map[pid], label=f'P{pid}')
                      for pid in pid_list]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=8)

    # Show WT and TAT summary below the chart
    summary = "  |  ".join(
        f"P{p['pid']}: WT={p['wt']}  TAT={p['tat']}" for p in schedule
    )
    avg_wt = sum(p['wt'] for p in schedule) / len(schedule)
    avg_tat = sum(p['tat'] for p in schedule) / len(schedule)

    fig.text(0.5, -0.15, summary, ha='center', fontsize=8)
    fig.text(0.5, -0.30,
             f"Avg Waiting Time: {avg_wt:.2f}   |   Avg Turnaround Time: {avg_tat:.2f}",
             ha='center', fontsize=9, fontweight='bold')

    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_yticks([])
    plt.tight_layout()
    plt.show()


def draw_rr_gantt(timeline, completed=None):
    fig, ax = plt.subplots(figsize=(10, 3))

    pid_list = sorted(set(pid for pid, _, _ in timeline))
    color_map = {pid: COLORS[i % len(COLORS)] for i, pid in enumerate(pid_list)}

    for pid, start, end in timeline:
        color = color_map[pid]
        ax.barh(0, end - start, left=start, color=color,
                edgecolor='black', height=0.5)
        # BUG FIX: center the label inside each bar
        ax.text(start + (end - start) / 2, 0,
                f"P{pid}", ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    ticks = sorted(set([s for _, s, _ in timeline] + [e for _, _, e in timeline]))
    ax.set_xticks(ticks)

    legend_patches = [mpatches.Patch(color=color_map[pid], label=f'P{pid}')
                      for pid in pid_list]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=8)

    if completed:
        summary = "  |  ".join(
            f"P{p['pid']}: WT={p['wt']}  TAT={p['tat']}" for p in completed
        )
        avg_wt = sum(p['wt'] for p in completed) / len(completed)
        avg_tat = sum(p['tat'] for p in completed) / len(completed)
        fig.text(0.5, -0.15, summary, ha='center', fontsize=8)
        fig.text(0.5, -0.30,
                 f"Avg Waiting Time: {avg_wt:.2f}   |   Avg Turnaround Time: {avg_tat:.2f}",
                 ha='center', fontsize=9, fontweight='bold')

    ax.set_title("Round Robin Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_yticks([])
    plt.tight_layout()
    plt.show()
