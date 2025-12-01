# 🚦 Traffic Digital Twin  
### SUMO + YOLOv8 for Vision-Based Traffic Flow Analysis & Policy Evaluation

This project creates a **Traffic Digital Twin pipeline** that connects **real video data** with a **SUMO simulation**, enabling comparison between *actual traffic* and *simulated traffic policies*.

It performs 3 major tasks:

1. **YOLOv8 Vehicle Detection**  
   - Extract vehicles per frame from a real traffic video  
   - Save results to `outputs/yolo_detections.csv`

2. **SUMO Simulation**  
   - Runs a SUMO intersection with custom routes and timing  
   - Outputs simulated traffic counts in `outputs/sumo_traffic.csv`

3. **Policy Analysis**  
   - Compares SUMO traffic with real video  
   - Tests multiple signal timing policies  
   - Saves summary to:  
     `outputs/policy_results.csv`

---

# 📁 Project Structure

```
traffic-digital-twin/
│
├── src/
│   ├── detect_traffic.py       # YOLOv8 detection from mp4 video
│   ├── run_sumo.py             # SUMO simulation runner
│   ├── analyze_policy.py       # Compare YOLO vs SUMO, evaluate policies
│
├── sumo/
│   ├── intersection.net.xml    # SUMO network
│   ├── routes.rou.xml          # Vehicle route definitions
│   ├── sim.sumocfg             # Simulation config
│   └── trips.trips.xml         # (optional) extra SUMO trips
│
├── outputs/
│   ├── yolo_detections.csv     # Saved YOLO vehicle counts
│   ├── sumo_traffic.csv        # Saved SUMO traffic counts
│   └── policy_results.csv      # Comparison of traffic policies
│
├── data/
│   └── traffic_video.mp4       # (ignored) your real traffic video
│
└── .gitignore                  # ignores venv, mp4, outputs, models
```

---

# 🏁 How to Run

## 1️⃣ Install dependencies
Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

(*If you want, I can generate a full requirements.txt for you.*)

---

## 2️⃣ Add your traffic video

Place any `.mp4` file here:

```
/data/traffic_video.mp4
```

---

## 3️⃣ Run YOLO Detection

```bash
python src/detect_traffic.py
```

This produces:

```
outputs/yolo_detections.csv
```

---

## 4️⃣ Run SUMO Simulation

```bash
python src/run_sumo.py
```

Produces:

```
outputs/sumo_traffic.csv
```

---

## 5️⃣ Run Policy Evaluation

```bash
python src/analyze_policy.py
```

Produces:

```
outputs/policy_results.csv
```

---

# 📊 Example Output (Policy Results)

| policy    | source | total_vehicles | mean_per_window | std_per_window |
|-----------|--------|----------------|------------------|----------------|
| Policy_A  | SUMO   | 12573          | 3157.00          | 118.55         |
| Policy_B  | SUMO   | 6286           | 628.65           | 81.30          |
| YOLO      | Video  | 3157           | —                | —              |

---

# 🧠 Future Improvements
- Add reinforcement learning for light timing  
- Live camera streaming  
- Multi-intersection networks  
- Multi-class vehicle detection  
- Calibration between real + simulated traffic  

---

# 📜 License
MIT License (optional — ask me if you want it)

---

# 👤 Author
**Sara Momen (saramomen1357)**  
Traffic Systems • Digital Twins • AI for Mobility

