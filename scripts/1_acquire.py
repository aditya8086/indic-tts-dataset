import pandas as pd
import subprocess
from pathlib import Path


RAW_AUDIO_DIR = Path("raw_audio")
CLIPS_DIR = Path("clips")

RAW_AUDIO_DIR.mkdir(exist_ok=True)
CLIPS_DIR.mkdir(exist_ok=True)


def time_to_seconds(timestamp):
    h, m, s = map(int, timestamp.split(":"))
    return h * 3600 + m * 60 + s


def download_audio(url, output_path):
    subprocess.run([
        "yt-dlp", "-x", "--audio-format", "wav",
        "-o", str(output_path), url
    ], check=True)


def extract_clip(source, output, start, end):
    start_sec = time_to_seconds(start)
    duration = time_to_seconds(end) - start_sec
    subprocess.run([
        "ffmpeg", "-y", "-i", str(source),
        "-ss", str(start_sec), "-t", str(duration),
        "-ar", "16000", "-ac", "1", str(output)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


# load clip definitions
english_df = pd.read_csv("metadata/english.csv")
hindi_df = pd.read_csv("metadata/hindi.csv")
df = pd.concat([english_df, hindi_df], ignore_index=True)
df = df.dropna(subset=["filename"]).reset_index(drop=True)

print(f"Loaded {len(df)} clips")

# download each unique source video once
unique_sources = df["source"].unique()
source_to_file = {}

print(f"Found {len(unique_sources)} unique source videos\n")

for i, url in enumerate(unique_sources, start=1):
    name = f"source_{i}"
    path = RAW_AUDIO_DIR / f"{name}.wav"
    source_to_file[url] = path

    if path.exists():
        print(f"[skip] {name}")
        continue

    print(f"[download] {name} <- {url}")
    try:
        download_audio(url, RAW_AUDIO_DIR / f"{name}.%(ext)s")
    except Exception as e:
        print(f"  failed: {e}")

# cut clips from downloaded sources
print("\nExtracting clips...\n")

success, failed = 0, 0

for _, row in df.iterrows():
    out_dir = CLIPS_DIR / row["language"]
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{row['filename']}.wav"

    if out_file.exists():
        continue

    try:
        extract_clip(
            source_to_file[row["source"]],
            out_file,
            row["start"],
            row["end"]
        )
        success += 1
        print(f"  ✓ {row['filename']}")
    except Exception:
        failed += 1
        print(f"  ✗ {row['filename']}")

print(f"\nDone — {success} succeeded, {failed} failed")