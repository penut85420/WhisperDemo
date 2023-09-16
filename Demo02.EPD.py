import wave

import pyaudio
import webrtcvad

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

# 設定 EPD Buffer 與 Voice Buffer
epd_len = 80
epd_buffer = [0] * epd_len  # 0.8s

voice_len = 200
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

    print(f"  {epd_state} {vad_ratio:.2f} {str(vad_result):5s}", end="\r", flush=True)

# 存放音檔
with wave.open("output.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16 Bits = 2 Bytes
    wf.setframerate(16000)
    wf.writeframes(b"".join(record_frames))

print("\nDone")
