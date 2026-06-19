from pathlib import Path
from dotenv import load_dotenv
from sarvamai import SarvamAI
import os


BATCH_SIZE = 20

ENG_CLIPS = Path("clips/eng")
HIN_CLIPS = Path("clips/hindi")

TRANSCRIPT_ENG = Path("transcripts_eng")
TRANSCRIPT_HIN = Path("transcripts_hindi")

TRANSCRIPT_ENG.mkdir(exist_ok=True)
TRANSCRIPT_HIN.mkdir(exist_ok=True)

load_dotenv()
client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))


def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def transcribe(audio_files, language_code, output_dir):
    batches = list(chunked(audio_files, BATCH_SIZE))

    print(f"\n{language_code} — {len(audio_files)} files, {len(batches)} batch(es)\n")

    for i, batch in enumerate(batches, start=1):
        print(f"batch {i}/{len(batches)}")

        job = client.speech_to_text_job.create_job(
            model="saaras:v3",
            mode="transcribe",
            language_code=language_code,
            with_diarization=False
        )
        job.upload_files(file_paths=[str(f) for f in batch])
        job.start()
        job.wait_until_complete()

        batch_dir = output_dir / f"batch_{i}"
        batch_dir.mkdir(exist_ok=True)
        job.download_outputs(output_dir=str(batch_dir))

        print(f"  saved to {batch_dir}\n")


transcribe(sorted(ENG_CLIPS.glob("*.wav")), "en-IN", TRANSCRIPT_ENG)
transcribe(sorted(HIN_CLIPS.glob("*.wav")), "hi-IN", TRANSCRIPT_HIN)

print("All transcriptions complete")