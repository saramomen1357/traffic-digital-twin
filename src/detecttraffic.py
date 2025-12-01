from pathlib import Path

# ABSOLUTE PATH
video = Path(r"C:\src\traffic-digital-twin\data\traffic_video.mp4")

print("CHECKING:", video)
print("EXISTS?:", video.exists())

if not video.exists():
    raise FileNotFoundError(f"VIDEO NOT FOUND at {video}")
else:
    print("VIDEO FOUND SUCCESSFULLY!")
