import os
from pathlib import Path
import pandas as pd
import traci

ROOT = Path(__file__).resolve().parents[1]
SUMO_DIR = ROOT / "sumo"
CFG_PATH = SUMO_DIR / "sim.sumocfg"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)
CSV_PATH = OUTPUTS_DIR / "sumo_traffic.csv"

def get_sumo_binary():
    # use sumo (no GUI)
    return os.environ.get("SUMO_BINARY", "sumo")

def main():
    if not CFG_PATH.exists():
        raise FileNotFoundError(f"SUMO config not found at {CFG_PATH}")

    sumo_binary = get_sumo_binary()
    sumo_cmd = [
        sumo_binary,
        "-c", str(CFG_PATH),
        "--step-length", "1.0",
        "--no-step-log", "true",
    ]

    print("[INFO] Starting SUMO...")
    traci.start(sumo_cmd)

    records = []
    step = 0
    try:
        while step < 600:  # 600 seconds = 10 minutes
            traci.simulationStep()

            veh_ids = traci.vehicle.getIDList()
            vehicle_count = len(veh_ids)

            records.append({
                "time_step": step,
                "vehicle_count": vehicle_count,
            })

            if step % 50 == 0:
                print(f"[INFO] Step {step}, vehicles in network: {vehicle_count}")

            step += 1
    finally:
        traci.close()
        print("[INFO] SUMO simulation ended.")

    df = pd.DataFrame(records)
    df["time_sec"] = df["time_step"].astype(float)
    df.to_csv(CSV_PATH, index=False)
    print(f"[DONE] Saved SUMO traffic data to {CSV_PATH}")

if __name__ == "__main__":
    main()
