from pathlib import Path
import pandas as pd


emotion_df = pd.read_csv("metadata/emotion_labels.csv")

source_df = pd.concat([
    pd.read_csv("metadata/english.csv"),
    pd.read_csv("metadata/hindi.csv")
], ignore_index=True)

lang_map = {
    row["filename"]: "en" if row["filename"].startswith("eng") else "hi"
    for _, row in source_df.iterrows()
}

rows = []
for _, row in emotion_df.iterrows():
    name = row["file_name"]
    folder = "eng" if name.startswith("eng") else "hindi"
    rows.append({
        "audio_path": f"clips/{folder}/{name}.wav",
        "transcript": row["transcript"],
        "language": lang_map[name],
        "style": row["label"]
    })

df = pd.DataFrame(rows)
df.to_csv("metadata/final_metadata.csv", index=False, encoding="utf-8-sig")

print(f"Final metadata saved — {len(df)} rows")