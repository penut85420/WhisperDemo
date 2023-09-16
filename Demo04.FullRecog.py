import numpy as np
import pyaudio
import webrtcvad
from faster_whisper import WhisperModel

# 初始化 Whisper 模型
asr = WhisperModel(
    "large-v2",
    device="cuda",
    compute_type="int8_float16",
    download_root="./Models",
)

# 初始化 VAD 模型
vad = webrtcvad.Vad()
vad.set_mode(1)

# 初始化錄音裝置
recorder = pyaudio.PyAudio()
stream = recorder.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=160,
)

while True:
    # 設定 EPD Buffer 與 Voice Buffer
    epd_len = 50
    epd_buffer = [0] * epd_len  # 0.8s

    voice_len = 100
    voice_buffer = [b""] * voice_len  # 2.0s

    record_frames = list()

    # 開始偵測 EPD
    epd_state = 0  # 0 - 未觸發, 1 - 觸發中, 2 - 結束
    while epd_state != 2:
        # 取得音訊並判斷 VAD
        frame = stream.read(160)
        vad_result = vad.is_speech(frame, 16000)

        # 處理 EPD Buffer Cycle
        epd_buffer.append(vad_result)
        epd_buffer.pop(0)

        # 計算 VAD Ratio
        vad_ratio = sum(epd_buffer) / len(epd_buffer)

        # 根據 VAD Ratio 與 EPD 狀態進行動作
        if epd_state == 0:
            if vad_ratio < 0.8:
                # 若尚未觸發，則將 Frame 放進 Buffer Cycle
                voice_buffer.append(frame)
                voice_buffer.pop(0)
            else:
                # 若觸發，則將 Voice Buffer 放入錄音段落
                epd_state = 1
                record_frames.extend(voice_buffer)
                record_frames.append(frame)
        elif epd_state == 1:
            record_frames.append(frame)
            if vad_ratio < 0.2:
                # 若小於門檻值則結束錄音
                epd_state = 2

        logging_msg = f"  {epd_state} {vad_ratio:.2f} {str(vad_result):5s}"
        print(logging_msg, end="\r", flush=True)

    # 轉為 Waveform 並進行 ASR
    waveform = np.frombuffer(b"".join(record_frames), dtype=np.int16)
    segments, info = asr.transcribe(waveform)

    print(f"Language: {info.language}")
    print(f"Lang Prob: {info.language_probability}")

    for seg in segments:
        print(f"[{seg.start:.2f}s -> {seg.end}s] {seg.text}")

    if seg.text == "結束":
        break
