from pathlib import Path
import subprocess

BASE_DIR = Path(
    r"C:\Users\17851\OneDrive - University of Toronto\Documents\GitHub\haoyanzheng.github.io\assets\tcfCO"
)

# 你可以按需要改参数：
# -b:a 96k  : 96kbps，听力练习通常足够且体积小
# -ac 1     : 单声道，进一步减小体积（如果你想保留立体声就删掉这两行参数）
FFMPEG_ARGS = ["-ac", "1", "-b:a", "96k"]

converted = 0
skipped = 0
failed = 0

for m4a_path in BASE_DIR.rglob("*.m4a"):
    mp3_path = m4a_path.with_suffix(".mp3")

    if mp3_path.exists():
        print(f"Skip (already exists): {mp3_path}")
        skipped += 1
        continue

    cmd = ["ffmpeg", "-y", "-i", str(m4a_path), *FFMPEG_ARGS, str(mp3_path)]
    print("Running:", " ".join(cmd))

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        converted += 1
    except subprocess.CalledProcessError:
        print(f"FAILED: {m4a_path}")
        failed += 1

print(f"\nDone. Converted={converted}, Skipped={skipped}, Failed={failed}")
