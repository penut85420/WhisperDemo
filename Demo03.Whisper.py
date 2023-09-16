from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v2",
    device="cuda",
    compute_type="int8_float16",
    download_root="./Models",
)

segments, info = model.transcribe("audio.mp3")

print(f"Language: {info.language}")
print(f"Lang Prob: {info.language_probability}")

for seg in segments:
    print(f"[{seg.start:.2f}s -> {seg.end}s] {seg.text}")
