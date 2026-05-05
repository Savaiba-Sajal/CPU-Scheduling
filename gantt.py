import matplotlib.pyplot as plt

def draw_gantt(schedule, title="Gantt Chart"):
    fig, ax = plt.subplots()

    for i, p in enumerate(schedule):
        ax.barh(0, p['burst'], left=p['start'])
        ax.text(p['start'], 0, f"P{p['pid']}")

    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_yticks([])
    plt.show()


def draw_rr_gantt(timeline):
    fig, ax = plt.subplots()

    for pid, start, end in timeline:
        ax.barh(0, end - start, left=start)
        ax.text(start, 0, f"P{pid}")

    ax.set_title("Round Robin Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_yticks([])
    plt.show()