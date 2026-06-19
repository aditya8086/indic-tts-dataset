from pathlib import Path
import pandas as pd


df = pd.read_csv("metadata/final_metadata.csv")

# split into eng/ and hindi/ groups based on audio_path
for folder_name, lang_code in [("eng", "en"), ("hindi", "hi")]:
    subset = df[df["language"] == lang_code].copy()

    # AudioFolder needs a `file_name` column matching the actual filename
    # inside the same folder (just the filename, not the full path)
    subset["file_name"] = subset["audio_path"].apply(lambda p: Path(p).name)

    out = subset[["file_name", "transcript", "language", "style"]]

    out_path = Path("clips") / folder_name / "metadata.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Wrote {len(out)} rows -> {out_path}")