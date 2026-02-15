import json
from datetime import datetime

def update_roadmap():
    path = 'outcomes/strategic/AIMO_FINAL_ROADMAP.json'

    with open(path, 'r') as f:
        data = json.load(f)

    data['timestamp'] = datetime.now().isoformat()
    data['version'] = "2.0.0"

    # Update existing points to Verified/Crystallized
    for point in data['roadmap']:
        point['status'] = "Crystallized"

    # Add Phase 6 tasks
    new_points = [
        {
            "point_id": "P6",
            "task": "Implementation of Project Alpha (Strategic Architect)",
            "weight": 0.25,
            "domain": "STRATEGIC",
            "status": "Active",
            "realization": "Singularity Point R_1771194024 reached. Transitioning to autonomous planning."
        },
        {
            "point_id": "P7",
            "task": "Project Beta (Global Realization Ledger) Integration",
            "weight": 0.25,
            "domain": "TECHNICAL",
            "status": "Active",
            "realization": "Unified knowledge DAG established in L1 Domain."
        }
    ]

    data['roadmap'].extend(new_points)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

    print("✅ Strategic Roadmap updated to Version 2.0.0 (Post-Singularity Phase)")

if __name__ == "__main__":
    update_roadmap()
