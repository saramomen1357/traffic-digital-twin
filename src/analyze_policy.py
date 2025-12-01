import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"
SUMO_PATH = OUTPUTS_DIR / "sumo_traffic.csv"
YOLO_PATH = OUTPUTS_DIR / "yolo_detections.csv"
POLICY_PATH = OUTPUTS_DIR / "policy_results.csv"

def aggregate_by_window(df, time_col, count_col, window_size_sec):
    df = df.copy()
    df["window_id"] = (df[time_col] // window_size_sec).astype(int)
    agg = df.groupby("window_id")[count_col].sum().reset_index()
    agg["window_start_sec"] = agg["window_id"] * window_size_sec
    agg["window_end_sec"] = (agg["window_id"] + 1) * window_size_sec
    agg = agg.rename(columns={count_col: "vehicle_count"})
    return agg

def summarize_policy(agg_df, policy_name, source):
    total = agg_df["vehicle_count"].sum()
    mean = agg_df["vehicle_count"].mean()
    std = agg_df["vehicle_count"].std(ddof=0)
    maxv = agg_df["vehicle_count"].max()

    return {
        "policy": policy_name,
        "source": source,
        "num_windows": len(agg_df),
        "total_vehicles": total,
        "mean_per_window": mean,
        "std_per_window": std,
        "max_per_window": maxv,
    }

def main():
    if not SUMO_PATH.exists():
        raise FileNotFoundError(f"{SUMO_PATH} not found. Run run_sumo.py first.")
    if not YOLO_PATH.exists():
        raise FileNotFoundError(f"{YOLO_PATH} not found. Run detect_traffic.py first.")

    sumo_df = pd.read_csv(SUMO_PATH)
    yolo_df = pd.read_csv(YOLO_PATH)

    policies = {
        "Policy_A_60s": 60,
        "Policy_B_30s": 30,
    }

    metrics = []

    for name, w in policies.items():
        sumo_agg = aggregate_by_window(sumo_df, "time_sec", "vehicle_count", w)
        metrics.append(summarize_policy(sumo_agg, name, "SUMO"))

        yolo_agg = aggregate_by_window(yolo_df, "time_sec", "vehicle_count", w)
        metrics.append(summarize_policy(yolo_agg, name, "YOLO"))

    results_df = pd.DataFrame(metrics)
    results_df.to_csv(POLICY_PATH, index=False)

    print("[DONE] Saved policy results to", POLICY_PATH)
    print(results_df)

if __name__ == "__main__":
    main()
