import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Base paths
ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
FIG_DIR = OUTPUTS / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Helper ----------

def safe_read_csv(path: Path, name: str):
    if not path.exists():
        print(f"[WARN] {name} not found at {path}")
        return None
    print(f"[INFO] Loaded {name} from {path}")
    return pd.read_csv(path)

# ---------- 1. YOLO vs SUMO time-series ----------

def plot_yolo_vs_sumo():
    yolo_path = OUTPUTS / "yolo_detections.csv"
    sumo_path = OUTPUTS / "sumo_traffic.csv"

    yolo = safe_read_csv(yolo_path, "YOLO detections")
    sumo = safe_read_csv(sumo_path, "SUMO traffic")

    if yolo is None or sumo is None:
        return

    # Expect columns: frame,time_sec,vehicle_count (YOLO)
    # and time_step,vehicle_count,time_sec (SUMO)
    plt.figure()
    plt.plot(yolo["time_sec"], yolo["vehicle_count"], label="YOLO (video)")
    plt.plot(sumo["time_sec"], sumo["vehicle_count"], label="SUMO (simulation)")

    plt.xlabel("Time [s]")
    plt.ylabel("Vehicle count")
    plt.title("Vehicle count over time: YOLO vs SUMO")
    plt.legend()
    plt.grid(True, alpha=0.3)

    out_path = FIG_DIR / "yolo_vs_sumo_timeseries.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"[DONE] Saved {out_path}")

# ---------- 2. YOLO vehicle-count histogram ----------

def plot_yolo_hist():
    yolo_path = OUTPUTS / "yolo_detections.csv"
    yolo = safe_read_csv(yolo_path, "YOLO detections")
    if yolo is None:
        return

    plt.figure()
    plt.hist(yolo["vehicle_count"], bins=20)
    plt.xlabel("Vehicles per frame")
    plt.ylabel("Frequency")
    plt.title("Distribution of detected vehicles per frame (YOLO)")
    plt.grid(True, alpha=0.3)

    out_path = FIG_DIR / "yolo_vehicle_histogram.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"[DONE] Saved {out_path}")

# ---------- 3. Policy comparison bar chart ----------

def plot_policy_bar():
    policy_path = OUTPUTS / "policy_results.csv"
    df = safe_read_csv(policy_path, "Policy results")
    if df is None:
        return

    # Example: mean_per_window by policy
    plt.figure()
    plt.bar(df["policy"], df["mean_per_window"])
    plt.xlabel("Policy")
    plt.ylabel("Mean vehicles per time window")
    plt.title("Policy comparison: average traffic load")
    plt.grid(True, axis="y", alpha=0.3)

    out_path = FIG_DIR / "policy_mean_bar.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"[DONE] Saved {out_path}")

# ---------- Main ----------

def main():
    print(f"[INFO] ROOT: {ROOT}")
    print(f"[INFO] Saving figures to: {FIG_DIR}")
    plot_yolo_vs_sumo()
    plot_yolo_hist()
    plot_policy_bar()
    print("[INFO] All plotting finished.")

if __name__ == "__main__":
    main()
