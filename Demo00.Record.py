import pyaudio

recorder = pyaudio.PyAudio()

stream = recorder.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=160,
)

# 10ms = 1 Frame, 5s = 5000ms = 500 Frames
frames = [stream.read(160) for _ in range(500)]

import wave

with wave.open("output.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16 Bits = 2 Bytes
    wf.setframerate(16000)
    wf.writeframes(b"".join(frames))
