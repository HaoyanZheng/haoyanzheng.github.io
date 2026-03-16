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


def rate_str(rate: int) -> str:
    """Convert int -10..10 to edge-tts rate string e.g. '-10%' or '+10%'."""
    pct = max(-50, min(50, rate * 5))
    return f"{pct:+d}%"


def volume_str(volume: int) -> str:
    """Convert 0..200 to edge-tts volume string e.g. '+0%' or '+50%'."""
    pct = max(-100, min(100, volume - 100))
    return f"{pct:+d}%"


async def synth_one(voice: str, text: str, out_path: Path, rate: int, volume: int):
    """Synthesize using edge-tts Communicate with rate and volume."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text,
        voice=voice,
        rate=rate_str(rate),
        volume=volume_str(volume),
    )
    await communicate.save(str(out_path))


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="assets/tcfEE/t2.csv")
    ap.add_argument("--outdir", default="assets/tcfEE/mp3")

    # ── Expression Écrite optimized ─────────────────────────────────────────
    # Denise: clearest, most neutral French — ideal for memorizing written text
    ap.add_argument("--voice", default="fr-FR-DeniseNeural")
    ap.add_argument("--lang", default="fr-FR")
    # Slightly slower (-3) so each word is clearly heard for memorization
    ap.add_argument("--rate", type=int, default=-3)      # -10..10
    ap.add_argument("--volume", type=int, default=100)   # 0..200
    # ────────────────────────────────────────────────────────────────────────

    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.outdir)

    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

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

        if _id in seen:
            seen[_id] += 1
            out_id = f"{_id}_{seen[_id]}"
        else:
            seen[_id] = 0
            out_id = _id

        out_path = out_dir / f"{out_id}.mp3"
        print(f"Generating {out_id}...")

        async with sem:
            await synth_one(
                voice=args.voice,
                text=text,
                out_path=out_path,
                rate=args.rate,
                volume=args.volume,
            )

    for r in rows:
        tasks.append(asyncio.create_task(run_row(r)))

    await asyncio.gather(*tasks)
    print(f"Done. MP3s in: {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())