#!/usr/bin/env python3
# tts_batch_edge.py
import argparse
import asyncio
import csv
import re
from pathlib import Path

import edge_tts


def normalize_id(s: str | None) -> str | None:
    if not s:
        return None
    s = str(s).strip()
    if not s:
        return None
    out = re.sub(r"[^\w\-]+", "", s).strip("_-").lower()
    return out or None


def pad_idx(idx: str | None) -> str | None:
    if idx is None:
        return None
    idx = str(idx).strip()
    if not idx:
        return None
    try:
        return str(int(idx))  # 1, 01, 001 -> "1"
    except ValueError:
        return idx


def build_auto_id(row: dict) -> str | None:
    tache = row.get("tache")
    kind = row.get("kind")
    idx = row.get("idx")
    if not (tache and kind and idx):
        return None

    try:
        t = int(str(tache).strip())
    except ValueError:
        return None
    if not (1 <= t <= 9):
        return None

    k = str(kind).strip().lower()
    if k not in ("q", "a"):
        return None

    i = pad_idx(idx)
    if not i:
        return None

    return f"t{t}{k}{i}"


def ssml_wrap(text: str, rate: int, volume: int, lang: str = "fr-CA") -> str:
    # rate: -10..10 -> map to +/- %
    rate_pct = max(-50, min(50, rate * 5))   # 0->0%, 10->50%
    vol_pct = max(0, min(200, volume))       # 0..200%

    escaped = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )
    return f"""<speak version="1.0" xml:lang="{lang}">
  <prosody rate="{rate_pct}%" volume="{vol_pct}%">{escaped}</prosody>
</speak>"""


async def synth_one_text(voice: str, text: str, out_path: Path):
    """Most robust: send plain text (no SSML)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(str(out_path))


async def synth_one_ssml(voice: str, text: str, out_path: Path, rate: int, volume: int, lang: str):
    """Use SSML (rate/volume). IMPORTANT: is_ssml=True."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ssml = ssml_wrap(text, rate=rate, volume=volume, lang=lang)
    communicate = edge_tts.Communicate(ssml, voice=voice, is_ssml=True)
    await communicate.save(str(out_path))


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="assets/tcfEE/t3.csv")
    ap.add_argument("--outdir", default="assets/tcfEE/mp3")
    ap.add_argument("--voice", default="fr-CA-AntoineNeural")
    ap.add_argument("--lang", default="fr-CA")
    ap.add_argument("--rate", type=int, default=0)       # -10..10 (approx)
    ap.add_argument("--volume", type=int, default=100)   # 0..200 (%)
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument(
        "--use-ssml",
        action="store_true",
        help="Enable SSML prosody so --rate/--volume take effect. If not set, script uses plain text (most robust)."
    )
    args = ap.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.outdir)

    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    # Read CSV
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    seen: dict[str, int] = {}
    sem = asyncio.Semaphore(max(1, args.concurrency))
    tasks = []

    async def run_row(row: dict):
        text = (row.get("text") or "").strip()
        if not text:
            return

        _id = normalize_id(row.get("id"))
        if not _id:
            _id = normalize_id(build_auto_id(row))

        if not _id:
            preview = text[:40].replace("\n", " ")
            print(f"Skipping row (no id): {preview}")
            return

        # Ensure uniqueness
        if _id in seen:
            seen[_id] += 1
            out_id = f"{_id}_{seen[_id]}"
        else:
            seen[_id] = 0
            out_id = _id

        out_path = out_dir / f"{out_id}.mp3"
        print(f"Generating {out_id}...")

        async with sem:
            if args.use_ssml:
                await synth_one_ssml(
                    voice=args.voice,
                    text=text,
                    out_path=out_path,
                    rate=args.rate,
                    volume=args.volume,
                    lang=args.lang,
                )
            else:
                await synth_one_text(args.voice, text, out_path)

    for r in rows:
        tasks.append(asyncio.create_task(run_row(r)))

    await asyncio.gather(*tasks)
    print(f"Done. MP3s in: {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())
