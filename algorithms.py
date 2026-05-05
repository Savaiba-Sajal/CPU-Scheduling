import copy
from collections import deque


def calculate_avg(times):
    return sum(times) / len(times) if times else 0


def fcfs(processes):
    processes = sorted(copy.deepcopy(processes), key=lambda x: x['arrival'])
    time = 0
    result = []

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start = time
        time += p['burst']
        completion = time
        tat = completion - p['arrival']
        wt = tat - p['burst']

        result.append({**p, 'start': start, 'completion': completion,
                       'tat': tat, 'wt': wt})

    return result


def sjf(processes):
    # BUG FIX: deep copy so original list is never mutated between runs
    processes = sorted(copy.deepcopy(processes), key=lambda x: (x['arrival'], x['burst']))
    time = 0
    completed = []
    ready = []

    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))

        if not ready:
            time = processes[0]['arrival']
            continue

        ready.sort(key=lambda x: x['burst'])
        p = ready.pop(0)

        start = time
        time += p['burst']
        completion = time
        tat = completion - p['arrival']
        wt = tat - p['burst']

        completed.append({**p, 'start': start, 'completion': completion,
                          'tat': tat, 'wt': wt})

    return completed


def priority_scheduling(processes):
    # BUG FIX: deep copy so original list is never mutated between runs
    processes = sorted(copy.deepcopy(processes), key=lambda x: (x['arrival'], x['priority']))
    time = 0
    completed = []
    ready = []

    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))

        if not ready:
            time = processes[0]['arrival']
            continue

        ready.sort(key=lambda x: x['priority'])
        p = ready.pop(0)

        start = time
        time += p['burst']
        completion = time
        tat = completion - p['arrival']
        wt = tat - p['burst']

        completed.append({**p, 'start': start, 'completion': completion,
                          'tat': tat, 'wt': wt})

    return completed


def round_robin(processes, quantum):
    queue = deque()
    time = 0
    # BUG FIX: deep copy so original list is never mutated between runs
    processes = sorted(copy.deepcopy(processes), key=lambda x: x['arrival'])
    remaining = {p['pid']: p['burst'] for p in processes}
    completed = []
    timeline = []

    i = 0
    while i < len(processes) or queue:
        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            time = processes[i]['arrival']
            continue

        p = queue.popleft()
        exec_time = min(quantum, remaining[p['pid']])

        start = time
        time += exec_time
        remaining[p['pid']] -= exec_time
        timeline.append((p['pid'], start, time))

        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i])
            i += 1

        if remaining[p['pid']] > 0:
            queue.append(p)
        else:
            completion = time
            tat = completion - p['arrival']
            wt = tat - p['burst']
            completed.append({**p, 'completion': completion,
                              'tat': tat, 'wt': wt})

    return completed, timeline
