from flask import Flask, render_template, jsonify, request
from collections import deque

app = Flask(__name__)

disasters = {
    "EARTHQUAKE": {
        "safety_actions": ["Drop, Cover, Hold On", "Stay away from windows", "Evacuate after shaking stops"],
        "emergency_contacts": ["Police: 7676154914", "Ambulance: 8217850392", "Disaster Helpline: 1078"]
    },
    "FIRE": {
        "safety_actions": ["Activate fire alarm", "Evacuate via fire exits", "Stay low if there's smoke"],
        "emergency_contacts": ["Fire Dept: 101", "Ambulance: 108", "Police: 100"]
    },
    "FLOOD": {
        "safety_actions": ["Move to higher ground", "Avoid floodwater", "Turn off electricity"],
        "emergency_contacts": ["Flood Control: 1070", "Ambulance: 108", "Police: 100"]
    },
    "CYCLONE": {
        "safety_actions": ["Seek strong shelter", "Stay away from windows", "Don't go out during eye of storm"],
        "emergency_contacts": ["Cyclone Warning: 1800-180-1717", "Ambulance: 108", "Police: 100"]
    }
}

def calculate_score(checked_items, total_items):
    if total_items == 0:
        return 0
    score = (checked_items / total_items) * 100
    return round(score)

def get_status(score):
    if score == 100:
        return "Fully Prepared"
    elif score >= 83:
        return "One more step to go"
    elif score >= 67:
        return "Almost Prepared"
    elif score >= 50:
        return "Halfway Done"
    elif score >= 33:
        return "Still More To Go"
    elif score >= 17:
        return "Needs Improvement"
    else:
        return "Start Preparing"

def bfs_evacuation(grid, start, exit_point):
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    queue = deque()
    queue.append((start, [start]))
    visited.add(start)

    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == exit_point:
            return path
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            new_pos = (new_row, new_col)
            if (0 <= new_row < rows and
                0 <= new_col < cols and
                grid[new_row][new_col] == 0 and
                new_pos not in visited):
                visited.add(new_pos)
                queue.append((new_pos, path + [new_pos]))
    return []

@app.route("/")
def index():
    return render_template("index.html", disaster_types=list(disasters.keys()))

@app.route("/get_disaster", methods=["POST"])
def get_disaster():
    data = request.json
    disaster_type = data.get("disaster_type")
    result = disasters.get(disaster_type, {})
    score = calculate_score(0, 6)
    status = get_status(score)
    return jsonify({
        "disaster_type": disaster_type,
        "preparedness_score": score,
        "safety_actions": result.get("safety_actions", []),
        "emergency_contacts": result.get("emergency_contacts", []),
        "status": status
    })

@app.route("/get_evacuation", methods=["POST"])
def get_evacuation():
    grid = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    exit_point = (4, 4)
    path = bfs_evacuation(grid, start, exit_point)
    return jsonify({
        "algorithm": "BFS",
        "start": start,
        "exit": exit_point,
        "shortest_path": path,
        "total_steps": len(path) - 1,
        "path_found": len(path) > 0
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')