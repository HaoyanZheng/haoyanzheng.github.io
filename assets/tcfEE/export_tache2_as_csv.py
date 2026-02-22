import csv
import re

# 用于判断“看起来像法语/拉丁字母文本”
LATIN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœÆæ]")

def extract_french_paragraphs(raw):
    out = []
    for row in raw:
        if not isinstance(row, (list, tuple)) or len(row) < 3:
            continue
        # 跳过 SECTION 行（通常 ["SECTION", ...] 或 ["SECTION", ..., ...]）
        if isinstance(row[0], str) and row[0].strip().upper() == "SECTION":
            continue

        fr = row[-1]
        if isinstance(fr, str):
            fr = fr.strip()
            if fr and LATIN_RE.search(fr):  # 确保不是空/纯中文
                out.append(fr)
    return out

french_paragraphs = extract_french_paragraphs(raw)

# 2) 导出 CSV
output_path = "assets/tcfEE/t2_french.csv"
with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    # 如需表头就取消注释下一行
    # w.writerow(["task", "q", "index", "paragraph"])

    for i, para in enumerate(french_paragraphs, start=1):
        w.writerow([2, "q", i, para])

print("Exported:", output_path)
print("Count:", len(french_paragraphs))
