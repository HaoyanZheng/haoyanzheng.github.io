from pathlib import Path
import subprocess

# 你的 WAV 文件所在根目录
BASE_DIR = Path(
    r"C:\Users\17851\OneDrive - University of Toronto\Documents\GitHub\haoyanzheng.github.io\assets\tcfCO"
)

for wav_path in BASE_DIR.rglob("*.wav"):
    mp3_path = wav_path.with_suffix(".mp3")

    # 已经有 mp3 就跳过
    if mp3_path.exists():
        print(f"Skip (already exists): {mp3_path}")
        continue

    print(f"Converting: {wav_path} -> {mp3_path}")

    # 调用 ffmpeg：单声道 + 96kbps，比特率基本听不出和原来区别
    cmd = [
        "ffmpeg",
        "-y",              # 覆盖输出文件（这里其实一般不存在，可保守保留）
        "-i", str(wav_path),
        "-ac", "1",        # 转成单声道，减小体积
        "-b:a", "96k",     # 比特率 96 kbps
        str(mp3_path),
    ]

    # 运行 ffmpeg，如果失败会抛异常
    subprocess.run(cmd, check=True)

print("All conversions done.")
