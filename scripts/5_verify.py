from pathlib import Path
import pandas as pd


df = pd.read_csv("metadata/final_metadata.csv")

en = df[df["language"] == "en"]
hi = df[df["language"] == "hi"]

print("=" * 45)
print("  Dataset Summary")
print("=" * 45)
print(f"  Total clips      : {len(df)}")
print(f"  English clips    : {len(en)}")
print(f"  Hindi clips      : {len(hi)}")

# duration from actual clip files
total_dur, missing = 0.0, []

try:
    import librosa
    for _, row in df.iterrows():
        p = Path(row["audio_path"])
        if p.exists():
            dur = librosa.get_duration(path=str(p))
            total_dur += dur
        else:
            missing.append(row["audio_path"])

    print(f"  Total duration   : {total_dur/60:.1f} min")
    print(f"  Avg clip length  : {total_dur/len(df):.1f} sec")
    if missing:
        print(f"  Missing files    : {len(missing)}")
except ImportError:
    print("  (install librosa for duration stats)")

print()
print("  Style distribution:")
for style, count in df["style"].value_counts().items():
    bar = "█" * count
    print(f"    {style:<15} {count:>3}  {bar}")

print()
print("  Language split:")
for lang, count in df["language"].value_counts().items():
    print(f"    {lang}  {count} clips")

print("=" * 45)