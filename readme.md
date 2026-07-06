# indic-tts-dataset

End-to-end pipeline for building a Hindi + English TTS training dataset from YouTube audio. Downloads source videos, cuts timestamped clips, transcribes with ASR, labels speaking style with an LLM, and publishes a structured dataset to HuggingFace.

**Dataset:** [`aditya1101203/indic-tts-dataset`](https://huggingface.co/datasets/aditya1101203/indic-tts-dataset)

---

## Pipeline

```
YouTube URLs + timestamps
    → 1_acquire.py          yt-dlp download + ffmpeg clip extraction (16kHz mono WAV)
    → 2_transcribe.py       batch ASR transcription (Saaras v3), saves raw JSON
    → 3_label_styles.py     speaking style labeling via LLM (closed taxonomy)
    → 4_build_metadata.py   merges transcripts + labels → final_metadata.csv
    → 5_verify.py           dataset summary — clip counts, duration, style distribution
    → 6_make_hf_metadata.py generates per-folder metadata.csv for HuggingFace AudioFolder
```

---

## Dataset stats

| | |
|---|---|
| Total clips | 57 |
| Total duration | ~54 minutes |
| English | 29 clips |
| Hindi | 28 clips |
| Audio format | 16kHz mono WAV |

**Style distribution:**

| Style | Count |
|---|---|
| educational | 17 |
| storytelling | 15 |
| motivational | 12 |
| opinion | 9 |
| conversational | 3 |
| review | 1 |

---

## Repo structure

```
indic-tts-dataset/
├── scripts/
│   ├── 1_acquire.py
│   ├── 2_transcribe.py
│   ├── 3_label_styles.py
│   ├── 4_build_metadata.py
│   ├── 5_verify.py
│   └── 6_make_hf_metadata.py
├── metadata/
│   ├── english.csv          # source URLs + timestamps for English clips
│   ├── hindi.csv            # source URLs + timestamps for Hindi clips
│   ├── style_labels.csv     # per-clip transcripts + style labels
│   └── final_metadata.csv   # audio_path, transcript, language, style
├── transcripts_eng/         # raw ASR JSON output per English clip
├── transcripts_hindi/       # raw ASR JSON output per Hindi clip
└── README.md
```

Audio files are not stored in this repo — they live on HuggingFace.

---

## Style taxonomy

Labels are assigned by prompting an LLM with the transcript and constraining output to one of:

| Label | Description |
|---|---|
| `educational` | structured explanation or instruction |
| `storytelling` | narrative, anecdote, personal experience |
| `motivational` | persuasive or inspirational tone |
| `opinion` | personal perspective or commentary |
| `conversational` | informal, dialogue-like delivery |
| `review` | evaluation of a product, idea, or experience |

---

## License

MIT